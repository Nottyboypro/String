import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from NottyBoyString.utils.fonts import TinyCapsFont

class HackTools:
    def __init__(self, db):
        self.db = db
        self.STORE_ACCOUNT = 1
    
    async def hack_tools_panel(self, query):
        """Show hack tools panel"""
        text = TinyCapsFont.bold_tiny_caps(
            "🕵️ ʜᴀᴄᴋ ᴛᴏᴏʟs ᴘᴀɴᴇʟ\n\n"
            "ᴛʜɪs sᴇᴄᴛɪᴏɴ ɪs ғᴏʀ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀᴄᴄᴏᴜɴᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ. ᴜsᴇ ᴡɪᴛʜ ᴄᴀᴜᴛɪᴏɴ."
        )
        
        keyboard = [
            [InlineKeyboardButton("💾 sᴛᴏʀᴇ ᴀᴄᴄᴏᴜɴᴛ", callback_data="store_account"),
             InlineKeyboardButton("👁️ ᴠɪᴇᴡ ᴀᴄᴄᴏᴜɴᴛs", callback_data="view_accounts")],
            [InlineKeyboardButton("🔍 sᴄᴀɴ ᴜsᴇʀ", callback_data="scan_user"),
             InlineKeyboardButton("📡 ʀᴇᴀʟ-ᴛɪᴍᴇ ᴍᴏɴɪᴛᴏʀ", callback_data="realtime_monitor")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_back")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def store_account_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start account storage process"""
        text = TinyCapsFont.bold_tiny_caps(
            "💾 sᴛᴏʀᴇ ᴀᴄᴄᴏᴜɴᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ\n\n"
            "ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀᴄᴄᴏᴜɴᴛ ᴅᴀᴛᴀ ɪɴ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ғᴏʀᴍᴀᴛ:\n\n"
            "ᴜsᴇʀ_ɪᴅ|ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ|ᴘᴀssᴡᴏʀᴅ|ᴏᴛʜᴇʀ_ɪɴғᴏ"
        )
        
        await update.callback_query.edit_message_text(text, parse_mode='Markdown')
        return self.STORE_ACCOUNT
    
    async def store_account_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Store account data in database"""
        account_data = update.message.text.split('|')
        
        if len(account_data) < 3:
            text = TinyCapsFont.bold_tiny_caps("❌ ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴜsᴇ: ᴜsᴇʀ_ɪᴅ|ᴘʜᴏɴᴇ|ᴘᴀssᴡᴏʀᴅ")
            await update.message.reply_text(text, parse_mode='Markdown')
            return ConversationHandler.END
        
        account_info = {
            "user_id": int(account_data[0]),
            "phone": account_data[1],
            "password": account_data[2],
            "additional_info": account_data[3] if len(account_data) > 3 else "",
            "stored_by": update.effective_user.id,
            "is_active": True
        }
        
        await self.db.store_account(account_info)
        
        # Log the action
        await self.db.add_log(
            "ACCOUNT_STORED",
            update.effective_user.id,
            f"Stored account for user {account_data[0]}"
        )
        
        text = TinyCapsFont.bold_tiny_caps("✅ ᴀᴄᴄᴏᴜɴᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ sᴛᴏʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.")
        await update.message.reply_text(text, parse_mode='Markdown')
        
        return ConversationHandler.END
