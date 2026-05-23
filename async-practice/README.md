# Async Practice

This repository contains simple Python examples demonstrating backend concepts using asynchronous programming.

## Files

- `main.py` - complete async pipeline that fetches Hacker News top stories and stores them in a local SQLite database.
- `hacker-stories.py` - async network examples showing sequential fetch, concurrent fetch, rate limiting, and timeout handling.

## What this code does

`main.py`:
- initializes a local SQLite database using `aiosqlite`
- fetches top story IDs from the Hacker News API using `aiohttp`
- uses `asyncio.Semaphore` to limit concurrent requests to the Hacker News details endpoint
- concurrently fetches the first 20 story details with `asyncio.gather`
- stores each story `id`, `title`, and `url` into the `stories` table

`hacker-stories.py`:
- fetches multiple web pages sequentially and prints content lengths
- fetches the same URLs concurrently with `asyncio.gather`
- demonstrates rate limiting using `asyncio.Semaphore`
- shows how to cancel or guard against slow operations with `asyncio.wait_for`

## Backend concepts used

### Asynchronous programming
- `async def` defines coroutine functions
- `await` pauses a coroutine until an asynchronous operation completes
- `asyncio.run()` starts the event loop and runs the main coroutine
- `asyncio.gather()` runs multiple coroutines concurrently and waits for all results

### HTTP client with `aiohttp`
- `aiohttp.ClientSession()` manages HTTP connections asynchronously
- `session.get(url)` performs an asynchronous HTTP request
- reading response data with `await response.text()` or `await response.json()` avoids blocking the event loop

### Rate limiting / concurrency control
- `asyncio.Semaphore(n)` restricts the number of coroutines that can run a critical section simultaneously
- semaphore is used around HTTP fetches to avoid sending too many requests at once

### Timeout handling
- `asyncio.wait_for(coro, timeout=...)` enforces a maximum wait time for a coroutine
- this prevents the program from hanging if a network request or slow task never returns

### SQLite persistence with `aiosqlite`
- `aiosqlite.connect()` opens a database connection in async mode
- `CREATE TABLE IF NOT EXISTS` creates the storage table once
- `await db.execute(...)` and `await db.commit()` persist SQL changes without blocking the event loop

### Complete async backend pipeline
- `main.py` shows a real backend-style flow:
  1. initialize database
  2. fetch data from remote API
  3. process results concurrently
  4. store data locally

## Requirements

- Python 3.8+
- `aiohttp`
- `aiosqlite`

Install dependencies:

```bash
pip install aiohttp aiosqlite
```

## Run the examples

To run the Hacker News pipeline:

```bash
python main.py
```

To run the network fetch demo:

```bash
python hacker-stories.py
```

## Notes

- `main.py` stores results in `hacker_stories.db`.
- `hacker-stories.py` uses real external URLs, so network connectivity is required.
- The sample code is designed for learning async backend patterns, not production deployment.
