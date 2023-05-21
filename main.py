import postgesql
import aiohttp
import asyncio


# Define async function that fetches JSON from a desired URL
async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_text = await response.json()
            return json_text


async def main(url):
    json_text = await fetch_json(url)
    return json_text


url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500"
data = asyncio.run(main(url))

postgesql.create_table()
print("Inserting into database started! Please, wait a second.")
id = 1

if '_embedded' in data:
    items = data['_embedded']['estates']
    for item in items:
        if 'name' in item:
            name = str(item['name'])
            images = item['_links']['images']
            img_list = [item['href'] for item in images]
            postgesql.bulk_insert([(id, name, img_list)])
            id = id + 1


else:
    print("No 'items' found in the JSON data.")

print("Inserting into database ended!")
