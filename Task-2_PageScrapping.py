# python packages
import time
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

# actual scrapping script
def pageScrapper(companyDetails):
  companyReport = {}

  # none overlapping attributes transferred to new object
  companyReport["rank"] = companyDetails["rank"]
  companyReport["name"] = companyDetails["name"]
  companyReport["link"] = companyDetails["link"]
  companyReport["revenue"] = companyDetails["revenue"]

  # opens link in new tab
  driver.get(companyDetails["link"])

  # wait for the subscribe to load for 40 second
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "listuser-header__name")))
  print("wait over for " + companyReport["rank"])
  companyStats = driver.find_elements(By.CSS_SELECTOR, "div.listuser-block__item:not([class*=' '])")

  for data in companyStats:
    keyName = data.find_element(By.CLASS_NAME, "profile-stats__title").text
    companyReport[keyName] = data.find_element(By.CLASS_NAME, "profile-stats__text").text
  
  try:
    moreListButton = driver.find_element(By.CLASS_NAME, "toggle-lists-button")
    moreListButton.click()
  except:
    pass
  finally:
    forbesListData = []
    forbesList = driver.find_element(By.CLASS_NAME, "ranking")
    achievements = forbesList.find_elements(By.CLASS_NAME, "listuser-block__item")
    
    for achievement in achievements:
      achievementData = {}
      achievementData["rank"] = achievement.find_element(By.CLASS_NAME, "listuser-item__list--rank").text
      achievementData["achievement"] = achievement.find_element(By.CLASS_NAME, "listuser-item__list--title").text
      forbesListData.append(achievementData)

    companyReport["achievements"] = forbesListData

  financialSummaryListData = []
  financialSummary = driver.find_element(By.CLASS_NAME, "financial-summary")
  yearDropDown = driver.find_elements(By.CLASS_NAME, "listuser-year-dropdown__option")

  dropDownButton = driver.find_element(By.CLASS_NAME, "listuser-year__button")

  for year in yearDropDown:
    dropDownButton.click()
    time.sleep(1)
    year.click()
    
    yearData = {}
    
    nonHiddenData = financialSummary.find_element(By.CSS_SELECTOR, "div.listuser-financial-data:not([class*=' '])")
    yearData["year"] = year.text
    yearData["revenue"] = nonHiddenData.find_element(By.CLASS_NAME, "listuser-financial-item__value").text
    financialSummaryListData.append(yearData)
  
  companyReport["financialSummary"] = financialSummaryListData

  return companyReport

# getting top 20 company list from previous scrapped data
def getTop20List():
  # initiating data array
  companyList = []

  # reading file
  with open("list.txt", "r") as file:
    data = file.read()

  # objects seperation
  companyDetailsObjs = data.split("\n")

  # converting to actual objects and storing in new list
  for companyDetail in companyDetailsObjs:
    # mitigate empty string
    if companyDetail:
      companyList.append(json.loads(companyDetail))

  # trimming down the list and returning it
  return companyList[:20]

# Opening the website
driver.get('https://www.forbes.com/lists/largest-private-companies/?sh=2f69ff46bac4')

# Waiting 30s for the website to load by checking if particular element is rendered
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "table-row")))

top20 = getTop20List()

results = []

for company in top20:
  results.append(pageScrapper(company))

with open("detailedReport.txt", "w") as file:
  for obj in results:
    file.write(json.dumps(obj) + "\n")

driver.close()
driver.quit()