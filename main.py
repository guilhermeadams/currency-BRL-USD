from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from datetime import datetime, timedelta
import pytz

app = FastAPI()

# Serve the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://economia.awesomeapi.com.br"
UTC_MINUS_3 = pytz.timezone("America/Sao_Paulo")


@app.get("/")
async def read_index():
    """Serve the index.html file at the root."""
    return FileResponse("static/index.html")


@app.get("/api/latest")
async def get_latest_rate():
    """Fetches the latest BRL to USD exchange rate."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/json/last/USD-BRL")
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Failed to fetch latest rate"
            )
        data = response.json()["USDBRL"]

        # Convert date to DD/MM/YYYY format and time to 24-hour format UTC-3
        create_date = datetime.strptime(
            data["create_date"], "%Y-%m-%d %H:%M:%S"
        ).astimezone(UTC_MINUS_3)
        data["create_date"] = create_date.strftime("%d/%m/%Y %H:%M:%S")
        return data


@app.get("/api/historical")
async def get_historical_rates(
    start_date: str = None, end_date: str = None, days: int = None
):
    """
    Fetches historical BRL to USD exchange rates.

    Parameters:
    - start_date: Start date in YYYYMMDD format.
    - end_date: End date in YYYYMMDD format.
    - days: Number of days from the current date to fetch data.

    Either start_date and end_date or days must be provided.
    """
    async with httpx.AsyncClient() as client:
        if start_date and end_date:
            url = f"{BASE_URL}/USD-BRL/?start_date={start_date}&end_date={end_date}"
        elif days:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
            url = f"{BASE_URL}/USD-BRL/?start_date={start_date}&end_date={end_date}"
        else:
            raise HTTPException(
                status_code=400,
                detail="Either date range or number of days must be provided",
            )

        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch historical rates",
            )

        data = response.json()

        # Convert timestamps to DD/MM/YYYY format in UTC-3
        for item in data:
            timestamp = datetime.utcfromtimestamp(int(item["timestamp"])).replace(
                tzinfo=pytz.utc
            )
            item["date"] = timestamp.astimezone(UTC_MINUS_3).strftime(
                "%d/%m/%Y %H:%M:%S"
            )

        return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
