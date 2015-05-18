# 
# Python 3.x
# 
# @todo:
#   - учитывать интервал в повторных запросах
#   - проверить производительность. Возможно лучше будет использовать Процессы вместо Потоков
# 	- обрабатывать списки более ассинхронно (код станет сложнее)
# 	- использвать execute (код загрязнится)
# 	- отсеять лишние запросы для проверки доступа (код сильно загрязнится)

import urllib.parse.urlencode
import time.clock
import http.client
import json

from threading import Thread
from collections import deque

class API:
	"""VK API Class"""

	# 
	# Методы, возвращающие списки
	# 
	ListableMethods = (
		'wall.get', 
		'wall.getReposts', 
		'photos.getProfile',
		'users.getFollowers',
		'video.get',
		'wall.getComments',
		'photos.getComments',
		'video.getComments',
		'likes.getList'
	)

	#
	# Методы, не требующие токена по-умолчанию
	#  (могут затребовать, если у пользователя скрыта страница) @todo
	#
	PublicMethods = (
		'wall.get',
		'wall.getReposts',
		'users.getFollowers',
		'wall.getComments',
		'likes.getList'
	)

	#
	# Максимальное допустимое количество возвращаемых элементов
	#  для методов, возвращающих списки
	#
	Limits = {
		'wall.get': 100,
		'wall.getReposts': 1000,
		'photos.getProfile': 1000,
		'users.getFollowers': 1000,
		'video.get': 200,
		'wall.getComments': 100,
		'photos.getComments': 100,
		'video.getComments': 100,
		'likes.getList': 1000
	}

	#
	# @param {list} tokens - список токенов
	# @param {int} threads - количество потоков
	# @param {double} interval - интервал для запросов с токеном
	# @param {int} executePerRequest - сколько запросов помещать в один. 0 Для простого режима
	#
	def __init__(self, tokens, threads=20, interval=0.5, executePerRequest=10) :

		self.tokens = deque(tokens)
		self.queueAuthorized = deque()
		self.queueUnauthorized = deque()
		self.lasttime = time.clock()
		self.interval = interval / len(tokens)
		self.executePerRequest = executePerRequest

		#
		# Потоки в вечном цикле проверяют наличие новых
		# заданий и исполняют их. 
		# @see API._worker
		#
		for i in range (threads):
			thread = Thread(target=self._worker)
			thread.daemon = True
			thread.start()

	#
	# Можно использовать для синхронных запросов.
	# Это статичный метод и может быть вызван без инициализации класса.
	# Возвращает данные в обработанном виде (@see API.request)
	# Внимание! Не контролирует допустимые задержки между запросами, 
	#  то есть есть возможность случайно привысить лимит в 3 запроса за секунду.
	#
	# @param {string} method - метод (пример: "wall.get")
	# @param {dict} options - опции метода (смотрите документацию API Вконтакте)
	# @param {string} token - токен (не обязательный)
	# @param {iter} tokens - список токенов (используются при явной необходимости)
	# 
	@staticmethod
	def force (method, options, token, tokens) :

		if token:
			options.access_token = token

		if tokens:
			tokens = deque(tokens)
		else:
			tokens = deque()

		# Ставим актуальную на сей момент версию API, если 
		#  не указана иная. Если этого не сделать, то 
		#  вконтакт будет считать, что мы используем 
		#  версию 3.0, но она сильно устарела. По крайней
		#  мере там списки возвращаются в виде
		#   [длина, элемент1, элемент2, ...]
		#  а не
		#  	{count: длина, items: [элемент1, элемент2]}
		if not options.v:
			options.v = '5.8'

		if method in API.ListableMethods:

			options.count = API.Limits[method]
			options.offset = 0
			response = API.raw(method, options, tokens=tokens)

			if not response:
				return []

			while len(response.items) < response.count:
				options.offset += options.count
				response.items += API.raw(method, options, token=tokens).items

			return response.items
		
		else:
			return API.raw(method, options, tokens=tokens)
			
	#
	# Отправляет запросы без предварительной обработки, за исключением
	#  обработки ошибок API. 
	# Это статичный метод и может быть вызван без инициализации класса.
	# Внимание! Не контролирует допустимые задержки между запросами, 
	#  то есть есть возможность привысить лимит в 3 запроса за секунду.
	#
	@staticmethod
	def raw (method, options, timeout=500, tokens) :
		connection = http.client.HTTPSConnection("api.vk.com", 443, timeout)
		connection.request("GET", ''.join(("/method/", method, '?', urllib.parse.urlencode(options)));
		try:
			data = json.loads(response.read())
		except ValueError, e:
			# Просто повторить запрос
			return API.raw(method, options, timeout * 2)
		else:
			if not data.error:
				return data.response
			else:
				API.parseError(data.error, method, options, tokens)

	#
	# Парсит ошибку и выполняет соответствующие действия.
	# 
	@staticmethod
	def parseError(error, method, options, tokens) :

		code = error.error_code

		# Временная ошибка
		if code in (1, 10, 113) :
			return API.raw(method, options)

		# Нефатальная неисправимая ошибка
		if code in (18, 19, 300) :
			return False
		
		# Фатальная ошибка (если в ней виноваты мы)
		if code in (3, 4, 5, 8, 11, 16, 20, 21, 23, 24, 100, 101, 150, 500, 600, 603) :
			raise Exception(error.error_desc)

		# Слишком много запросов в секунду
		if code in (6) :  
			sleep(1)
			return API.raw(method, options) 
		
		# Часто повторяется действие
		if code in (9) : 
			sleep(60)
			return API.raw(method, options)

		# Капча или валидация 
		if code in (14, 17) : 
			raise Exception(error.error_desc, '(do it yourself)') 

		# Нет доступа
		if code in (7, 15, 200, 201, 204, 212) : 
			if options.access_token:
				return False
			else:
				tokens.rotate(1)
				options.access_token = tokens[0]
				if not options.access_token:
					return False
				return API.raw(method, options)

		# Что-то непонятное
		raise Exception(error.error_desc, code, '(unknown error)')

	#
	# Ставит запрос в очередь.
	# Ассинхронный.
	# В случае запроса списка (типа "wall.get", "photos.getProfile") возвращает сразу список
	#  или False в случае ошибки.
	# Иначе результатом выполнения будет {root}.response
	# 
	# @param {string} method - метод (пример: "wall.get")
	# @param {dict} options - опции метода (смотрите документацию API Вконтакте)
	# @param {function} callback - колбэк. Вызывается с результатом запроса в качестве первого аргумента. False в случае ошибки.
	# @param {boolean} auth - принудительная авторизация. Если страница была изначально дана с параметром {hidden:1}, то этот параметр для вас
	#
	def request (self, method, options, callback, auth=False) :

		task = {
			method: method,
			options: options,
			callback: callback
		}

		if auth or method not in API.PublicMethods:
			self.queueAuthorized.append(task)
		else:
			self.queueUnauthorized.append(task)

	#
	# Возвращает токен.
	# Каждый раз смещает список токенов на 1,
	#  т.е. они выдаются циклически
	#
	def getToken (self) :
		self.tokens.rotate(1)
		return self.tokens[0]


	#
	# Генерирует код для метода execute
	# @param {list} requests - список запросов
	#  формат - [{method: метод, data: {параметры}}]
	# @see vk.com/dev/execute
	#
	@staticmethod
	def generateExecuteScript (requests) :
		code = 'return ['

		for request in requests :
			code += ''.join(('API.', request.method, '(', json.dumps(request.data), '),'))

		return code[:-1] + '];'

	#
	# Это выполняется в отдельном потоке.
	# При первой возможности из очереди заданий 
	#  получается задание и затем выполняется.
	#
	def _worker(self) :
		while True :
			if len(self.queueAuthorized) and time.clock() - self.lasttime > self.interval :
				if self.executePerRequest and :
					
					requests = []

					while len(requests) < self.executePerRequest and len(self.queueAuthorized):
						requests.append(self.queueAuthorized.popleft())
				else :
					# Берем задачу из очереди
					task = self.queueAuthorized.popleft()

					# Время последнего запроса обновляем
					self.lasttime = time.clock()

					# Выполняем запрос
					task.callback(API.force(task.method, task.options, self.getToken()))

			elif len(self.queueAuthorized):
				task = self.queueUnauthorized.popleft()
				task.callback(API.force(task.method, task.options, False, self.tokens))
			else
				pass

	#
	# Это выполняется в несколько потоков в фоне
	#
	def _worker(self) :
		
		# Если включена оптимизация через execute
		if self.executePerRequest :
			while True :

				# Выполняем запрос только если в очереди достаточно реквестов
				if len (self.queueAuthorized >= self.executePerRequest) and time.clock() - self.lasttime > self.interval:

					requests = []

					while len (requests) < self.executePerRequest and len (self.queueAuthorized):
						requests.append(self.queueAuthorized.popleft())

					script = API.generateExecuteScript(requests)
					params = {code: script}
					data = API.force('execute', params, self.getToken())

					for id, response in data :
						requests[id].callback(response)
					

				elif len(self.queueAuthorized) :
					task = self.queueUnauthorized.popleft()
					task.callback(API.force(task.method, task.options, False, self.tokens))
		else :
			while True :
				if len(self.queueAuthorized) and time.clock() - self.lasttime > self.interval :
					
					# Берем задачу из очереди
					task = self.queueAuthorized.popleft()

					# Время последнего запроса обновляем
					self.lasttime = time.clock()

					# Выполняем запрос
					task.callback(API.force(task.method, task.options, self.getToken()))

				elif len(self.queueAuthorized):
					task = self.queueUnauthorized.popleft()
					task.callback(API.force(task.method, task.options, False, self.tokens))