import consoleParser
import socket
import select
import curses
import os
import sys
import math
import time
import tqdm
import _thread

######### Global variables so changing numbers is easier:
bufferSize = 8192
waitLtime = 1
waitStime = 0.5

typedMessage = ""

######### A class that im using as a struct in C, this is probably a bad practice:
class ccReturns:
	cont = False
	listSize = 0


def printHelp():
	######### This is a generic print help function for the clientConsole(). If the client writes a wrong command or something like that this shows up...
	print("\n\n")
	print("  file add: Adds a file to the download list.")	
	print("  file addn: Adds a file to the download list by its index number.")	
	print("  file remove: Removes a file from the download list.")
	print("  file removen: Removes a file from the download list by its index number.")
	print("  file clear: Erases all the contents from the download list.")
	print("  all files: Adds all the available files to de download list.")
	print("  * There is no distinction between file and files commands...")
	print("\n  show  files: Shows the files in your download list")
	print("  show sfiles: Shows the files that the server has available for download.")
	print("\n  update: Updates the server file list.")
	print("\n  download: Starts the download of the chosen files in your download list.")
	print("              ** If the list is empty, downloads everything from the server!")
	print("\n  disconnect: Ends the connection with the server.")
	print("\n  exit: Closes the program.")
	print("\n\n")



def clientConsole(s, filenumber, files):
	######### This is a function that is called by the client when it connects with a file server. It allows the client to choose wich files to download...
	retMe = ccReturns()
	########## The server sends us strings with all the info about the files available for download:
	serverFiles = []
	print("  Receiving the file list...")
	while len(serverFiles) < filenumber:
		filename = s.recv(bufferSize)
		decodedfilename = filename.decode("utf-8")
		actualfilename = ""
		for char in decodedfilename:
			if char == "|":
				serverFiles.append(actualfilename)
				actualfilename = ""
			else:
				actualfilename += char
	print("  Done. \n\n")
	
	######### Handling user commands:
	linea = input(" >> ")
	parsed = consoleParser.parsear(linea)
	comando = parsed[0]

	while comando != "download" and comando != "exit" and comando != "disconnect":
		if comando == "help" or comando == "-?" or comando == "-h" or comando == "?":		
			printHelp()
		elif comando == "show":
			if len(parsed) > 1:
				if parsed[1] == "file" or parsed[1] == "files":
					print("\n\n  ")
					if files:
						ind = 0
						for fil in files:
							print(f"  [{ind}]   {fil}")
							ind += 1
						ind = 0
					else: print("  File list is empty. (Download everything mode)")
					print("\n\n")
				if parsed[1] == "sfiles" or parsed[1] == "sfile":
					s.send(bytes("show sfiles", "utf-8"))
					print("\n\n")
					ind = 0
					for x in serverFiles:
						print(f"  [{ind}]   {x}")
						ind += 1
					ind = 0
					print("\n\n")
			else:
				print("\n ERROR: I don't know what to show. Use 'help' for more info.\n")
		elif comando == "file" or comando == "files":
			if len(parsed) > 2:
				if parsed[1] == "add":
					for x in range(2, len(parsed)):
						files.append(parsed[x])
				elif parsed[1] == "addn":
					for x in range(2, len(parsed)):
						try: files.append(serverFiles[int(parsed[x])])
						except IndexError: print("\n ERROR:",parsed[x],"overflows the index range. \n")
				elif parsed[1] == "remove":
					for x in range(2, len(parsed)):
						try: files.remove(parsed[x])
						except ValueError: print("\n ",parsed[x],"is not on the list. \n")
				elif parsed[1] == "removen":
					del parsed[0:2]
					parsed = list(map(int, parsed))
					for x in sorted(parsed, reverse=True):
						try: del files[x]
						except IndexError: print("\n ERROR:",x,"overflows the index range. \n")
				else: print("\n  I dont know what to do with that file list. I can only 'add', 'remove' or 'clear', nothing else! \n")
			elif parsed[1] == "clear" or parsed[1] == "clr": files.clear()
		elif comando == "all" and (parsed[1] == "file" or parsed[1] == "files"):
			files = serverFiles.copy()
		elif comando == "update":
			serverFiles.clear()
			print("  Receiving the file list...")
			s.sendall(bytes("update sfiles", "utf-8"))
			while len(serverFiles) < filenumber:
				filename = s.recv(bufferSize)
				decodedfilename = filename.decode("utf-8")
				actualfilename = ""
				for char in decodedfilename:
					if char == "|":
						serverFiles.append(actualfilename)
						actualfilename = ""
					else:
						actualfilename += char
				print("  Done. \n\n")	
			
		linea = input(" >> ")
		parsed = consoleParser.parsear(linea)
		comando = parsed[0]
	
	retMe.listSize = len(files)
	if comando == "download":
	######### We inform the file list size to the server and send it so he knows which files he has to send us.		
		if not files:
			files = serverFiles
			retMe.listSize = len(files)
		
		s.sendall(bytes("listsize", "utf-8"))
		time.sleep(waitStime)
		s.sendall(bytes(str(retMe.listSize), "utf-8"))
		time.sleep(waitStime)
		for fi in files:
			s.sendall(bytes(f"{fi}|", "utf-8"))
		retMe.cont = True
		return retMe
	elif comando == "disconnect":
		retMe.cont = False
		return retMe
	elif comando == "exit":
		s.close()		
		exit()
	else:
		print("\n  ERROR: Invalid command. Use 'help' for more info.\n")


def clientFileHandler(clientsocket, filenameList, files, address):
	######### This is a thread that is started by the file server to handle multiple clients at the same time...
	try:
		print("\n\n  Connection with",address,"has been established. \n")
		clientsocket.sendall(bytes("\n\n  Connection established! \n", "utf-8"))
		time.sleep(waitLtime)
		
		######### Notify the client what kind of server we are:
		clientsocket.sendall(bytes("Fileserver", "utf-8"))
		time.sleep(waitLtime)
		
		######### Sending how many files we have for download:		
		clientsocket.sendall(bytes(str(len(files)), "utf-8"))
		time.sleep(waitLtime)

		######### We send to the client the list of available files for download:
		print("  Sending file list...")		
		for filn in filenameList:
			clientsocket.sendall(bytes(f"{filn}|","utf-8"))
		print("  Done.\n")

		######### Client is chosing files (on clientConsole()):
		clientcommand = clientsocket.recv(bufferSize)
		while clientcommand.decode("utf-8") != "listsize":
			if clientcommand.decode("utf-8") == "update sfiles":
				for filn in filenameList:
					clientsocket.sendall(bytes(f"{filn}|","utf-8"))
			clientcommand = clientsocket.recv(bufferSize)

		######### Client is done chosing,  now we should receive a package with the size of the list of files that must be uploaded.
		print("\n  Receiving list of files to upload for the client...\n")			
		listsize = clientsocket.recv(bufferSize)
		toDownloadList = []
		while len(toDownloadList) < int(listsize.decode("utf-8")):
			recvfilename = clientsocket.recv(bufferSize)
			decodedRecvfilename = recvfilename.decode("utf-8")
			actualRecvfilename = ""
			for char in decodedRecvfilename:
				if char == "|":
					print("     ",actualRecvfilename)
					toDownloadList.append(actualRecvfilename)
					actualRecvfilename = ""
				else:
					actualRecvfilename += char
		print("\n  Done.")
					
		print("\n  Compiling list of files to upload...")
		index = 0
		indexlist = []
		for name in toDownloadList:
			for filename in filenameList: 
				if name == filename:
					indexlist.append(index)
					break				
				index +=1
			index = 0
		index = 0
		print("  Done.\n")
				
		######### Start sending all the files:
		for x in range(0, len(indexlist)):
			transferError = False
			print("\n ",address[0],"is downloading",files[indexlist[x]])
			filesize = os.stat(files[indexlist[x]]).st_size
			time.sleep(waitLtime)
					
			######### Send file header so the client knows filename and filesize:
			clientsocket.sendall(bytes(f"<{os.path.basename(files[indexlist[x]])}|{filesize}>", "utf-8"))
			time.sleep(waitLtime)				
					
			######### Open file and send everything in it:				
			with open(files[indexlist[x]], "rb") as fi:
				while fi.tell() < filesize:
					chunk = fi.read(bufferSize)
					if not chunk:
						break
					try:						
						clientsocket.sendall(chunk)
					except socket.error:
						print("\n  ERROR: Error sending data.")
						print("  Client",address[0],"disconnected?\n\n")
						transferError = True
						break
			if not transferError: print("  Done.")
	except KeyboardInterrupt:
		return


def ipv4ServerFilter(clientsocket, address, whitebool, whitelist, blackbool, blacklist):
	######### This function is called by ipv4FileServerFire() and ipv4ChatServerFire() when a new client is trying to connect.
	######### Filtering connections with blacklist and whitelist:
	if whitebool or blackbool:
		print("\n\n  Inbound connection from", address[0])
		clientsocket.sendall(bytes("\n\n  Waiting for approval...\n", "utf-8"))

		if whitebool:
			if not address[0] in whitelist:
				clientsocket.close()
				print("\n ",address[0],"Blocked, it was not on the whitelist.")
				return True
		if blackbool:
			if address[0] in blacklist:
				clientsocket.close()
				print("\n ",address[0],"Blocked, it was on the blacklist.")
				return True
	return False


def ipv4FileServerFire(ipaddr, chosenport, whitebool, whitelist, blackbool, blacklist, files):
	######### This is the function that is called when the user choses the server option and the file list is not empty on the main file: pylfer.py #########
	######### We create a list only with filenames, removing the file paths from the main list:
	filenameList = []
	for fil in files:
		filenameList.append(os.path.basename(fil))

	######### Creating the socket for connections:	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except:
		print("  ERROR: Socket creation failed. Check ip address, port and try again...")
		print("         Probably the port is already on use.\n\n")
		return
	try:
		s.bind((ipaddr, int(chosenport)))
	except:
		print("  ERROR: socket binding failed, try again or change the port.")
		print("\n\n")
		return
	s.listen(5)
	print("\n  Listening on port",chosenport,"...\n")

	try:	
		while True:
			######### Accepting the connection from the client:
			clientsocket, address = s.accept()
			if ipv4ServerFilter(clientsocket, address, whitebool, whitelist, blackbool, blacklist):
				continue

			######### A connection has passed all the filters, we send all the work to a thread so we can handle multiple clients...
			_thread.start_new_thread(clientFileHandler, (clientsocket, filenameList, files, address))			
				
	except KeyboardInterrupt:
		s.close()
		print("\n  Server stopped.\n\n")
		return


def ipv4ChatServerFire(ipaddr, chosenport, whitebool, whitelist, blackbool, blacklist):
	######### This is the function that is called when the user choses the server option and the file list is empty on the main file: pylfer.py #########
	######### Creating the socket for connections:	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except:
		print("  ERROR: Socket creation failed. Check ip address, port and try again...")
		print("         Probably the port is already on use.\n\n")
		return
	try:
		s.bind((ipaddr, int(chosenport)))
	except:
		print("  ERROR: socket binding failed, try again or change the port.")
		print("\n\n")
		return
	s.listen(5)
	print("\n  Listening on port",chosenport,"...\n")

	######### This is the list of all the sockets to broadcast the incoming messages to all the clients:
	socketList = [s]
	######### Start the server cycle:
	try:	
		while True:
			######### We use this so the server doesnt block when listening for new messages. It delegates the listening to the OS and it only tell us when a socket has something new i believe:
			read_sock, write_sock, excep_sock = select.select(socketList, [], socketList)
			for sock in read_sock:
				######### New clients arriving:
				if sock == s:
					######### Accepting the connection from the client, then we filter the socket with the blacklist and whitelist:
					clientsocket, address = s.accept()
					if ipv4ServerFilter(clientsocket, address, whitebool, whitelist, blackbool, blacklist):
						continue
					######### Sending the 'Ok, you are welcome' message:
					print("\n\n  Connection with",address,"has been established. \n")
					clientsocket.sendall(bytes("\n\n  Connection established! \n", "utf-8"))
					######### Appending the socket to the list so the client receives messages from other clients:
					socketList.append(clientsocket)
					time.sleep(waitLtime)
					######### Notify the client what kind of server we are:
					clientsocket.sendall(bytes("Chatserver", "utf-8"))
					time.sleep(waitLtime)
				######### Clients already connected sending messages:
				else:
					try:
						message = sock.recv(bufferSize)
						if not message:
							print("  A client has disconnected.\n")
							socketList.remove(sock)
							continue
					except:
						print("  A client has disconnected.\n")
						socketList.remove(sock)
						continue
					######### Printing messages on the server screen:
					decodedMessage = consoleParser.parseMessage(message.decode("utf-8")) 
					print(f"  {decodedMessage.username}: {decodedMessage.msg}")
					######### Broadcasting message to all the sockets (except the server):
					for clientsock in socketList:
						if clientsock != s and clientsock != sock:
							clientsock.sendall(bytes(f" {decodedMessage.username}: {decodedMessage.msg}", "utf-8"))
							time.sleep(waitLtime)
			for sock in excep_sock:
				socketList.remove(sock)
	except KeyboardInterrupt:
		s.close()
		print("\n  Server stopped.\n\n")
		return


def clientChatReceiver(serversocket):
	######### This is a thread that is called by the client when it connects with a chat server. It allows the client to receive and write messages at the same time:
	global typedMessage
	while True:
		try:			
			message = serversocket.recv(bufferSize)
		except:
			return
		if not message:
			print("  ERROR: There was a problem receiving a message.")
			print("         Maybe the server went offline.\n")
			return
		else:
			print("\r", " "*(len(typedMessage)+5), end = " ")
			decodedMessage = message.decode("utf-8")
			print("\r", decodedMessage, end = " ")
			print("\r\n  >> ", typedMessage, end = "\n\033[A") # Yep, this end is weird but it wouldnt print the typedMessage otherwise. We do a newline and then we come back.


def ipv4ClientFire(ipaddr, chosenport, files):
	######### This is the function that is called when the user choses the client mode on the main file: pylfer.py #########
	######### Creating the socket for connections:	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except s.error:
		print("  ERROR: Socket creation failed, try again. The port may be busy with another process.")
		print("\n\n")
		return 	

	######### Connecing to the server:
	try:	
		s.connect((ipaddr, int(chosenport)))
	except:
		print("  ERROR: Address-related error connecting to server.")
		print("         Is the port the right one?")
		print("\n\n")
		return	

	######### Catching server welcome message:
	msg = s.recv(30)
	print(msg.decode("utf-8"))
	
	######### Waiting for server to check if clients ip is on a whitelist/blacklist. Server should send a message if everything is ok.
	if msg.decode("utf-8") == "\n\n  Waiting for approval...\n":
		msg = s.recv(30)
		print(msg.decode("utf-8"))
	if msg.decode("utf-8") != "\n\n  Connection established! \n":
		print("\n  Connection finished. \n")
		return
	
	######### The server should tell us if it is a File server or a Chat server:
	msg = s.recv(10)
	if msg.decode("utf-8") == "Fileserver":
		######### Server should send us how many files has available for download:	
		msg = s.recv(8)
		filenumber = msg.decode("utf-8")
		msg = ""
		print("\n  There are",filenumber,"files available for download.")
		
		######### Now we can talk with the server, select all the files we want and stuff:
		keepGoing = clientConsole(s, int(filenumber), files)
		if keepGoing.cont:

			######### We send a message to the server to start the file transfer:
			print("  Starting download...\n")
			for x in range(0, keepGoing.listSize):
				
				######### We receive the file header from the server, we decode it so we know when a file is done downloading and which is its name:			
				fileRawHeader = s.recv(bufferSize)
				fileDecodedHeader = fileRawHeader.decode("utf-8")
				fileHeader = consoleParser.parseHeader(fileDecodedHeader)

				######### The file header could be corrupt. In that case we move on to the next file in the list.			
				if fileHeader.filesize == 0 or fileHeader.filename == "":
					print("  ERROR: There was a problem with the file header. \n")
					continue
				
				progress = tqdm.tqdm(fileHeader.filesize, f"  Downloading {fileHeader.filename}", unit="B", unit_scale=True, unit_divisor=1024, total = fileHeader.filesize)
				######### We create a file so we can write what we are downloading in it, using the filename that te server gave to us:			
				with open(fileHeader.filename, "wb") as fi:
					######### We check how big is the max variable size on this machine and if it is enough to handle the filesize:
					if fileHeader.filesize > sys.maxsize:
						byteaccumulator = 0
						while byteaccumulator < fileHeader.filesize:
							try:				
								chunk = s.recv(bufferSize)					
							except socket.error:
								print("  ERROR: Error receiving data.")
								print("\n\n")
								break
							if not chunk:
								break
							byteaccumulator += len(chunk)
							fi.write(chunk)
							progress.update(len(chunk))
					else:
						while fi.tell() < fileHeader.filesize:
							try:				
								chunk = s.recv(bufferSize)					
							except socket.error:
								print("  ERROR: Error receiving data.")
								print("\n\n")
								break
							if not chunk:
								break
							fi.write(chunk)
							progress.update(len(chunk))
				progress.close()
				print("  Done.\n")
		s.close()
	elif msg.decode("utf-8") == "Chatserver":
		username = input("  Username: ")
		print("\n\n")
		_thread.start_new_thread(clientChatReceiver,(s,))
		screen = curses.initscr()
		screen.keypad(True)
		try:
			global typedMessage
			print("  >> ", end = " ")
			while True:
				key = screen.getkey()
				if key != os.linesep:
					typedMessage += str(key)
				else:
					stringToPrint = "\r  " + username + ": " + typedMessage
					print(stringToPrint, end = "\r\n  >> ")
					sendstring = username + "|" + typedMessage
					s.sendall(bytes(sendstring, "utf-8"))
					time.sleep(waitLtime)
					typedMessage = ""
		except KeyboardInterrupt:
			print("\n\n")
			s.close()
			screen.keypad(False)
			curses.endwin()
			return
	else:
		print("  ERROR: There was a problem receiving the server identification message.")
		print("         Try connecting again.\n")
		s.close()
		return


















