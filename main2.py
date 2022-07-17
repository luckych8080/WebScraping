from xml.dom.expatbuilder import DOCUMENT_NODE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://web2.co.merced.ca.us/RecorderWorksInternet/')

# print(driver.title)

# Search button click
try:
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "MainContent_Manager1_linkSearch"))
    )
    search.click()
except:
    driver.quit()

# search by Document button
try:
    searchByDoc = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "MainContent_SearchParent1_StandartSearchMenu1_SearchByDocType"))
    )
    searchByDoc.click()
except:
    driver.quit()

# Enter StartDate
startDate = driver.find_element_by_id("MainContent_SearchParent1_SearchByDocType1_StartEndDate1_fromDate")
startDate.clear()
startDate.send_keys("01/04/2012")

# Enter End date
endDate = driver.find_element_by_id("MainContent_SearchParent1_SearchByDocType1_StartEndDate1_toDate")
endDate.clear()
endDate.send_keys("5/3/2021")


# Check box DEED
Deed = driver.find_element_by_id("MainContent_SearchParent1_SearchByDocType1_DocumentTypes1_chType180")
Deed.click()

# Click Search Button
try:
    SearchButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "MainContent_SearchParent1_SearchByDocType1_btnSearch"))
    )
    SearchButton.click()
except:
    driver.quit()




try:
    Document = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl02_docLinkTD"))
    )
    Document.click()
except:
    print("document opening")
    driver.quit()



while(True):

    AllData = json.loads('{ }')
    try:
        DocNumber = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DocumentSpinner1_docNumber"))
        )
        x = {"Document Number": DocNumber.text}
        AllData.update(x)
        # print(DocNumber.text)
    except:
        print("document number")
        driver.quit()


    # APN
    try:
        APNData = driver.find_element_by_id("D").find_element_by_class_name("detailsData")
        x = {"APN": APNData.text}
        AllData.update(x)
    except:
        print(json.dumps(AllData))

    # GrantorsData
    GrantorsData = driver.find_element_by_id("Grantors").find_elements_by_tag_name("tr")
    GrantorsArr = []
    for e in GrantorsData:
        GrantorsArr.append(e.text)
    x = {"Grantors": GrantorsArr}
    AllData.update(x)


    # GranteesData
    GranteesData = driver.find_element_by_id("Grantees").find_elements_by_tag_name("tr")
    GranteesArr = []
    for e in GranteesData:
        GranteesArr.append(e.text)
    x = {"Grantees": GranteesArr}
    AllData.update(x)


    # Recording Date
    RecordingDate = driver.find_element_by_id("generalData").find_elements_by_class_name("detailsData")
    x = {"Number of Pages": RecordingDate[0].text, "Recording Date": RecordingDate[1].text}
    AllData.update(x)

    # reading and catching all data from file
    with open('Merced_Parcel[APN].json', 'r') as feedsjson:
        feeds = json.load(feedsjson)

    # appending to existing data then adding to file
    with open("Merced_Parcel[APN].json", "w") as outfile:
        feeds.append(AllData)
        json.dump(feeds, outfile, indent=4)

    # print(json.dumps(AllData))



    # Next page
    try:
        NextResult = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DocumentSpinner1_nextBtn"))
        )
        NextResult.click()
    except:
        driver.quit()


    time.sleep(2)




time.sleep(50)

driver.quit() 

