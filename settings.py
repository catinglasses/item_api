from pydantic import root_validator
from pydantic.networks import IPvAnyAddress
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Class granting database access via construction of DATABASE_URL from .env-file and error handling for easier debug"""
    DB_HOST: IPvAnyAddress
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = None

    @root_validator(pre=True)
    def create_db_url(cls, values):
        """"Construct DATABASE_URL from individual components"""
        try:
            db_user = values.get("DB_USER")
            db_pass = values.get("DB_PASS")
            db_host = values.get("DB_HOST")
            db_port = values.get("DB_PORT")
            db_name = values.get("DB_NAME")
        
            if all([db_user, db_pass, db_host, db_name]):
                values["DATABASE_URL"] = (
                    f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
                )
            else:
                raise ValueError("Missing database connection params.")
        except Exception as e:
            raise ValueError(f"Error constructing DATABASE_URL: {e}")

        return values


    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    print(e.json())
