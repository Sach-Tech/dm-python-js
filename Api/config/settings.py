from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str= "myapp1"
    mongo_url: str = "mongodb://root:example@localhost:27017/"
    
    class Config:
        env_file = ".env"