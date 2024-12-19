import time
import polars as pl
from playwright.sync_api import Page, ElementHandle, BrowserContext

def save_pokemon_data(context: BrowserContext, page: Page, pokemon_url: str, pokemon_name: str) -> None:

    page2 = context.new_page()
    page2.goto(pokemon_url)

    pokemon_image = page2.query_selector('table a[class="image"]').query_selector("img").get_attribute("src")
    print(pokemon_image)

    pokemon_types = []
    types = page2.query_selector('td.roundy[colspan="2"]').query_selector("table[style*='margin']").query_selector_all('td')

    for type in types:
        pokemon_types.append(type.query_selector('a span b').inner_text())
    print(pokemon_types)
    print()

    time.sleep(2)
    page2.close()




