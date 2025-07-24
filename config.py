import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PATHS_DIRECTORY = 'D:/Projects/Campus_navigation_system-main/PATHS/'
