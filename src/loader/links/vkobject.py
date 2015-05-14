class VKObject:
	"""VK Object (comment itself, post, photo, etc) class"""
	
	def __init__(self, typed, owner, raw) :
		self.uoid = typed + str(raw.id) + '@' + str(raw.owner)
		self.id = raw.id
		self.owner_id = owner
		self.from_id = raw.from_id
		self.text = raw.text or None
		self.attachments = raw.attachments or []
		self.objects = []

	def attachObject(self, obj) :
		self.objects.append(obj)