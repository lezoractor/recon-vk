from loader.links import vkobject

class VKLink:
	"""Link type (like, repost, commenting fact, etc)"""

	def __init__(self, from, to) :

		self.links = [{
			"from": from,
			"to": to,
			"object": obj.id
		}]

		self.objects = []
	
	def attachObject (self, obj) :
		self.objects.append(obj)