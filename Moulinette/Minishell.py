from Bash import Bash,temp_dir
import signal
import time
import os
from enum import Enum

current_dir = os.path.dirname(os.path.realpath(__file__))
exec_dir = os.path.dirname(current_dir)
minishell_dir = exec_dir

class Action(Enum):
	SEND = 1
	READ = 2
	SEND_SIGNAL = 3
	READ_ERROR = 4
	SEND_CTRLD = 5
	SEND_CTRLC = 6
	SEND_CTRLBACKSLASH = 7
	SEND_ARROWUP = 8
	SEND_ARROWDOWN = 9
	CLOSE = 10

def remove_specialChar(output):
	#replace all \n\x1b[A + \x1b[C * ? + \x1b[95m by \n\x1b[95m
	lines = output.split(" \n\x1b[A")
	new_text = lines[0]
	del lines[0]
	for line in lines:
		if not "\x1b[K" in line:
			return output
		temp = line.split("\n",1)
		new_text += "\n"+temp[1]
	return new_text

def cleanOutput(output):
	output = remove_specialChar(output)
	res = ""
	if "\033[95m" in output:
		lines = output.split("\033[95m")
	else:
		lines = output.split("\033[96m")
	res = lines[0]
	del lines[0]
	for line in lines:
		temp = line.split("\x1b[39m$ ",1)
		if len(temp) > 1:
			res += '@MINISHELL@>' + temp[1]
		else:
			res += temp[0]
	return res

def removePrompt(output):
	res = ""
	lines = output.split("@MINISHELL@>")
	res = lines[0]
	del lines[0]
	for line in lines:
		temp = line.split("\n",1)
		if len(temp) > 1:
			res += temp[1]
		else:
			res += temp[0]
	return res

def colorWhiteSpacesChar(char, color = "\033[41m", chars = ["\n","\t"," "]):
	if char in chars:
		#color background in red
		return color + char + "\033[0m"
	return char

def colorWhiteSpaces(str, color = "\033[41m", chars = ["\n","\t"," "]):
	for char in chars:
		str = str.replace(char, color + char + "\033[0m")
	return str

def RemoveBelowMain(output):
	def getLines(content, tofind):
		temps = content.split('\n')
		lines = []
		for line in temps:
			if tofind in line:
				lines.append(line)
		return lines
	forks = []
	reachables = getLines(output, "still reachable:")
	reachables = [(x.split('still reachable:',1)[1]).split(' ')[1] for x in reachables]
	reachables = [int(x.replace(",","")) for x in reachables]

	definitely = getLines(output, "definitely lost:")
	definitely = [(x.split('definitely lost:',1)[1]).split(' ')[1] for x in definitely]
	definitely = [int(x.replace(",","")) for x in definitely]

	indirectly = getLines(output, "indirectly lost:")
	indirectly = [(x.split('indirectly lost:',1)[1]).split(' ')[1] for x in indirectly]
	indirectly = [int(x.replace(",","")) for x in indirectly]

	possibly = getLines(output, "possibly lost:")
	possibly = [(x.split('possibly lost:',1)[1]).split(' ')[1] for x in possibly]
	possibly = [int(x.replace(",","")) for x in possibly]
	for childText in output.split("== ERROR SUMMARY:")[:-1]:
		lst = childText.split("(below main)")
		del lst[-1]
		lost = {"still reachable":0,"definitely lost":0,"indirectly lost":0,"possibly lost":0}
		for i in lst:
			if "blocks are still reachable in loss record" in i:
				temp = getLines(i, "blocks are still reachable in loss record")[-1]
				type = "still reachable"
			elif "blocks are definitely lost in loss record" in i:
				temp = getLines(i, "blocks are definitely lost in loss record")[-1]
				type = "definitely lost"
			elif "blocks are indirectly lost in loss record" in i:
				temp = getLines(i, "blocks are indirectly lost in loss record")[-1]
				type = "indirectly lost"
			elif "blocks are possibly lost in loss record" in i:
				temp = getLines(i, "blocks are possibly lost in loss record")[-1]
				type = "possibly lost"
			elif "terminating with default action of signal" in i:
				continue
			else:
				raise Exception("Error: Unknown type of lost")
			if "(" in temp:
				temp = temp.split('(',1)[1]
				temp = temp.split(')',1)[0]
				temp = temp.split(',')
				for v in temp:
					while v[0] == ' ':
						v = v[1:]
					v = v.split(' ')
					if v[1] == "direct":
						if type == "definitely lost":
							lost[type] += int(v[0].replace(",",""))
					elif v[1] == "indirect":
						if type == "indirectly lost":
							lost[type] += int(v[0].replace(",",""))
					elif v[1] == "possibly":
						if type == "possibly lost":
							lost[type] += int(v[0].replace(",",""))
					else:
						raise Exception("Error: Unknown type of lost")
			else:
				temp = temp.split(' ')[1]
				temp = temp.replace(",","")
				temp = int(temp)
				lost[type] += temp
		forks.append(lost)
	return reachables,definitely,indirectly,possibly, forks

def CheckLeaks(allowed_error = {}):#{"error contexts":count}
	def PrintRed(text):
		return "\033[91m"+text+"\033[0m\n"
	def PrintLineError(tofind):
		temp = text.split(tofind)
		del temp[0]
		strError = ""
		for line in temp:
			strError += line.split("\n",1)[0]+ "\n"
		return strError
	#check for leaks
	#with open(temp_dir+"/valgrind-out.txt", "r") as f:
	#	text = f.read()
	text = ""
	lst = os.listdir(temp_dir)
	for file in lst:
		if "valgrind-out." in file:
			with open(temp_dir+"/"+file, "r") as f:
				t = f.read()
				t = t.replace("All heap blocks were freed -- no leaks are possible","""LEAK SUMMARY:
==00000==    definitely lost: 0 bytes in 0 blocks
==00000==    indirectly lost: 0 bytes in 0 blocks
==00000==      possibly lost: 0 bytes in 0 blocks
==00000==    still reachable: 0 bytes in 0 blocks
==00000==         suppressed: 0 bytes in 0 blocks""")
				text +=t
			#remove file
			os.remove(temp_dir+"/"+file)
	reachables,definitely,indirectly,possibly, forks = RemoveBelowMain(text)

	count_reachables = 0
	for idx in range(len(reachables)):
		if reachables[idx] != forks[idx]["still reachable"]:
			count_reachables += 1

	count_definitely = 0
	for idx in range(len(definitely)):
		if definitely[idx] != forks[idx]["definitely lost"]:
			count_definitely += 1

	count_indirectly = 0
	for idx in range(len(indirectly)):
		if indirectly[idx] != forks[idx]["indirectly lost"]:
			count_indirectly += 1

	count_possibly = 0
	for idx in range(len(possibly)):
		if possibly[idx] != forks[idx]["possibly lost"]:
			count_possibly += 1
	
	allow_error_count = 0
	for key in allowed_error:
		if text.count(key) == allowed_error[key]:
			allow_error_count += allowed_error[key]
	summary =  text.count('ERROR SUMMARY:') != text.count('ERROR SUMMARY: 0 errors from 0 contexts') + allow_error_count
	jump = text.count('Conditional jump or move') != 0
	dlost =  text.count('definitely lost:') != text.count('definitely lost: 0 bytes in 0 blocks') and count_definitely != 0
	ilost = text.count('indirectly lost:') != text.count('indirectly lost: 0 bytes in 0 blocks') and count_indirectly != 0
	plost =  text.count('possibly lost:') != text.count('possibly lost: 0 bytes in 0 blocks') and count_possibly != 0
	slost = text.count('still reachable:') != text.count('still reachable: 0 bytes in 0 blocks') and count_reachables != 0
	error = summary or jump or dlost or ilost or plost or slost
	strError = ""
	if error:
		strError += PrintRed("Valgrind errors Detected :")
	if summary:
		strError += PrintRed("ERROR SUMMARY")
		strError += PrintLineError("ERROR SUMMARY: ")
	if jump:
		strError += PrintRed("Conditional jump or move")
	if dlost:
		strError += PrintRed("definitely lost")
		strError += PrintLineError("definitely lost: ")
	if ilost:
		strError += PrintRed("indirectly lost")
		strError += PrintLineError("indirectly lost: ")
	if plost:
		strError += PrintRed("possibly lost")
		strError += PrintLineError("possibly lost: ")
	if slost:
		strError += PrintRed("still reachable")
		strError += PrintLineError("still reachable: ")
	return strError


class Minishell:
	valgrind=False
	envEmpty=False
	ulimit="unlimited"
	def __init__(self, valgrind=False, envEmpty=False, ulimit="unlimited") -> None:
		self.bash = Bash()
		self.historic = []
		self.valgrind = valgrind or Minishell.valgrind
		self.envEmpty = envEmpty or Minishell.envEmpty
		self.ulimit = int(ulimit) if ulimit != "unlimited" else Minishell.ulimit
		self.allowed_error = {}
		if int(self.valgrind) + int(self.envEmpty) + int(self.ulimit != "unlimited") > 1:
			print("Error: Only one option can be set at a time")
			exit(1)
		if self.valgrind:
			print("Valgrind mode")
			val_temp_dir = temp_dir
			val_current_dir = current_dir
			#chqge to absolute path
			if not os.path.isabs(val_temp_dir):
				val_temp_dir = os.path.abspath(val_temp_dir)
			if not os.path.isabs(val_current_dir):
				val_current_dir = os.path.abspath(val_current_dir)
			self.bash.SendCommand("valgrind --child-silent-after-fork=no --leak-check=full --show-leak-kinds=all --show-below-main=no --track-origins=yes --trace-children=yes --log-file="+val_temp_dir+"/valgrind-out.%p --suppressions="+val_current_dir+"/ignore_readline.supp ./minishell")
			Bash.time_sleep = 0.5
			string = ""
			while not "@MINISHELL@>" in string:
				string = cleanOutput(self.bash.ReadAllOutput())
			self.bash.incOut = 0
			time.sleep(0.5)
		elif self.envEmpty:
			print("Empty environment mode")
			self.bash.SendCommand("env -i ./minishell")
		elif self.ulimit != "unlimited":
			print("Ulimit mode", self.ulimit)
			self.bash.SendCommand("ulimit -v "+str(self.ulimit)+";./minishell")
		else:
			self.bash.SendCommand("./minishell")

	def Send(self, command: str):
		self.historic.append((Action.SEND,command))
		self.bash.SendCommand(command)

	def Write(self, command: str):
		self.historic.append((Action.SEND,command))
		self.bash.WriteCommand(command)

	def Read(self):
		self.historic.append((Action.READ,""))
		return self.bash.ReadAllOutput()
	
	def SendSignal(self,signal_type):
		self.historic.append((Action.SEND_SIGNAL,signal_type))
		os.kill(self.bash.process.pid, signal_type)

	def ReadError(self):
		self.historic.append((Action.READ_ERROR,""))
		return self.bash.ReadAllError()
	
	def SendCtrlD(self):
		self.historic.append((Action.SEND_CTRLD,""))
		self.bash.SendCtrlD()

	def SendCtrlC(self):
		self.historic.append((Action.SEND_CTRLC,""))
		self.bash.SendCtrlC()

	def SendCtrlBackslash(self):
		self.historic.append((Action.SEND_CTRLBACKSLASH,""))
		self.bash.SendCtrlBackslash()

	def SendArrowUp(self):
		self.historic.append((Action.SEND_ARROWUP,""))
		self.bash.SendArrowUp()

	def SendArrowDown(self):
		self.historic.append((Action.SEND_ARROWDOWN,""))
		self.bash.SendArrowDown()
	
	def Close(self):
		self.historic.append((Action.CLOSE,""))
		self.bash.SendCtrlD()
		output = self.bash.ReadAllOutput()
		error = self.bash.ReadAllError()
		self.bash.close()
		#delete temp files
		if self.valgrind:
			error += CheckLeaks(self.allowed_error)
		return output, error
	
	def ExecAction(self, action):
		actions = {
			Action.SEND: self.Send,
			Action.READ: self.Read,
			Action.SEND_SIGNAL: self.SendSignal,
			Action.READ_ERROR: self.ReadError,
			Action.SEND_CTRLD: self.SendCtrlD,
			Action.SEND_CTRLC: self.SendCtrlC,
			Action.SEND_ARROWUP: self.SendArrowUp,
			Action.SEND_ARROWDOWN: self.SendArrowDown,
			Action.CLOSE: self.Close
		}
		actions[action[0]](action[1])
	
#SendSignal(signal.SIGTERM)  # Envoie SIGTERM au processus

class MinishellDiff(Minishell):
	def __init__(self) -> None:
		super().__init__()
		#self.bash.ReadAllOutput()
		#self.bash.SendCommand("")
		self.bashPosix = Bash()

	def Send(self, command: str):
		super().Send(command)
		self.bashPosix.SendCommand(command)

	def Write(self, command: str):
		super().Write(command)
		self.bashPosix.WriteCommand(command)

	def Read(self):
		return cleanOutput(super().Read())
	
	def ReadPosix(self):
		return self.bashPosix.ReadAllOutput()
	
	def CompareOutput(self, print_diff=False):
		outputPosix = ""
		output = self.Read()
		output+= "\n" + self.ReadError()
		temp = self.ReadPosix().split("\n")
		for line in temp:
			if "\x1b[95m" in line:
				continue
			else:
				outputPosix += line + '\n'
		if (len(temp) > 0):
			outputPosix = outputPosix[:-1]
		temp = self.ReadErrorPosix().split("\n")
		for line in temp:
			if ("line" in line):
				outputPosix+=line[14:]+"\n"
			else:
				outputPosix+=line+"\n"
		if (len(temp) > 0):
			outputPosix = outputPosix[:-1]
		#remove all lines with @MINISHELL@>
		output = removePrompt(output)
		if print_diff:
			str1 = ""
			str2 = ""
			index1, index2 = 0, 0
			while index1 < len(output) and index2 < len(outputPosix):
				if output[index1] == outputPosix[index2]:
					temp = "\033[92m" + output[index1] + "\033[0m"
					str1 += temp
					str2 += temp
					index1 += 1
					index2 += 1
				else:
					str1+="\033[91m" + colorWhiteSpaces(output[index1]) + "\033[0m"
					index1 += 1
			if index1 < len(output):
				str1+="\033[91m" + colorWhiteSpaces(output[index1:]) + "\033[0m"
			if index2 < len(outputPosix):
				str2+="\033[91m" + colorWhiteSpaces(outputPosix[index2:]) + "\033[0m"
			print("minishell:")
			print(str1)
			print("posix:")
			print(str2)
		return output == outputPosix
	
	def SendSignal(self,signal_type):
		super().SendSignal(signal_type)
		os.kill(self.bashPosix.process.pid, signal_type)

	def ReadError(self):
		return super().ReadError()
	
	def ReadErrorPosix(self):
		return self.bashPosix.ReadAllError()
	
	def SendCtrlD(self):
		super().SendCtrlD()
		self.bashPosix.SendCtrlD()

	def SendCtrlC(self):
		super().SendCtrlC()
		self.bashPosix.SendCtrlC()

	def SendArrowUp(self):
		super().SendArrowUp()
		self.bashPosix.SendArrowUp()

	def SendArrowDown(self):
		super().SendArrowDown()
		self.bashPosix.SendArrowDown()

	def SendCtrlBackslash(self):
		super().SendCtrlBackslash()
		self.bashPosix.SendCtrlBackslash()

	def Close(self):
		self.historic.append((Action.CLOSE,""))
		self.bash.SendCtrlD()
		self.bashPosix.SendCtrlD()
		output = self.bash.ReadAllOutput()
		outputPosix = self.bashPosix.ReadAllOutput()
		error = self.bash.ReadAllError()
		errorPosix = self.bashPosix.ReadAllError()
		self.bash.close()
		self.bashPosix.close()
		#delete temp files
		if outputPosix:
			outputPosix = "\n@POSIX@\n"+outputPosix
		if errorPosix:
			errorPosix = "\n@POSIX@\n"+errorPosix
		if self.valgrind:
			error += CheckLeaks(self.allowed_error)
		return output+outputPosix, error+errorPosix

if __name__ == "__main__":
	os.chdir(exec_dir)
	testO = MinishellDiff()
	testO.Send("ls")
	print(testO.CompareOutput(True))