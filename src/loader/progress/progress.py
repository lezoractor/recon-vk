#
# Модуль, отвечающий за отображение текущего прогресса.
# Возможен вывод в консоль, а так же API, чтоб затем 
#  присобачить сюда веб-интерфейс или еще что-нибудь.
# 
# Для отладки тож сойдет
#


#
# Программный интерфейс получения данных о прогрессе
#


#
# Доля выполнения всех задач
#
def getOverallProgress () :
	pass

#
# Прогресс определенной задачи
#
def getTaskProgress (id) :
	pass 

#
# Получение лога
#
# @param {time} timeFrom - время, начиная с которого нужно получить записи
# @param {string} logLevel - debug, info, warn, fatal
# @param {boolean} blockUntilLog - если True, вернет значение только когда оно появится.
#
def getLog(timeFrom=0, logLevel="info", blockUntilLog=False) :
	pass


#
# Интерфейс записи данных о прогрессе
#

#
# Логгировать что-то..
#
def log (message, id=-1, loglevel="info") :
	pass

#
# Отчитаться о начале обработки задачи
#
def started (task="Unknown task", loglevel="debug", parent=0) :
	return 0 # Номер задачи

#
# Отчитаться о завершении обработки задачи
#
def finished (id) :
	pass