import selenium
import time
import sys
import csv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

##########################################################

# A few lazy consts we're going to need later
nano_sleep = 0.5
micro_sleep = 1.5
small_sleep = 3
sleep = 5
big_sleep = 15

find_element = lambda driver, xpath: driver.find_element("xpath", xpath)
click_element = lambda driver, xpath: driver.find_element("xpath", xpath).click()
text_element = lambda driver, xpath, text: driver.find_element("xpath", xpath).send_keys(text)
file_element = lambda driver, xpath, filepath: driver.find_element("xpath", xpath).send_keys(filepath)
wait = lambda x: time.sleep(x)


##########################################################
# Load entries from csv
##########################################################

csv_file = ''
job_number = 1
raw_data = None

# Time to get a file:
if len(sys.argv) < 2:
    print("Please provide a path to a properly formatted csv file containing your timesheet data.")
    file_name = input()
else:
    file_name = sys.argv[1]

# Check if invalid
if not os.path.exists(file_name):
    raise ValueError("Cannot find file!")

# Read the file contents
with open(file_name, 'r', encoding='utf-8') as f:
    raw_data = f.readlines()

# Determine job number, default to 1
# NOTE This is indicative of the order not the actual job ID
if len(sys.argv) < 3:
    job_number = 1
else:
    job_number = sys.argv[2]

##########################################################
# Figure out which driver we're using
##########################################################

# I'm only testing this on Firefox myself
try:
    driver = webdriver.Firefox()
except:
    try:
        driver = webdriver.Chrome()
    except:
        print("No Driver found, please use a recent version of either Firefox or Chrome")
        exit()


##########################################################
# Login
##########################################################

initial_url = 'https://uosp.ascenderpay.com/uosp-wss/faces/landing/SAMLLanding.jspx'

driver.get(initial_url)
print("Please Login")
print("Once you have Logged in, Press Enter to Continue")
while input() != '':
    continue


##########################################################
# Get a new timesheet
##########################################################
# Switch to the academic timesheet frame
driver.switch_to.frame("P1_IFRAME")

# Access the academic time sheet from the main menu
# NOTE: You may need to change this to Professional Timesheet (may possibly break)
driver.find_element("xpath", '''//span[@title='Academic/Sessional Timesheet']''').click()
wait(micro_sleep)

# Switch to the popped up frame
driver.switch_to.default_content()
driver.switch_to.frame(2)
driver.switch_to.frame(1)

# Click Add new Timesheet
click_element(driver, "/html/body/p[2]/a")
wait(micro_sleep)

# Start Date
text_element(driver, '//*[@id="P_START_DATE"]', raw_data[0].split(',')[0])
text_element(driver, '//*[@id="P_CALENDAR_CODE"]', "CAL")
click_element(driver, '/html/body/p[3]')
wait(micro_sleep)

# Select Job
try:
    click_element(driver,
        f"/html/body/div/form/table/tbody/tr[{job_number}]/td[1]/input"
        )
    wait(micro_sleep)

    # Continue
    driver.find_element("name", "Z_ACTION").click()
    wait(small_sleep)

except:
    pass

input("If continue isn't pressed, please click yourself.")


##########################################################
# Fill in the timesheet
##########################################################

# Hack for some reason during testing it cannot find table
# entries if we do not reload the frame
driver.switch_to.default_content()
driver.switch_to.frame(2)
driver.switch_to.frame(1)

# Get the right number of rows
n_rows = len(raw_data)
if n_rows > 20:
    for _ in range(n_rows - 20):
        click_element(driver, "/html/body/form/p[3]/input[5]")
        wait(nano_sleep)

# Enter Data
for i, entry in enumerate(raw_data):
    wait(nano_sleep)
    entry = entry.split(',')

    # Date
    element = driver.find_element("xpath", f'''//*[@id="TSEntry"]/tr[{i + 1}]/td[4]''')
    field = element.find_element("xpath", './*[@id="P_WORK_DATE"]')
    field.send_keys(entry[0])

     # Hours
    element = driver.find_element("xpath",
    '/html/body/form/table/tbody/tr[{}]/td[6]'.format(i + 1))
    field = element.find_element("xpath", './*[@id="P_UNITS"]')
    field.send_keys(entry[1])

    # Paycode
    element = driver.find_element("xpath",
    '/html/body/form/table/tbody/tr[{}]/td[7]'.format(i + 1))
    field = element.find_element("xpath",'./*[@id="P_PAYCODE"]')
    field.send_keys(entry[2])

    if len(entry) > 3:
        # Analysis Code
        if len(entry[3]) > 0:
            try: # Because of pointless dialogue boxes
                element = driver.find_element("xpath",
                '/html/body/form/table/tbody/tr[{}]/td[10]'.format(i + 1))
                field = element.find_element("xpath",'./*[@id="P_GL_SUB_ACCOUNT"]')
                field.send_keys(entry[3])
            except:
                pass

    if len(entry) > 4:
        # Topic
        if len(entry[4]) > 0:
            try: # Because of pointless dialogue boxes
                element = driver.find_element("xpath",
                '/html/body/form/table/tbody/tr[{}]/td[12]'.format(i + 1))
                field = element.find_element("xpath",'./*[@id="P_TOPIC"]')
                field.send_keys(entry[4])
            except: # This skips the dialogue boxes
                element = driver.find_element("xpath",
                '/html/body/form/table/tbody/tr[{}]/td[12]'.format(i + 1))
                field = element.find_element("xpath",'./*[@id="P_TOPIC"]')
                field.send_keys(entry[4])

    if len(entry) > 5:
        # Details
        if len(entry[5]) > 0:
            try: # Because of pointless dialogue boxes
                element = driver.find_element("xpath",
                '/html/body/form/table/tbody/tr[{}]/td[13]'.format(i + 1))
                field = element.find_element("xpath",'./*[@id="P_TOPIC_DETAILS"]')
                field.send_keys(entry[5])
            except:
                pass

# You get to enter the approver and press the button
print("READY TO LODGE!")
input("Don't forget to select your timesheet approver")
