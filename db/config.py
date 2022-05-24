from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname:str
    database_username:str
    database_password:str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    token_exp_time:int
    
    class Config:
        env_file= '.env'
    
    
settings = Settings()    
    