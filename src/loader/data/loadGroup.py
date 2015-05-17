#
# @param {int} postsLimit - лимит, сколько постов надо загружать. 0 для отключения
# @param {int} followersLimit - лимит участников группы. Учитывается только если у группы закрыта для комментирования стена. Группа не будет учитываться вообще если лимит будет достигнут.
#
def loadGroup (user, callback, postsLimit=5000, followersLimit=10000) :
	pass