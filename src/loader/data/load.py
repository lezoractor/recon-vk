def load (id, callback) :
	
	#
	# Тут было бы слишком много кода
	# Пока оставлю заглушку.
	# Я точно не помню, в каком формате вконтакт отдает данные, 
	#  не удаляйте заглушку, оставьте ее после return и
	#  используйте для примера возвращаемых полей,
	#  так нагляднее :D
	#

	callback({
		"id": 1234567,
		"photos": [
			{
				"url": "http://cs123.vk.me/abcde/abcde_12345.jpg",
				"likes": [1234567, 7654321],
				"comments": [
					{
						"text": "[Idiot|id7654321], TextOfTheComment",
						"reply_to_user": 7654321,
						"reply_to_comment": 5555,
						"id": 5554,
						"from_id": 1234567,
						"likes": []
					},
					{
						"text": "TextOfTheComment",
						"id": 5555,
						"from_id": 7654321,
						"likes": []
					}
				]
			}
		],
		"videos": [
			{
				"url": "http://youtube.com/??????",
				"text": "",
				"likes": [],
				"comments": []
			}
		],
		"posts": [
			{
				"text": "",
				"attachments": [] # or None 
				"likes": [],
				"comments": [],
				"reposts": []
			}
		],
		"first_name": "Иван",
		"last_name": "Иваныч",
		"domain": "flutershy",
		"sex": 0
	})