from loader.links import vkobject

class VKLink:
	"""Link type (like, repost, commenting fact, etc)"""

	def __init__(self, from, to) :

		obj = VKObject(obj)

		self.links = [{
			"from": from,
			"to": to,
			"object": obj.id
		}]

		self.objects = []
	
	def attachObject (self, obj) :
		self.objects.append(obj)