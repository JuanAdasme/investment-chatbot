from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

URL = "http://corocenit.cl/quienes-somos/"


def get_indicators():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    with Chrome(options=chrome_options) as browser:
        browser.get(URL)
        html = browser.page_source
    soup = bs(html, "html.parser")
    print(soup)

    h2_list = soup.find_all("h2")

    for h2 in h2_list:
        print(h2.get_text())

    """ indicators_spans = soup.find(
        id="top-indicators").find_all("span", {"class": "ng-binding"})
    indicators = [span.get_text() for span in indicators_spans]
    return {"IPSA": indicators[0], "UF": indicators[1], "DÓLAR": indicators[2]} """
