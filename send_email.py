# Import modules
import smtplib
from random import randint
from main import send_mail

# Email that will be sending the email to the user
sender_email = "*REMOVED*"
# The users inputted email
reciever_email = send_mail
# Google generated random password allowing this program access to sender email
password = "*REMOVED*"

# Generates one time code
OTC = randint(1000, 9999)
OTC_Email = str(OTC)

# Establishes connection to smtplib server module
# Allowing for email to be sent to the user
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
# Logs into sender email using credentials above
server.login(sender_email, password)

# sending the actual email
server.sendmail(sender_email, reciever_email, OTC_Email)
