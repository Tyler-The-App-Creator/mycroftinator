import requests
url = "https://srv11.akinator.com:9152/"
session = requests.get(url+"ws/new_session?callback=&partner=&player=website-desktop&uid_ext_session=&frontaddr=NDYuMTA1LjExMC40NQ==&constraint=ETAT%3C%3E%27AV%27")
data = session.json()
sessionID = data['parameters']['identification']['session']
signature = data['parameters']['identification']['signature']
progThres = 85

#makes a request to the akinator servers and returns the next question or answer in JSON format
def nextStep(answer, step):
	response = {
		"type":"",
		"json":{}
	}
	nextstep = requests.get(url+"ws/answer?callback=&session="+sessionID+"&signature="+signature+"&step="+str(step)+"&answer="+answer)
	response['json'] = nextstep.json()
	response['type'] = 'question'
	if float(response['json']['parameters']['progression']) >= progThres:
		guessAnswer = requests.get(url+"ws/list?callback=&session="+sessionID+"&signature="+signature+"&step="+str(step+1))
		if guessAnswer.json()['completion'] == "OK":
			response['json'] = guessAnswer.json()
			response['type'] = "answer"	
	return response

#parses JSON object into either answer or question
def getResponse(jsonObj):
	response = {
		"question":"",
		"answer":""
	}

	if jsonObj == data:
		response['question'] = jsonObj['parameters']['step_information']['question']
	else:
		if jsonObj['type'] == 'answer':
			response['answer'] = jsonObj['json']['parameters']['elements'][0]['element']['name']
		else:
			response['question'] = jsonObj['json']['parameters']['question']

	return response	

#Stores all options the user can enter as an answer, use ansToNumber['ans'] to retrieve the corresponding number
ansToNumber = {
	"yes":'0',
	"y":'0',
	"n":'1',
	"no":'1',
	"idk":"2",
	"i dont know":"2",
	"prob":"3",
	"probably":"3",
	"prob not":"4",
	"probably not":"4"
}