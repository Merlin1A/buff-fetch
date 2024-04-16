# CSGO Skin Data Fetcher

### Overview
The CSGO Skin Data Fetcher is an asynchronous Python script that collects CS:GO skin data in batches, handles rate limits, and outputs JSON files for further analysis.

### Features
- Asynchronous Data Fetching: Uses aiohttp for non-blocking HTTP requests to rapidly fetch skin data.
- Batch Processing: Manages API calls in predefined sizes with built-in delays to comply with API rate limits.
- JSON Output: Generates two JSON files, one mapping skin names to their IDs and another with all API responses.

### Output Files
- name_to_goods_id.json: Maps cleaned skin names to their respective goods IDs.
- all_skin_responses.json: Stores all API responses for further processing.

### Configuration
- API_URL: API endpoint for skin data.
- TOTAL_GOODS_IDS: Total number of skin IDs to fetch.
- BATCH_SIZE: Number of IDs per batch.
- RATE_LIMIT_DELAY: Seconds to wait between batches to respect rate limits.

### Requirements
- Python 3.7+
- aiohttp
- asyncio


### License
Distributed under the MIT License. See LICENSE for details.
