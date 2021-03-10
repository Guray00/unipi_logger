#!/usr/bin/python

WEBPAGE = "http://131.100.1.1"


import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import logging
import atexit

#ATEXIT - HANDLING QUIT MESSAGE
def exit_handler():
    logging.info("=======================================================")
atexit.register(exit_handler)


# return an argument value
def getArg(arg):
    j = 0
    for i in sys.argv:
        j+=1
        if(i == arg):
            return sys.argv[j]
    return False

# HANDLING LOGGING
loglevel = getArg("--log")
numeric_level = 0
if (loglevel != False):
	numeric_level = getattr(logging, loglevel.upper(), None)
	if not isinstance(numeric_level, int):
		raise ValueError('Invalid log level: %s' % loglevel)

else:
	loglevel = "debug"
	numeric_level = getattr(logging, loglevel.upper(), None)

logging.basicConfig(filename=sys.argv[0].replace(".py","")+'.log', format='%(asctime)s\t%(levelname)s\t\t%(message)s', level=numeric_level, datefmt= "[%y/%m/%d - %H:%M:%S]")



######################################

#		PROGRAM STARTS HERE

######################################


#check if the connection is estabilished
def check_connection():
    url=WEBPAGE
    timeout=1
    try:
        _ = requests.get(url, timeout=timeout)
        return False
    except requests.ConnectionError:
        return True

#retrives login informations
def getCredentials():
    usr = ""
    pw  = ""
    j=0
    for i in sys.argv:
        j+=1
        
        #checking for "-u" argument
        if(i == "-u" or i == "--user"):
            usr=sys.argv[j]
        
        #checking for "-pw" argument
        elif(i == "-pw" or i == "--password"):
            pw=sys.argv[j]

    if(usr == "" or pw == ""):
        if(usr == ""):
            logging.error("Aborted, please provide an user with \"-u\". No connection as been estabilished.")
            logging.warning(" "*22 +"Example: python {} -u <username> -pw <password>".format(sys.argv[0]))
            exit()

    elif(pw == ""):
            logging.error("Aborted, please provide a password with \"-pw\". No connection as been estabilished.")
            logging.warning(" "*22 +"Example: python {} -u <username> -pw <password>".format(sys.argv[0]))
            exit()

    return [usr,pw]



# If is true, we are already connected, therefore we don't need to try.
if(check_connection()):
    logging.info("Already connected, aborting.")
    exit()
exit()

# taking credentials, if wrong input, fails inside the function
CREDENTIALS = getCredentials()


#OPTION FOR CHROMEDRIVER
options = Options()
options.headless = True

chromedriver_location = getArg("-l")
if (not chromedriver_location):
    chromedriver_location = getArg("--location")

if (not chromedriver_location):
    if (os.name == 'nt'):
	    logging.error("Aborting. No default location for chromedriver in windows, provide with \"-l\" or \"--location\".")
	    exit()
    else:
        chromedriver_location = "/usr/bin/chromedriver"
        
driver = webdriver.Chrome(executable_path=chromedriver_location, options=options)
driver.implicitly_wait(3)
driver.get(WEBPAGE)

#print(driver.page_source)
login    = driver.find_element_by_css_selector("#frmValidator>div>div>div:nth-child(1)> input") .send_keys(CREDENTIALS[0])
password = driver.find_element_by_css_selector("#frmValidator > div > div > div:nth-child(3) > input").send_keys(CREDENTIALS[1])
submit	 = driver.find_element_by_css_selector("#frmValidator > div > div > button").click()

try:
    driver.find_element_by_css_selector("#timeval")
    logging.info("Successfully connected.")

except:
    logging.critical("Something went wrong, not logged.")

# quitting chrome
driver.quit()



