import aiosqlite
import asyncio


# Db handling 
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

    async def findUserByUsername(self, username):
        cursor = await self.db.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,)
        )
        return await cursor.fetchone()

    async def storeUser(self, username, password):
        await self.db.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, password),
        )
        await self.db.commit()


# Auth business logic
class Auth:
    def __init__(self):
        self.db = None
        self.data = None

    async def initialize(self, filePath):
        self.db = await aiosqlite.connect(filePath) # db object life time
        self.data = Data(self.db)
        await self.data.initializeDB()

    def _ensure_initialized(self):   # check if auth initiazlize table
        if self.data is None:
            raise RuntimeError("Auth not initialized. Call initialize() first.")

    async def closeDB(self):
        if self.db:
            await self.db.close()

    async def register(self, user):
        self._ensure_initialized()

        existing = await self.data.findUserByUsername(user.username)

        if existing:
            print("User already exists")
            return False

        await self.data.storeUser(user.username, user.password)
        print("User Registered Successfully")
        return True

    async def login(self, user):
        self._ensure_initialized()

        row = await self.data.findUserByUsername(user.username)

        if row is None:
            print("User does not exist")
            return False

        db_username, db_password = row

        if db_password != user.password:
            print("Wrong password")
            return False

        user.isLogin = True
        print("User logged in successfully")
        return True


# user class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.isLogin = False


# Login required decorator
def login_required(func):
    def wrapper(*args, **kwargs):
        user = args[0]  # assumes first argument is user

        if not hasattr(user, "isLogin") or not user.isLogin:
            print("User is not authenticated")
            return None

        return func(*args, **kwargs)

    return wrapper


@login_required
def dashboard(user):
    print(f"Welcome {user.username} to dashboard")


# main flow
async def main():
    auth = Auth()
    await auth.initialize("users.db")

    user1 = User("yasir", "786")

    await auth.register(user1)
    await auth.login(user1)

    dashboard(user1)

    await auth.closeDB()


asyncio.run(main())