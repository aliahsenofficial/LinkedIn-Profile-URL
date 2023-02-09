import csv
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


if __name__ == "__main__":

    keyword = input("Enter the keyword: ")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('../chromedriver.exe', options=chrome_options)
    
    driver.get('https://www.linkedin.com/login')
    sleep(2)

    # Enter your EMAIL ADDRESS and PASSWORD here
    driver.find_element(By.ID, 'username').send_keys('YOUR EMAIL ADDRESS')
    driver.find_element(By.ID, 'password').send_keys('YOUR PASSWORD')

    driver.find_element(By.XPATH, "//*[@type='submit']").click()
    sleep(randint(2,4))

    # Number of pages we'll me scraping
    with open('profile_urls.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Profile URL"])

        count = 0
        for no in range(1,100):
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION&page={}".format(keyword,no)
            driver.get(search_url)
            driver.maximize_window()
            sleep(randint(1,3))

            # Scrolling to avoid banning
            for scroll in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(randint(1,3))

            search = BeautifulSoup(driver.page_source,'lxml')
            print("Going to scrape Page # {}".format(no))
            
            peoples = search.findAll('span', 'entity-result__title-text')
            for people in peoples:
                profile_url = people.find('a')['href']
                writer.writerow([profile_url])
                count += 1

    print('Total URL Scraped: ', count)   
    driver.quit()
