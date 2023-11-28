import time
from bs4 import BeautifulSoup as bs
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from modules.constants import SII_UF_URL, SII_DOLLAR_URL, YAHOO_FINANCE_URL


def get_indicators():
    indicators_file = open("indicators.txt", "w+", encoding="utf-8")
    options = Options()
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    options.add_argument(f"user-agent={random_user_agent}")
    options.add_argument("--headless")
    options.add_argument("--window-size=0,0")
    driver = webdriver.Chrome(options=options)

    currency_values = []

    dollar_values = get_values_from_sii(
        driver, SII_DOLLAR_URL, indicators_file)
    uf_values = get_values_from_sii(driver, SII_UF_URL, indicators_file)
    driver.quit()
    indicators_file.close()

    currency_values.append(dollar_values)
    currency_values.append(uf_values)

    return currency_values


# Obtener valor histórico mensual desde el SII (dólar y UF)
def get_values_from_sii(driver, url, file):
    driver.get(url)
    soup = bs(driver.page_source.encode("utf-8"), "html.parser")
    dom = etree.HTML(str(soup))
    values = {}

    for i in range(1, 31):
        pattern = f"^\s*{i}\s*$"
        namespace = {"re": "http://exslt.org/regular-expressions"}
        value = dom.xpath(
            f"//div[@id='mes_noviembre']/div/table/tbody/tr/th/strong[re:match(text(), '{pattern}')]/../following-sibling::td", namespaces=namespace)[0]
        if value.text is not None:
            values[f"Día {i}"] = f"${value.text} pesos chilenos"

    for value in values:
        file.write(f"{value}: {values[value]}\n")

    return values


def get_info_from_news(driver: webdriver.Chrome):
    try:
        span = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Noticias')]")))
        span.click()

        most_recent = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//u")))
        most_recent.click()

        title = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'caas-title-wrapper')]/h1")))

        paragraphs = driver.find_elements(
            By.XPATH, "//div[@class='caas-body']/p")

        info = title.text + "".join(p.text for p in paragraphs)

        return info
    except:
        print("Error al leer la página de noticias.")
        return None


def get_company_stocks(company_name):
    options = Options()
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    options.add_argument(f"user-agent={random_user_agent}")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    driver.get(YAHOO_FINANCE_URL)

    info = {}

    try:
        # Si carga la página de cookies, las rechaza.
        reject_cookies_button = driver.find_element(
            By.XPATH, "//*[@id='consent-page']/div/div/div/form/div[2]/div[2]/button[2]")
        if reject_cookies_button is not None:
            reject_cookies_button.click()

        search_bar = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='yfin-usr-qry']")))
        search_bar.click()
        search_bar.send_keys(company_name)
        time.sleep(2)
        first_item = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//ul[contains(@class, 'modules_list__L4Xjs')]/li")))
        first_item.click()
        stock_value = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='quote-header-info']/div[3]/div[1]/div[1]/fin-streamer")))
        previous_value = driver.find_element(
            By.XPATH, "//*[@id='quote-header-info']/div[3]/div[1]/div[1]/fin-streamer[2]/span")
        variation = driver.find_element(
            By.XPATH, "//*[@id='quote-header-info']/div[3]/div[1]/div[1]/fin-streamer[3]/span")
        range_52_weeks = driver.find_element(
            By.XPATH, "//table[contains(@class,'W(100%)')][1]/tbody/tr[5]/td[2]")

        info["Valor"] = f"{stock_value.text} dólares"
        info["Cierre anterior"] = f"{previous_value.text} dólares"
        info["Variación"] = variation.text[1:-1]
        info["Rango de 52 semanas"] = range_52_weeks.text

        driver.find_element(
            By.XPATH, "//*[@id='quote-nav']/ul/li[7]/a").click()

        benefits_current_year = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//table[contains(@class, 'W(100%)') and contains(@class, 'M(0)') and contains(@class, 'Bdc($seperatorColor)') and contains(@class, 'Mb(25px)')]/tbody/tr[2]/td[4]")))
        benefits_next_year = driver.find_element(
            By.XPATH, "//table[contains(@class, 'W(100%)') and contains(@class, 'M(0)') and contains(@class, 'Bdc($seperatorColor)') and contains(@class, 'Mb(25px)')]/tbody/tr[2]/td[5]")

        info["Estimación de beneficios este año"] = benefits_current_year.text
        info["Estimación de beneficios próximo año"] = benefits_next_year.text

        driver.find_element(
            By.XPATH, "//span[contains(text(), 'Resumen')]").click()

        # Buscar noticias relevantes.
        news = get_info_from_news(driver)

        if news is not None:
            info['Noticias recientes'] = news

    except:
        print("Ha ocurrido un error al recabar información de las noticias recientes.")
        return None

    finally:
        driver.quit()
        return info
