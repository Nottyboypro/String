class TinyCapsFont:
    """ᴛɪɴʏ ᴄᴀᴘs ғᴏɴᴛ ᴄᴏɴᴠᴇʀᴛᴇʀ"""
    
    NORMAL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    TINY_CAPS = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ0123456789"
    
    @classmethod
    def convert(cls, text: str) -> str:
        """ᴄᴏɴᴠᴇʀᴛ ᴛᴇxᴛ ᴛᴏ ᴛɪɴʏ ᴄᴀᴘs"""
        translation_table = str.maketrans(cls.NORMAL, cls.TINY_CAPS)
        return text.translate(translation_table)
    
    @classmethod
    def bold_tiny_caps(cls, text: str) -> str:
        """ᴄᴏɴᴠᴇʀᴛ ᴛᴏ ʙᴏʟᴅ ᴛɪɴʏ ᴄᴀᴘs"""
        tiny_text = cls.convert(text)
        return f"**{tiny_text}**"

class MessageTemplates:
    """ᴘʀᴇ-ғᴏʀᴍᴀᴛᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴇᴍᴘʟᴀᴛᴇs"""
    
    @staticmethod
    def welcome_message():
        return TinyCapsFont.bold_tiny_caps(
            "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɴᴏᴛᴛʏʙᴏʏ sᴛʀɪɴɢ sᴇssɪᴏɴ ʙᴏᴛ!\n\n"
            "ɪ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴘᴏᴡᴇʀғᴜʟ sᴛʀɪɴɢ sᴇssɪᴏɴs ғᴏʀ:\n"
            "• ᴘʏʀᴏɢʀᴀᴍ - ᴍᴏᴅᴇʀɴ ᴍᴛᴘʀᴏᴛᴏ ʟɪʙʀᴀʀʏ\n"
            "• ᴛᴇʟᴇᴛʜᴏɴ - ғᴜʟʟ-ғᴇᴀᴛᴜʀᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ʟɪʙʀᴀʀʏ\n\n"
            "🔐 ғᴇᴀᴛᴜʀᴇs:\n"
            "- sᴇᴄᴜʀᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ\n"
            "- ɴᴏ ᴅᴀᴛᴀ sᴛᴏʀᴀɢᴇ ᴘᴏʟɪᴄʏ\n"
            "- ғᴀsᴛ ᴀɴᴅ ʀᴇʟɪᴀʙʟᴇ\n"
            "- ᴍᴜʟᴛɪ-ʟᴀɴɢᴜᴀɢᴇ sᴜᴘᴘᴏʀᴛ"
        )
    
    @staticmethod
    def pyrogram_info():
        return TinyCapsFont.bold_tiny_caps(
            "🔥 ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ\n\n"
            "ᴀᴅᴠᴀɴᴛᴀɢᴇs:\n"
            "- ᴍᴏᴅᴇʀɴ ᴀɴᴅ ᴀsʏɴᴄ\n"
            "- ᴇᴀsʏ ᴛᴏ ᴜsᴇ\n"
            "- ʙᴇsᴛ ғᴏʀ ʙᴏᴛs\n"
            "- ɢᴏᴏᴅ ᴅᴏᴄᴜᴍᴇɴᴛᴀᴛɪᴏɴ"
        )
    
    @staticmethod
    def telethon_info():
        return TinyCapsFont.bold_tiny_caps(
            "⚡ ᴛᴇʟᴇᴛʜᴏɴ sᴇssɪᴏɴ\n\n"
            "ᴀᴅᴠᴀɴᴛᴀɢᴇs:\n"
            "- ғᴜʟʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘɪ sᴜᴘᴘᴏʀᴛ\n"
            "- ɢʀᴇᴀᴛ ғᴏʀ ᴜsᴇʀʙᴏᴛs\n"
            "- ᴘᴏᴡᴇʀғᴜʟ ғᴇᴀᴛᴜʀᴇs\n"
            "- ᴀᴄᴛɪᴠᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ"
        )
