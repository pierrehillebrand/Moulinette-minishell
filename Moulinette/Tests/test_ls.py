from CheckerLib import *

@AddTest("ls_1")
class TestTest1(BaseTest):
    def __init__(self, id, *args, **kargs):
        super().__init__(id, *args, **kargs)
        
    def Init(self):
        self.minishell = MinishellDiff()
        return 

    def Run(self):
        self.WriteTempFile("test1","echo Hello World!")
        self.WriteTempFile("test2","echo Hello World!")
        self.CreateTempDir("testdir")
        self.minishell.Send("ls")
        #self.minishell.SendArrowUp()
        #self.minishell.Send("")
        #self.minishell.SendSignal(signal.SIGTERM)
        #output = self.minishell.Read()
        output = self.minishell.CompareOutput(BaseTest.DEBUG)
        DebugPrint("Is output correct: ",output)
        return output