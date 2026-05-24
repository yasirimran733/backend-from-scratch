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
            "SELECT username,password FROM users WHERE users.username = ?", (user.username,)
        )
        return await result.fetchone()

    async def storeUser(self, user):
        await self.db.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (user.username, user.password),
        )
        await self.db.commit()


# Auth Manager
class Auth:
    def __init__(self):
        self.db = None
        self.data = None

    async def initialize(self, filePath):
        self.db  = await aiosqlite.connect(filePath)
        self.data = Data(self.db)
        await self.data.initializeDB()

    async def closeDB(self):
        assert self.db is not None
        await self.db.close()

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
        elif result[1] != user.password:
            print("Passoword is Worng!. Try Again")
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

    def verifyLogin(self):
        return self.isLogin


def login_required(func):
    def wrapper(*args,**kwargs):
        if args[0].isLogin == True:
            return func(*args,**kwargs)
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
asyncio.run(auth.login(user))
asyncio.run(auth.closeDB())

dashboard(user)
