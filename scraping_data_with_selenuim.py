
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re,csv

# getting the url
url = "https://www.newegg.com/global/uk-en/p/pl?N=101698787&icid=656387&cm_sp=Homepage-Circle-_-international%2F21-1780-_-%2F%2Fpromotions.newegg.com%2Finternational%2F21-1780%2Flaptop2.png"
driver = webdriver.Chrome()
driver.get(url)

# setting waits to our driver to get all the content that we need
wait = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-container')))
# targetting  container that we need
container = driver.find_elements(By.CLASS_NAME, "item-container")
# defining some variables to store scraped data
href1 = []
image1 = []
description1 = []
price1 = []
features = []
# getting href,image and description
for element in container:
    # getting link of product
    href = element.find_element(By.TAG_NAME, 'a')
    link = href.get_attribute('href')

    # getting image
    img = element.find_element(By.TAG_NAME, 'img')
    image = img.get_attribute('src')

    # getting description
    description = img.get_attribute('title')

    # storing data
    href1.append(link)
    image1.append(image)
    description1.append(description)

# getting resolution,color,operating_system,cpu,model,CPU, and weight
elements = driver.find_elements(By.CSS_SELECTOR, '.item-info')
for element in elements:
    # targetting container of product's features
    tag = element.find_element(By.CSS_SELECTOR, '.item-features')
    lists = tag.find_elements(By.TAG_NAME, 'li')

    # removing unnecessary texts and storing the remains
    every_item = []
    for li in lists:
        text = li.get_attribute('textContent')
        if 'Part Number:' in text:
            continue
        if 'Return Policy:' in text:
            continue
        if '#' and 'Model' in text:
            texts = text.split('#')
            word = "".join(texts)
            every_item.append(word)
        if '#' and 'Item' in text:
            continue
        if 'Resolution:' in text:
            every_item.append(text)
        if 'Color:' in text:
            every_item.append(text)
        if 'Operating System:' in text:
            every_item.append(text)
        if 'CPU:' in text:
            every_item.append(text)
        if 'Weight' in text:
            every_item.append(text)
    features.append(every_item)

# getting price
prices = driver.find_elements(By.CSS_SELECTOR, '.price-current')
for price in prices:
    actual_price = price.get_attribute('textContent')
    # substituting every character except digits and dot (.) with empty space by using re
    get_price = re.sub(r'[^\d.]', "", actual_price)

    # checking if it has price or not
    if get_price:
        price1.append(float(get_price))
    else:
        price1.append(1000.00)

# storing all gotten data to a dictionary
laptops = {}
for description, image, href, features, price in zip(description1, image1, href1, features, price1):
    resolution = ""
    weight = ""
    color = ""
    operating_system = ""
    model = ""
    cpu = ""
    for e in features:
        if 'Resolution:' in e:
            resolution += e
        if 'Weight:' in e:
            weight += e
        if 'Color:' in e:
            color += e
        if 'Operating System:' in e:
            operating_system += e
        if 'Model' in e:
            model += e
        if 'CPU' in e:
            cpu += e

    laptops[price] = [description, image, href, price, resolution, weight, color, operating_system, model, cpu]

# storing data in the database
counter = 0
for key, value in laptops.items():
    counter += 1
    print(key, value)

    # storing data to a csv file as substitution
    with open('products.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ['description', 'image', 'href', 'price', 'resolution', 'weight', 'color', 'operating_system', 'model',
             'cpu'])
        for k, v in laptops.items():
            writer.writerow(v)
    print('-------------------------------------------------------------------------------------------')
print('counter:', counter)
print('data scraped successfully')

driver.quit()
