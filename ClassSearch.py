import pandas as pd #Im a data science student what were you expecting I need pandas
import csv
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions as EC

classNum = 301 #Class Num
subjectName = "DAT" #Class Subject
termNum = 2237 #Fall 2023 term num

options = Options()
options.headless = True #Hide the Gui of the browser

def main(classNum, subjectName, termNum):
    driverChrome = webdriver.Chrome('/Users/keval/Downloads/chromedriver_mac64/chromedriver')
    wait = WebDriverWait(driverChrome, 10) #Wait for up to 10 seconds
    driverChrome.get(f"https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr={classNum}&honors=F&promod=F&searchType=all&subject={subjectName}&term={termNum}")
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div")))
    text = (element.text)
    driverChrome.close()
    return text

def csvWriter(text):
    rows = [text.split('\n')[i:i+12] for i in range(0, len(text.split('\n')), 12)]
    print(rows)
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i, row in enumerate(rows):
            if 'Add' in row:
                writer.writerow(row[:row.index('Add')+1])
                writer.writerow(row[row.index('Add')+1:])
            else:
                writer.writerow(row)

text = main(classNum, subjectName, termNum)
# csvWriter(text)
a = text.split('\n')
print(a)
finallist = []
for i in range(0,len(a)):
    if a[i] == (subjectName + " " + str(classNum)):
        l = []
        try:
            for j in range(0,11):
                if (a[i+j].strip(' ') == 'ASU Online') or (a[i+j].strip(' ') == 'Internet - Hybrid'):
                    l.append(a[i+j])
                    l.append(a[i+j+1])
                    l.append(a[i+j+2])
                    l.append(a[i+j+3])
                    break
                else:
                    l.append(a[i+j])
        except:
            continue
        finallist.append(l)
    else:
        continue
print(finallist)

AvailabilityList = []
for i in finallist:
    l1 = []
    Availability = (i[-1])
    s = Availability.split(" ")
    l1.append(i[0])
    l1.append(i[2])
    if(int(s[0]) > 0):
        ans = "Available"
    else:
        ans = "Not Available"
    l1.append(ans)
    l1.append(i[-1])
    AvailabilityList.append(l1)
for i in AvailabilityList:
    print(i)