import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_NAME = "ɴᴏᴛᴛʏʙᴏʏsᴛʀɪɴɢʙᴏᴛ"
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    
    # API Credentials
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH")
    
    # Admin
    OWNER_ID = int(os.getenv("OWNER_ID", 123456789))
    ADMINS = [int(x) for x in os.getenv("ADMINS", "").split()] if os.getenv("ADMINS") else []
    
    # MongoDB
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/NottyBoyBot")
    
    # Log Group
    LOG_GROUP = int(os.getenv("LOG_GROUP", 0))
    
    # Security
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "nottyboy_secret_key_2024")

config = Config()
