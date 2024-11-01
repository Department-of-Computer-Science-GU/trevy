import asyncio
import os
import aiohttp
from desktop_notifier import DesktopNotifier
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
# city name whose weather update is retrieved 
CITY = "Gulu"

async def main():
    notifier = DesktopNotifier()
    if not API_KEY:
        print("Error: OPENWEATHER_API_KEY not found in .env file.")
        return

    async with aiohttp.ClientSession() as session:
        try:
            weather_data = await get_weather(session, CITY, API_KEY)
            if weather_data:
                title = f"Weather in {weather_data['name']}"
                message = f"{weather_data['weather'][0]['description']}, {weather_data['main']['temp']}°C"
                await notifier.send(title=title, message=message)
        except aiohttp.ClientError as e:
            print(f"Network error: {e}")
        except KeyError as e:
            print(f"KeyError in weather data: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()

async def get_weather(session, city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"

    try:
        async with session.get(complete_url) as response:
            response.raise_for_status()
            data = await response.json()
            print(f"Raw JSON response:\n{data}")
            return data
    except aiohttp.ClientError as e:
        print(f"Network error in get_weather: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred in get_weather: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())