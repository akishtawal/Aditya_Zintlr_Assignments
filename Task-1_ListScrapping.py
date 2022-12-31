# python packages
import json

# selenium packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


options = Options()
# options.headless = True
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-session-crashed-bubble")
driver = webdriver.Chrome(options=options)

# Opening the website
driver.get('https://www.forbes.com/lists/largest-private-companies/?sh=2f69ff46bac4')

# Waiting 30s for the website to load by checking if particular element is rendered
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "table-row")))

# getting all the table rows
table_rows = driver.find_elements(By.CLASS_NAME, "table-row")

# initiating data array
companyList = []

button = driver.find_element(By.CLASS_NAME, "next-button")

while "background-color: rgb(220, 0, 0); opacity: 0.25;" not in button.get_attribute("style"):
  for row in table_rows:
    if "display: none;" not in row.get_attribute("style"):
      company_detail = {}
      company_detail["rank"] = row.find_element(By.CLASS_NAME, "rank").text
      company_detail["name"] = row.find_element(By.CLASS_NAME, "organizationName").text
      company_detail["state"] = row.find_element(By.CLASS_NAME, "state").text
      company_detail["industry"] = row.find_element(By.CLASS_NAME, "industries").text
      company_detail["revenue"] = row.find_element(By.CLASS_NAME, "revenue").text
      company_detail["employees"] = row.find_element(By.CLASS_NAME, "employees").text
      company_detail["link"] = row.get_attribute("href")
      print(company_detail["rank"])
      companyList.append(company_detail)
  
  button.click()

with open("list.txt", "w") as file:
  for obj in companyList:
    file.write(json.dumps(obj) + "\n")

driver.close()
driver.quit()