import logging
from telegram import Update
from NottyBoyString.utils.fonts import TinyCapsFont

class BotLogger:
    def __init__(self, db, bot, log_group_id: int):
        self.db = db
        self.bot = bot
        self.log_group_id = log_group_id
    
    async def log_to_group(self, message: str, log_type: str = "INFO"):
        """Log message to log group"""
        try:
            log_message = TinyCapsFont.bold_tiny_caps(f"📡 {log_type} ʟᴏɢ\n\n{message}")
            await self.bot.send_message(chat_id=self.log_group_id, text=log_message, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Failed to send log to group: {e}")
    
    async def log_user_action(self, user_id: int, action: str, details: str):
        """Log user action to database and group"""
        # Log to database
        await self.db.add_log("USER_ACTION", user_id, f"{action}: {details}")
        
        # Log to group
        log_message = f"👤 ᴜsᴇʀ: {user_id}\n⚡ ᴀᴄᴛɪᴏɴ: {action}\n📝 ᴅᴇᴛᴀɪʟs: {details}"
        await self.log_to_group(log_message, "USER_ACTION")
    
    async def log_session_generated(self, user_id: int, session_type: str):
        """Log session generation"""
        log_message = f"🔐 ɴᴇᴡ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ\n\nᴜsᴇʀ: {user_id}\nᴛʏᴘᴇ: {session_type}"
        await self.log_user_action(user_id, "SESSION_GENERATED", f"Type: {session_type}")
    
    async def log_admin_action(self, admin_id: int, action: str, target: str = ""):
        """Log admin action"""
        log_message = f"🛡️ ᴀᴅᴍɪɴ ᴀᴄᴛɪᴏɴ\n\nᴀᴅᴍɪɴ: {admin_id}\nᴀᴄᴛɪᴏɴ: {action}\nᴛᴀʀɢᴇᴛ: {target}"
        await self.log_to_group(log_message, "ADMIN_ACTION")
