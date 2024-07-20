import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
from bs4 import BeautifulSoup
import pandas as pd

EMAIL_ADDRESS = 'arjunfans123@gmail.com'
EMAIL_PASSWORD = 'usod xurz pkes scha'

data = []

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    datas = next(reader)
    for row in reader:
        data.append(row)

a = 1
email_list = []
product_url_list = []
target_price_list = []

for k in data:
    for j in k:
        if a == 1:
            email_list.append(j)
        if a == 2:
            product_url_list.append(j)
        if a == 3:
            target_price_list.append(j)
        a+=1
    a=1



a = 0
for i in range(len(email_list)):
    for j in range(i+1):
        email = email_list[a]
        product_url = product_url_list[a]
        target_price = float(target_price_list[a])

        print(email)
        print(product_url)
        print(target_price)
        a += 1


        def send_email(to_email, product_url, price):
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to_email
            msg['Subject'] = 'Flipkart Price Alert'

            body = f'The price for the product has dropped to ₹{price}. Check it out here: {product_url}'
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, to_email, text)
            server.quit()


        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        }
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        #
        #     # Extracting the price
        price_str = soup.find(class_="Nx9bqj CxhGGd").get_text()
        price_ = price_str.replace(",", "")
        price = int(price_[1:])
        print(price)


        if price < target_price:
            send_email(email, product_url, price)
            data = {
                'E-Mail': [email],
                'Product_Url': [product_url],
                'Target_Price': [target_price],
            }


