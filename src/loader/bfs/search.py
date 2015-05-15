#
# Поиск в ширину.
#
# Можно чтоб всех не грузить, ввести функцию эвристической оценки.
# Грузить всех на 1 уровне глубины, а потом грузить только тех,
#  на кого ссылаются больше, чем n вершин первой глубины..
#

from loader.data import load
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

def search (start, config) :
	
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

