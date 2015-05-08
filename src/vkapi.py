# Код не будет работать, не все методы реализованы..
# P.S. Я пишу на Python 3.x
# 
# @todo:
# 	- обрабатывать списки более ассинхронно
# 	- использвать execute
# 	- обрабатывать ошибки

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
	#
	def __init__(self, tokens, threads=20, interval=0.5) :

		self.tokens = deque(tokens)
		self.queueAuthorized = deque()
		self.queueUnauthorized = deque()
		self.lasttime = time.clock()
		self.interval = interval

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
	#  то есть есть возможность привысить лимит в 3 запроса за секунду.
	#
	@staticmethod
	def force (method, options, token) :

		if token:
			options.access_token = token

		# Вроде это текущая версия
		options.v = '5.56'

		if method in API.ListableMethods:

			options.count = API.Limits[method]
			options.offset = 0
			response = API.raw(method, options)

			if not response:
				return []

			while len(response.items) < response.count:
				options.offset += options.count
				response.items += API.raw(method, options).items

			return response.items
		
		else:
			return API.raw(method, options)
			

	#
	# Отправляет запросы без предварительной обработки, за исключением
	#  обработки ошибок API. 
	# Это статичный метод и может быть вызван без инициализации класса.
	# Внимание! Не контролирует допустимые задержки между запросами, 
	#  то есть есть возможность привысить лимит в 3 запроса за секунду.
	#
	@staticmethod
	def raw (method, options, timeout=500) :
		connection = http.client.HTTPSConnection("api.vk.com", 443, timeout)
		connection.request("GET", "/method/" + method + '?' + urllib.parse.urlencode(options));
		try:
			data = json.loads(response.read())
		except ValueError, e:
			# Просто повторить запрос
			return API.raw(method, options, timeout * 2)
		else:
			if not data.error:
				return data.response
			else:
				API.parseError(data.error, method, options)


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
	# Это выполняется в отдельном потоке.
	# При первой возможности из очереди заданий 
	#  получается задание и затем выполняется.
	#
	def _worker(self) :
		while True:
			if len(self.queueAuthorized) and time.clock() - self.lasttime > self.interval:
				
				# Берем задачу из очереди
				task = self.queueAuthorized.popleft()

				# Время последнего запроса обновляем
				self.lasttime = time.clock()

				# Выполняем запрос
				API.force(task.method, task.options, self.getToken())
				
			elif len(self.queueAuthorized):
				task = self.queueUnauthorized.popleft()
				API.force(task.method, task.options, False)
			else
				pass
	

	



