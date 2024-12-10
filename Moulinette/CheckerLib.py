import os
import sys
import time
import subprocess
from Minishell import *

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    
class ColorsBg:
    RED = '\033[101m'
    GREEN = '\033[102m'
    YELLOW = '\033[103m'
    BLUE = '\033[104m'
    PURPLE = '\033[105m'
    CYAN = '\033[106m'
    WHITE = '\033[107m'

def PrintColor(text,color,end="\n"):
    print(color+text+'\033[0m',end=end)

def IfValid(valid,title="",end="\n"):
    if valid :
        PrintColor("OK ! "+title,Colors.GREEN)
    else:
        PrintColor("Error ! "+title,Colors.RED)
    return valid

def CheckNorme(path, normeflag):
    res = subprocess.run(["norminette"]+normeflag+[path],stdout=subprocess.PIPE,cwd=minishell_dir)
    result = res.stdout.decode().rstrip()
    string = ""
    valid = True
    for line in result.split("\n"):
        if not ": OK!" in line:
            if line != "":
                valid = False
                string += line+"\n"
    if not valid:
        PrintColor(string,Colors.RED)
    return valid

def DebugPrint(*args, **kargs):
    if BaseTest.DEBUG:
        print(*args, **kargs)

class BaseTest:
    DEBUG = False
    def __init__(self, id, *args, **kargs):
        self.success = False
        self.id = id
        self.tempfiles = []
        
    def WriteTempFile(self, path, content):
        self.tempfiles.append(path)
        with open(path,"w") as file:
            file.write(content)
        return
    
    def CreateTempDir(self, path):
        self.tempfiles.append(path)
        os.mkdir(path)
        return
    
    def Init(self):
        self.minishell = Minishell()
        return 

    def Run(self):
        return True
    
    def PrintResult(self):
        return 
    
    def Close(self):
        #reverse order to delete files first
        out, error = self.minishell.Close()
        self.tempfiles.reverse()
        for file in self.tempfiles:
            if os.path.exists(file):
                if os.path.isdir(file):
                    os.rmdir(file)
                else:
                    os.remove(file)
        if error:
            PrintColor(error,Colors.RED)
            return False
        return True

Tests = {}

def AddTest(id, *args, **kargs):
    id = str(id).lower()
    def decorator(classType):
        Tests[id] = classType(id, *args, **kargs)
        return classType
    return decorator

def BetterId(id):
    #detect if id as ex00 etc...
    id = str(id)
    string = ""
    i = 0
    while i < len(id) and id[i].isalpha():
        string += id[i]
        i += 1
    string += " "
    string += id[i:].replace("_"," ")
    string = string[0].upper() + string[1:]
    return string

def ExecTest(id):
    res = True
    if id in Tests:
        exo = Tests[id]
        PrintColor("#"*15+" "+BetterId(exo.id)+" "+"#"*15,Colors.YELLOW)
        exo.Init()
        exo.success = exo.Run()
        exo.PrintResult()
        res = exo.success and res
        IfValid(exo.success,BetterId(exo.id))
        error = exo.Close()
        if not error:
            IfValid(False,"Error while closing test")
            exo.success = False
        PrintColor("#"*40,Colors.YELLOW if exo.success else Colors.RED)
        res = exo.success and res
    else:
        res = False
        print(f"Test {id} not found")
    print("")
    return res
    
def ExecAllTests(StartTest):
    lstFail = []
    lst = list(Tests.keys())
    #lst.sort()
    res = True
    #place norme at the top
    if "norme" in lst:
        lst.remove("norme")
        lst = ["norme"] + lst
    if StartTest in lst:
        while lst[0] != StartTest:
            lst.pop(0)
    for id in lst:
        resTemp = ExecTest(id)
        if not resTemp:
            lstFail.append(id)
        res = resTemp and res
    return res, lstFail