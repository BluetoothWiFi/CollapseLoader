from .Logger import logger
from tqdm import tqdm
import requests
import zipfile
import os

class DataManager:
    """Used to manage loader data"""

    def __init__(self) -> None:
        self.root_dir = 'data/'
        self.server = 'https://axkanxneklh7.objectstorage.eu-amsterdam-1.oci.customer-oci.com/n/axkanxneklh7/b/loader/o/'
        self.server_assets = 'https://axkanxneklh7.objectstorage.eu-amsterdam-1.oci.customer-oci.com/n/axkanxneklh7/b/assets/o/'
        self.version = '1.2.1'

        if not os.path.isdir(self.root_dir):
            os.mkdir(self.root_dir)
            logger.debug('Created root dir')

        try:
            requests.get(self.server, timeout=3)
            logger.debug('Using the main server')
            
        except requests.exceptions.RequestException:
            logger.debug("The main server is down/inaccessible, we're using fallback")
            self.server = 'https://loader.collapseloader.org' # Uses a fallback server if the main server is down

        logger.debug('Initialized DataManager')

    def get_local(self, path: str) -> str:
        """Get file locally"""
        return self.root_dir + path
    
    def get_url(self, path: str) -> str:
        """Gets a link from the web, uses a fallback server if the main one is down"""
        return self.server + path
    
    def download(self, path: str) -> True:
        logger.debug(f'Downloading {path}')

        filename = os.path.basename(path)
        jar = os.path.splitext(filename)[0] + '.jar'
        path = self.root_dir + filename 
        path_dir = self.root_dir + os.path.splitext(filename)[0] + '/'
        
        if not filename.endswith('.jar'):
            if os.path.isdir(path_dir):
                logger.debug(f'{path} Already downloaded, skip')
                return
            
            else:
                os.mkdir(path_dir)

        elif filename.endswith('.jar'):
            if os.path.exists(path_dir + jar):
                logger.debug(f'{path} file downloaded, skip')
                return

            else:
                os.mkdir(path_dir)

        response = requests.get(self.server + filename, stream=True)
 
        total_size = int(response.headers.get('content-length', 0))

        with tqdm(total=total_size, unit="B", unit_scale=True, ascii=True, ncols=80, colour='blue') as progressbar:
            with open(self.root_dir + filename, "wb") as f:
                for d in response.iter_content(1024):
                    f.write(d)
                    progressbar.update(len(d))

        if filename.endswith('.zip'):
            with zipfile.ZipFile(self.root_dir + filename, 'r') as zip_file:
                zip_file.extractall(path_dir)

            os.remove(self.root_dir + filename)

        if filename.endswith('.jar'):
            os.rename(self.root_dir + filename, path_dir + filename)
    
data = DataManager()