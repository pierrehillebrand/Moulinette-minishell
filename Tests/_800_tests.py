from CheckerLib import *

class TestReturnNothing(BaseTest):
    def __init__(self, id, *args, **kargs):
        super().__init__(id, *args, **kargs)
    
    def _input(self):
        return ""
    
    def Run(self):
        __input = self._input()
        self.minishell.Send(__input)
        output = self.minishell.Read()
        output = cleanOutput(output)
        correct_output = "@MINISHELL@>"+__input+"\n@MINISHELL@>"
        res = output == correct_output
        output = colorWhiteSpaces(output,ColorsBg.CYAN, chars=["\t"," "])
        correct_output = colorWhiteSpaces(correct_output,ColorsBg.CYAN, chars=["\t"," "])
        DebugPrint("your output:\n"+output+"\ncorrect output:\n"+correct_output)
        return res

class TestDiff(BaseTest):
    def __init__(self, id, *args, **kargs):
        super().__init__(id, *args, **kargs)
    
    def Init(self):
        self.minishell = MinishellDiff()
        return 

    def _input(self):
        return ""
    
    def Run(self):
        _input = self._input()
        self.minishell.Send(_input)
        self.minishell.Send("echo $?")
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

class TestDiffExit(BaseTest):
    def __init__(self, id, *args, **kargs):
        super().__init__(id, *args, **kargs)
    
    def Init(self):
        self.minishell = MinishellDiff()
        return 

    def _input(self):
        return ""
    
    def Run(self):
        _input = self._input()
        self.minishell.Send(_input)
        self.minishell.Send("echo $?")
        output = self.minishell.Read() + "\n"
        temp = self.minishell.ReadError().split("\n")
        for line in temp:
            if ("line" in line):
                output+=line[14:]+"\n"
            else:
                output+=line+"\n"
        if (len(temp) > 0):
            output = output[:-1]
        outputPosix = "exit\n" + self.minishell.ReadPosix() + "\n"
        temp = self.minishell.ReadErrorPosix().split("\n")
        for line in temp:
            if ("line" in line):
                outputPosix+=line[14:]+"\n"
            else:
                outputPosix+=line+"\n"
        if (len(temp) > 0):
            outputPosix = outputPosix[:-1]
        output = removePrompt(output)
        if (BaseTest.DEBUG):
            print("minishell:")
            print(output)
            print("bash posix:")
            print(outputPosix)
        res = output == outputPosix
        DebugPrint("Is output correct: ",res)
        return res

class TestReturn(BaseTest):
    def __init__(self, id, *args, **kargs):
        super().__init__(id, *args, **kargs)

    def _input(self):
        return ""

    def _response(self):
        return ""

    def Run(self):
        __input = self._input()
        response = self._response()
        self.minishell.Send(__input)
        output = self.minishell.Read()
        output = cleanOutput(output)
        correct_output = "@MINISHELL@>"+__input+"\n"+response+"@MINISHELL@>"
        res = output == correct_output
        output = colorWhiteSpaces(output,ColorsBg.CYAN, chars=["\t"," "])
        correct_output = colorWhiteSpaces(correct_output,ColorsBg.CYAN, chars=["\t"," "])
        DebugPrint("your output:\n"+output+"\ncorrect output:\n"+correct_output)
        return res

class TestReturnError(BaseTest):
    def _input(self):
        return ""
    
    def _error(self):
        return ""
    
    def error_unexpected(self,name):
        return "syntax error near unexpected token `" + name + "'\n"
    
    def error_is_directory(self,name):
        return name + ": Is a directory\n"
    
    def error_cmd_not_found(self,name):
        return name + ": command not found\n"

    def error_no_such(self,name):
        return name + ": No such file or directory\n"
    
    def error_invalid_identifier(self, name):
        return "export: `" + name + "': not a valid identifier\n"
    
    def error_learn_to_use(self, name, flag):
        return name + ": " + flag + ": invalid option\n" + name + ": usage: " + name + " [-fn] [name[=value] ...] or export -p\n"

    def Run(self):
        __input = self._input()
        self.minishell.Send(__input)
        output = self.minishell.Read()
        output = cleanOutput(output)
        correct_output = "@MINISHELL@>"+__input+"\n@MINISHELL@>"
        res = output == correct_output
        output = colorWhiteSpaces(output,ColorsBg.CYAN, chars=["\t"," "])
        correct_output = colorWhiteSpaces(correct_output,ColorsBg.CYAN, chars=["\t"," "])
        DebugPrint("your output:\n"+output+"\ncorrect output:\n"+correct_output)
        output = self.minishell.ReadError()
        res = output == self._error() and res
        DebugPrint("your error:\n"+output+"\ncorrect error:\n"+self._error())
        return res

@AddTest("newline_1")#line 2
class TestTest(TestReturnNothing):
    def _input(self):
        return ""
    
@AddTest("space_1")#line 3
class TestTest(TestReturnNothing):
    def _input(self):
        return "                 "
    
@AddTest("tab_1")#line 4
class TestTest(BaseTest):
    def Init(self):
        super().Init()
        self.CreateTempDir("test")
        self.minishell.Send("cd test")
        self.minishell.Read()
        self.minishell.Send("")
        self.minishell.bash.incOut+=1
    
    def Run(self):
        __input = "\t"
        self.minishell.Send(__input)
        output = self.minishell.Read()
        output = cleanOutput(output)
        correct_output = "@MINISHELL@>"+"\n@MINISHELL@>"
        res = output == correct_output
        output = colorWhiteSpaces(output,ColorsBg.CYAN, chars=["\t"," "])
        correct_output = colorWhiteSpaces(correct_output,ColorsBg.CYAN, chars=["\t"," "])
        DebugPrint("your output:\n"+output+"\ncorrect output:\n"+correct_output)
        return res
    
@AddTest("colon_1")#line 5
class TestTest(TestReturnError):
    def _input(self):
        return ":"

    def _error(self):
        return self.error_cmd_not_found(":")

@AddTest("semicolon_1")#added line
class TestTest(TestReturnError):
    def _input(self):
        return ";"

    def _error(self):
        return self.error_cmd_not_found(";")
    
@AddTest("exclamation_1")#line 6
class TestTest(TestReturnError):
    def _input(self):
        return "!"

    def _error(self):
        return self.error_cmd_not_found("!")
    
@AddTest("redir_out_1")#line 7
class TestTest(TestReturnError):
    def _input(self):
        return ">"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("redir_in_1")#line 8
class TestTest(TestReturnError):
    def _input(self):
        return "<"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("redir_out_append_1")#line 9
class TestTest(TestReturnError):
    def _input(self):
        return ">>"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("redir_in_heredoc_1")#line 10
class TestTest(TestReturnError):
    def _input(self):
        return "<<"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("redir_in_out_1")#line 11
class TestTest(TestReturnError):
    def _input(self):
        return "<>"
    
    def _error(self):
        return self.error_unexpected(">")
    
@AddTest("redir_out_2")#line 12
class TestTest(TestReturnError):
    def _input(self):
        return ">>>>>"
    
    def _error(self):
        return self.error_unexpected(">>")
    
@AddTest("redir_out_3")#line 13
class TestTest(TestReturnError):
    def _input(self):
        return ">>>>>>>>>>>>>>>"
    
    def _error(self):
        return self.error_unexpected(">>")
    
@AddTest("redir_in_2")#line 14
class TestTest(TestReturnError):
    def _input(self):
        return "<<<<<"
    
    def _error(self):
        return self.error_unexpected("<<")
    
@AddTest("redir_in_3")#line 15
class TestTest(TestReturnError):
    def _input(self):
        return "<<<<<<<<<<<<<<<"
    
    def _error(self):
        return self.error_unexpected("<<")
    
@AddTest("redir_out_4")#line 16
class TestTest(TestReturnError):
    def _input(self):
        return "> > > >"
    
    def _error(self):
        return self.error_unexpected(">")
    
@AddTest("redir_out_5")#line 17
class TestTest(TestReturnError):
    def _input(self):
        return ">> >> >> >>"
    
    def _error(self):
        return self.error_unexpected(">>")
    
@AddTest("redir_out_6")#line 18
class TestTest(TestReturnError):
    def _input(self):
        return ">>>> >> >> >>"
    
    def _error(self):
        return self.error_unexpected(">>")

@AddTest("fslash_1")#line 19
class TestTest(TestReturnError):
    def _input(self):
        return "/"
    
    def _error(self):
        return self.error_is_directory("/")
    
@AddTest("fslash_2")#line 20
class TestTest(TestReturnError):
    def _input(self):
        return "//"
    
    def _error(self):
        return self.error_is_directory("//")
    
@AddTest("fslash_3")#line 21
class TestTest(TestReturnError):
    def _input(self):
        return "/."

    def _error(self):
        return self.error_is_directory("/.")
    
@AddTest("fslash_4")#line 22
class TestTest(TestReturnError):
    def _input(self):
        return "/./../../../../.."
        
    def _error(self):
        return self.error_is_directory("/./../../../../..")
    
@AddTest("fslash_5")#line 23
class TestTest(TestReturnError):
    def _input(self):
        return "///////"
        
    def _error(self):
        return self.error_is_directory("///////")
    
@AddTest("hyphen_1")#line 24
class TestTest(TestReturnError):
    def _input(self):
        return "-"
        
    def _error(self):
        return self.error_cmd_not_found("-")
    
@AddTest("pipe_error_1")#line 25
class TestTest(TestReturnError):
    def _input(self):
        return "|"
        
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("pipe_error_2")#line 26
class TestTest(TestReturnError):
    def _input(self):
        return "| hola"
        
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("pipe_error_3")#line 27
class TestTest(TestReturnError):
    def _input(self):
        return "| | |"
        
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("pipe_error_4")#line 28
class TestTest(TestReturnError):
    def _input(self):
        return "||"
        
    def _error(self):
        return self.error_unexpected("||")
    
@AddTest("pipe_error_5")#line 29
class TestTest(TestReturnError):
    def _input(self):
        return "|||||"
        
    def _error(self):
        return self.error_unexpected("||")
    
@AddTest("pipe_error_6")#line 30
class TestTest(TestReturnError):
    def _input(self):
        return "|||||||||||||"
    
    def _error(self):
        return self.error_unexpected("||")
    
@AddTest("pipe_error_7")#line 31
class TestTest(TestReturnError):
    def _input(self):
        return ">>|><"
    
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("and_1")#line 32
class TestTest(TestReturnError):
    def _input(self):
        return "&&"
        
    def _error(self):
        return self.error_unexpected("&&")
    
@AddTest("and_2")#line 33
class TestTest(TestReturnError):
    def _input(self):
        return "&&&&&"
    
    def _error(self):
        return self.error_unexpected("&&")
    
@AddTest("and_3")#line 34
class TestTest(TestReturnError):
    def _input(self):
        return "&&&&&&&&&&&&&&"
    
    def _error(self):
        return self.error_unexpected("&&")

@AddTest("cmd_0")#line 41
class TestTest(TestReturnError):
    def _input(self):
        return '""'
    def _error(self):
        return self.error_cmd_not_found('')

@AddTest("cmd_1")#line 42
class TestTest(TestReturnError):
    def _input(self):
        return '"hola"'
    def _error(self):
        return self.error_cmd_not_found('hola')

@AddTest("cmd_2")#line 43
class TestTest(TestReturnError):
    def _input(self):
        return "'hola'"
    def _error(self):
        return self.error_cmd_not_found("hola")

@AddTest("cmd_3")#line 53
class TestTest(TestReturnError):
    def _input(self):
        return "hola"
    def _error(self):
        return self.error_cmd_not_found("hola")

@AddTest("cmd_4")#line 54
class TestTest(TestReturnError):
    def _input(self):
        return "hola que tal"
    def _error(self):
        return self.error_cmd_not_found("hola")

@AddTest("cmd_5")#line 55
class TestTest(TestReturnError):
    def _input(self):
        return "Makefile"
    def _error(self):
        return self.error_cmd_not_found("Makefile")

@AddTest("echo_1")#line 56
class TestTest(TestReturn):
    def _input(self):
        return "echo"
    
    def _response(self):
        return "\n"
    
@AddTest("echo_2")#line 57
class TestTest(TestReturn):
    def _input(self):
        return "echo -n"
    
    def _response(self):
        return ""
    
@AddTest("echo_3")#line 58
class TestTest(TestReturn):
    def _input(self):
        return "echo Hola"
    
    def _response(self):
        return "Hola\n"
    
@AddTest("echo_4")#line 59
class TestTest(TestReturnError):
    def _input(self):
        return "echoHola"
    
    def _error(self):
        return self.error_cmd_not_found("echoHola")
    
@AddTest("echo_5")#line 60
class TestTest(TestReturnError):
    def _input(self):
        return "echo-nHola"
    
    def _error(self):
        return self.error_cmd_not_found("echo-nHola")
    
@AddTest("echo_6")#line 61
class TestTest(TestReturn):
    def _input(self):
        return 'echo -n Hola'
    
    def _response(self):
        return "Hola"
    
@AddTest("echo_7")#line 62
class TestTest(TestReturn):
    def _input(self):
        return 'echo "-n" Hola'
    
    def _response(self):
        return "Hola"
    
@AddTest("echo_8")#line 63
class TestTest(TestReturn):
    def _input(self):
        return "echo -nHola"
    
    def _response(self):
        return "-nHola\n"
    
@AddTest("echo_9")#line 64
class TestTest(TestReturn):
    def _input(self):
        return "echo Hola -n"
    
    def _response(self):
        return "Hola -n\n"
    
@AddTest("echo_10")#line 65
class TestTest(TestReturn):
    def _input(self):
        return "echo Hola Que Tal"
    
    def _response(self):
        return "Hola Que Tal\n"
    
@AddTest("echo_11")#line 66
class TestTest(TestReturn):
    def _input(self):
        return "echo         Hola"
    
    def _response(self):
        return "Hola\n"
    
@AddTest("echo_12")#line 67
class TestTest(TestReturn):
    def _input(self):
        return "echo     Hola     Que     Tal"
    
    def _response(self):
        return "Hola Que Tal\n"
    
@AddTest("echo_13")#line 68
class TestTest(TestReturn):
    def _input(self):
        return "echo      n hola"
    
    def _response(self):
        return "n hola\n"
    
@AddTest("echo_14")#line 69
class TestTest(TestReturn):
    def _input(self):
        return "echo '      ' | cat -e"
    
    def _response(self):
        return "      $\n"
    
@AddTest("echo_15")#line 70
class TestTest(TestReturn):
    def _input(self):
        return "echo         | cat -e"
    
    def _response(self):
        return "$\n"
    
@AddTest("echo_16")#line 71
class TestTest(TestReturn):
    def _input(self):
        return '""''echo hola""'''' que""'' tal""'''
    
    def _response(self):
        return "hola que tal\n"
    
@AddTest("echo_17")#line 72
class TestTest(TestReturn):
    def _input(self):
        return "echo -n -n"
    
    def _response(self):
        return ""
    
@AddTest("echo_18")#line 73
class TestTest(TestReturn):
    def _input(self):
        return "echo -n -n Hola Que"
    
    def _response(self):
        return "Hola Que"
    
@AddTest("echo_19")#line 74
class TestTest(TestReturn):
    def _input(self):
        return "echo -p"
    
    def _response(self):
        return "-p\n"
    
@AddTest("echo_20")#line 75
class TestTest(TestReturn):
    def _input(self):
        return "echo -nnnnnn"
    
    def _response(self):
        return ""
    
@AddTest("echo_21")#line 76
class TestTest(TestReturn):
    def _input(self):
        return "echo -n -nnn -nnnn"
    
    def _response(self):
        return ""
    
@AddTest("echo_22")#line 77
class TestTest(TestReturn):
    def _input(self):
        return "echo -n-nnn -nnnn"
    
    def _response(self):
        return "-n-nnn -nnnn\n"
    
@AddTest("echo_23")#line 78
class TestTest(TestReturn):
    def _input(self):
        return "echo -n -nnn hola -nnnn"
    
    def _response(self):
        return "hola -nnnn"
    
@AddTest("echo_24")#line 79
class TestTest(TestReturn):
    def _input(self):
        return "echo -n -nnn-nnnn"
    
    def _response(self):
        return "-nnn-nnnn"
    
@AddTest("echo_25")#line 80
class TestTest(TestReturn):
    def _input(self):
        return "echo ------n"
    
    def _response(self):
        return "------n\n"
    
@AddTest("echo_26")#line 81
class TestTest(TestReturn):
    def _input(self):
        return "echo -nnn ------n"
    
    def _response(self):
        return "------n"
    
@AddTest("echo_27")#line 82
class TestTest(TestReturn):
    def _input(self):
        return "echo -nnn -----nn---nnnn"
    
    def _response(self):
        return "-----nn---nnnn"
    
@AddTest("echo_28")#line 83
class TestTest(TestReturn):
    def _input(self):
        return "echo -nnn -------nnnn"
    
    def _response(self):
        return "-------nnnn"
    
@AddTest("echo_29")#line 84
class TestTest(TestReturn):
    def _input(self):
        return "echo $"
    
    def _response(self):
        return "$\n"

@AddTest("echo_30")#line 85
class TestTest(TestReturn):
    def _input(self):
        return "echo $?"
    
    def _response(self):
        return "0\n"
    
@AddTest("echo_31")#line 86
class TestTest(TestReturn):
    def _input(self):
        return "echo $?$"
    
    def _response(self):
        return "0$\n"
    
@AddTest("echo_32")#line 87
class TestTest(TestReturn):
    def _input(self):
        return "echo $? | echo $? | echo $?"
    
    def _response(self):
        return "0\n"
    
@AddTest("echo_33")#line 88
class TestTest(TestReturn):
    def _input(self):
        return "echo $:$= | cat -e"
    
    def _response(self):
        return "$:$=$\n"
    
@AddTest("echo_34")#line 89
class TestTest(TestReturn):
    def _input(self):
        return "echo ' $ ' | cat -e"
    
    def _response(self):
        return " $ $\n"
    
@AddTest("echo_35")#line 90
class TestTest(TestReturn):
    def _input(self):
        return "echo ' $ ' | cat -e"
    
    def _response(self):
        return " $ $\n"
    
@AddTest("echo_36")#line 91
class TestTest(TestDiff):
    def _input(self):
        return "echo $HOME"
    
@AddTest("echo_37")#line 92
class TestTest(TestReturn):
    def _input(self):
        return "echo \$HOME"
    
    def _response(self):
        return "$HOME\n"
    
@AddTest("echo_38")#line 93
class TestTest(TestDiff):
    def _input(self):
        return "echo my shit terminal is [$TERM]"
    
@AddTest("echo_39")#line 94
class TestTest(TestReturn):
    def _input(self):
        return "echo my shit terminal is [$TERM4"
    
    def _response(self):
        return "my shit terminal is [\n"
    
@AddTest("echo_40")#line 95
class TestTest(TestReturn):
    def _input(self):
        return "echo my shit terminal is [$TERM4]"
    
    def _response(self):
        return "my shit terminal is []\n"

# Hell no
'''@AddTest("echo_41")#line 96
class TestTest(TestReturn):
    def _input(self):
        return "echo $UID"
    
    def _response(self):
        return "1000\n")'''
    
@AddTest("echo_42")#line 97
class TestTest(TestReturn):
    def _input(self):
        return "echo $HOME9"
    
    def _response(self):
        return "\n"
    
@AddTest("echo_43")#line 98
class TestTest(TestReturn):
    def _input(self):
        return "echo $9HOME"
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_44")#line 99
class TestTest(TestDiff):
    def _input(self):
        return "echo $HOME%"

# Still no
'''@AddTest("echo_45")#line 100
class TestTest(TestReturn):
    def _input(self):
        return "echo"
    
    def _response(self):
        return "\n")'''
    
@AddTest("echo_46")#line 101
class TestTest(TestDiff):
    def _input(self):
        return "echo Le path de mon HOME est $HOME"
    
@AddTest("echo_47")#line 102
class TestTest(TestDiff):
    def _input(self):
        return "echo $USER$var\$USER$USER\$USERtest$USER"
    
@AddTest("echo_48")#line 103
class TestTest(TestReturn):
    def _input(self):
        return "echo $hola*"
    
    def _response(self):
        return "*\n"
    
@AddTest("echo_49")#line 104
class TestTest(TestReturn):
    def _input(self):
        return "echo -nnnn $hola"
    
    def _response(self):
        return ""
    
@AddTest("echo_50")#line 105
class TestTest(TestReturnError):
    def _input(self):
        return "echo > <"
    
    def _error(self):
        return self.error_unexpected("<")
    
@AddTest("echo_51")#line 106
class TestTest(TestReturnError):
    def _input(self):
        return "echo | |"
    
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("echo_52")#line 107
class TestTest(TestReturnError):
    def _input(self):
        return "EechoE"
    
    def _error(self):
        return self.error_cmd_not_found("EechoE")
    
@AddTest("echo_53")#line 108
class TestTest(TestReturnError):
    def _input(self):
        return ".echo."
    
    def _error(self):
        return self.error_cmd_not_found(".echo.")
    
@AddTest("echo_54")#line 109
class TestTest(TestReturnError):
    def _input(self):
        return ">echo>"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("echo_55")#line 110
class TestTest(TestReturnError):
    def _input(self):
        return "<echo<"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("echo_56")#line 111
class TestTest(TestReturnError):
    def _input(self):
        return ">>echo>>"
    
    def _error(self):
        return self.error_unexpected("newline")
    
@AddTest("echo_57")#line 112
class TestTest(TestReturnError):
    def _input(self):
        return "|echo|"
    
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("echo_58")#line 113
class TestTest(TestReturnError):
    def _input(self):
        return "|echo -n hola"
    
    def _error(self):
        return self.error_unexpected("|")
    
@AddTest("echo_59")#line 124
class TestTest(TestReturn):
    def _input(self):
        return 'echo $""'
    
    def _response(self):
        return "\n"
    
@AddTest("echo_60")#line 125
class TestTest(TestReturn):
    def _input(self):
        return 'echo "$"""'
    
    def _response(self):
        return "$\n"
    
@AddTest("echo_61")#line 126
class TestTest(TestReturn):
    def _input(self):
        return "echo '$'''"
    
    def _response(self):
        return "$\n"
    
@AddTest("echo_62")#line 127
class TestTest(TestReturn):
    def _input(self):
        return 'echo $"HOME"'
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_63")#line 128
class TestTest(TestReturn):
    def _input(self):
        return "echo $''HOME"
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_64")#line 129
class TestTest(TestReturn):
    def _input(self):
        return 'echo $""HOME'
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_65")#line 130
class TestTest(TestReturn):
    def _input(self):
        return 'echo "$HO"ME'
    
    def _response(self):
        return "ME\n"
    
@AddTest("echo_66")#line 131
class TestTest(TestReturn):
    def _input(self):
        return "echo '$HO'ME"
    
    def _response(self):
        return "$HOME\n"
    
@AddTest("echo_67")#line 132
class TestTest(TestReturn):
    def _input(self):
        return 'echo "$HO""ME"'
    
    def _response(self):
        return "ME\n"
    
@AddTest("echo_68")#line 133
class TestTest(TestReturn):
    def _input(self):
        return "echo '$HO''ME'"
    
    def _response(self):
        return "$HOME\n"
    
@AddTest("echo_69")#line 134
class TestTest(TestReturn):
    def _input(self):
        return 'echo "\'$HO\'\'ME\'"'
    
    def _response(self):
        return "'''ME'\n"
    
@AddTest("echo_70")#line 135
class TestTest(TestDiff):
    def _input(self):
        return 'echo ""$HOME'
    
@AddTest("echo_71")#line 136
class TestTest(TestDiff):
    def _input(self):
        return 'echo "" $HOME'
    
@AddTest("echo_72")#line 137
class TestTest(TestDiff):
    def _input(self):
        return "echo ''$HOME"
    
@AddTest("echo_73")#line 138
class TestTest(TestDiff):
    def _input(self):
        return "echo '' $HOME"
    
@AddTest("echo_74")#line 139
class TestTest(TestReturn):
    def _input(self):
        return 'echo $"HO""ME"'
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_75")#line 140
class TestTest(TestReturn):
    def _input(self):
        return "echo $'HO''ME'"
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_76")#line 141
class TestTest(TestReturn):
    def _input(self):
        return "echo $'HOME'"
    
    def _response(self):
        return "HOME\n"
    
@AddTest("echo_77")#line 142
class TestTest(TestReturn):
    def _input(self):
        return 'echo "$"HOME'
    
    def _response(self):
        return "$HOME\n"
    
@AddTest("echo_78")#line 143
class TestTest(TestReturn):
    def _input(self):
        return "echo $=HOME"
    
    def _response(self):
        return "$=HOME\n"
    
@AddTest("echo_79")#line 144
class TestTest(TestReturn):
    def _input(self):
        return 'echo $"HOLA"'
    
    def _response(self):
        return "HOLA\n"
    
@AddTest("echo_80")#line 145
class TestTest(TestReturn):
    def _input(self):
        return "echo $'HOLA'"
    
    def _response(self):
        return "HOLA\n"
    
@AddTest("echo_81")#line 146
class TestTest(TestReturn):
    def _input(self):
        return "echo $DONTEXIST Hola"
    
    def _response(self):
        return "Hola\n"
    
@AddTest("echo_82")#line 147
class TestTest(TestReturn):
    def _input(self):
        return 'echo "hola"'
    
    def _response(self):
        return "hola\n"
    
@AddTest("echo_83")#line 148
class TestTest(TestReturn):
    def _input(self):
        return "echo 'hola'"
    
    def _response(self):
        return "hola\n"
    
@AddTest("echo_84")#line 149
class TestTest(TestReturn):
    def _input(self):
        return "echo ''hola''"
    
    def _response(self):
        return "hola\n"
    
@AddTest("echo_85")#line 150
class TestTest(TestReturn):
    def _input(self):
        return "echo ''h'o'la''"
    
    def _response(self):
        return "hola\n"
    
@AddTest("echo_86")#line 151
class TestTest(TestReturn):
    def _input(self):
        return "echo \"''h'o'la''\""
    
    def _response(self):
        return "''h'o'la''\n"
    
@AddTest("echo_87")#line 152
class TestTest(TestReturn):
    def _input(self):
        return "echo \"'\"h'o'la\"'\""
    
    def _response(self):
        return "'hola'\n"
    
@AddTest("echo_88")#line 153
class TestTest(TestReturnError):
    def _input(self):
        return "echo\"'hola'\""
    
    def _error(self):
        return self.error_cmd_not_found("echo'hola'")
    
@AddTest("echo_89")#line 154
class TestTest(TestReturn):
    def _input(self):
        return "echo \"'hola'\""
    
    def _response(self):
        return "'hola'\n"
    
@AddTest("echo_90")#line 155
class TestTest(TestReturn):
    def _input(self):
        return "echo '\"hola\"'"
    
    def _response(self):
        return "\"hola\"\n"
    
@AddTest("echo_91")#line 156
class TestTest(TestReturn):
    def _input(self):
        return "echo '''ho\"''''l\"a'''"
    
    def _response(self):
        return "ho\"l\"a\n"
    
@AddTest("echo_92")#line 157
class TestTest(TestReturn):
    def _input(self):
        return 'echo hola """"""""""""'
    
    def _response(self):
        return "hola \n"
    
@AddTest("echo_93")#line 158
class TestTest(TestReturn):
    def _input(self):
        return "echo hola\"''''''''''\""
    
    def _response(self):
        return "hola''''''''''\n"
    
@AddTest("echo_94")#line 159
class TestTest(TestReturn):
    def _input(self):
        return "echo hola''''''''''''"
    
    def _response(self):
        return "hola\n"
    
@AddTest("echo_95")#line 160
class TestTest(TestReturn):
    def _input(self):
        return 'echo hola\'""""""""""\''
    
    def _response(self):
        return 'hola""""""""""\n'
    
@AddTest("echo_96")#line 161
class TestTest(TestReturnError):
    def _input(self):
        return 'e"cho hola"'
    
    def _error(self):
        return self.error_cmd_not_found("echo hola")
    
@AddTest("echo_97")#line 162
class TestTest(TestReturnError):
    def _input(self):
        return "e'cho hola'"
    
    def _error(self):
        return self.error_cmd_not_found("echo hola")
    
@AddTest("echo_98")#line 163
class TestTest(TestReturn):
    def _input(self):
        return 'echo "hola    " | cat -e'
    
    def _response(self):
        return "hola    $\n"
    
@AddTest("echo_99")#line 164
class TestTest(TestReturn):
    def _input(self):
        return 'echo ""hola'
    
    def _response(self):
        return "hola\n"
    
@AddTest("echo_100")#line 165
class TestTest(TestReturn):
    def _input(self):
        return 'echo "" hola'
    
    def _response(self):
        return " hola\n"
    
@AddTest("echo_101")#line 166
class TestTest(TestReturn):
    def _input(self):
        return 'echo ""        hola'
    
    def _response(self):
        return " hola\n"
    
@AddTest("echo_102")#line 167
class TestTest(TestReturn):
    def _input(self):
        return "echo hola\"\"bonjour"
    
    def _response(self):
        return "holabonjour\n"
    
@AddTest("echo_103")#line 168
class TestTest(TestReturn):
    def _input(self):
        return "\"e\"'c'ho 'b'\"o\"nj\"o\"'u'r"
    
    def _response(self):
        return "bonjour\n"
    
@AddTest("echo_104")#line 169
class TestTest(TestReturnError):
    def _input(self):
        return "\"\"e\"'c'ho 'b'\"o\"nj\"o\"'u'r\""
    
    def _error(self):
        return self.error_cmd_not_found("e'c'ho 'b'onjo'u'r")
    
@AddTest("echo_105")#line 170
class TestTest(TestReturn):
    def _input(self):
        return 'echo "$DONTEXIT"Makefile'
    
    def _response(self):
        return "Makefile\n"
    
@AddTest("echo_106")#line 171
class TestTest(TestReturn):
    def _input(self):
        return 'echo "$DONTEXIST""Makefile"'
    
    def _response(self):
        return "Makefile\n"

@AddTest("echo_107")#line 172
class TestTest(TestReturn):
    def _input(self):
        return "echo '$DONTEXIST' 'Makefile'"
    
    def _response(self):
        return "$DONTEXIST Makefile\n"

@AddTest("var_1")#line 173
class TestTest(TestReturnError):
    def _input(self):
        return "$?"
    
    def _error(self):
        return self.error_cmd_not_found("0")

@AddTest("var_2")#line 174
class TestTest(TestReturnError):
    def _input(self):
        return "$?$?"
    
    def _error(self):
        return self.error_cmd_not_found("00")

@AddTest("var_3")#line 175
class TestTest(TestDiff):
    def _input(self):
        return "?$HOME"

@AddTest("var_4")#line 176
class TestTest(TestReturnError):
    def _input(self):
        return "$"
    
    def _error(self):
        return self.error_cmd_not_found("$")

@AddTest("var_5")#line 177
class TestTest(TestDiff):
    def _input(self):
        return "$HOME"

@AddTest("var_6")#line 178
class TestTest(TestReturnNothing):
    def _input(self):
        return "$HOMEdskjhfkdshfsd"


@AddTest("var_7")#line 179
class TestTest(TestReturnError):
    def _input(self):
        return '"$HOMEdskjhfkdshfsd"'
    
    def _error(self):
        return self.error_cmd_not_found("")

@AddTest("var_8")#line 180
class TestTest(TestReturnError):
    def _input(self):
        return "'$HOMEdskjhfkdshfsd'"
    
    def _error(self):
        return self.error_cmd_not_found("$HOMEdskjhfkdshfsd")

@AddTest("var_9")#line 181
class TestTest(TestReturnNothing):
    def _input(self):
        return "$DONTEXIST"

@AddTest("var_10")#line 182
class TestTest(TestDiff):
    def _input(self):
        return "$LESS$VAR"

@AddTest("ctrl_1")#line 183
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.SendCtrlC()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_2")#line 184
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        _input = "hola"
        self.minishell.Write(_input)
        self.minishell.SendCtrlC()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res
'''
@AddTest("ctrl_3")#line 185
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Send("cat")
        self.minishell.Send("")
        self.minishell.Send("")
        self.minishell.SendCtrlC()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_4")#line 186
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Send("cat | rev")
        self.minishell.Send("\n")
        self.minishell.Send("\n")
        self.minishell.SendCtrlC()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_5")#line 187
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.SendCtrlD()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_6")#line 188
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Write("hola")
        self.minishell.SendCtrlD()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_7")#line 189
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.SendCtrlBackslash()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_8")#line 190
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Write("hola")
        self.minishell.SendCtrlBackslash()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_9")#line 191
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Send("cat")
        self.minishell.Send("\n")
        self.minishell.Send("\n")
        self.minishell.SendCtrlBackslash()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_10")#line 192
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Send("sleep 3 | sleep 3 | sleep 3")
        self.minishell.SendCtrlC()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_11")#line 193
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Send("sleep 3 | sleep 3 | sleep 3")
        self.minishell.SendCtrlD()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("ctrl_12")#line 194
class TestTest(BaseTest):
    def Init(self):
        self.minishell = MinishellDiff()
        return 
    
    def Run(self):
        self.minishell.Send("sleep 3 | sleep 3 | sleep 3")
        self.minishell.SendCtrlBackslash()
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

'''

@AddTest("env_1")#line 195
class TestTest(TestDiff):
    def Run(self):
        self.minishell.Send("env")
        res = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",res)
        return res

@AddTest("env_2")#line 202
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send("export HOLA=bonjour")
        return "env | grep HOLA"

@AddTest("env_3")#line 203
class TestTest(BaseTest):
    def Run(self):
        self.minishell.Send("export        HOLA=bonjour")
        self.minishell.Send("env")
        output = self.minishell.Read().split("\n")[-2]
        correct_output= 'HOLA=bonjour'
        output = colorWhiteSpaces(output,ColorsBg.CYAN, chars=["\t"," "])
        correct_output = colorWhiteSpaces(correct_output,ColorsBg.CYAN, chars=["\t"," "])
        DebugPrint("your output:\n"+output+"\ncorrect output:\n"+correct_output)
        res = output == correct_output
        return res

@AddTest("env_7")#line 207
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("unset _")
        return "export $DONTEXIST"

@AddTest("env_8")#line 208
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'export | grep "HOME"'

@AddTest("env_9")#line 209
class TestTest(TestReturnError):
    def _input(self):
        return 'export ""'

    def _error(self):
        return self.error_invalid_identifier("")

@AddTest("env_10")#line 210
class TestTest(TestReturnError):
    def _input(self):
        return 'export ='

    def _error(self):
        return self.error_invalid_identifier("=")

@AddTest("env_11")#line 211
class TestTest(TestReturnError):
    def _input(self):
        return 'export %'

    def _error(self):
        return self.error_invalid_identifier("%")

@AddTest("env_12")#line 212
class TestTest(TestReturnError):
    def _input(self):
        return 'export $?'

    def _error(self):
        return self.error_invalid_identifier("0")

@AddTest("env_13")#line 213
class TestTest(TestReturnError):
    def _input(self):
        return 'export ?=2'

    def _error(self):
        return self.error_invalid_identifier("?=2")

@AddTest("env_14")#line 214
class TestTest(TestReturnError):
    def _input(self):
        return 'export 9HOLA='

    def _error(self):
        return self.error_invalid_identifier("9HOLA=")

@AddTest("env_15")#line 215
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send("export HOLA9=bonjour")
        return 'env | grep HOLA9'

@AddTest("env_16")#line 216
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export _HOLA=bonjour')
        return "env | grep _HOLA"

@AddTest("env_17")#line 217
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export ___HOLA=bonjour')
        return "env | grep ___HOLA"

@AddTest("env_18")#line 218
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export _HO_LA_=bonjour')
        return "env | grep _HO_LA_"

@AddTest("env_19")#line 219
class TestTest(TestReturnError):  
    def _input(self):
        return 'export HOL@=bonjour'

    def _error(self):
        return self.error_invalid_identifier("HOL@=bonjour")

@AddTest("env_20")#line 220
class TestTest(TestDiff):
    def _input(self):
        return 'export HOL\~A=bonjour'

@AddTest("env_21")#line 221
class TestTest(TestReturnError):
    def _input(self):
        return 'export -HOLA=bonjour'
    
    def _error(self):
        return self.error_learn_to_use("export", "-H")

@AddTest("env_22")#line 222
class TestTest(TestReturnError):
    def _input(self):
        return 'export "--HOLA=bonjour"'

    def _error(self):
        return self.error_learn_to_use("export", "--")

@AddTest("env_23")#line 223
class TestTest(TestDiff):
    def _input(self):
        return 'export HOLA-=bonjour'

@AddTest("env_24")#line 224
class TestTest(TestDiff):
    def _input(self):
        return 'export HO-LA=bonjour'

@AddTest("env_25")#line 225
class TestTest(TestDiff):
    def _input(self):
        return 'export HOL.A=bonjour'

@AddTest("env_26")#line 226
class TestTest(TestDiff):
    def _input(self):
        return 'export HOLA\\\$A=bonjour'

@AddTest("env_27")#line 227
class TestTest(TestDiff):
    def _input(self):
        return 'export HO\\\\LA=bonjour'

@AddTest("env_28")#line 228
class TestTest(TestDiff):
    def _input(self):
        return 'export HOL}A=bonjour'

@AddTest("env_29")#line 229
class TestTest(TestDiff):
    def _input(self):
        return 'export HOL{A=bonjour'

@AddTest("env_30")#line 230
class TestTest(TestDiff):
    def _input(self):
        return 'export HO*LA=bonjour'

@AddTest("env_31")#line 231
class TestTest(TestDiff):
    def _input(self):
        return 'export HO#LA=bonjour'

@AddTest("env_32")#line 232
class TestTest(TestDiff):
    def _input(self):
        return 'export HO@LA=bonjour'

@AddTest("env_33")#line 233
class TestTest(TestDiff):
    def _input(self):
        return 'export HO!LA=bonjour'

@AddTest("env_34")#line 234
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HO$?LA=bonjour')
        return "env | grep HO$?LA"

@AddTest("env_35")#line 235
class TestTest(TestDiff):
    def _input(self):
        return 'export +HOLA=bonjour'

@AddTest("env_36")#line 236
class TestTest(TestDiff):
    def _input(self):
        return 'export HOL+A=bonjour'

@AddTest("env_37")#line 240
class TestTest(TestDiff):
    def _input(self):
        return 'export HOLA =bonjour'

@AddTest("env_38")#line 241
class TestTest(TestDiff):
    def _input(self):
        return 'export HOLA = bonjour'

@AddTest("env_39")#line 242
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bon jour')
        return "env | grep HOLA"

@AddTest("env_40")#line 243
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA= bonjour')
        return "env | grep HOLA"

@AddTest("env_41")#line 244
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bonsoir')
        self.minishell.Send('export HOLA=bonretour')
        self.minishell.Send('export HOLA=bonjour')
        return "env | grep HOLA"

@AddTest("env_42")#line 245
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=$HOME')
        return "env | grep HOLA"

@AddTest("env_43")#line 246
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bonjour$HOME')
        return "env | grep HOLA"

@AddTest("env_44")#line 247
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=$HOMEbonjour')
        return "env | grep HOLA"

@AddTest("env_45")#line 248
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bon$jour')
        return "env | grep HOLA"

@AddTest("env_46")#line 254
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bon@jour')
        return "env | grep HOLA"

@AddTest("env_47")#line 257
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bon"jour"')
        return "env | grep HOLA"

@AddTest("env_48")#line 258
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA$USER=bonjour')
        return "env | grep HOLA$USER"

@AddTest("echo_export_1")#line 259
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=bonjour=casse-toi')
        return "echo $HOLA"

@AddTest("echo_export_2")#line 260
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export "HOLA=bonjour"=casse-toi')
        return "echo $HOLA"

@AddTest("echo_export_3")#line 261
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send('export BYE=casse-toi')
        return "echo $HOLA et $BYE"

@AddTest("echo_export_4")#line 262
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=bonjour BYE=casse-toi')
        return "echo $HOLA et $BYE"

@AddTest("echo_export_5")#line 263
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export A=a B=b C=c')
        return "echo $A $B $C"

@AddTest("echo_export_6")#line 264
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send('export $HOLA=bonjour')
        self.minishell.Send('unset HOLA')
        return "env | grep bonjour"

@AddTest("echo_export_7")#line 265
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="bonjour    "')
        return "echo $HOLA | cat -e"

@AddTest("echo_export_8")#line 266
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="    -n bonjour   "')
        return "echo $HOLA"

@AddTest("echo_export_9")#line 267
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="bonjour    "/')
        return "echo $HOLA"

@AddTest("echo_export_10")#line 268
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("export HOLA=")
        return "echo $HOLA"

@AddTest("echo_export_11")#line 269
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=at')
        return "/usr/bin/c$HOLA Makefile"

@AddTest("echo_export_12")#line 270
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export "" HOLA=bonjour')
        return "env | grep HOLA"

@AddTest("echo_export_13")#line 271
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('echo NAME=minishell > Makefile')
        self.minishell.Send('export HOLA="cat Makefile | grep NAME"')
        return "/usr/bin/$HOLA"

@AddTest("echo_export_14")#line 272
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=hey')
        return "echo $HOLA$HOLA$HOLA=hey$HOLA"

@AddTest("echo_export_15")#line 273
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="  bonjour hey  "')
        return "echo $HOLA | cat -e"

@AddTest("echo_export_16")#line 274
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="  bonjour  hey  "')
        return 'echo """$HOLA""" | cat -e'

@AddTest("echo_export_17")#line 275
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="  bonjour  hey  "')
        return 'echo wesh"$HOLA".'

@AddTest("echo_export_18")#line 276
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="  bonjour  hey   "')
        return "echo wesh""$HOLA."

@AddTest("echo_export_19")#line 277
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="  bonjour  hey   "')
        return 'echo wesh$""HOLA.'

@AddTest("echo_export_20")#line 278
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="  bonjour  hey   "')
        return 'echo wesh$"HOLA HOLA".'

@AddTest("echo_export_21")#line 279
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send('export HOLA=" hola et $HOLA"')
        return "echo $HOLA"

@AddTest("echo_export_22")#line 280
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send("export HOLA=' hola et $HOLA'")
        return "echo $HOLA"

@AddTest("echo_export_23")#line 281
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send('export HOLA=" hola et $HOLA"$HOLA')
        return "echo $HOLA"

@AddTest("echo_export_24")#line 282
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="ls       -l    -a"')
        return "echo $HOLA"

@AddTest("echo_export_25")#line 283
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="s -la"')
        return "l$HOLA"

@AddTest("echo_export_26")#line 284
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="s -la"')
        return 'l"$HOLA"'

@AddTest("echo_export_27")#line 285
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="s -la"')
        return "l'$HOLA'"

@AddTest("echo_export_28")#line 286
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="l"')
        return "$HOLAs"

@AddTest("echo_export_29")#line 287
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA="l"')
        return '"$HOLA"s'

@AddTest("echo_export_30")#line 288
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOL=A=bonjour')
        return "env | grep HOL"

@AddTest("echo_export_31")#line 289
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=l')
        return "'$HOLA's"

@AddTest("echo_export_32")#line 290
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOL=A=""')
        return "env | grep HOL"

@AddTest("echo_export_33")#line 291
class TestTest(TestDiff):
    def _input(self):
        return 'export TE+S=T'

@AddTest("echo_export_34")#line 292
class TestTest(TestDiff):
    def _input(self):
        return 'export ""=""'

@AddTest("echo_export_35")#line 293
class TestTest(TestDiff):
    def _input(self):
        return "export ''=''"

@AddTest("echo_export_36")#line 294
class TestTest(TestDiff):
    def _input(self):
        return 'export "="="="'

@AddTest("echo_export_37")#line 295
class TestTest(TestDiff):
    def _input(self):
        return "export '='='='"

@AddTest("echo_export_38")#line 296
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=p')
        self.minishell.Send('export BYE=w')
        return '$HOLA"BYE"d'

@AddTest("echo_export_39")#line 297
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=p')
        self.minishell.Send('export BYE=w')
        return '"$HOLA"\'BYE\'d'

@AddTest("echo_export_40")#line 298
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=p')
        self.minishell.Send('export BYE=w')
        return '"$HOLA""$BYE"d'

@AddTest("echo_export_41")#line 299
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=p')
        self.minishell.Send('export BYE=w')
        return '$"HOLA"$"BYE"d'

@AddTest("echo_export_42")#line 300
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=p')
        self.minishell.Send('export BYE=w')
        return "$'HOLA'$'BYE'd"

@AddTest("echo_export_43")#line 301
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export HOLA=-n')
        return '"echo $HOLA" hey'

@AddTest("echo_export_44")#line 302
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('export A=1 B=2 C=3 D=4 E=5 F=6 G=7 H=8')
        return 'echo "$A\'$B"\'$C"$D\'$E\'"$F\'"\'$G\'$H"'

@AddTest("unset_1")#line 303
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send('env | grep HOLA')
        self.minishell.Send("unset _")
        self.minishell.Send("unset HOLA")
        return 'env'

@AddTest("unset_2")#line 304
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('export HOLA=bonjour')
        self.minishell.Send('env | grep HOLA')
        self.minishell.Send("unset _")
        self.minishell.Send("unset HOLA")
        self.minishell.Send("unset HOLA")
        return 'env'

@AddTest("unset_3")#line 305
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('unset PATH')
        return 'echo $PATH'

@AddTest("unset_4")#line 306
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('unset PATH')
        return 'ls'

@AddTest("unset_5")#line 307
class TestTest(TestDiff):
    def _input(self):
        return 'unset ""'

@AddTest("unset_6")#line 308
class TestTest(TestDiff):
    def _input(self):
        return 'unset INEXISTANT'

@AddTest("unset_7")#line 309
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('unset PWD')
        self.minishell.Send('env | grep PWD')
        return 'pwd'

@AddTest("unset_8")#line 310
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('pwd')
        self.minishell.Send('unset PWD')
        self.minishell.Send('env | grep PWD')
        self.minishell.Send('cd $PWD')
        return 'pwd'

@AddTest("unset_9")#line 311
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send('unset OLDPWD')
        return 'env | grep OLDPWD'

@AddTest("unset_10")#line 312
class TestTest(TestDiff):
    def _input(self):
        return 'unset 9HOLA'

@AddTest("unset_11")#line 313
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOLA9'

@AddTest("unset_12")#line 314
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOL?A'

@AddTest("unset_13")#line 315
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOLA HOL?A'

@AddTest("unset_14")#line 316
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOL?A HOLA'

@AddTest("unset_15")#line 317
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOL?A HOL.A'

@AddTest("unset_16")#line 318
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOLA='

@AddTest("unset_17")#line 341
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("unset PATH")
        return 'echo $PATH'

@AddTest("unset_18")#line 342
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("unset PATH")
        return 'cat Makefile'

@AddTest("test_random")#line 353
class TestTest(TestDiff):
    def _input(self):
        return 'export hola | unset hola | echo $?'

@AddTest("test_bin_1")#line 354
class TestTest(TestDiff):
    def _input(self):
        return '/bin/echo'

@AddTest("test_bin_2")#line 355
class TestTest(TestDiff):
    def _input(self):
        return '/bin/echo Hola Que Tal'

@AddTest("test_bin_3")#line 356
class TestTest(TestDiff):
    def _input(self):
        return '/bin/env'

@AddTest("test_bin_4")#line 357
class TestTest(TestDiff):
    def _input(self):
        return '/bin/cd Desktop'

@AddTest("pwd_1")#line 360
class TestTest(TestDiff):
    def _input(self):
        return 'pwd'

@AddTest("pwd_2")#line 361
class TestTest(TestDiff):
    def _input(self):
        return 'pwd hola'

@AddTest("pwd_3")#line 362
class TestTest(TestDiff):
    def _input(self):
        return 'pwd ./hola'

@AddTest("pwd_4")#line 363
class TestTest(TestDiff):
    def _input(self):
        return 'pwd hola que tal'

@AddTest("pwd_5")#line 364
class TestTest(TestDiff):
    def _input(self):
        return 'pwd -p'

@AddTest("pwd_6")#line 365
class TestTest(TestDiff):
    def _input(self):
        return 'pwd --p'

@AddTest("pwd_7")#line 366
class TestTest(TestDiff):
    def _input(self):
        return 'pwd ---p'

@AddTest("pwd_8")#line 366
class TestTest(TestDiff):
    def _input(self):
        return 'pwd pwd pwd'

@AddTest("pwd_9")#line 369
class TestTest(TestDiff):
    def _input(self):
        return 'pwd ls'

@AddTest("pwd_10")#line 370
class TestTest(TestDiff):
    def _input(self):
        return 'pwd ls env'

@AddTest("cd_1")#line 371
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("cd")
        return 'pwd'

@AddTest("cd_2")#line 372
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ./')
        return "pwd"

@AddTest("cd_3")#line 373
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ./././.')
        return 'pwd'

@AddTest("cd_4")#line 374
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ././././')
        return 'pwd'

@AddTest("cd_5")#line 375
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ..')
        return 'pwd'

@AddTest("cd_6")#line 376
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ../')
        return 'pwd'

@AddTest("cd_7")#line 377
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ../..')
        return 'pwd'

@AddTest("cd_8")#line 378
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ../.')
        return 'pwd'

@AddTest("cd_9")#line 379
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd .././././.')
        return 'pwd'

@AddTest("cd_10")#line 380
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd srcs')
        return 'pwd'

@AddTest("cd_11")#line 381
class TestTest(TestDiff):
    def _input(self):
        return 'cd srcs objs'

@AddTest("cd_12")#line 382
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd "srcs"')
        return 'pwd'

@AddTest("cd_13")#line 383
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd "srcs"')
        return 'pwd'

@AddTest("cd_14")#line 384
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd \'/etc\'')
        return 'pwd'

@AddTest("cd_15")#line 385
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd /e\'tc\'')
        return 'pwd'

@AddTest("cd_16")#line 386
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd /e"tc"')
        return 'pwd'

@AddTest("cd_17")#line 387
class TestTest(TestDiff):
    def _input(self):
        return 'cd sr'


@AddTest("cd_18")#line 388
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd Makefile')
        return 'pwd'

@AddTest("cd_19")#line 389
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ../minishell')
        return 'pwd'

@AddTest("cd_20")#line 390
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ../../../../../../..')
        return 'pwd'

@AddTest("cd_21")#line 391
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd .././../.././../bin/ls')
        return 'pwd'

@AddTest("cd_22")#line 392
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd /')
        return 'pwd'

@AddTest("cd_23")#line 393
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd \'/\'')
        return 'pwd'

@AddTest("cd_24")#line 394
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ///')
        return 'pwd'

@AddTest("cd_25")#line 397
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd ////////')
        return 'pwd'

@AddTest("cd_26")#line 398
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd \'////////\'')
        return 'pwd'

@AddTest("cd_27")#line 399
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd /minishell')
        return 'pwd'

@AddTest("cd_28")#line 400
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd /')
        return 'pwd'

@AddTest("cd_29")#line 401
class TestTest(TestDiff):
    def _input(self):
        return 'cd _'

@AddTest("cd_31")#line 405
class TestTest(TestDiff):
    def _input(self):
        return 'cd ---'

@AddTest("cd_32")#line 406
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd $HOME')
        return 'pwd'

@AddTest("cd_33")#line 407
class TestTest(TestDiff):
    def _input(self):
        return 'cd $HOME $HOME'

@AddTest("cd_34")#line 408
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd $HOME/Documents')
        return 'pwd'

@AddTest("cd_35")#line 409
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send('cd "$PWD/../"')
        return 'pwd'

@AddTest("cd_36")#line 410
class TestTest(TestDiff):
    def _input(self):
        return "cd '$PWD/../'"

@AddTest("cd_37")#line 411
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("unset HOME")
        return 'cd $HOME'

@AddTest("cd_39")#line 413
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("unset HOME")
        self.minishell.Send("export HOME")
        return 'cd'

@AddTest("cd_40")#line 414
class TestTest(TestDiff):
    def _input(self):
        return 'cd minishell Docs crashtest.c'

@AddTest("composite_1")#line 422
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("mkdir truc")
        self.minishell.bash.SendCommand("mkdir truc/bidule")
        self.minishell.bash.SendCommand("cd truc/bidule")
        self.minishell.bash.SendCommand("rm -rf ../../truc")
        self.minishell.bashPosix.SendCommand("mkdir truc")
        self.minishell.bashPosix.SendCommand("mkdir truc/bidule")
        self.minishell.bashPosix.SendCommand("cd truc/bidule")
        self.minishell.bashPosix.SendCommand("rm -rf ../../truc")
        self.minishell.Send("pwd")
        return 'cd ..'

@AddTest("composite_2")#line 423
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("mkdir truc")
        self.minishell.bash.SendCommand("mkdir truc/bidule")
        self.minishell.bash.SendCommand("cd truc/bidule")
        self.minishell.bash.SendCommand("rm -rf ../../truc")
        self.minishell.bashPosix.SendCommand("mkdir truc")
        self.minishell.bashPosix.SendCommand("mkdir truc/bidule")
        self.minishell.bashPosix.SendCommand("cd truc/bidule")
        self.minishell.bashPosix.SendCommand("rm -rf ../../truc")
        return 'pwd'

@AddTest("composite_3")#line 424
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("mkdir truc")
        self.minishell.bash.SendCommand("mkdir truc/bidule")
        self.minishell.bash.SendCommand("cd truc/bidule")
        self.minishell.bash.SendCommand("rm -rf ../../truc")
        self.minishell.bashPosix.SendCommand("mkdir truc")
        self.minishell.bashPosix.SendCommand("mkdir truc/bidule")
        self.minishell.bashPosix.SendCommand("cd truc/bidule")
        self.minishell.bashPosix.SendCommand("rm -rf ../../truc")
        self.minishell.Send("echo $PWD")
        return 'echo $OLDPWD'

@AddTest("composite_4")#line 425
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("mkdir truc")
        self.minishell.bash.SendCommand("mkdir truc/bidule")
        self.minishell.bash.SendCommand("cd truc/bidule")
        self.minishell.bash.SendCommand("rm -rf ../../truc")
        self.minishell.bashPosix.SendCommand("mkdir truc")
        self.minishell.bashPosix.SendCommand("mkdir truc/bidule")
        self.minishell.bashPosix.SendCommand("cd truc/bidule")
        self.minishell.bashPosix.SendCommand("rm -rf ../../truc")
        self.minishell.Send("pwd")
        self.minishell.Send("cd")
        self.minishell.Send("echo $PWD")
        return 'echo $OLDPWD'

@AddTest("composite_5")#line 426
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("mkdir truc")
        self.minishell.bash.SendCommand("cd truc/")
        self.minishell.bash.SendCommand("rm -rf ../truc")
        self.minishell.bashPosix.SendCommand("mkdir truc/")
        self.minishell.bashPosix.SendCommand("cd truc/")
        self.minishell.bashPosix.SendCommand("rm -rf ../truc")
        self.minishell.Send("echo $PWD")
        return 'echo $OLDPWD'

@AddTest("permissions_1")#line 431
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("chmod 000 minishell")
        self.minishell.Send("./minishell")
        return 'chmod 777 minishell'

@AddTest("permissions_2")#line 432
class TestTest(TestDiff):
    def _input(self):
        return '/usr/bin/ls hola'

@AddTest("permissions_3")#line 433
class TestTest(TestDiff):
    def _input(self):
        return '../../../Makefile'

@AddTest("permissions_4")#line 434
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("./minishell")
        return 'exit'

@AddTest("permissions_5")#line 435
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("echo $SHLVL")
        self.minishell.Send("./minishell")
        self.minishell.Send("echo $SHLVL")
        return 'exit'

@AddTest("permissions_6")#line 436
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("touch hola")
        self.minishell.bash.SendCommand("./hola")
        self.minishell.bash.SendCommand("rm hola")
        self.minishell.bashPosix.SendCommand("touch hola")
        self.minishell.bashPosix.SendCommand("./hola")
        self.minishell.bashPosix.SendCommand("rm hola")
        return ''

@AddTest("permissions_7")#line 437
class TestTest(TestDiff):
    def _input(self):
        return 'env | "wc" -l'

@AddTest("permissions_8")#line 438
class TestTest(TestDiff):
    def _input(self):
        return 'env | "wc "-l'

@AddTest("permissions_9")#line 439
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"1 errors from 1 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'expr 1 + 1'

@AddTest("permissions_10")#line 440
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"1 errors from 1 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'expr $? + $?'

@AddTest("exit_1")#line 445
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit'

@AddTest("exit_2")#line 446
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit exit'

@AddTest("exit_3")#line 447
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit hola'

@AddTest("exit_4")#line 448
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit hola que tal'

@AddTest("exit_5")#line 449
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 42'

@AddTest("exit_6")#line 450
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 000042'

@AddTest("exit_7")#line 451
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 666'

@AddTest("exit_8")#line 452
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 666 666'

@AddTest("exit_9")#line 453
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -666 666'

@AddTest("exit_10")#line 454
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit hola 666'

@AddTest("exit_11")#line 445
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 666 666 666 666'

@AddTest("exit_12")#line 446
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 666 hola 666'

@AddTest("exit_13")#line 447
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit hola 666 666'

@AddTest("exit_14")#line 458
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 259'

@AddTest("exit_15")#line 459
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -4'

@AddTest("exit_16")#line 460
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -42'

@AddTest("exit_17")#line 461
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -0000042'

@AddTest("exit_18")#line 462
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -259'

@AddTest("exit_19")#line 463
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -666'

@AddTest("exit_20")#line 464
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit +666'

@AddTest("exit_21")#line 465
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 0'

@AddTest("exit_22")#line 466
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit +0'

@AddTest("exit_23")#line 467
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -0'

@AddTest("exit_24")#line 468
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit +42'

@AddTest("exit_25")#line 469
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -69 -96'

@AddTest("exit_26")#line 470
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit --666'

@AddTest("exit_27")#line 471
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit ++++666'

@AddTest("exit_28")#line 472
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit +++++++++0'

@AddTest("exit_29")#line 473
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -------0'

@AddTest("exit_30")#line 474
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit "666"'

@AddTest("exit_31")#line 475
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return "exit '666'"

@AddTest("exit_32")#line 476
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'-666\''

@AddTest("exit_33")#line 477
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'+666\''

@AddTest("exit_34")#line 478
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'----666\''

@AddTest("exit_35")#line 479
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'++++666\''

@AddTest("exit_36")#line 480
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'6\'66'

@AddTest("exit_37")#line 481
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'2\'66\'32\''

@AddTest("exit_38")#line 482
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit "\'666\''

@AddTest("exit_39")#line 483
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'"666"\''

@AddTest("exit_37")#line 484
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit \'666\'"666"666'

@AddTest("exit_38")#line 485
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit +\'666\'"666"666'

@AddTest("exit_39")#line 486
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -\'666\'"666"666'

@AddTest("exit_40")#line 487
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 9223372036854775807'

@AddTest("exit_41")#line 488
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit 9223372036854775808'

@AddTest("exit_42")#line 489
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -9223372036854775808'

@AddTest("exit_43")#line 490
class TestTest(TestDiffExit):
    def _input(self):
        self.minishell.bashPosix.SendCommand("bash --posix")
        return 'exit -9223372036854775809'

@AddTest("pipe_1")#line 491
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("cat | cat | cat | ls")
        self.minishell.SendCtrlD()
        return ''

@AddTest("pipe_2")#line 492
class TestTest(TestDiff):
    def _input(self):
        return 'ls | exit'

@AddTest("pipe_3")#line 493
class TestTest(TestDiff):
    def _input(self):
        return 'ls | exit 42'

@AddTest("pipe_4")#line 494
class TestTest(TestDiff):
    def _input(self):
        return 'exit | ls'

@AddTest("pipe_5")#line 495
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("echo hola > bonjour")
        self.minishell.Send("exit | cat -e bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        return 'ls'

@AddTest("pipe_6")#line 496
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("echo hola > bonjour")
        self.minishell.Send("cat -e bonjour | exit")
        self.minishell.bash.SendCommand("rm bonjour")
        return 'ls'

@AddTest("pipe_7")#line 497
class TestTest(TestDiff):
    def _input(self):
        return 'echo | echo'

@AddTest("pipe_8")#line 498
class TestTest(TestDiff):
    def _input(self):
        return 'echo hola |echo hola que tal'

@AddTest("pipe_9")#line 499
class TestTest(TestDiff):
    def _input(self):
        return 'pwd | echo hola'


@AddTest("pipe_10")#line 500
class TestTest(TestDiff):
    def _input(self):
        return 'env |echo hola que tal'


@AddTest("pipe_11")#line 501
class TestTest(TestDiff):
    def _input(self):
        return 'echo oui | cat -e'


@AddTest("pipe_12")#line 502
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'echo oui | echo non | echo hola | grep oui'


@AddTest("pipe_13")#line 503
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'echo oui | echo non | echo hola | grep non'


@AddTest("pipe_14")#line 504
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'echo oui | echo non | echo hola | grep hola'


@AddTest("pipe_15")#line 505
class TestTest(TestDiff):
    def _input(self):
        return 'echo hola | cat -e | cat -e | cat -e'


@AddTest("pipe_16")#line 506
class TestTest(TestDiff):
    def _input(self):
        return 'cd .. | echo "hola"'


@AddTest("pipe_17")#line 507
class TestTest(TestDiff):
    def _input(self):
        return 'cd / |echo "hola"'


@AddTest("pipe_18")#line 508
class TestTest(TestDiff):
    def _input(self):
        return 'cd .. | pwd'


@AddTest("pipe_19")#line 509
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'ifconfig | grep ":"'


@AddTest("pipe_20")#line 510
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'ifconfig | grep hola'


@AddTest("pipe_21")#line 511
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'whoami | grep $USER'


@AddTest("pipe_22")#line 512
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.bash.SendCommand("whoami | grep $USER > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("whoami | grep $USER > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        return ("ls")


@AddTest("pipe_23")#line 513
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("whoami | cat -e | cat -e > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("whoami | cat -e | cat -e > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        return ("ls")


@AddTest("pipe_24")#line 514
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("whereis ls | cat -e | cat -e > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("whereis ls | cat -e | cat -e > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        return ("ls")


@AddTest("pipe_25")#line 515
class TestTest(TestDiff):
    def _input(self):
        return 'ls | hola'


@AddTest("pipe_26")#line 516
class TestTest(TestDiff):
    def _input(self):
        return 'ls | /usr/bin/ls hola'


@AddTest("pipe_27")#line 517
class TestTest(TestDiff):
    def _input(self):
        return 'ls | ls | hola'


@AddTest("pipe_28")#line 518
class TestTest(TestDiff):
    def _input(self):
        return 'ls | hola | ls'


@AddTest("pipe_29")#line 519
class TestTest(TestDiff):
    def _input(self):
        return 'ls | ls | hola | rev'


@AddTest("pipe_30")#line 520
class TestTest(TestDiff):
    def _input(self):
        return 'ls | ls | echo hola | rev'


@AddTest("pipe_31")#line 521
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"4 errors from 4 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'ls -la | grep "."'


@AddTest("pipe_32")#line 522
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'ls -la | grep "\'.\'"'


@AddTest("pipe_33")#line 523
class TestTest(TestDiff):
    def _input(self):
        return 'echo ../../../alias.sh | cat -e | cat -e | cat -e | cat -e| cat -e | cat -e | cat -e | cat -e| cat -e | cat -e | cat -e'


@AddTest("pipe_34")#line 524
class TestTest(TestDiff):
    def _input(self):
        return 'ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls | ls'


@AddTest("pipe_35")#line 525
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'echo hola | cat | cat | cat | cat | cat | grep hola'


@AddTest("pipe_36")#line 526
class TestTest(TestDiff):
    def _input(self):
        return 'echo hola | cat'


@AddTest("pipe_37")#line 527
class TestTest(TestDiff):
    def _input(self):
        return 'echo hola| cat'


@AddTest("pipe_38")#line 528
class TestTest(TestDiff):
    def _input(self):
        return 'echo hola |cat'


@AddTest("pipe_39")#line 529
class TestTest(TestDiff):
    def _input(self):
        return 'echo hola|cat'


@AddTest("pipe_42")#line 532
class TestTest(TestDiff):
    def _input(self):
        return 'ech|o hola | cat'


@AddTest("pipe_43")#line 533
class TestTest(TestDiff):
    def _input(self):
        return 'cat ../../../Makefile | cat -e | cat -e'


@AddTest("pipe_44")#line 534
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'cat ../../../Makefile | grep srcs | cat -e'


@AddTest("pipe_45")#line 535
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":2}
    def _input(self):
        return 'cat ../../../Makefile | grep srcs | grep srcs | cat -e'


@AddTest("pipe_46")#line 536
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'cat ../../../Makefile | grep pr | head -n 5 | cd file'


@AddTest("pipe_47")#line 537
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        return 'cat ../../../Makefile | grep pr | head -n 5 | hello'


@AddTest("pipe_48")#line 538
class TestTest(TestDiff):
    def _input(self):
        return 'export HOLA=bonjour | cat -e | cat -e'


@AddTest("pipe_49")#line 539
class TestTest(TestDiff):
    def _input(self):
        return 'unset HOLA | cat -e'


@AddTest("pipe_50")#line 540
class TestTest(TestDiff):
    def Init(self):
        super().Init()
        self.minishell.allowed_error = {"2 errors from 2 contexts (suppressed: 0 from 0)":1}
    def _input(self):
        self.minishell.Send("export HOLA | echo hola")
        return 'env | grep PROUT'


@AddTest("pipe_51")#line 541
class TestTest(TestDiff):
    def _input(self):
        return 'export | echo hola'


@AddTest("pipe_54")#line 544
class TestTest(TestDiff):
    def _input(self):
        return 'slee 3 | exit'


@AddTest("pipe_56")#line 546
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > a")
        self.minishell.bash.SendCommand(">>b echo que tal")
        self.minishell.bash.SendCommand("cat a | <b cat | cat > c | cat")
        self.minishell.bash.SendCommand("rm a b c")
        self.minishell.bashPosix.SendCommand("echo hola > a")
        self.minishell.bashPosix.SendCommand(">>b echo que tal")
        self.minishell.bashPosix.SendCommand("cat a | <b cat | cat > c | cat")
        self.minishell.bashPosix.SendCommand("rm a b c")
        return ("ls")

@AddTest("test_redir_1")#line 612
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > a")
        self.minishell.bash.SendCommand("cat a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo hola > a")
        self.minishell.bashPosix.SendCommand("cat a")
        self.minishell.bashPosix.SendCommand("rm a")
        return ("ls")

@AddTest("test_redir_2")#line 613
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > a")
        self.minishell.bash.SendCommand("echo que tal >> a")
        self.minishell.bash.SendCommand("cat a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo hola > a")
        self.minishell.bashPosix.SendCommand("echo que tal >> a")
        self.minishell.bashPosix.SendCommand("cat a")
        self.minishell.bashPosix.SendCommand("rm a")
        return ("ls")

@AddTest("test_redir_3")#line 614
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > a")
        self.minishell.bash.SendCommand("echo que tal >> a")
        self.minishell.bash.SendCommand("cat <a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo hola > a")
        self.minishell.bashPosix.SendCommand("echo que tal >> a")
        self.minishell.bashPosix.SendCommand("cat <a")
        self.minishell.bashPosix.SendCommand("rm a")
        return ("ls")

@AddTest("test_redir_4")#line 615
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bash.SendCommand("echo que tal >> a")
        self.minishell.bash.SendCommand("cat a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo hola > a")
        self.minishell.bashPosix.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo que tal >> a")
        self.minishell.bashPosix.SendCommand("cat a")
        self.minishell.bashPosix.SendCommand("rm a")
        return ("ls")

@AddTest("test_redir_5")#line 616
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola que tal > a")
        self.minishell.bash.SendCommand("cat a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo hola que tal > a")
        self.minishell.bashPosix.SendCommand("cat a")
        self.minishell.bashPosix.SendCommand("rm a")
        return ("ls")

@AddTest("test_redir_6")#line 617
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola que tal > a")
        self.minishell.bash.SendCommand("cat -e a")
        self.minishell.bash.SendCommand("rm a")
        self.minishell.bashPosix.SendCommand("echo hola que tal > a")
        self.minishell.bashPosix.SendCommand("cat -e a")
        self.minishell.bashPosix.SendCommand("rm a")
        return ("ls")

@AddTest("test_redir_7")#line 618
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("export HOLA=hey")
        self.minishell.bash.SendCommand("echo bonjour > $HOLA")
        self.minishell.bash.SendCommand("echo $HOLA")
        self.minishell.bash.SendCommand("rm $HOLA")
        self.minishell.bashPosix.SendCommand("echo bonjour > $HOLA")
        self.minishell.bashPosix.SendCommand("echo $HOLA")
        self.minishell.bashPosix.SendCommand("rm $HOLA")
        return ("ls")

@AddTest("test_redir_8")#line 619
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("whereis grep > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("whereis grep > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_9")#line 620
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("ls -la > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("ls -la > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_10")#line 621
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("pwd > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("pwd > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_11")#line 622
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("pwd >        bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("pwd >        bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_12")#line 626
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand(">bonjour echo hola")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand(">bonjour echo hola")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_13")#line 627
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand(">bonjour | echo hola")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand(">bonjour | echo hola")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_14")#line 628
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("prout hola > bonjour")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("prout hola > bonjour")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_15")#line 629
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_16")#line 630
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_17")#line 631
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour")
        self.minishell.bash.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour >> bonjour >> bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_18")#line 632
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola >> bonjour >> bonjour > bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour >> bonjour > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_19")#line 633
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola >> bonjour >> bonjour > bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour >> bonjour > bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour >> bonjour > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour >> bonjour > bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_20")#line 634
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour >> bonjour >> bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour >> bonjour >> bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_21")#line 635
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("cat < bonjour < hello")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour < hello")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_22")#line 636
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("cat < hello < bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("cat < hello < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_23")#line 637
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand("echo hola > bonjour > hello > bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour > hello > bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_24")#line 638
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("echo hola > bonjour > hello > bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour > hello > bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_25")#line 639
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand("echo hola > bonjour >> hello > bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour >> hello > bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_26")#line 640
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand("echo hola > bonjour > hello >> bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour > hello >> bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_27")#line 641
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("echo hola > bonjour > hello >> bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour > hello >> bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_28")#line 642
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand("echo hola >> bonjour > hello > bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour > hello > bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_29")#line 643
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour > hello > bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour > hello > bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_30")#line 644
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand("echo hola >> bonjour >> hello >> bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour >> hello >> bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_31")#line 645
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("echo hey > bonjour")
        self.minishell.bash.SendCommand("echo hola >> bonjour >> hello >> bonjour")
        self.minishell.bash.SendCommand("cat hello")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("echo hey > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola >> bonjour >> hello >> bonjour")
        self.minishell.bashPosix.SendCommand("cat hello")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return ("ls")

@AddTest("test_redir_32")#line 646
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand(">bonjour echo hola bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand(">bonjour echo hola bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return ("ls")

@AddTest("test_redir_33")#line 647
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("hola>bonjour>hola>>bonjour>hola hey")
        self.minishell.bash.SendCommand(">bonjour hola >hola")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("cat hola")
        self.minishell.bash.SendCommand("rm bonjour hola")
        self.minishell.bashPosix.SendCommand("hola>bonjour>hola>>bonjour>hola hey")
        self.minishell.bashPosix.SendCommand(">bonjour hola >hola")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("cat hola")
        self.minishell.bashPosix.SendCommand("rm bonjour hola")
        return ("ls")

@AddTest("test_redir_34")#line 648
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo bonjour > hola1")
        self.minishell.bash.SendCommand("echo hello > hola2")
        self.minishell.bash.SendCommand("echo 2 >hola1 >> hola2")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("cat hola1")
        self.minishell.bash.SendCommand("cat hola2")
        self.minishell.bash.SendCommand("rm hola1 hola2")
        self.minishell.bashPosix.SendCommand("echo bonjour > hola1")
        self.minishell.bashPosix.SendCommand("echo hello > hola2")
        self.minishell.bashPosix.SendCommand("echo 2 >hola1 >> hola2")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("cat hola1")
        self.minishell.bashPosix.SendCommand("cat hola2")
        self.minishell.bashPosix.SendCommand("rm hola1 hola2")
        return ("ls")

@AddTest("test_redir_35")#line 649
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo bonjour > hola1")
        self.minishell.bash.SendCommand("echo hello > hola2")
        self.minishell.bash.SendCommand("echo 2 >>hola1 > hola2")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("cat hola1")
        self.minishell.bash.SendCommand("cat hola2")
        self.minishell.bash.SendCommand("rm hola1 hola2")
        self.minishell.bashPosix.SendCommand("echo bonjour > hola1")
        self.minishell.bashPosix.SendCommand("echo hello > hola2")
        self.minishell.bashPosix.SendCommand("echo 2 >>hola1 > hola2")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("cat hola1")
        self.minishell.bashPosix.SendCommand("cat hola2")
        self.minishell.bashPosix.SendCommand("rm hola1 hola2")
        return ("ls")

@AddTest("test_redir_36")#line 650
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("> pwd")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm pwd")
        self.minishell.bashPosix.SendCommand("> pwd")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm pwd")
        return ("ls")

@AddTest("test_redir_37")#line 651
class TestTest(TestDiff):
    def _input(self):
        return ("< pwd")

@AddTest("test_redir_38")#line 653
class TestTest(TestDiff):
    def _input(self):
        return ("cat < pwd")

@AddTest("test_redir_39")#line 654
class TestTest(TestDiff):
    def _input(self):
        return ("cat < srcs/pwd")

@AddTest("test_redir_40")#line 655
class TestTest(TestDiff):
    def _input(self):
        return ("cat < ../pwd")

@AddTest("error_redir_1")#line 656
class TestTest(TestReturnError):
    def _input(self):
        return ("cat >>")
    def _error(self):
        return self.error_unexpected("newline")

@AddTest("error_redir_2")#line 657
class TestTest(TestReturnError):
    def _input(self):
        return ("cat >>>")
    def _error(self):
        return self.error_unexpected(">")

@AddTest("error_redir_3")#line 658
class TestTest(TestReturnError):
    def _input(self):
        return ("cat >> <<")
    def _error(self):
        return self.error_unexpected("<<")

@AddTest("error_redir_4")#line 659
class TestTest(TestReturnError):
    def _input(self):
        return ("cat >> > >> << >>")
    def _error(self):
        return self.error_unexpected(">")

@AddTest("more_error_1")#line 660
class TestTest(TestDiff):
    def _input(self):
        return "cat < ls"

@AddTest("more_error_2")#line 661
class TestTest(TestDiff):
    def _input(self):
        return "cat < ls > ls"

@AddTest("more_error_3")#line 662
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("cat > ls1 < ls2")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm ls1")
        self.minishell.bashPosix.SendCommand("cat > ls1 < ls2")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm ls1")
        return "ls"

@AddTest("more_error_4")#line 663
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("echo que tal >> bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("echo que tal >> bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("more_error_5")#line 664
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bash.SendCommand("echo que tal >> bonjour")
        self.minishell.bash.SendCommand("cat < bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo que tal >> bonjour")
        self.minishell.bashPosix.SendCommand("cat < bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("more_error_6")#line 665
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("e'c'\"h\"o hola > bonjour")
        self.minishell.bash.SendCommand("cat 'bo'\"n\"jour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("e'c'\"h\"o hola > bonjour")
        self.minishell.bashPosix.SendCommand("cat 'bo'\"n\"jour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("more_error_7")#line 667
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour hey")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("/usr/bin/cat hey")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour hey")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("/usr/bin/cat hey")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("more_error_8")#line 668
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand(">bonjour >hello <prout")
        self.minishell.bash.SendCommand("/usr/bin/cat bonjour hello")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand(">bonjour >hello <prout")
        self.minishell.bashPosix.SendCommand("/usr/bin/cat bonjour hello")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return "ls"

@AddTest("more_error_9")#line 669
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("echo hola > hello")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand(">bonjour >hello <prout")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("/usr/bin/cat bonjour hello")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > hello")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand(">bonjour >hello <prout")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("/usr/bin/cat bonjour hello")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        return "ls"

@AddTest("more_error_10")#line 670
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("echo hey > hello")
        self.minishell.bash.SendCommand(">bonjour <prout >hello")
        self.minishell.bash.SendCommand("/usr/bin/cat bonjour hello")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("echo hey > hello")
        self.minishell.bashPosix.SendCommand(">bonjour <prout >hello")
        self.minishell.bashPosix.SendCommand("/usr/bin/cat bonjour hello")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("more_error_11")#line 671
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("echo hey > hello")
        self.minishell.bash.SendCommand("rm bonjour hello")
        self.minishell.bash.SendCommand(">bonjour <prout >hello")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("/usr/bin/cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("echo hey > hello")
        self.minishell.bashPosix.SendCommand("rm bonjour hello")
        self.minishell.bashPosix.SendCommand(">bonjour <prout >hello")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("/usr/bin/cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("verif_args_1")#added
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("ls >bonjour -l")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("ls >bonjour -l")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("verif_args_2")#added
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("ls >bonjour -a <bonjour -l")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("ls >bonjour -a <bonjour -l")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("even_more_redirs_1")#line 672
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > bonjour")
        self.minishell.bash.SendCommand("<bonjour cat | wc > bonjour")
        self.minishell.bash.SendCommand("cat bonjour")
        self.minishell.bash.SendCommand("rm bonjour")
        self.minishell.bashPosix.SendCommand("echo hola > bonjour")
        self.minishell.bashPosix.SendCommand("<bonjour cat | wc > bonjour")
        self.minishell.bashPosix.SendCommand("cat bonjour")
        self.minishell.bashPosix.SendCommand("rm bonjour")
        return "ls"

@AddTest("even_more_redirs_2")#line 673
class TestTest(TestDiff):
    def _input(self):
        self.minishell.Send("rm bonjour > bonjour")
        return "/usr/bin/ls -l bonjour"

@AddTest("even_more_redirs_3")#line 674
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bash.SendCommand(">$HOLA")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm \"$HOLA\"")
        self.minishell.bashPosix.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bashPosix.SendCommand(">$HOLA")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm \"$HOLA\"")
        return "ls"

@AddTest("even_more_redirs_4")#line 675
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bash.SendCommand(">\"$HOLA\"")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm \"$HOLA\"")
        self.minishell.bashPosix.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bashPosix.SendCommand(">\"$HOLA\"")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm \"$HOLA\"")
        return "ls"

@AddTest("even_more_redirs_5")#line 676
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bash.SendCommand(">$\"HOLA\"")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm HOLA")
        self.minishell.bashPosix.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bashPosix.SendCommand(">$\"HOLA\"")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm HOLA")
        return "ls"

@AddTest("even_more_redirs_6")#line 677
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bash.SendCommand(">$HOLA>hey")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm \"$HOLA\" hey")
        self.minishell.bashPosix.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bashPosix.SendCommand(">$HOLA>hey")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm \"$HOLA\" hey")
        return "ls"

@AddTest("even_more_redirs_7")#line 678
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bash.SendCommand(">hey>$HOLA")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm \"$HOLA\" hey")
        self.minishell.bashPosix.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bashPosix.SendCommand(">hey>$HOLA")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm \"$HOLA\" hey")
        return "ls"

@AddTest("even_more_redirs_8")#line 679
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bash.SendCommand(">hey>$HOLA>hey>hey")
        self.minishell.bash.SendCommand("ls")
        self.minishell.bash.SendCommand("rm \"$HOLA\" hey")
        self.minishell.bashPosix.SendCommand("export HOLA=\"bonjour hello\"")
        self.minishell.bashPosix.SendCommand(">hey>$HOLA>hey>hey")
        self.minishell.bashPosix.SendCommand("ls")
        self.minishell.bashPosix.SendCommand("rm \"$HOLA\" hey")
        return "ls"

@AddTest("even_more_redirs_9")#line 680
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("export A=hey")
        self.minishell.bash.SendCommand("export A B=Hola D E C=\"Que Tal\"")
        self.minishell.bash.SendCommand("echo $PROUT$B$C > a > b > c")
        self.minishell.bash.SendCommand("cat a")
        self.minishell.bash.SendCommand("cat b")
        self.minishell.bash.SendCommand("cat c")
        self.minishell.bash.SendCommand("rm a b c")
        self.minishell.bashPosix.SendCommand("export A=hey")
        self.minishell.bashPosix.SendCommand("export A B=Hola D E C=\"Que Tal\"")
        self.minishell.bashPosix.SendCommand("echo $PROUT$B$C > a > b > c")
        self.minishell.bashPosix.SendCommand("cat a")
        self.minishell.bashPosix.SendCommand("cat b")
        self.minishell.bashPosix.SendCommand("cat c")
        self.minishell.bashPosix.SendCommand("rm a b c")
        return "ls"

@AddTest("even_more_redirs_10")#line 681
class TestTest(TestDiff):
    def _input(self):
        self.minishell.bash.SendCommand("echo hola > a > b > c")
        self.minishell.bash.SendCommand("cat a")
        self.minishell.bash.SendCommand("cat b")
        self.minishell.bash.SendCommand("cat c")
        self.minishell.bash.SendCommand("rm a b c")
        self.minishell.bashPosix.SendCommand("echo hola > a > b > c")
        self.minishell.bashPosix.SendCommand("cat a")
        self.minishell.bashPosix.SendCommand("cat b")
        self.minishell.bashPosix.SendCommand("cat c")
        self.minishell.bashPosix.SendCommand("rm a b c")
        return "ls"

@AddTest("even_more_redirs_11")#added
class TestTest(TestDiff):
    def _input(self):
        return ">$e"
