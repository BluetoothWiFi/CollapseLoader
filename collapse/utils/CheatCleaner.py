from .Logger import logger
from .Selector import selector
from .Settings import settings
import shutil
import os

class CheatCleaner:
    def __init__(self):
        # Absolute path
        self.folders = [
            'C:\\Celestial',
            'C:\\baritone',
            'C:\\shaderpacks',
            'C:\\resourcepacks',
            'C:\\RockAntiLeak',
            'C:\\Rockstar',
            'C:\\MoonProject',
            'C:\\hachrecode',
            'C:\\Nursultan',
            f'C:\\Users\\{os.getlogin()}\\.avalon'
        ]
    
    def scan_folders(self):
        if selector.ask('Remove all cheats folder [y,n]?'):
            for folder in self.folders:
                if os.path.isdir(folder):
                    logger.info('Removing folder: ' + folder)

                    SafeDir = settings.get('SafeDirName')
                    
                    shutil.move(folder, SafeDir)
                    shutil.rmtree(SafeDir, ignore_errors=True)

cheatcleaner = CheatCleaner()
