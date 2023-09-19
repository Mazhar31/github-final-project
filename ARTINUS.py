from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
import pandas as pd
from bs4 import BeautifulSoup
import time


low_data = list()

driver = webdriver.Chrome()
url = "http://partner.artinus.net/partner/"
driver.get(url)
driver.maximize_window()

email = driver.find_element(By.XPATH, '//input[@id="memid"]')
pwd = driver.find_element(By.XPATH, '//input[@id="password"]')

user_email = "1818100517"
password = "!rlawjddjs123"

ActionChains(driver).send_keys_to_element(email, user_email).perform()
ActionChains(driver).send_keys_to_element(pwd, password).perform()

login_button = driver.find_element(By.XPATH, '//button[@class="btnSubmitFix sizeM"]')

login_button.click()
time.sleep(3)


# Lists of all elemenets that should be scraped

url_list = list()
category_listt = list()
thumbnail_img = list()
product_name = list()
price2 = list()
price3= list()
model = list()
message2 = list()
message1 = list()
delivery_fee = list()
maker = list()
country = list()
option1 = list()
option2 = list()
product_details = list()
sold_out = list()




# Getting the list of navbar elements
navbar = driver.find_elements(By.XPATH, '//ul[@class="catedep1"]/li/a')

# navbar_links = navbar.find_elements(By.TAG_NAME, 'a')
# Getting the links of navbar elements and storing in a list
navbar_links = list()
for link in navbar:
    value = link.get_attribute("href")
    navbar_links.append(value)
    # link_text = link.text
    # print(link_text)
    # link.click()
    # time.sleep(5)
    # driver.back()
    # time.sleep(5)

# Moving to each navbar link one by one
for nav in navbar_links:
    driver.get(nav)
    time.sleep(2)

    # Extracting all the categorires elements and adding categories links in menu_category_list
    menu_category = driver.find_elements(By.XPATH, '//ul[@class="menuCategory"]/li/a')
    menu_category_list = list()
    for menu in menu_category:
        menu_category_list.append(menu.get_attribute('href'))

    # Going on each category page and extracting all products link so we can visit each product and scrap data we need
    for category in menu_category_list:
        
        driver.get(category)
        time.sleep(2)


        page_links = driver.find_elements(By.XPATH, '//div[@style="text-align:center;padding:40px"]/a[b]')


        prd_links = driver.find_elements(By.XPATH, '//ul[@class="prdList grid4"]/li/div[@class="description"]/strong/a')
        prd_list = list()
        for prd in prd_links:
            prd_list.append(prd.get_attribute('href'))

        for product in prd_list:
            driver.get(product)
            time.sleep(2)
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            select_option = soup.find('tbody', class_="xans-element- xans-product xans-product-option xans-record-").find('tr').find('td').find('select')
            option_elements = select_option.find_all('option')
            # option_elements = driver.find_elements(By.XPATH, '//tbody[@class="xans-element- xans-product xans-product-option xans-record-"]/tr/td/select/option')
            options = list()
            for opt in option_elements[1:]:
                options.append(opt)
            elements_data = driver.find_elements(By.XPATH, '//ul[@class="disnoul"]/li/span[2]')
            if len(elements_data) == 8:
                if len(options) > 0:
                    for opt in options:
                        opt_text = opt.get_text(strip=True, separator=' ')
    
                        try:
                            opt_split = opt_text.split('(')
                            option1.append(opt_split[0])
                            # option2.append(opt_split[-1])
                            if opt_split[-1] == "품절)":
                                option2.append("품절")
                            else:
                                option2.append(" ")
    
                        except:
                            # opt_text = opt.text
                            option1.append(opt_text)
                            option2.append(" ")
                        
    
            
        
                        # Scraping the required data
                        url_list.append(product)
            
                        thumbnail = driver.find_element(By.XPATH, '//div[@class="thumbnail"]/img')
                        thumb = thumbnail.get_attribute('src')
                        thumbnail_img.append(thumb)
            
                        catt = driver.find_elements(By.XPATH, '//div[@class="xans-element- xans-product xans-product-headcategory path "]/ol/li')
                        catt_text = list()
                        for cat in catt:
                            catt_text.append(cat.text)
            
            
                        category_listt.append("".join(catt_text))
            
            
                        prdd_name = driver.find_element(By.XPATH, '//div[@class="headingArea"]/h2')
                        product_name.append(prdd_name.text)
            
                        price = driver.find_element(By.XPATH, '//div[@class="custom_de"]')
                        price_txt = price.text
                        price2.append(price_txt.split('\n')[0])
                        price3.append(price_txt.split(':')[-1])
                        
                        model.append(elements_data[2].text)
                        message2.append(elements_data[3].text)
                        message1.append(elements_data[4].text)
                        delivery_fee.append(elements_data[5].text)
                        maker.append(elements_data[6].text)
                        country.append(elements_data[7].text)

                        detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/div/p/img')
                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/p/img')
                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//div[last()]//img')

                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//img')


                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/p//img')

                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div//p//img')

                        
                        # //div[@id="icontab_one"]/div/div/div/div/p/img
                        # //div[@id="icontab_one"]/div/div/div/div/p/img
                        det_imgs = list()
                        for tasveer in detailsss:
                            det_imgs.append(tasveer.get_attribute('outerHTML'))

                        product_details.append("<div id=GYU style=width:100%; margin:0 auto align=center>"+"<br/>".join(det_imgs)+"</div>")

                        check_avail = driver.find_elements(By.XPATH, '//span[@class="icon"]/img')
                        # src="/images/icon/icon_07.gif"
                        for avail in check_avail:
                            found = 0
                            txtt = avail.get_attribute('src')
                            spltt = txtt.split('/')[-1]
                            
                            str = 'icon_07.gif'
                            if str == spltt:
                                found = 1

                            else:
                                continue

                        if found == 1:
                            sold_out.append(True)

                        else:
                            sold_out.append(False)
                            
        
                else:
                    low_data.append(product)             
            elif len(elements_data) == 7:
                if len(options) > 0:
                    for opt in options:
                        opt_text = opt.get_text(strip=True, separator=' ')
    
                        try:
                            opt_split = opt_text.split('(')
                            option1.append(opt_split[0])
                            # option2.append(opt_split[-1])
                            if opt_split[-1] == "품절)":
                                option2.append("품절")
                            else:
                                option2.append(" ")
    
                        except:
                            # opt_text = opt.text
                            option1.append(opt_text)
                            option2.append(" ")
                        
    
            
        
                        # Scraping the required data
                        url_list.append(product)
            
                        thumbnail = driver.find_element(By.XPATH, '//div[@class="thumbnail"]/img')
                        thumb = thumbnail.get_attribute('src')
                        thumbnail_img.append(thumb)
            
                        catt = driver.find_elements(By.XPATH, '//div[@class="xans-element- xans-product xans-product-headcategory path "]/ol/li')
                        catt_text = list()
                        for cat in catt:
                            catt_text.append(cat.text)
            
            
                        category_listt.append("".join(catt_text))
            
            
                        prdd_name = driver.find_element(By.XPATH, '//div[@class="headingArea"]/h2')
                        product_name.append(prdd_name.text)
            
                        price = driver.find_element(By.XPATH, '//div[@class="custom_de"]')
                        price_txt = price.text
                        price2.append(price_txt.split('\n')[0])
                        price3.append(price_txt.split(':')[-1])
                        
                        model.append(elements_data[2].text)
                        message2.append(" ")
                        message1.append(elements_data[3].text)
                        delivery_fee.append(elements_data[4].text)
                        maker.append(elements_data[5].text)
                        country.append(elements_data[6].text)

                        detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/div/p/img')
                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/p/img')
                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//div[last()]//img')

                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//img')


                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/p//img')

                        if len(detailsss) < 1:
                            detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div//p//img')

                        
                        # //div[@id="icontab_one"]/div/div/div/div/p/img
                        # //div[@id="icontab_one"]/div/div/div/div/p/img
                        det_imgs = list()
                        for tasveer in detailsss:
                            det_imgs.append(tasveer.get_attribute('outerHTML'))

                        product_details.append("<div id=GYU style=width:100%; margin:0 auto align=center>"+"<br/>".join(det_imgs)+"</div>")

                        check_avail = driver.find_elements(By.XPATH, '//span[@class="icon"]/img')
                        # src="/images/icon/icon_07.gif"
                        for avail in check_avail:
                            found = 0
                            txtt = avail.get_attribute('src')
                            spltt = txtt.split('/')[-1]
                            
                            str = 'icon_07.gif'
                            if str == spltt:
                                found = 1

                            else:
                                continue

                        if found == 1:
                            sold_out.append(True)

                        else:
                            sold_out.append(False)
                            
        
                else:
                    low_data.append(product)
                        
                
                    
                                
        if len(page_links) > 0:
            for i in range(0, len(page_links)):
                last_part = category.split('?')[1]
                pagination = f"http://partner.artinus.net/partner/?page={i+2}&order=&by=&num_per_page=&mod=&actpage=&searchval=&{last_part}"
                # http://partner.artinus.net/partner/?page=2&order=&by=&num_per_page=&mod=&actpage=&searchval=&cate=035001002&inc=list
                
                # time.sleep(5)
                # page_links[i].click()
                driver.get(pagination)
                time.sleep(2)


                prd_links = driver.find_elements(By.XPATH, '//ul[@class="prdList grid4"]/li/div[@class="description"]/strong/a')
                prd_list = list()
                for prd in prd_links:
                    prd_list.append(prd.get_attribute('href'))
        
                for product in prd_list:
                    driver.get(product)
                    time.sleep(2)
                    
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')
                    select_option = soup.find('tbody', class_="xans-element- xans-product xans-product-option xans-record-").find('tr').find('td').find('select')
                    option_elements = select_option.find_all('option')

                    # option_elements = driver.find_elements(By.XPATH, '//tbody[@class="xans-element- xans-product xans-product-option xans-record-"]/tr/td/select/option')
                    options = list()
                    for opt in option_elements[1:]:
                        options.append(opt)
                    elements_data = driver.find_elements(By.XPATH, '//ul[@class="disnoul"]/li/span[2]')
                    if len(elements_data) == 8:
                        if len(options) > 0:
                            for opt in options:
                                opt_text = opt.text
            
                                try:
                                    
                                    opt_split = opt_text.split('(')
                                    option1.append(opt_split[0])
                                    if opt_split[-1] == "품절)":
                                        option2.append("품절")
                                    else:
                                        option2.append(" ")
                                    
                                        
                                    
            
                                except:
                                    # opt_text = opt.text
                                    option1.append(opt_text)
                                    option2.append(" ")
                                
            
                        
                                
                
                                # Scraping the required data
                                url_list.append(product)
                    
                                thumbnail = driver.find_element(By.XPATH, '//div[@class="thumbnail"]/img')
                                thumb = thumbnail.get_attribute('src')
                                thumbnail_img.append(thumb)
                    
                                catt = driver.find_elements(By.XPATH, '//div[@class="xans-element- xans-product xans-product-headcategory path "]/ol/li')
                                catt_text = list()
                                for cat in catt:
                                    catt_text.append(cat.text)
                    
                    
                                category_listt.append("".join(catt_text))
                    
                    
                                prdd_name = driver.find_element(By.XPATH, '//div[@class="headingArea"]/h2')
                                product_name.append(prdd_name.text)
                    
                                price = driver.find_element(By.XPATH, '//div[@class="custom_de"]')
                                price_txt = price.text
                                price2.append(price_txt.split('\n')[0])
                                price3.append(price_txt.split(':')[-1])
                    
                                # price_3 = driver.find_element(By.XPATH, '//strong[@id="span_product_price_text"]')
                                # price3.append(price_3.text)
                                
                                model.append(elements_data[2].text)
                                message2.append(elements_data[3].text)
                                message1.append(elements_data[4].text)
                                delivery_fee.append(elements_data[5].text)
                                maker.append(elements_data[6].text)
                                country.append(elements_data[7].text)
        
                                detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/div/p/img')
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/p/img')
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//div[last()]//img')
        
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//img')
        
        
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/p//img')
        
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div//p//img')

                                # //div[@id="icontab_one"]/div/div/div/div/p/img
                                # //div[@id="icontab_one"]/div/div/div/div/p/img
                                det_imgs = list()
                                for tasveer in detailsss:
                                    det_imgs.append(tasveer.get_attribute('outerHTML'))
        
                                product_details.append("<div id=GYU style=width:100%; margin:0 auto align=center>"+"<br/>".join(det_imgs)+"</div>")

                                check_avail = driver.find_elements(By.XPATH, '//span[@class="icon"]/img')
                                # src="/images/icon/icon_07.gif"
                                for avail in check_avail:
                                    found = 0
                                    txtt = avail.get_attribute('src')
                                    spltt = txtt.split('/')[-1]
                                    
                                    str = 'icon_07.gif'
                                    if str == spltt:
                                        found = 1
        
                                    else:
                                        continue
        
                                if found == 1:
                                    sold_out.append(True)
        
                                else:
                                    sold_out.append(False)
                                
                                    
                
                                
                        else:
                            low_data.append(product)
                    elif len(elements_data) == 7:
                        if len(options) > 0:
                            for opt in options:
                                opt_text = opt.text
            
                                try:
                                    
                                    opt_split = opt_text.split('(')
                                    option1.append(opt_split[0])
                                    if opt_split[-1] == "품절)":
                                        option2.append("품절")
                                    else:
                                        option2.append(" ")
                                    
                                        
                                    
            
                                except:
                                    # opt_text = opt.text
                                    option1.append(opt_text)
                                    option2.append(" ")
                                
            
                        
                                
                
                                # Scraping the required data
                                url_list.append(product)
                    
                                thumbnail = driver.find_element(By.XPATH, '//div[@class="thumbnail"]/img')
                                thumb = thumbnail.get_attribute('src')
                                thumbnail_img.append(thumb)
                    
                                catt = driver.find_elements(By.XPATH, '//div[@class="xans-element- xans-product xans-product-headcategory path "]/ol/li')
                                catt_text = list()
                                for cat in catt:
                                    catt_text.append(cat.text)
                    
                    
                                category_listt.append("".join(catt_text))
                    
                    
                                prdd_name = driver.find_element(By.XPATH, '//div[@class="headingArea"]/h2')
                                product_name.append(prdd_name.text)
                    
                                price = driver.find_element(By.XPATH, '//div[@class="custom_de"]')
                                price_txt = price.text
                                price2.append(price_txt.split('\n')[0])
                                price3.append(price_txt.split(':')[-1])
                    
                                # price_3 = driver.find_element(By.XPATH, '//strong[@id="span_product_price_text"]')
                                # price3.append(price_3.text)
                                
                                model.append(elements_data[2].text)
                                message2.append(" ")
                                message1.append(elements_data[3].text)
                                delivery_fee.append(elements_data[4].text)
                                maker.append(elements_data[5].text)
                                country.append(elements_data[6].text)
        
                                detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/div/p/img')
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/div/p/img')
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//div[last()]//img')
        
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div[@align="center"]/div[@style="text-align: center"]//img')
        
        
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div/p//img')
        
                                if len(detailsss) < 1:
                                    detailsss = driver.find_elements(By.XPATH, '//div[@class="cont"]/div//p//img')

                                # //div[@id="icontab_one"]/div/div/div/div/p/img
                                # //div[@id="icontab_one"]/div/div/div/div/p/img
                                det_imgs = list()
                                for tasveer in detailsss:
                                    det_imgs.append(tasveer.get_attribute('outerHTML'))
        
                                product_details.append("<div id=GYU style=width:100%; margin:0 auto align=center>"+"<br/>".join(det_imgs)+"</div>")

                                check_avail = driver.find_elements(By.XPATH, '//span[@class="icon"]/img')
                                # src="/images/icon/icon_07.gif"
                                for avail in check_avail:
                                    found = 0
                                    txtt = avail.get_attribute('src')
                                    spltt = txtt.split('/')[-1]
                                    
                                    str = 'icon_07.gif'
                                    if str == spltt:
                                        found = 1
        
                                    else:
                                        continue
        
                                if found == 1:
                                    sold_out.append(True)
        
                                else:
                                    sold_out.append(False)
                                
                                    
                
                                
                        else:
                            low_data.append(product)                        

        

            


driver.quit()


data_for_df = {"url": url_list,
               "category": category_listt,
               "thumbnail": thumbnail_img,
               "product name": product_name,
               "price2": price2,
               "price3": price3,
               "model": model,
               "message1": message1,
               "message2": message2,
               "delivery fee": delivery_fee,
               "maker": maker,
               "country": country,
               "option1": option1,
               "option2": option2,
               "detail images": product_details,
               "sold out": sold_out
              }


df = pd.DataFrame(data_for_df)

df['price2'] = df['price2'].str.replace('[^\d]', '', regex=True)
df['price3'] = df['price3'].str.replace('[^\d]', '', regex=True)
df['sold out'] = df['sold out'].replace({True: 'sold out', False: ''})


df.to_excel("Scraped Data.xlsx")

