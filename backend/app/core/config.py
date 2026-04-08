from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Optimizacion Embalses API"
    app_version: str = "0.1.0"
    frontend_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


settings = Settings()