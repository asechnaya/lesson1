def get_answers(question, answers): 
		if question in answers:
			print((answers[question]).lower())
		else: 
			print('ой')
		return answers

while True:

	question = input ('question??  ')
	answers = {"привет": "И тебе привет!", "как дела": "Лучше всех", "пока": "Увидимся"}

	get_answers(question, answers)