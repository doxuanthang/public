import subprocess
from time import sleep
try:
    from colorama import Fore, Back, Style
except:
    subprocess.run("pip install colorama")
    from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.RESET_ALL)
print('back to normal now')
