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
    driverChrome = webdriver.Chrome("/snap/bin/chromium.chromedriver")
    wait = WebDriverWait(driverChrome, 10) #Wait for up to 10 seconds

    driverChrome.get(f"https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr={classNum}&honors=F&promod=F&searchType=all&subject={subjectName}&term={termNum}")
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div")))
    text = (element.text)
    driverChrome.close()
    return text

def csv_writer(text):
    rows = [text.split('\n')[i:i+12] for i in range(0, len(text.split('\n')), 12)]
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i, row in enumerate(rows):
            if 'Add' in row:
                writer.writerow(row[:row.index('Add')+1])
                writer.writerow(row[row.index('Add')+1:])
            else:
                writer.writerow(row)
            

text = main(classNum, subjectName, termNum)
textSplit = text.split('\n')
print(textSplit)