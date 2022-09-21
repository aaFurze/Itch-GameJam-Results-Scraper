from bs4 import BeautifulSoup
import httpx


async def get_jam_submissions_html(base_url: str, max_pages: int = 100):
    webpages_html = []
    running = True
    page_num = 1

    async with httpx.AsyncClient() as client:
        while page_num <= max_pages and running:
            addon = f"?page={page_num}"
            html = await get_webpage_data(client, f"{base_url}{addon}")

            if html:
                webpages_html.append(html)
                page_num += 1
                continue
            else:
                running = False

    return webpages_html


async def get_webpage_data(client: httpx.AsyncClient, url: str):
    result = await client.get(url)
    if result.status_code != 200:
        return None
    return BeautifulSoup(result.text, "lxml")
