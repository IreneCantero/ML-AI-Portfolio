import time
from playwright.sync_api import sync_playwright, Page, ElementHandle, BrowserContext
from save_pokemon_info import save_pokemon_data


def reject_cookies(page: Page) -> Page:

    page.get_by_role("button", name="Configuraciones").click()
    page.get_by_role("button", name="Rechazar todo").click()
    
    return page

def get_table_data(context: BrowserContext, page: Page, table: ElementHandle):

    base_url = "https://bulbapedia.bulbagarden.net"

    time.sleep(2)
    pokemon_list = table.query_selector_all("tr")

    # Avoid first element as it is the table header
    for pokemon in pokemon_list[1:7]:
        data = pokemon.query_selector('td a')
        pokemon_url = base_url + data.get_attribute('href')
        pokemon_name = data.get_attribute('title')
        print(pokemon_name)
        print(pokemon_url)

        save_pokemon_data(context=context, page=page, pokemon_url=pokemon_url, pokemon_name=pokemon_name)


def obtain_data(context: BrowserContext, page: Page, url: str) -> None:
    # Go to a website
    page.goto(url)

    # Reject Cookies
    page = reject_cookies(page=page)

    tables = page.query_selector_all(selector='table[class="roundy"]')
    table = tables[0]
    for table in tables[0:1]:
        get_table_data(context=context, page=page, table=table)

    time.sleep(5)



def init_browser() -> None:
    # Launching the browser and opening a page

    pokemons_url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser in non-headless mode (visible)
        context = browser.new_context()
        page = context.new_page()
        
        obtain_data(context=context, page=page, url=pokemons_url)

        # Close the browser
        browser.close()


## JUST FOR TESTING

init_browser()

"""
<a class="cmpboxbtn cmpboxbtncustom cmptxt_btn_settings" role="button" href="#" draggable="false">
    <span id="cmpbntcustomtxt">Configuraciones</span></a>
"""