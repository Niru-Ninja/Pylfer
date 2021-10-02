import banners
import connection
import consoleParser
import portforwardlib
import os
import glob


def printHelp():

	######### Printing all the help as pretty as we can:
	print("\n\n")
	print("  banner: Shows a pretty random banner.\n")
	print("  set: Changes an option before the connection. You can change:\n")
	print("           mode: client/server")
	print("           ip: ip to connect to as a client. Can be equal to 'localhost' or 'locip' for automated ip assignment.")
	print("           ipmode: ipv4/ipv6 changes automatically if you specify an ip address.")
	print("           port: port to set up the connection.")
	print("           upnp: on/off enables upnp port forwarding.")
	print("           whitelist: on/off allows only specified ips to connect to your server.")
	print("           blacklist: on/off prevents the specified ips to connect to your server.")
	print("\n  show: Shows the values of each option. You can specify a particular option to only show that value (more detail).")
	print("  show locip: Shows your local ip.")
	print("\n\n  FILE LIST: As a server, this is the list of files that will be available for download.")
	print("             If left empty, the server will start as a chat server.")
	print("             As a client, this is the list of files you will request to the server for download.")
	print("             You can leave it empty and use 'show sfiles' command after the connection to select wich files to download.\n")
	print("  file add: Adds a file to the file list.")
	print("  file allfilesin: Adds all files from a directory to the file list.")
	print("  file remove: Removes a file from the file list.")
	print("  file removen: Removes a file from the file list by its index number.")
	print("  file clear: Erases all contents from the file list.")
	print("\n\n  WHITELIST: Its only used in server mode. Is the list of ips that are allowed to connect to the server. Its not obligatory.")
	print("             It doesnt work if the whitelist parameter is not set to true ('set whitelist true')\n")
	print("  whitelist add: Adds an ip to the whitelist.")
	print("  whitelist remove: Removes an ip from the whitelist.")
	print("  whitelist removen: Removes an ip from the whitelist by its index number.")
	print("  whitelist clear: Erases all contents from the whitelist.")
	print("\n\n  BLACKLIST: Its only used in server mode. Its the list of ips that are not allowed to connect to the server. Its not obligatory.")
	print("             It doesnt work if the blacklist parameter is not set to true ('set blacklist true')\n")
	print("  blacklist add: Adds an ip to the blacklist.")
	print("  blacklist remove: Removes an ip from the blacklist.")
	print("  blacklist removen: Removes an ip from the blacklist by its index number.")
	print("  blacklist clear: Erases all contents from the blacklist.")
	print("\n\n  fire: executes the connection with the chosen options.")
	print("\n  exit: Closes the program.")
	print("\n\n")


def validIPAddress(IP):
	######### Checks if the ip that the user gave to us is valid, and identifies if it is IPv4 or IPv6:	
	def isIPv4(s):
		try: return str(int(s)) == s and 0 <= int(s) <= 255
		except: return False
	def isIPv6(s):
		if len(s) > 4:
			return False
		try : return int(s, 16) >= 0 and s[0] != '-'
		except:
			return False
	if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
		return "IPv4"
	if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
		return "IPv6"
	return "ERROR"


def checkFileList(files):
	######### Checking if files chosen by the server exist so there is no problem when uploading:
	for x in range(0,len(files)):
		if os.path.isfile(files[x]):
			continue
		else:
			print("\n  The file:",files[x]," does not exist.") 
			answ = input("  Do you want to remove it? y/n    ")
			if answ == "y": files.remove(files[x])
			print("\n")
			return False
	return True


def allFilesInDirectory(directory):
	######### Returns a list with all the filepaths of the files in a given directory:
	retMe = [f for f in glob.glob(directory + "**/*", recursive=True)]
	return retMe


######### We print our awesome banner:
banners.printBanner()

######### Default values of all the options:
mode = "client"
ip = "127.0.0.1"
port = "4444"
upnp = False
files = []
whitelist = []
whitebool = False
blacklist = []
blackbool = False
ipmode = "IPv4"

######### Pre-cycle for user input:
linea = input(" > ")
parsed = consoleParser.parsear(linea)
comando = parsed[0]

######### Listening at user commands and responding accordingly:
while comando != "exit":

	######### Print-stuff commands:
	if comando == "help" or comando == "-?" or comando == "-h" or comando == "?":
		printHelp()
	elif comando == "banner":
		banners.printBanner()

	######### If the user wants to set some option:
	elif comando == "set":
		if len(parsed) > 2:
			if parsed[1] == "mode" or parsed[1] == "mod":
				if parsed[2] == "client" or parsed[2] == "server":
					mode = parsed[2]
				else: print("\n  ERROR: Only 'client' or 'server' is allowed here.\n")
			elif parsed[1] == "ipmode" or parsed[1] == "ipmod" or parsed[1] == "ipm":
				if parsed[2] == "ipv4" or parsed[2] == "4" or parsed[2] == "v4":
					ipmode = "IPv4"
				elif parsed[2] == "ipv6" or parsed[2] == "6" or parsed[2] == "v6":
					ipmode = "IPv6"
				else: print("\n  ERROR: Only 'ipv4', 'v4' or '4'. Or 'ipv6', 'v6' or '6' are the valid options.\n")
			elif parsed[1] == "ip":
				if parsed[2] == "locip":
					ip = portforwardlib.get_my_ip()
					ipmode = validIPAddress(ip)
				else:
					ipmode = validIPAddress(parsed[2])
					if ipmode == "ERROR" and parsed[2] != "localhost": print("\n ERROR: The ip address is not valid. \n")
					elif parsed[2] == "localhost": ip = "127.0.0.1"
					else: ip = parsed[2]
			elif parsed[1] == "port":
				if int(parsed[2]) < 65535:
					port = parsed[2]
				else: print("\n  ERROR: Port number is too high. Must be < 65535. \n")
			elif parsed[1] == "upnp":
				if parsed[2] == "on" or parsed[2] == "1" or parsed[2] == "true": upnp = True
				elif parsed[2] == "off" or parsed[2] == "0" or parsed[2] == "false": upnp = False
				else: print("\n  ERROR: upnp can be set only to 'on' or 'off'. We are working with bools here, 1 or 0, true or false. Pick one!")
			elif parsed[1] == "whitelist":
				if parsed[2] == "on" or parsed[2] == "1" or parsed[2] == "true": whitebool = True
				elif parsed[2] == "off" or parsed[2] == "0" or parsed[2] == "false": whitebool = False
				else: print("\n  ERROR: Only 'on' or 'off' for whitelist. '1' or '0', 'true' or 'false' are also valid. Check 'help'")
			elif parsed[1] == "blacklist":
				if parsed[2] == "on" or parsed[2] == "1" or parsed[2] == "true": blackbool = True
				elif parsed[2] == "off" or parsed[2] == "0" or parsed[2] == "false": blackbool = False
				else: print("\n  ERROR: Only 'on' or 'off' for blacklist. '1' or '0', 'true' or 'false' are also valid. Check 'help'")
			else: print("\n  ERROR: I dont know what you want to set.\n")
		else: print("\n  ERROR: You will need more parameters than that. Use 'help' for more info.\n")
	
	######### The user wants us to show all the options and we do so:	
	elif comando == "show":
		######### Differentiating between showing a particular option, or showing all the options: first we do the particular ones:
		if len(parsed) > 1 and parsed[1] != "options":
			if parsed[1] == "mode" or parsed[1] == "mod": print("\n  mode: ",mode,"\n")
			if parsed[1] == "ip": print("\n  ip: ",ip,"\n")
			if parsed[1] == "ipmode" or parsed[1] == "ipmod" or parsed[1] == "ipm": print("\n  ipmode: ",ipmode,"\n")
			if parsed[1] == "port": print("\n  port: ",port,"\n")
			if parsed[1] == "upnp": print("\n  upnp: ",upnp,"\n")
			if parsed[1] == "locip": print("\n  Local IP:",portforwardlib.get_my_ip(),"\n")

			######### Here we do all the lists: whitelist, blacklist and filelist.
			if parsed[1] == "whitelist": 
				print("\n  whitelist status: ",whitebool,"\n") 
				if whitelist:
					ind = 0
					for x in whitelist:
						print(f"  [{ind}]   {x}")
						ind += 1
					ind = 0
					print("\n\n") 
			if parsed[1] == "blacklist": 
				print("\n  blacklist status: ",blackbool,"\n  ")
				if blacklist:
					ind = 0
					for x in blacklist:
						print(f"  [{ind}]   {x}")
						ind += 1
					ind = 0
					print("\n\n")
			if parsed[1] == "file" or parsed[1] == "files":
				print("\n\n  ")
				if files:
					ind = 0
					for file in files:
						print(f"  [{ind}]   {file}")
						ind += 1
					ind = 0
				else: print("File list is empty.")
				print("\n\n")

			######### The user seems to be lost or something idk:
			if parsed[1] == "help":
				print("\n You are not supposed to use this command that way! But i'll help you anyways...")
				printHelp()

		######### Showing all the options:
		else:
			print("\n\n  	mode: ",mode,"\n")
			print("  	ip: ",ip,"\n")
			print("  	ipmode: ",ipmode,"\n")
			print("  	port: ",port,"\n")
			print("  	upnp: ",upnp,"\n")
			print("  	whitelist: ",whitebool,"\n")
			print("  	blacklist: ",blackbool,"\n\n")

	######### Handling file and directory names input:
	elif comando == "file" or comando == "files":
		if len(parsed) > 2:
			if parsed[1] == "add":
				for x in range(2, len(parsed)):
					files.append(parsed[x])
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
			elif parsed[1] == "allfilesin":
				if os.path.exists(parsed[2]):
					files.extend(allFilesInDirectory(parsed[2]))
				else:
					print("\n  ERROR: directory not found. \n")
			else: print("\n  I dont know what to do with that file list. I can only 'add', 'remove' or 'clear', nothing else! \n")
		elif parsed[1] == "clear" or parsed[1] == "clr": files.clear()

	######### Handling ips input on Whitelist and Blacklist, both are almost the same:
	elif comando == "whitelist":
		if len(parsed) > 2:
			if parsed[1] == "add":
				for x in range(2, len(parsed)):
					if validIPAddress(parsed[x]) != "ERROR": whitelist.append(parsed[x])
					else: print("\n ",parsed[x],"is not a valid ip address. \n")
			elif parsed[1] == "remove":
				for x in range(2, len(parsed)):
					try: whitelist.remove(parsed[x])
					except ValueError: print("\n ",parsed[x],"is not on the list. \n")
			elif parsed[1] == "removen":
				del parsed[0:2]
				parsed = list(map(int, parsed))
				for x in sorted(parsed, reverse=True):
					try: del whitelist[x]
					except IndexError: print("\n ERROR:",x,"overflows the index range. \n")
			else: print("\n  I dont know what to do with that whitelist. I can only 'add', 'remove' or 'clear', nothing else! \n")
		elif parsed[1] == "clear" or parsed[1] == "clr": whitelist.clear()
		elif parsed[1] == "on" or parsed[1] == "1" or parsed[1] == "true": whitebool = True
		elif parsed[1] == "off" or parsed[1] == "0" or parsed[1] == "false": whitebool = False
	elif comando == "blacklist":
		if len(parsed) > 2:
			if parsed[1] == "add":
				for x in range(2, len(parsed)):
					if validIPAddress(parsed[x]) != "ERROR": blacklist.append(parsed[x])
					else: print("\n",parsed[x],"is not a valid ip address. \n")
			elif parsed[1] == "remove":
				for x in range(2, len(parsed)):
					try: blacklist.remove(parsed[x])
					except ValueError: print("\n ",parsed[x],"is not on the list. \n")
			elif parsed[1] == "removen":
				del parsed[0:2]
				parsed = list(map(int, parsed))
				for x in sorted(parsed, reverse=True):
					try: del blacklist[x]
					except IndexError: print("\n ERROR:",x,"overflows the index range. \n")
			else: print("\n  I dont know what to do with that blacklist. I can only 'add', 'remove' or 'clear', nothing else! \n")
		elif parsed[1] == "clear" or parsed[1] == "clr": blacklist.clear()
		elif parsed[1] == "on" or parsed[1] == "1" or parsed[1] == "true": blackbool = True
		elif parsed[1] == "off" or parsed[1] == "0" or parsed[1] == "false": blackbool = False
	
	######### All options ready, user wants to fire up the connection:
	elif comando == "fire":
		######### This is for upnp, it usually fails on windows so we save the 'success' of the function to handle the failures:
		success = True
		if upnp:
			success = portforwardlib.forwardPort(port,port,None,ip,False,"TCP",0,"Pylfer",True)

		######### Checking if we are server or client and what version of ip we have:	
		if mode == "server" and ipmode == "IPv4" and success:
			######### Remember if file list is empty then we should be a chat server:
			if files:
				######### Just checking if all the files exist, maybe there was an input error here:
				if checkFileList(files):
					######### All ok, lets go:
					connection.ipv4FileServerFire(ip, port, whitebool, whitelist, blackbool, blacklist, files)
				else: print("  ERROR: There was a problem with at least one file on de file list... \n\n")
			else:
				connection.ipv4ChatServerFire(ip, port, whitebool, whitelist, blackbool, blacklist)
		######### Client connection is easier, not much to check:
		elif mode == "client" and ipmode == "IPv4" and success:
			connection.ipv4ClientFire(ip, port, files)
		######### IPv6 connections, i have no idea how to do those yet:
		elif ipmode == "IPv6": print("  Sorry, but Pylfer does not support IPv6 connection yet. \n\n")

		######### Upnp failed, probably a windows machine or upnp is disabled, or the device doesnt support upnp:
		elif not success:
			print("\n  ERROR: Upnp port forwarding failed. ")
			print("  Connection has not started because upnp failed, set it to false or check your upnp device. \n")

	######### The user messed up the command, nothing matches with the input:
	else: print("\n  ERROR: Invalid command. Use 'help' for more info.\n")
	
	linea = input(" > ")
	parsed = consoleParser.parsear(linea)
	comando = parsed[0]