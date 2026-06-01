from dotenv import load_dotenv
load_dotenv()
import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "autoparts_shop")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@autoparts.com")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    ITEMS_PER_PAGE: int = 5
    PAYMENT_PROVIDER_TOKEN: str = os.getenv("PAYMENT_PROVIDER_TOKEN", "YOUR_PAYMENT_TOKEN")
    ADMIN_IDS: List[int] = field(default_factory=list)

    def __post_init__(self):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        self.ADMIN_IDS = [int(x) for x in admin_ids_str.split(",") if x.strip().isdigit()]

config = Config()
