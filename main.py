import re
import aiohttp
import asyncio
import json
import logging
from math import ceil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "https://api.buff.market/api/market/goods/info?game=csgo&goods_id="
TOTAL_GOODS_IDS = 28762
BATCH_SIZE = 400 
RATE_LIMIT_DELAY = 1  


async def fetch_skin_data(session, goods_id):
    """Asynchronously fetches data for a single goods_id."""
    url = f"{API_URL}{goods_id}"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if 'data' in data and 'name' in data['data'] and 'id' in data['data']:
                    return data
                else:
                    logging.warning(f"Response for goods_id {goods_id} does not contain 'data' key.")
                    return None
            else:
                logging.warning(f"Failed to retrieve data for goods_id {goods_id}, status: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error fetching data for goods_id {goods_id}: {e}")
        return None


async def fetch_batch(session, batch):
    """Fetches a batch of goods_id data."""
    tasks = [fetch_skin_data(session, goods_id) for goods_id in batch]
    return await asyncio.gather(*tasks)


def remove_unicode_sequences(text):
    """Removes Unicode characters and escape sequences from the text and trims any extra spaces."""
    text = re.sub(r'\\u[0-9A-Fa-f]{4}', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text.strip()


async def main():
    """Main function for fetching skin data."""
    async with aiohttp.ClientSession() as session:
        name_to_goods_id = {}
        all_skin_responses = []
        for i in range(1, TOTAL_GOODS_IDS, BATCH_SIZE):
            batch = range(i, min(i + BATCH_SIZE, TOTAL_GOODS_IDS))
            responses = await fetch_batch(session, batch)
            for resp in responses:
                if resp is not None:
                    skin_name = remove_unicode_sequences(resp["data"]["name"])
                    goods_id = resp["data"]["id"]
                    name_to_goods_id[skin_name] = goods_id
                    all_skin_responses.append(resp)
            logging.info(f"Completed batch {i // BATCH_SIZE + 1}/{ceil(TOTAL_GOODS_IDS / BATCH_SIZE)}")
            
            await asyncio.sleep(RATE_LIMIT_DELAY)

        with open("name_to_goods_id.json", "w") as mapping_file:
            json.dump(name_to_goods_id, mapping_file, indent=2)

        with open("all_skin_responses.json", "w") as responses_file:
            json.dump(all_skin_responses, responses_file, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
