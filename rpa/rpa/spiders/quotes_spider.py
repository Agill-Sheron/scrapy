import scrapy
from scrapy_splash import SplashRequest
from selenium import webdriver
from scrapy import Request
import csv
from shutil import which
import time

from selenium.common.exceptions import NoSuchElementException

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS = ['--headless']


class AppSpider(scrapy.Spider):
    name = 'rpa'

    with open("rpa.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Phone Number', 'URL','Website', 'Address', 'Postal Code', 'Municipality', 'Manager'])

    start_urls = ['https://www.rhra.ca']

    urls = ['https://www.rhra.ca/en/retirement-home-database/']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        yield SplashRequest('https://www.rhra.ca/en/retirement-home-database/', callback=self.parse, args={'wait': '5'})

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()

        # print('URRRRRRRRRRRRRRRLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' + response.url)
        time.sleep(5)
        viewMore = self.driver.find_element_by_xpath('.//*[(@id = "register_view_more_row")]//a')
        # wow = response.xpath('.//*[(@id = "register_view_more_row")]//a/text()').extract_first()
        # print('#################################################################################################################: ' + wow)
        # while (viewMore.is_displayed()):
        time.sleep(5)
        viewMore = self.driver.find_element_by_xpath('.//*[(@id = "register_view_more_row")]//a')
        self.driver.execute_script("arguments[0].click();", viewMore)
        # while True:
        #     try:
        #         viewMore.click()
        #     except NoSuchElementException:
        #         break

        time.sleep(5)
        # print('CLICKKKKKKEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEED')

        self.driver.close()
        elems = self.driver.find_elements_by_xpath('.//*[(@id = "rhra_entry_list")]//a')
        links = [elem.get_attribute('href') for elem in elems]



        count = 0
        for link in links:
            yield SplashRequest(link, callback=self.getdata, args={'wait': '5'})
            count += 1
            print("Thats the count" + str(count))


    def getdata(self, response):
        separator = " "
        rpaName = response.css('.search-detail::text').extract_first()
        email = response.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "my-4", " " )) and (((count(preceding-sibling::*) + 1) = 14) and parent::*)]//a/text()').extract()
        website = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "my-4", " " )) and (((count(preceding-sibling::*) + 1) = 13) and parent::*)]//a/text()').extract()
        phone = response.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "col-sm-7", " " ))]/text()')[9].extract()
        URL = response.url
        address = response.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "col-sm-7", " " ))]/text()')[5].extract()
        postal = response.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "col-sm-7", " " ))]/text()')[6].extract().split(' ')[2:]
        municipality = response.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "col-sm-7", " " ))]/text()')[6].extract().split(' ')[:1]
        manager = response.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "col-sm-7", " " ))]/text()')[8].extract()


        print("Name: " + rpaName.strip() + "\n"
              "Phone Number: " + phone.strip() + "\n"
               "Email: " + email[0] + "\n"
              "URL: " + URL.strip() + "\n"
               "Website: " + website[0] + "\n"
              "Address: " + address.strip() + "\n"
              "Postal: " + separator.join(postal) + "\n"
              "Municipality: " + municipality[0] + "\n"
               "Manager: " + manager.strip() + "\n"

              + "\n \n"
              )

        with open("rpa.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Email', 'Phone Number', 'URL','Website', 'Address', 'Postal Code', 'Municipality', 'Manager'])
            print([rpaName, email, phone, URL, website, address, postal, municipality, manager])



