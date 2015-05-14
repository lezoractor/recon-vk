from loader.links import vkobject

class VKLink:
	"""Link type"""

	def __init__(self, from, to, obj) :

		obj = VKObject(obj)

		self.links = [{
			"from": from,
			"to": to,
			"object": obj.id
		}]

		self.objects = obj.getList()
	

	