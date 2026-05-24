# authentication decoration, reusable everywhere , no need to write logic again and again
# Complete auth flow without db

import aiosqlite
import asyncio
import uuid


# Data Manager
class Data:
    def __init__(self, db):
        self.db = db

    async def initializeDB(self):
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT                                                      
            )    
        """)
        await self.db.commit()
        print("Table Created Successfully")

    async def findUser(self, user):
        result = await self.db.execute(
            "SELECT username,password FROM users WHERE users.username = ? AND users.password = ?",
            (user.username, user.password),
        )
        return await result.fetchone()

    async def storeUser(self, user):
        await self.db.execute(
            "INSERT OR REPLACE INTO users(username,password) VALUES (?,?)",
            (user.username, user.password),
        )
        await self.db.commit()


# Auth Manager
class Auth:
    def __init__(self):
        self.data = Data("")

    async def initialize(self, filePath):
        async with aiosqlite.connect(filePath) as db:
            self.data = Data(db)
            await self.data.initializeDB()

    async def register(self, user):
        result = await self.data.findUser(user)
        if result is not None:
            print("User already Exists")
            return False
        else:
            await self.data.storeUser(user)
            print("User Registered Successfully")
            return True

    async def login(self, user):
        result = await self.data.findUser(user)
        if result is None:
            print("User Does not Exists")
            return False
        else:
            user.isLogin = True
            print("User logged in Successfully")
            return True


# User class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.isLogin = False

    def verifyLogin(self, user):
        return user.isLogin


def login_required(func):
    def wrapper(user):
        if user.isLogin == True:
            return func(user)
        else:
            print("User is not authenticated")

    return wrapper


@login_required
def dashboard(user):
    print("Welcome to dashboard")


user = User("yasir", "786")
auth = Auth()
asyncio.run(auth.initialize("users.db"))
user1 = User("yas", "782")
asyncio.run(auth.register(user))
asyncio.run(auth.login(user1))


dashboard(user1)
