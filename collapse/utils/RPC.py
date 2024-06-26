from pypresence import Presence
from threading import Thread
from time import sleep, time

from .Data import data
from .Settings import settings
from .Logger import logger

class RPC(Thread):
    """RPC, used to display activity in Discord"""

    client_id = '1225803664204234772'
    RPC = Presence(client_id)

    details = 'Choosing a client'

    start_time = time()
    disabled = True if settings.get('rpc') == 'False' else False

    def update(self):
        """updates the activity"""
        try:
            self.RPC.update(state=settings.get('nickname'), details=self.details, large_image='https://i.imgur.com/ZpWg110.gif', 
                            buttons=[
                                {'label': 'Discord', 'url': 'https://collapseloader.org/discord'},
                                {'label': 'collapseloader.org', 'url': 'https://collapseloader.org'} 
                            ],
                            start=self.start_time,
                            large_text=f'Version {data.version}' )
        except:
            logger.error('RPC crashed')
            logger.debug('Trying to connect')

            try:
                    self.RPC.connect()
                    logger.info('Connected to discord')

            except:
                logger.error('Cannot reconnect to Discord')


    def run(self):
        """starts a thread for the rpc"""

        try:
            self.RPC.connect()
        except:
            return
        
        while True:
            if not self.disabled:
                self.update()

            else:
                self.RPC.clear()

            sleep(1)

rpc = RPC()