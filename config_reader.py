from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr


# Uses a .env file to gain tokens

class Settings(BaseSettings):
    bot_token: SecretStr
    payment_token: SecretStr
    sid: SecretStr
    token: SecretStr
    bitrix_api: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
