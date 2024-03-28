# 3.12.23 -> 19.07.24

# Import
import os, platform
from Src.Util.console import console

# Class import
from .config import config_manager

# Variable
CLEAN = config_manager.get_bool('GENERAL', 'clean_console')
SHOW = config_manager.get_bool('GENERAL', 'show_message')

def get_os_system():
    """
    This function returns the name of the operating system.
    """
    os_system = platform.system()
    return os_system

def start_message():
    """
    Display a start message.

    This function prints a formatted start message, including a title and creator information.
    """

    msg = """

   _____  .__   __              .___      _____.__       .__       .__                      
  /  _  \ |  |_/  |______     __| _/_____/ ____\__| ____ |__|______|__| ____   ____   ____  
 /  /_\  \|  |\   __\__  \   / __ |/ __ \   __\|  |/    \|  \___   /  |/  _ \ /    \_/ __ \ 
/    |    \  |_|  |  / __ \_/ /_/ \  ___/|  |  |  |   |  \  |/    /|  (  <_> )   |  \  ___/ 
\____|__  /____/__| (____  /\____ |\___  >__|  |__|___|  /__/_____ \__|\____/|___|  /\___  >
        \/               \/      \/    \/              \/         \/              \/     \/ 

    """

    if CLEAN: 
        if get_os_system() == 'Windows':
            os.system("cls")
        else:
            os.system("clear")
    
    if SHOW:
        console.print(f"[bold yellow]{msg}")
        console.print(f"[magenta]Created by: Ghost6446\n")

        row = "-" * console.width
        console.print(f"[yellow]{row} \n")