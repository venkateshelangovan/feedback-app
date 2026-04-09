import httpx

url = "http://localhost:8000/submit-feedback"
payload = {
    "name": "Antigravity Debug",
    "email": "debug@example.com",
    "rating": 5,
    "experience": "Testing Telegram 400 Bad Request error detail."
}

async def run_debug():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_debug())
