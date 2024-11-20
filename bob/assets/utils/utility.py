from assets import *

gold = "\033[38;2;255;215;0m"
d = "\033[1;90m"
r = Style.RESET_ALL

def center(var:str, space:int=None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())

def gradient(text):
    gradient = []
    start = (255, 255, 0)
    end = (255, 140, 0)

    for i in range(len(text)):
        ratio = i / max(len(text) - 1, 1)
        r = int((1 - ratio) * start[0] + ratio * end[0])
        g = int((1 - ratio) * start[1] + ratio * end[1])
        b = int((1 - ratio) * start[2] + ratio * end[2])
        gradient.append(f"\033[38;2;{r};{g};{b}m{text[i]}\033[0m")

    return "".join(gradient)  



class AsciiArt:
    def __init__(self, text: str, w=Fore.WHITE, g=gold):
        self.text = text.splitlines()  
        self.edgeC = w
        self.color = g

    def printlogo(self):
        os.system("cls")  
        edges = ["╗", "║", "╚", "╝", "═", "╔"]
        terminal_width = shutil.get_terminal_size().columns  

        for line in self.text:
            cen = line.center(terminal_width)
            acolor = ""

            for char in cen:
                if char in edges:  
                    acolor += self.edgeC + char
                else:  
                    acolor += self.color + char

            print(acolor + Fore.RESET)

login = """
██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
                                       
"""

spade = """
███████╗██████╗  █████╗ ██████╗ ███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
███████╗██████╔╝███████║██║  ██║█████╗  
╚════██║██╔═══╝ ██╔══██║██║  ██║██╔══╝  
███████║██║     ██║  ██║██████╔╝███████╗
╚══════╝╚═╝     ╚═╝  ╚═╝╚═════╝ ╚══════╝
                                                                              
"""
spadeprint = AsciiArt(spade)
loginprint = AsciiArt(login)
