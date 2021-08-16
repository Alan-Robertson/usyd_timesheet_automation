import selenium
import time
import sys
import csv

from selenium import webdriver

##########################################################

# A few lazy consts we're going to need later

nano_sleep = 0.5
micro_sleep = 1.5
small_sleep = 3
sleep = 5
big_sleep = 15

click_element = lambda driver, xpath: driver.find_element_by_xpath(xpath).click()
text_element = lambda driver, xpath, text: driver.find_element_by_xpath(xpath).send_keys(text)
file_element = lambda driver, xpath, filepath: driver.find_element_by_xpath(xpath).send_keys(filepath)
wait = lambda x: time.sleep(x)


##########################################################
# Load entries from csv
##########################################################

csv_file = ''
job_number = 1

# Time to get a file:
if len(sys.argv) < 2:
    print("Please provide a path to a properly formatted csv file containing your timesheet data.")
    file_name = input()
else:
    file_name = sys.argv[1]

try:
    # Yeah this is a hack job
    raw_data = open(file_name, 'r').readlines()
except:
    print("File error")
    exit()

# Determine job number, default to 1
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

initial_url = 'https://myhr.sydney.edu.au/alesco-wss-v17/faces/app/WJ0000.jspx'


driver.get(initial_url)
print("Please Login")
print("Once you have Logged in, Press Enter to Continue")
while input() != '':
    continue


##########################################################
# Get a new timesheet
##########################################################

# Access elements from the menu
click_element(driver,
    "/html/body/div[1]/form/div/div/div/div[1]/div/div[3]/div/div/table/tbody/tr/td/div/div[1]/div[1]/table/tbody/tr/td[8]/div/div/table/tbody/tr/td[2]/a")
wait(micro_sleep)

click_element(driver,
    "/html/body/div[1]/form/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]")
wait(small_sleep)

# Switch to iframe
driver.switch_to.frame("pt1:r1:0:pt1:Main::f")

# Create new timesheet
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
        "/html/body/div/form/table/tbody/tr[{}]/td[1]/input".format(job_number)
        )
    wait(micro_sleep)

    # Continue
    click_element(driver,
        "/html/body/div/form/p[3]/input[1]")
    wait(small_sleep)
except:
    pass


##########################################################
# Fill in the timesheet
##########################################################

# Get the right number of rows
n_rows = len(raw_data)
if n_rows > 20:
    for _ in range(n_rows - 20):
        click_element(driver, "/html/body/form/p[3]/input[5]")
        wait(nano_sleep)


# Enter Data
for i, entry in enumerate(raw_data):
    entry = entry.split(',')

    # Date
    element = driver.find_element_by_xpath(
        "/html/body/form/table/tbody/tr[{}]/td[4]".format(i + 1))
    field = element.find_element_by_xpath('./*[@id="P_WORK_DATE"]')
    field.send_keys(entry[0]) 

     # Hours
    element = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr[{}]/td[6]'.format(i + 1))
    field = element.find_element_by_xpath('./*[@id="P_UNITS"]')
    field.send_keys(entry[1])    

    # Paycode
    element = driver.find_element_by_xpath(
    '/html/body/form/table/tbody/tr[{}]/td[7]'.format(i + 1)) 
    field = element.find_element_by_xpath('./*[@id="P_PAYCODE"]')
    field.send_keys(entry[2])

    if len(entry) > 3:
        # Analysis Code
        if len(entry[3]) > 0:
            try: # Because of pointless dialogue boxes
                element = driver.find_element_by_xpath(
                '/html/body/form/table/tbody/tr[{}]/td[10]'.format(i + 1))
                field = element.find_element_by_xpath('./*[@id="P_GL_SUB_ACCOUNT"]')
                field.send_keys(entry[3])
            except:
                pass

    if len(entry) > 4:
        # Topic
        if len(entry[4]) > 0:
            try: # Because of pointless dialogue boxes
                element = driver.find_element_by_xpath(
                '/html/body/form/table/tbody/tr[{}]/td[12]'.format(i + 1)) 
                field = element.find_element_by_xpath('./*[@id="P_TOPIC"]')
                field.send_keys(entry[4])
            except: # This skips the dialogue boxes
                element = driver.find_element_by_xpath(
                '/html/body/form/table/tbody/tr[{}]/td[12]'.format(i + 1)) 
                field = element.find_element_by_xpath('./*[@id="P_TOPIC"]')
                field.send_keys(entry[4])

    if len(entry) > 5:
        # Details
        if len(entry[5]) > 0:
            try: # Because of pointless dialogue boxes
                element = driver.find_element_by_xpath(
                '/html/body/form/table/tbody/tr[{}]/td[13]'.format(i + 1)) 
                field = element.find_element_by_xpath('./*[@id="P_TOPIC_DETAILS"]')
                field.send_keys(entry[5])
            except:
                pass

# You get to enter the approver and press the button
print("READY TO LODGE!")
print("Don't forget to select your timesheet approver")