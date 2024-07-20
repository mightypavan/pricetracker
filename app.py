import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, render_template
import lxml
import time
import pandas as pd
import socket

start = time.time()

app = Flask(__name__)

EMAIL_ADDRESS = 'arjunfans123@gmail.com'
EMAIL_PASSWORD = 'usod xurz pkes scha'

def get_price(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    # Extracting the price
    price_str = soup.find(class_="Nx9bqj CxhGGd").get_text()
    print(price_str)
    price_ = price_str.replace(",", "")
    print(price_)
    price = int(price_[1:])
    print(price)
    return price_str

def send_email(to_email, product_url, price):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = 'Flipkart Price Alert'

    body = f'The price for the product has dropped to {price}. Check it out here: {product_url}'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, to_email, text)
    server.quit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/track', methods=['POST'])
def track():
    product_url = request.form['product_url']
    email = request.form['email']
    target_price = float(request.form['target_price'])

    price = get_price(product_url)
    if price < target_price:
        send_email(email, product_url, price)
        end = time.time()
        print(end - start)
        data = {
            'E-Mail' : [email],
            'Product_Url' : [product_url],
            'Target_Price' : [target_price],
        }
        df = pd.DataFrame(data)
        df.to_csv('data.csv', mode='a', index=False, header=False)
        return f'Your target price is {target_price} but the current price {price} is already lower.'
    else:
        data = {
            'E-Mail': [email],
            'Product_Url': [product_url],
            'Target_Price': [target_price],
        }
        df = pd.DataFrame(data)
        df.to_csv('data.csv', mode='a', index=False, header=False)
        return f'Tracking initiated. Current price is {price}. You will receive an alert when the price drops below {target_price}.'
    
    



def find_open_port():
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a random available port
    sock.bind(('127.0.0.1', 0))

    # Get the port that was actually bound
    _, port = sock.getsockname()

    # Close the socket
    sock.close()

    return port

if __name__ == '__main__':
    dynamic_port = find_open_port()

    app.run(debug=True, port=dynamic_port)


