import sys, getopt, time
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests


def get_request(driver, output_folder):
    text = input('Text: ')
    url = 'https://translate.google.com/#view=home&op=translate&sl=ja&tl=ja&text=' + text
    driver.get(url)

    try:
        # Wait until element exists and is clickable
        res_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'res-tts'))
            and
            EC.element_to_be_clickable((By.CLASS_NAME, 'res-tts'))
        )
        res_element.click()
        time.sleep(1)
 
        last_req = None
        for request in driver.requests:
            if request.response and request.response.headers['Content-Type'] == 'audio/mpeg':
                last_req = request
                print(request)
        if last_req != None:
            response = requests.get(last_req)
            with open(output_folder + '\\' + text + '.mp3', 'wb') as file:
                file.write(response.content)

    finally:
        time.sleep(0)
        # driver.quit()


def main(argv):
    opt_file = open('./options.txt', 'r')
    exec_path = (opt_file.readline())
    output_folder = (opt_file.readline())

    options = Options()
    options.add_argument('headless')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    
    # Start Driver
    # Make sure the selenium chrome driver is the same as current chrome version
    driver = webdriver.Chrome(options=options, executable_path='C:\BrowserDrivers\chromedriver.exe')
    driver.set_window_size(1440, 900)

    print('Use CTRL+C to quit :)')
    while True:
        get_request(driver, output_folder)

if __name__ == "__main__":
    main(sys.argv[1:])