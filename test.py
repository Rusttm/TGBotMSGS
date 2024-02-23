import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:

        pokemon_url = 'https://sermangroup.ru/upload/iblock/649/64935424bee727cd0add46fc588c1249.jpg'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])

asyncio.run(main())