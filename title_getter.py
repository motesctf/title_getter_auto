import asyncio
import time
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/96.0.4664.93 Safari/537.36"
}
RESULTS = []
DOMAINS_FILE = "data/test.txt"  # файл с доменами
OUT_FILE = "output.txt"  # файл вывода


def check_http(url: str):
    if url.split(':')[0] in ['http', 'https']:
        return url
    return "http://" + url


async def get_title(url: str, content: str):
    html = BeautifulSoup(content, 'html.parser')
    title = None
    try:
        title = html.title.text
    except:
        pass
    out = f"url: {url}\ntitle: {title}"
    print(out)
    RESULTS.append(out)


async def requester(domain: str):
    url = check_http(domain)
    async with aiohttp.ClientSession(headers=HEADERS, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        try:
            async with session.get(url=url, timeout=1000) as response:
                content = await response.text()
                return await get_title(response.url, content)
        except Exception as error:
            print(error)
            pass
    await asyncio.sleep(1)


async def main(domains: list):
    tasks = []
    for domain in domains:
        tasks.append(requester(domain))
    await asyncio.gather(*tasks)

    async with aiofiles.open(OUT_FILE, 'w') as title_file:
        for result in RESULTS:
            await title_file.write(result + "\n\n")


if __name__ == '__main__':
    with open(DOMAINS_FILE) as domains_file:
        raw_domains = domains_file.readlines()
        domains = list(set(domain.strip().replace('value', '').replace('"', '').strip() for domain in raw_domains))

    asyncio.run(main(domains))
