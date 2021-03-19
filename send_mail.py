import smtplib

# function that sends an email if the prices fell down
def post(link):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('mgupt176@gmail.com', 'sanjana2281')

  subject = 'Price Fell Down'
  body = "Check the amazon link "

  msg = f"Subject: {subject}\n\n{body}"
  
  server.sendmail(
    'mgupt176@gmail.com',
    'sharma.sanjana2281@gmail.com',
    msg
  )
  server.quit()
  return 'Hey Email has been sent'

