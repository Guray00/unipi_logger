#!/usr/bin/python

WEBPAGE = "http://131.100.1.1"


import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import logging
import atexit
import json
import time
import math

#ATEXIT - HANDLING QUIT MESSAGE
def exit_handler():
    logging.debug("=======================================================")
atexit.register(exit_handler)


# return an argument value
def getArg(arg):
    j = 0
    for i in sys.argv:
        j+=1
        if(i == arg):
            return sys.argv[j]
    return False

# HANDLING LOGGING	===============================================================
loglevel = getArg("--log")
if (loglevel != False):
	numeric_level = getattr(logging, loglevel.upper(), None)
	if not isinstance(numeric_level, int):
		raise ValueError('Invalid log level: %s' % loglevel)

else:
	loglevel = "info"
	numeric_level = getattr(logging, loglevel.upper(), None)

logging.basicConfig(filename=sys.argv[0].replace(".py","")+'.log', format='%(asctime)s\t%(levelname)s\t\t%(message)s', level=numeric_level, datefmt= "[%d/%m/%y - %H:%M:%S]")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# HANDLING DATA FILE ==============================================================
data = dict()
data["attempts"]     = 0
data["time"] 	     = math.trunc(time.time())
data["last_session"] = -1
try:
	# updates local data with the file
	with open(os.path.dirname(os.path.realpath(__file__)) +'/.data') as json_file:
		data = json.load(json_file)

except:
	# if file doesn't exists, we make it
	with open(os.path.dirname(os.path.realpath(__file__)) +'/.data', "w") as json_file:
		logging.debug(".data not found, making...")
		json.dump(data, json_file)

# increases attempts
def increaseData():
	global data
	try:# updates local data with the file
		with open(os.path.dirname(os.path.realpath(__file__)) +'/.data', "w") as json_file:
			data["attempts"]+= 1
			data["time"] = math.trunc(time.time())
			json.dump(data, json_file)

	except Exception as e:
		logging.critical("Aborting, error in increaseData: "+e)
		exit()

# reset attempts
def resetData(success=False):
	global data
	try:# updates local data with the file
		with open(os.path.dirname(os.path.realpath(__file__)) +'/.data', "w") as json_file:
			
			if(data["attempts"] != 0):
				logging.info("Resetting attempts.")
			else:
				logging.debug("Resetting attempts.")

			data["attempts"] = 0
			data["time"]     = math.trunc(time.time())		

			if (success):
				data["last_session"] = time.ctime()

			data = json.dump(data, json_file)
			
	
	except Exception as e:
		logging.critical("Aborting, error in resetData: "+ e)
		exit()


############################################################################


#			PROGRAM STARTS HERE


############################################################################

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

	#checking correct input
    if(usr == "" or pw == ""):
        if(usr == ""):
            logging.error("Aborted, please provide an user with \"-u\". No connection as been estabilished.")
            logging.warning("Example: python {} -u <username> -pw <password>".format(sys.argv[0]))
            exit()

        elif(pw == ""):
            logging.error("Aborted, please provide a password with \"-pw\". No connection as been estabilished.")
            logging.warning("Example: python {} -u <username> -pw <password>".format(sys.argv[0]))
            exit()

    return [usr,pw]

# if has been done more than 15 attempts, we must way 4 hours to retry
now = math.trunc(time.time())
if (data["attempts"] >= 15 and (now - data["time"]) < 4*60*60):
	logging.critical("Too many request. ABORTING.")
	exit()

# reset attempts after 4 hours
elif((now - data["time"]) >= 4*60*60 and data["attempts"] != 0):
	resetData()


# If is true, we are already connected, therefore we don't need to try.
if(check_connection()):
    logging.debug("Already connected, aborting.")
    exit()


# taking credentials, if wrong input, fails inside the function
CREDENTIALS = getCredentials()


#OPTION FOR CHROMEDRIVER
options = Options()
options.headless = True		#dosn't show the chrome window

#taking chromedriver location checking -l argument
chromedriver_location = getArg("-l")
if (not chromedriver_location):
	#if not found, try with --location
    chromedriver_location = getArg("--location")

#if still not found, checking for default position
if (not chromedriver_location):
    if (os.name == 'nt'): #nt = windows
	    logging.error("Aborting. No default location for chromedriver in windows, provide with \"-l\" or \"--location\".")
	    exit()
    else:				  #try with debian default
        chromedriver_location = "/usr/bin/chromedriver"
        
driver = webdriver.Chrome(executable_path=chromedriver_location, options=options)
driver.implicitly_wait(5)		#wait for page max 5 seconds
driver.set_page_load_timeout(5)	#wait for page max 5 seconds

try:
	#connecting to the page
	driver.get(WEBPAGE)
except:
	#page dosn't load, giving error
	increaseData()
	logging.error("Login page not found, aborting.")
	exit()

#we are on the page, filling inputs
try:
	login    = driver.find_element_by_css_selector("#frmValidator>div>div>div:nth-child(1)> input") .send_keys(CREDENTIALS[0])
	password = driver.find_element_by_css_selector("#frmValidator > div > div > div:nth-child(3) > input").send_keys(CREDENTIALS[1])
	submit	 = driver.find_element_by_css_selector("#frmValidator > div > div > button").click()

except:
	# inputs not found, aborting
	increaseData()
	logging.critical("Not loading elements, aborting.")
	exit()

#cheking if we have successfully connected
try:
    driver.find_element_by_css_selector("#timeval")
    logging.info("Successfully connected.")
    resetData(True)

except:
    increaseData()
    logging.critical("Something went wrong, not logged.")

# closing chrome
driver.quit()



