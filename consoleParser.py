class Header:
	filename = ""
	filesize = 0

class MsgPacket:
	username = ""
	msg = ""


def parsear(com):
	######### The structure of a command is: COMMAND PARAMETER1 PARAMETER2 [...] PARAMETER-N
	######### The user can also use "" to simbolize that spaces are considered part of a parameter, like this: COMMAND PARAMETER1 "STRING WITH SPACES AS PARAMETER2" PARAMETER3 [...]
	com += " "
	acumulador = ""
	palabras = []

	onsameword = False
	for caracter in com:
		if caracter == '"': 
			onsameword = not onsameword
			continue
		if onsameword: acumulador += caracter
		elif caracter != " ": acumulador += caracter
		else:
			palabras.append(acumulador)
			acumulador = ""
	return palabras


def parseHeader(packHead):
	######### The structure of a header is: <FILENAME|FILESIZE>
	retMe = Header()
	retMe.filename = ""

	infilesize = False

	auxcount = 0
	auxstring = ""
	if packHead[0] != '<':
		return retMe

	for x in range(1, len(packHead)):
		if packHead[x] == '|':
			break
		retMe.filename += packHead[x]
		auxcount = x + 1

	if auxcount >= len(packHead):
		return retMe
	if packHead[auxcount] != '|':
		return retMe

	for r in range(auxcount+1, len(packHead)):
		if packHead[r] == '>': break
		auxstring += packHead[r]

	retMe.filesize = int(auxstring)
	return retMe


def parseMessage(message):
	######### The structure of a message is: USERNAME|MESSAGE
	retMe = MsgPacket()
	inusername = True
	for char in message:
		if inusername:
			if char == "|":
				inusername = False
				continue
			retMe.username += char
		else:
			retMe.msg += char
	return retMe










	
