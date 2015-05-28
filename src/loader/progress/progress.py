#
# Модуль, отвечающий за отображение текущего прогресса.
# Возможен вывод в консоль, а так же API, чтоб затем 
#  присобачить сюда веб-интерфейс или еще что-нибудь.
# 
# Для отладки тож сойдет
#

tasks = []
nodes = []

class task:
	def __init__ (self, name="Unknown task", loglevel="debug", parent=rootTask) :
		self.name = name
		self.loglevel = loglevel
		self.parent = parent
		self.done = False
		self.id = len(tasks)
		self.childTasks = []
		tasks.append(self)
		
		if (parent) :
			parent.childTasks.append(self)

	def done (self) :
		self.done = True
		log(name + " done.", self.id, self.loglevel)

	def getProgress (self) :
		if self.done :
			return 1;

		summ = 0.0

		for child in self.childTasks :
			summ += child.getProgress()

		if not self.childTasks :
			return 0

		return summ / len(self.childTasks)

rootTask = task("Root task", "info", False)
tasks.append(rootTask)

#
# Получение лога
#
# @param {time} timeFrom - время, начиная с которого нужно получить записи
# @param {string} logLevel - debug, info, warn, fatal
# @param {boolean} blockUntilLog - если True, вернет значение только когда оно появится.
#
def getLog(timeFrom=0, logLevel="info", blockUntilLog=False) :
	while True :
		for node in nodes :
			if 


#
# Логгировать что-то..
#
def log (message, id=-1, loglevel="info") :
	nodes.append({message: message, id: id, loglevel: loglevel})
	# @todo Печатать, если loglevel соответствуюет таковому в конфигах
