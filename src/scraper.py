from typing import List
from bs4 import BeautifulSoup
import httpx


async def get_jam_submissions_html(base_url: str, max_pages: int = 100) -> List[BeautifulSoup]:
    '''
    When provided a base_url, retrieves results pages until it runs out of pages or reaches the maximum number of pages
    specified by the max_pages parameter.
    Uses httpx library to enable asyncronous fetching of pages.
    Adds "?page={page_num}" to the end of base_url to retrieve the pages.
    '''
    if max_pages is None:
        max_pages = 100 
    webpages_html: List[BeautifulSoup] = []
    running = True
    page_num = 1

    async with httpx.AsyncClient() as client:
        while page_num <= max_pages and running:
            addon = f"?page={page_num}"
            html = await get_webpage_data(client, f"{base_url}{addon}")

            if html:
                webpages_html.append(html)
                print(f"Page {page_num} results retrieved.")
                page_num += 1
                continue
            else:
                running = False

    return webpages_html


async def get_webpage_data(client: httpx.AsyncClient, url: str) -> BeautifulSoup:
    '''
    Asynchronous function that retrieves a get request for the speicified page, and then returns a BeautifulSoup object of the 
    requests html if the status code returned is 200, else None.
    Requires a AsyncClient be provided from the httpx module.
    '''
    result = await client.get(url)
    if result.status_code != 200:
        return None
    return BeautifulSoup(result.text, "lxml")


def check_webpage_exists(url: str):
    if url.strip()[:5] != "https":
        return False
    result = ""
    try:
        result = httpx.get(url)
    except httpx.ConnectError:
        print("Invalid website address provided. Did you enter the url correctly?")
    if not result: return False
    if result.status_code == 200:
        return True
    return False
