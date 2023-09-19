from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.get('https://www.scubapro.co.kr/')

# Define a function to click the "See More" button
def click_see_more():
    try:
        see_more_button = driver.find_element(By.XPATH, '//a[contains(text(), "더보기")]')
        see_more_button.click()
        time.sleep(3)  # Add a delay to allow content to load
        return True
    except Exception as e:
        return False



# navbar = list()
elements = driver.find_elements(By.XPATH, '//ul[@class="no01"]/li/a')

url = list()
img_src = list()
name = list()
price3 = list()
option_1 = list()
option_2 = list()
in_detail = list()

links = []
for element in elements:
    links.append(element.get_attribute('href'))

for link in links:
    # link = element.get_attribute('href')
    # Click the "See More" button repeatedly until it's no longer present
    pages = driver.get(link)
    time.sleep(5)
    while click_see_more():
        time.sleep(2)
        pass

    time.sleep(3)
    product_links = driver.find_elements(By.XPATH, '//li[contains(@onclick, "location.href")]')

    # Create a list to store data from each product page
    # product_data = []

    extracted_urls = []
    # Loop through each product link and click on it
    for product_link in product_links:
        onclick_value = product_link.get_attribute('onclick')
        if onclick_value:
            link_value = onclick_value.split("'")[1]
            extracted_urls.append("https://www.scubapro.co.kr/product/"+link_value)

    for link in extracted_urls:
        driver.get(link)
        time.sleep(2)  # Add a delay to allow the product page to load
        # name.append(product_link.find_element(By.XPATH, '//div[@class="prd_name"]').text)
        something = driver.page_source
        soup = BeautifulSoup(something, 'html.parser')
        options_div = soup.find('div', class_='pro_btn')
        options_try = options_div.find_all('option')
        options = options_try[1:]
        for option in options:
            
            url.append(driver.current_url)
            
            image_src = driver.find_element(By.XPATH, '//div[@class="main_img"]/img')
            img_src.append(image_src.get_attribute('src'))
            
            naam = soup.find('div', class_ ='prd_name').get_text(strip=True, separator=' ')
            name.append(naam)
            
            pric = soup.find('div', class_='pric')
            price3.append(pric.find('strong').get_text(strip=True, separator=' '))

            detail_imgs_list = driver.find_elements(By.XPATH, '//div[@class="in_detail"]/div/img')
            imgs = list()
            if len(detail_imgs_list)<1:
                detail_imgs_list = driver.find_elements(By.XPATH, '//div[@class="in_detail"]/p/img')
                
            for img in detail_imgs_list:
                imgs.append(img.get_attribute('outerHTML'))

            in_detail.append("<div id=GYU style=width:100%; margin:0 auto align=center>"+"<br/>".join(imgs)+"</div>")

            option_prettify = option.get_text(strip=True, separator=' ')
            data = option_prettify.split('|')
            if data[-1] == "구매가능" or "품절":
                option_2.append(data[-1].strip())
                option_1.append("|".join(data[:len(data)-1]))

            else:
                option_1.append("|".join(data))
                
            # if len(data) == 2:
            #     option_1.append(data[0]+"|")
            #     if data[1] == "구매가능" or "품절":
            #         option_2.append(data[1])
            # if len(data) > 2:
            #     option_1.append(data[0]+"|")
            #     option_3.append(data[1]+" |")
            #     if data[2] == "구매가능" or "품절":
            #         option_2.append(data[2])
            
        driver.back()
        time.sleep(2)
        # driver.quit()
        # break




        # time.sleep(5)
        # product_link.click()
        # time.sleep(10)
    # driver.quit()
    # break

driver.quit()


df = pd.DataFrame({"URL": url,"Thumbnail": img_src,"Product Name": name,"Price": price3,"option_1": option_1,"option_2": option_2,"in_details": in_detail})

df.to_excel("Scraped Data.xlsx")