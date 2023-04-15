import pandas as pd #Im a data science student what were you expecting I need pandas
import csv
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions as EC

classNum = 412 #Class Num
subjectName = "CSE" #Class Subject
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

def generate_availability_list(class_num, subject_name, term_num):
    # Get the input text data and split it into lines
    text = main(class_num, subject_name, term_num)
    lines = text.split('\n')

    # Find the lines containing the desired subject and class number
    class_header = subject_name + " " + str(class_num)
    class_lines = [line for line in lines if line.strip(' ') == class_header]

    # Extract availability information from each class line
    availability_list = []
    for class_line in class_lines:
        class_info = []
        try:
            # Look for availability information in the next 11 lines
            for i in range(11):
                line = lines[lines.index(class_line) + i]
                if line.strip(' ') == 'ASU Online' or line.strip(' ') == 'Internet - Hybrid':
                    # If availability info is found, add it to the class info list
                    class_info.extend([line, lines[lines.index(line) + 1], lines[lines.index(line) + 2], lines[lines.index(line) + 3]])
                    break
                else:
                    class_info.append(line)
        except:
            continue
        # If availability info was found, add it to the availability list
        if class_info:
            availability = class_info[-1]
            availability_list.append([class_info[0], class_info[2], "Available" if int(availability.split()[0]) > 0 else "Not Available", availability])

    # Print the availability list
    for availability_info in availability_list:
        print(availability_info)

generate_availability_list(classNum, subjectName, termNum)