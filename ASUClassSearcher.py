import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions as EC

classNum = 301 #Class Num
subjectName = "DAT" #Class Subject
termNum = 2237 #Fall 2023 term num
classNumber = 88817

options = Options()
options.headless = True #Hide the Gui of the browser

def getClassesFromPage(classNum, subjectName, termNum):
    driverChrome = webdriver.Chrome("/snap/bin/chromium.chromedriver")
    wait = WebDriverWait(driverChrome, 10) #Wait for up to 10 seconds

    driverChrome.get(f"https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr={classNum}&honors=F&promod=F&searchType=all&subject={subjectName}&term={termNum}")
    #Getting the site for the class we want
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div")))
    text = (element.text)
    driverChrome.close()
    return text

def classNumberSearcher(classNumber, termNum):
    url = (f"https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&keywords={classNumber}&promod=F&searchType=all&term={termNum}")
    driverChrome = webdriver.Chrome("/snap/bin/chromium.chromedriver")
    wait = WebDriverWait(driverChrome, 10) #Wait for up to 10 seconds
    driverChrome.get(url)
    #Getting the site for the class we want
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div")))
    text = (element.text)
    driverChrome.close()
    return text

def csvWriter(text):
    #Split the text into a list of strings
    lines = text.split('\n')

    #Create an empty list to store the extracted data
    class_data = []

    #Iterate through the lines and extract data for the specified subject and class number
    for i in range(0, len(lines)):
        if lines[i] == (subjectName + " " + str(classNum)):
            data = []
            try:
                for j in range(0, 11):
                    if (lines[i+j].strip(' ') == 'ASU Online') or (lines[i+j].strip(' ') == 'Internet - Hybrid'):
                        data.append(lines[i+j])
                        data.append(lines[i+j+1])
                        data.append(lines[i+j+2])
                        data.append(lines[i+j+3])
                        break
                    else:
                        data.append(lines[i+j])
            except:
                continue
            class_data.append(data)
        else:
            continue

    columns = ['Class', 'Class Number', 'Availability','Seats']
    availability_list = [] #Create a list to store availability data
    for data in class_data: #Iterate through each extracted class and check if seats are available
        class_info = [[]] # Initialize an empty nested list
        availability = (data[-1])
        s = availability.split(" ")
        class_info[0].append(data[0]) #Append each element to the nested list
        class_info[0].append(data[2])
        if int(s[0]) > 0:
            availability_status = "Available"
        else:
            availability_status = "Not Available"
        class_info[0].append(availability_status)
        class_info[0].append(data[-1])
        availability_list.append(class_info[0])
    with open('output.csv', 'w') as f:
        for class_info in availability_list:
            df = pd.DataFrame([class_info], columns=columns)
            df.to_csv(f, header=f.tell()==0, index=False)
    


# text = getClassesFromPage(classNum, subjectName, termNum)
text = classNumberSearcher(classNumber ,termNum)
csvWriter(text)

