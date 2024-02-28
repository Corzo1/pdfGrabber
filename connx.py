import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os

empNum = input("employee Number")
empPW = input("employee Password")
download_directory = r"D:\PROGRAMMING\python programs\eb games\PDFS"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": r"D:\PROGRAMMING\python programs\eb games\PDFS",  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,  # It will not show PDF directly in chrome
    },
)


def wait_for_file(text):
    old_path = os.path.join(download_directory, "frmPayAdvicesExDetail.pdf")
    new_filename = f"{text}.pdf"
    new_path = os.path.join(download_directory, new_filename)

    timeout = 30  # Maximum time to wait for the file to download (in seconds)
    interval = 0.1  # Interval to check for the file (in seconds)

    elapsed_time = 0
    while not os.path.exists(old_path):
        time.sleep(interval)
        elapsed_time += interval
        if elapsed_time > timeout:
            raise TimeoutError("Timeout waiting for the file to download.")

    os.rename(old_path, new_path)


def reverse_text(normal_text):
    parts = normal_text.split(".")
    reversed_text = ".".join(reversed(parts))
    return reversed_text


driver = webdriver.Chrome(options=chrome_options)

driver.get("https://connx.ebgames.com.au/frmLogin.aspx")


username = driver.find_element(By.ID, "txtUserName")
username.send_keys(empNum)
password = driver.find_element(By.ID, "txtPassword")
password.send_keys(empPW)
password.send_keys(Keys.RETURN)

new_url = "https://connx.ebgames.com.au/frmPayAdvicesEx.aspx"
driver.get(new_url)
table_element = driver.find_element(
    By.XPATH, '//*[@id="ctl00_cphMainContent_rgGrid_ctl00"]/tbody'
)
rows = table_element.find_elements(By.XPATH, ".//tr")

for row in rows:
    link_element = row.find_element(By.XPATH, ".//td/a")
    link_element.click()
    link = link_element.get_attribute("href")

    span_element = row.find_element(By.XPATH, ".//td/a/span")
    text = span_element.text
    new_text = text.replace("/", ".")
    new_text = reverse_text(new_text)
    wait_for_file(new_text)

    print(f"Link: {link}")
    print(f"Text: {text}")
    print("------")


driver.quit()
