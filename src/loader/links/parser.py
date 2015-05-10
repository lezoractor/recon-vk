import loader.data.load
import loader.links.Link

from collections import deque

#
# Получает список связей, связанных с этой страницей
# Смотрите loader.js в старой проге
# 
def parse (user) :
	links = deque()

	#
	# Слишком сильно упирается в схему возвращаемого значения loader.data.load
	# поэтому @todo
	#

	for photo in user.photos :
		pass