from CheckerLib import *

@AddTest("Norme")
class TestNorme(BaseTest):
    def __init__(self, id, *args, **kargs):
        super().__init__(id, *args, **kargs)

    def Init(self):
        return
    
    def Run(self):
        normeflag = ["-R","CheckForbiddenSourceHeader"]
        norme = True
        norme = CheckNorme("libft",normeflag) and norme
        norme = CheckNorme("srcs",normeflag) and norme
        return norme
    
    def PrintResult(self):
        return
    
    def Close(self):
        return True