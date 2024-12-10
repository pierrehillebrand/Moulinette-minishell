import subprocess
import select
import time
import os
import tempfile
import threading

current_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = os.path.join(current_dir, "temp")

#reset temp directory
os.system(f"rm -rf {temp_dir}")
os.system(f"mkdir -p {temp_dir}")

class Bash:
    time_sleep = 0.05
    def __init__(self) -> None:
        # Créer un fichier temporaire pour rediriger stdout et stderr
        self.temp_fileOut = tempfile.NamedTemporaryFile(mode='w+', delete=False, dir=temp_dir)
        self.temp_fileOut_name = self.temp_fileOut.name  # Obtenir le nom du fichier temporaire
        self.temp_fileErr = tempfile.NamedTemporaryFile(mode='w+', delete=False, dir=temp_dir)
        self.temp_fileErr_name = self.temp_fileErr.name  # Obtenir le nom du fichier temporaire

        
        # Lancer le processus bash
        self.process = subprocess.Popen(
            ['bash','--posix'],  # Démarrer un shell bash
            stdin=subprocess.PIPE,  # Pour envoyer des commandes
            stdout=self.temp_fileOut,    # Rediriger stdout vers le fichier temporaire
            stderr=self.temp_fileErr,    # Rediriger stderr vers le fichier temporaire
            text=True,                  # Pour gérer les chaînes de caractères
            universal_newlines=True,    # Pour gérer les sauts de ligne
        )
        self.incOut = 0
        self.incErr = 0

    def SendCommand(self, command: str):
        time.sleep(Bash.time_sleep)
        """Envoyer une commande au shell."""
        if self.process.stdin and self.process.poll() is None:  # Vérifier si le stdin est ouvert
            self.process.stdin.write(command + '\n')  # Écrire la commande
            self.process.stdin.flush()  # Assurer que la commande est envoyée
        time.sleep(Bash.time_sleep)
        
    def WriteCommand(self, command: str):
        time.sleep(Bash.time_sleep)
        """Envoyer une commande au shell."""
        if self.process.stdin and self.process.poll() is None:
            self.process.stdin.write(command)
            self.process.stdin.flush()
        time.sleep(Bash.time_sleep)

    def ReadAllOutput(self):
        time.sleep(Bash.time_sleep)
        """Lire tout le contenu du fichier temporaire."""
        with open(self.temp_fileOut_name, 'r', encoding='Latin-1') as f:
            f.seek(self.incOut)
            output = f.read()  # Lire tout le contenu
            self.incOut = f.tell()
        return output
    
    def ReadAllError(self):
        time.sleep(Bash.time_sleep)
        """Lire tout le contenu du fichier temporaire."""
        with open(self.temp_fileErr_name, 'r', encoding='Latin-1') as f:
            f.seek(self.incErr)
            output = f.read()
            self.incErr = f.tell()
        output = output.replace("\x07","")
        return output
    
    def SendCtrlD(self):
        time.sleep(Bash.time_sleep)
        """Envoyer Ctrl+D au shell pour fermer le processus."""
        if self.process.stdin and self.process.poll() is None:
            self.process.stdin.write('\x04')
            self.process.stdin.flush()
        time.sleep(Bash.time_sleep)
            
    def SendCtrlC(self):
        time.sleep(Bash.time_sleep)
        """Envoyer Ctrl+C au shell pour fermer le processus."""
        if self.process.stdin and self.process.poll() is None:
            self.process.stdin.write('\x03')
            self.process.stdin.flush()
        time.sleep(Bash.time_sleep)
        
	#Ctrl+\
    def SendCtrlBackslash(self):
        time.sleep(Bash.time_sleep)
        """Envoyer Ctrl+\ au shell pour fermer le processus."""
        if self.process.stdin and self.process.poll() is None:
            self.process.stdin.write('\x1c')
            self.process.stdin.flush()
        time.sleep(Bash.time_sleep)

    def SendArrowUp(self):
        time.sleep(Bash.time_sleep)
        """Envoyer Ctrl+C au shell pour fermer le processus."""
        if self.process.stdin and self.process.poll() is None:
            self.process.stdin.write('\x1b[A')
            self.process.stdin.flush()
        time.sleep(Bash.time_sleep)

    def SendArrowDown(self):
        time.sleep(Bash.time_sleep)
        """Envoyer Ctrl+C au shell pour fermer le processus."""
        if self.process.stdin and self.process.poll() is None:
            self.process.stdin.write('\x1b[B')
            self.process.stdin.flush()
        time.sleep(Bash.time_sleep)

    def close(self):
        """Fermer le processus et le fichier temporaire."""
        self.process.stdin.close()  # Fermer l'entrée standard
        self.process.wait()  # Attendre que le processus se termine
        self.temp_fileOut.close()  # Fermer le fichier temporaire
        self.temp_fileErr.close()
    
    def __del__(self):
        self.close()
        # Supprimer les fichiers temporaires
        os.remove(self.temp_fileOut_name)
        os.remove(self.temp_fileErr_name)
        
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    exec_dir = os.path.dirname(current_dir)
    os.chdir(exec_dir)
    bash = Bash()
    bash.SendCommand("./minishell")
    bash.SendCommand("Test")
    print(bash.ReadAllOutput(), end="")
    bash.SendCommand("Hello World")
    bash.SendCtrlD()
    print(bash.ReadAllOutput(), end="")
    print("Error:")
    print(bash.ReadAllError(), end="")
    bash.close()  # Fermer le processus et le fichier temporaire