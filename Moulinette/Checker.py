from CheckerLib import *
import Bash
import os, sys, shutil
import importlib

os.system("clear")

current_dir = os.path.dirname(os.path.realpath(__file__))
#check if minishell is compiled
if not os.path.exists(os.path.join(minishell_dir,"minishell")):
	print("Minishell not found")
	exit()
#copy minishell to temp folder
exec_dir = os.path.join(Bash.temp_dir,"tempExec")
if not os.path.exists(exec_dir):
	os.mkdir(exec_dir)
shutil.copy(os.path.join(minishell_dir,"minishell"),os.path.join(exec_dir,"minishell"))

# Importer les tests
for file in os.listdir(os.path.join(current_dir,"Tests")):
    if file.endswith(".py"):
        spec = importlib.import_module("Tests."+file[:-3])

os.chdir(exec_dir)

#if __name__ == "__main__":
#     sys.argv = [sys.argv[0]] + ['-d','-v','pipe_1']

if len(sys.argv) == 2 and sys.argv[1] == "help":
	print("Usage: python3 Checker.py [test] [all/norme]")
	print("Options:")
	print("  -d: Debug mode, affiche les commandes et les résultats")
	print("  -v: Valgrind mode, lance les tests avec valgrind")
	print("  -e: Empty environment, lance les tests avec un environnement vide")
	print("  -m=VALUE: Set ulimit -v VALUE")
	print("  -s=VALUE: Start tests from VALUE, default is norme")
	print("les options v,e,m ne peuvent pas être utilisées en même temps")

	exit()

if "-d" in sys.argv:
	BaseTest.DEBUG = True
	sys.argv.remove("-d")
     
if "-v" in sys.argv:
	Minishell.valgrind = True
	Bash.Bash.time_sleep *= 2
	sys.argv.remove("-v")

if "-e" in sys.argv:
	Minishell.envEmpty = True
	sys.argv.remove("-e")

#if start with -m=
idx = -1
for i in range(len(sys.argv)):
	if sys.argv[i].startswith("-m="):
		idx = i
		break
if idx != -1:
	try:
		Minishell.ulimit = str(int(sys.argv[idx][3:]))
	except:
		print("Error: Invalid value for -m")
	del sys.argv[idx]

#if start with -s=
StartTest = 'norme'
idx = -1
for i in range(len(sys.argv)):
	if sys.argv[i].startswith("-s="):
		idx = i
		break
if idx != -1:
	StartTest = sys.argv[idx][3:]
	del sys.argv[idx]


if len(sys.argv) > 2:
    PrintColor("Usage: python3 Checker.py [test] [all/norme]",Colors.RED)
    PrintColor("Help: python3 Checker.py help",Colors.RED)
    exit()

# Lancer les tests
if len(sys.argv) > 1 and sys.argv[1].lower() != "all":
    ID = sys.argv[1].lower()
    if ID in Tests:
        ExecTest(ID)
    else:
        print("Test not found")
else:
    res, lstFail = ExecAllTests(StartTest)
    if res:
        PrintColor("All tests passed",Colors.GREEN)
    else:
        PrintColor("Some tests failed",Colors.RED)
        PrintColor("Failed tests:\n" + "\n".join(lstFail),Colors.RED)
