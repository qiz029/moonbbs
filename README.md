# moonbbs_buyer_spider
A easy spider that find the item on the latest list

To use this function, one must setup the email address and password in main.py

currenly private

# Api Contract
- GET / : "welcome to moonbbs"
- POST /wish

  HEADER: "Content-type": "application/json"

  {
    "num": {num},
    "items": {
      "1": "item1",
      "2": "item2"
    }
  }
- POST /email

  HEADER: "Content-type": "application/json"

  {
    "email": {email_add},
    "password": {password}
  }
- POST /interval/{time interval of refreshing}
- GET /wish NOT SUPPORTED
- POST /start
