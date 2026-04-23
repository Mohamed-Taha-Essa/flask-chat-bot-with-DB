import os 
from dataclasses import dataclass
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
@dataclass
class Settings:

    API_V1_PREFIX:str = '/api/v1'
    SERVICE_NAME:str = 'Chat Service'
    VERSION:str = '1.0.0'


    #server setttings
    HOST:str ='0.0.0.0'
    PORT:int = 8001
    DEBUG:bool = True


    #database settings 
    DATABASE_URL:str = f"sqlite:///{os.path.join(BASE_DIR, 'my_database.db')}"

def get_settings()->Settings:
    return(Settings(
            API_V1_PREFIX  = os.getenv( "API_V1_PREFIX",  '/api/v1'), 
            SERVICE_NAME  = os.getenv( "SERVICE_NAME", 'Chat Service' ), 
            VERSION  = os.getenv( "VERSION", '1.0.0' ), 


            #server setttings
            HOST  = os.getenv( "HOST", '0.0.0.0' ),
            PORT = os.getenv( "PORT",  "8001"), 
            DEBUG = os.getenv( "DEBUG", "True" ), 


            #database settings 
            DATABASE_URL  = os.getenv( "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'my_database.db')}"
        ), 
    ))
    

settings = get_settings()