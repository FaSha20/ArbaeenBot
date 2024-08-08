from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
madahis = []

arab_madahs = {
    "باسم کربلایی": "https://navaapp.com/filter?persone_id=5f72e1c1cdb65662225678a3&page=1",
    "حیدر البیاتی": "https://navaapp.com/filter?persone_id=6486cfc9ae350cb7de0f0081&page=1",
    "الحسین فیصل": "https://navaapp.com/filter?persone_id=5f7300df5e8a500b51107529&page=1",
    "نزار القطری": "https://navaapp.com/filter?persone_id=62b992cb7a2d6e01d502cf24&page=1",
    "حسین خیرالدین": "https://navaapp.com/filter?persone_id=64f287a6f37a50a367092909&page=1",
    "محمد الجنامی" : "https://navaapp.com/filter?persone_id=64ebeef58f967e176a082235&page=1"
}

for madah_name, url in arab_madahs.items():
    driver.get(url)

    # Click on the filter button
    filter_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[1]"))
    )
    filter_button.click()
    print("Filter button clicked")

    # Click on the favorite filter
    favorite_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/a[3]"))
    )
    favorite_filter.click()
    print("Favorite filter clicked")

    # Wait for the cards to be visible and then get them
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "favorite-card"))
    )
    time.sleep(10)  # Wait a bit to ensure the content is fully loaded

    cards = driver.find_elements(By.CLASS_NAME, "favorite-card")

    if cards:
        print("Cards found:", len(cards))
        print("First card title:", cards[0].find_element(By.TAG_NAME, 'strong').text)
    else:
        print("No cards found")

    for card in cards:
        metadata = {'artist': madah_name}
        try:
            metadata['name'] = card.find_element(By.TAG_NAME, 'strong').text
        except:
            continue
        try:
            otherdata = card.find_element(By.TAG_NAME, 'small').text
        except:
            continue
        metadata['type'], metadata['subject'], metadata['year'] = (otherdata.split(',') + [""] * 3)[:3]

        

        play_sound_btn = WebDriverWait(card, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-play-sound'))
        )
        driver.execute_script("arguments[0].click();", play_sound_btn)


        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "nava-wrapper"))
        )
        time.sleep(3)  # Wait a bit to ensure the content is fully loaded

        try:
            metadata['download_link'] = driver.find_element(By.TAG_NAME, 'source').get_attribute('src')
        except:
            metadata['download_link'] = ""

        print(metadata['name'],metadata['download_link'])

        madahis.append(metadata)




with open('arabic_mahadis1.json', 'w', encoding='utf-8') as json_file:
    json.dump(madahis, json_file, ensure_ascii=False, indent=4)


driver.close()
