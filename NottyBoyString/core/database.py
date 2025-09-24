import motor.motor_asyncio
from bson import ObjectId
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self, mongo_url: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        self.db = self.client.NottyBoyBot
        self.users = self.db.users
        self.sessions = self.db.sessions
        self.admins = self.db.admins
        self.logs = self.db.logs
        self.accounts = self.db.accounts
        
        # Create indexes
        self._create_indexes()
    
    async def _create_indexes(self):
        """Create database indexes"""
        await self.users.create_index("user_id", unique=True)
        await self.sessions.create_index("user_id")
        await self.admins.create_index("admin_id", unique=True)
        await self.logs.create_index("timestamp")
    
    # User Management
    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str = ""):
        """Add user to database"""
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "sessions_created": 0,
            "is_banned": False,
            "is_premium": False,
            "created_at": datetime.now(),
            "last_active": datetime.now(),
            "account_info": {}
        }
        
        await self.users.update_one(
            {"user_id": user_id},
            {"$setOnInsert": user_data},
            upsert=True
        )
    
    async def increment_session_count(self, user_id: int, session_type: str):
        """Increment session count and add session record"""
        # Update user session count
        await self.users.update_one(
            {"user_id": user_id},
            {
                "$inc": {"sessions_created": 1},
                "$set": {"last_active": datetime.now()}
            }
        )
        
        # Add session record
        session_data = {
            "user_id": user_id,
            "session_type": session_type,
            "created_at": datetime.now(),
            "ip_address": "N/A",
            "user_agent": "Telegram Bot"
        }
        
        await self.sessions.insert_one(session_data)
    
    async def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """Get user statistics"""
        return await self.users.find_one({"user_id": user_id})
    
    async def get_all_users(self) -> List[Dict]:
        """Get all users (Admin only)"""
        return await self.users.find().to_list(length=None)
    
    async def get_total_users_count(self) -> int:
        """Get total users count"""
        return await self.users.count_documents({})
    
    # Admin Management
    async def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        admin = await self.admins.find_one({"admin_id": user_id})
        return admin is not None or user_id in [123456789]  # Add owner ID
    
    async def add_admin(self, admin_id: int, added_by: int, privileges: Dict):
        """Add new admin"""
        admin_data = {
            "admin_id": admin_id,
            "added_by": added_by,
            "added_at": datetime.now(),
            "privileges": privileges,
            "is_active": True
        }
        
        await self.admins.insert_one(admin_data)
    
    # Account Storage (Hack Tools)
    async def store_account(self, account_data: Dict):
        """Store account information (Admin feature)"""
        account_data["stored_at"] = datetime.now()
        account_data["is_active"] = True
        
        await self.accounts.insert_one(account_data)
    
    async def get_all_accounts(self) -> List[Dict]:
        """Get all stored accounts (Admin only)"""
        return await self.accounts.find({"is_active": True}).to_list(length=None)
    
    async def get_accounts_by_user(self, user_id: int) -> List[Dict]:
        """Get accounts by user ID"""
        return await self.accounts.find({"user_id": user_id}).to_list(length=None)
    
    # Logging
    async def add_log(self, log_type: str, user_id: int, details: str):
        """Add log entry"""
        log_data = {
            "type": log_type,
            "user_id": user_id,
            "details": details,
            "timestamp": datetime.now(),
            "ip_address": "N/A"
        }
        
        await self.logs.insert_one(log_data)
        return log_data
    
    async def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent logs"""
        return await self.logs.find().sort("timestamp", -1).limit(limit).to_list(length=None)