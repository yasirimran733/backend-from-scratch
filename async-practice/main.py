import asyncio
import time
import aiohttp

# Fetching 3 urls sequentially
async def fetch_sequentially(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
# one by one url fetching and printing the content length        
async def seq_call():
    urls =["https://www.github.com" , "https://www.google.com" , "https://www.facebook.com"]
    start = time.perf_counter()
    for url in urls:
        content =  await fetch_sequentially(url)
        print(f"Fetched {url} with content length: {len(content)}")
    end = time.perf_counter()
    print(f"Time taken to fetch sequentially: {end - start:.2f})    seconds")  


asyncio.run(seq_call())

# Fetching 3 urls concurrently
# need to create a task for each url and then gather the results together

async def fetch_concurrently(url,session):
    async with session.get(url) as response:
        return await response.text()

async def concurrent_call():
    urls =["https://www.github.com" , "https://www.google.com" , "https://www.facebook.com"]

    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        print("Fetching concurrently...")
        tasks = [fetch_concurrently(url,session) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, content in zip(urls, results):
            print(f"Fetched {url} with content length: {len(content)}")
    end = time.perf_counter()

    print(f"Time taken to fetch concurrently: {end - start:.2f})    seconds")          

asyncio.run(concurrent_call())

# Now using concept of rate limiting using semaphore to limit the number of concurrent requests

async def fetch_with_rate_limit(url,session,semaphore):
    async with semaphore:
        async with session.get(url) as response:
            return await response.text()
        
async def rate_limit_call():
    urls =["https://www.github.com" , "https://www.google.com" ] * 10 # 20 urls
    semaphore = asyncio.Semaphore(5) # limit to 5 concurrent requests 
    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        print("Fetching with rate limit...")
        tasks = [fetch_with_rate_limit(url,session,semaphore) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, content in zip(urls, results):
            print(f"Fetched {url} with content length: {len(content)}")
    end = time.perf_counter()

    print(f"Time taken to fetch with rate limit: {end - start:.2f})    seconds")  

asyncio.run(rate_limit_call())


# Now learn the concept of timeout to avoid waiting indefinitely for a response from a url

async def slow_process():
    print("Starting slow process...")
    await asyncio.sleep(5) # simulating a slow process that takes 5 seconds
    print("Slow process completed!")
    return "Slow process result"

async def timeout_call():
    try:
        result = await asyncio.wait_for(slow_process(),timeout=6) # set timeout to 3 seconds
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("The slow process timed out!")    

asyncio.run(timeout_call())


# Error hadling instantly , Timout takes time to catch error but if using 
