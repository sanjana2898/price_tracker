import smtplib

# function that sends an email if the prices fell down
def post(reciever, link,product_name,price,website):
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('mgupt176@gmail.com', 'sanjana2281')

		subject = f'!! Price Fell Down !! {product_name} on {website} to Rs.{price}'
		body = f"Check the link below\n{link}\n at {website}"

		msg = f"Subject: {subject}\n\n{body}"

		server.sendmail(
		'mgupt176@gmail.com',
		reciever,
		msg
		)
		server.quit()
		return True
	except Exception as e:
		print(e)
		return False

if __name__== "__main__":
	post("sharma.sanjana2281@gmail.com",
	"https://www.amazon.in/realme-Buds-Wireless-Earbuds-Black/dp/B08BPHPNCT/ref=sr_1_5?dchild=1&keywords=realme+buds&qid=1616229880&sr=8-5",
	"test product",
	2000,
	"amazon",
	)
    