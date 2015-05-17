#
# Поиск в ширину.
#
# Можно чтоб всех не грузить, ввести функцию эвристической оценки.
# Грузить всех на 1 уровне глубины, а потом грузить только тех,
#  на кого ссылаются больше, чем n вершин первой глубины..
#

from loader.data import load
from loader.data import loadGroup
from loader.links import *
from progress import *

#
# Получает список страниц, которые прямо или косвенно связаны
#  с данной страницей.
# Возвращает два значения: люди и группы
# Ссылки и объекты сохраняются в базу данных,
#  или берутся от туда, если есть.
#
def getLinksFromUser (uid, callback) :
	
	def onparse (links) :
	
		people = set()
		groups = set()

		for link in links :
			if link['from'] != uid :				
				if link['from'].type == 'user' :
					people.add(link['from'])
				else if link['from'].type == 'group' : 
					groups.add(link['from'])
			else if link.to.type != uid:
				if link.to.type == 'user' :
					people.add(link.to)
				else if link.to.type == 'group' : 
					groups.add(link.to)

		callback(people, groups)

	def onload (user) :
		parse(user, onparse)

	load(uid, onload)


#
# Загрузка людей, имеющих отношение к группе
# Группы, у которых *закрыта* для комментирования
#  стена и больше 10к подписчиков просто не 
#  учитываются и не загружаются. 
# Группы, у которых *открыта* для комментирования
#  стена и больше 10к подписчиков - обрабатываются
#  только последние 10к постов
# Группы с менее чем 100 участниками означают
#  то, что участники связаны между собой прямо
#
# Возвращает список самых активных
#  @todo: сейчас он возвращает тупо список всех.
# 
def getLinksFromGroup (uid, callback) :
	def onparse (links) :
	
		# Просто список связанных людей будет так.
		people = set([link in links if link.to != uid] + [link in links if link['from'] != uid]])

		callback(people, groups)

	def onload (user) :
		parse(user, onparse)

	loadGroup(uid, onload)

def search (start, config) :
	
	#
	# Загрузка активных участников групп
	#
	def onGroupLoad (people) :
		pass

	#
	# Загрузка последних пользователей, которые не имеют связи с центральным,
	#  они нужны для определения того, что из себя представляет та или иная 
	#  группа людей. 
	#
	def onThirdUserLoad (people, groups) :
		pass

	#
	# Загрузка основного состава людей, которые хоть как-то связаны с целью
	#
	def onSecondUserLoad (people, groups) :
		pass

	#
	# Вызывается только один раз, при загрузке цели
	#
	def onTargetUserLoad (people, groups) :
		for user in people :
			getLinksFromUser(user.id, onUserLoad)
		for group in groups :
			# @todo


	getLinksFromUser(uid, onUserLoad)

