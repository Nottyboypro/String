import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from NottyBoyString.core.database import MongoDB
from NottyBoyString.handlers.start import StartHandlers
from NottyBoyString.handlers.session_gen import SessionHandlers
from NottyBoyString.handlers.admin import AdminHandlers
from NottyBoyString.handlers.hack_tools import HackTools
from NottyBoyString.plugins.logger import BotLogger
from NottyBoyString.utils.logger import setup_logger
import config

# Setup logging
logger = setup_logger()

class NottyBoyBot:
    def __init__(self):
        self.db = MongoDB(config.MONGO_URL)
        self.logger = BotLogger(self.db, None, config.LOG_GROUP)
        
        # Initialize handlers
        self.start_handlers = StartHandlers(self.db, self.logger)
        self.session_handlers = SessionHandlers(self.db, self.logger)
        self.admin_handlers = AdminHandlers(self.db, self.logger)
        self.hack_tools = HackTools(self.db)
        
        self.application = None
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_handlers.start))
        self.application.add_handler(CommandHandler("admin", self.admin_handlers.admin_panel))
        self.application.add_handler(CommandHandler("stats", self.start_handlers.user_stats))
        
        # Admin conversation handler
        admin_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.hack_tools.store_account_start, pattern="^store_account$")],
            states={
                self.hack_tools.STORE_ACCOUNT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.hack_tools.store_account_data)
                ]
            },
            fallbacks=[CallbackQueryHandler(self.admin_handlers.admin_panel, pattern="^admin_back$")]
        )
        
        self.application.add_handler(admin_conv_handler)
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callbacks))
    
    async def handle_callbacks(self, update, context):
        """Handle all callback queries"""
        query = update.callback_query
        data = query.data
        
        if data in ["pyrogram_info", "telethon_info", "user_stats", "back_to_main"]:
            await self.start_handlers.handle_callbacks(update, context)
        elif data == "generate_pyrogram":
            await self.session_handlers.generate_pyrogram_session(query)
        elif data == "generate_telethon":
            await self.session_handlers.generate_telethon_session(query)
        elif data.startswith("admin_"):
            await self.admin_handlers.handle_admin_callbacks(update, context)
        elif data == "hack_tools":
            await self.hack_tools.hack_tools_panel(query)
        elif data == "view_accounts":
            await self.admin_handlers.show_all_accounts(query)
    
    def run(self):
        """Start the bot"""
        self.application = Application.builder().token(config.BOT_TOKEN).build()
        self.logger.bot = self.application.bot
        self.setup_handlers()
        
        logger.info("🤖 ɴᴏᴛᴛʏʙᴏʏ sᴛʀɪɴɢ sᴇssɪᴏɴ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ!")
        self.application.run_polling()

if __name__ == "__main__":
    bot = NottyBoyBot()
    bot.run()