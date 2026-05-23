import asyncio 
import aiohttp
import time
import aiosqlite
BASE_URL = "https://hacker-news.firebaseio.com/v0"
# Fetch , Rate Limit , Error Handling , DB
# Complete Async Pipeline in Python: Fetch and Store

# Initizlize db with table for storing stories
async def init_db():
    async with aiosqlite.connect("hacker_stories.db") as db:  # Connect with db or create if not exists
        await db.execute("""
        CREATE TABLE IF NOT EXISTS stories(
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT
        )
    """)
        await db.commit() # Saving database changes
 
async def fetch_top_stories(session):  # Fetch top story ids
    async with session.get(f"{BASE_URL}/topstories.json") as response:
        return await response.json()
    
async def store_story(db,story):   # Save story details in db
    await db.execute("INSERT OR REPLACE INTO stories (id,title,url) VALUES(?,?,?)",(story["id"],story.get("title",""),story.get("url","")))
    print(f"Stored story: {story.get('title','No Title')}")
    await db.commit()

async def fetch_story(session,story_id): # Fetch story details with rate limit using semaphore
    async with session.get(f"{BASE_URL}/item/{story_id}.json") as response:
        return await response.json()
        
async def fetch_limited_story(session,story_id,semaphore): # Fetch story details with rate limit using semaphore
    async with semaphore:
        story = await fetch_story(session,story_id)
        if story is None:
            print(f"Failed to fetch story with id: {story_id}")
        return story
        
async def main():
    async with aiosqlite.connect("hacker_stories.db") as db:
        async with aiohttp.ClientSession() as session:
            story_ids = await fetch_top_stories(session)
        
            print(len(story_ids))    

            semaphore = asyncio.Semaphore(5) # Limit to 5 concurrent requests
            tasks = []

            for story_id in story_ids[:20]:
                tasks.append(fetch_limited_story(session, story_id,semaphore))

            stories = await asyncio.gather(*tasks)  # Concurrently fetch story details

        for story in stories:
            if story: 
                await store_story(db,story)
        await db.commit()        


if __name__ == "__main__":
    # asyncio.run(init_db())
    asyncio.run(main())

