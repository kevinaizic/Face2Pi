#!/usr/bin/env python
#Tested on v2.7.14
#
#*Obviously embedding the password is a risk but I'm lazy and this will only be on my LAN behind a menacing pfSense firewall

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
import os
from datetime import datetime

# $dir as arg
dir = "/home/pi/datasets/" + sys.argv[1]
clusters = os.listdir(dir + "/cluster")
found = os.listdir(dir)
message = "Detected: " + str(len(clusters)) #first/only person appended

if len(clusters) == 1:
    message += "person"
else:
    message += "people"    

#########################################################################################################################
# Below adapted from https://www.linkedin.com/pulse/python-script-send-email-attachment-using-your-gmail-account-singh/ #
#########################################################################################################################

#optionally include other recipients
recipients = ['me@gmail.com'] #,'bcc@example.com','bcc2@example.com'] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = str(sys.argv[1])
msg['From'] = 'me@gmail.com'
msg['Reply-to'] = 'me@gmail.com'
 
msg.preamble = 'Multipart massage.\n'
 
part = MIMEText(str(message)) #email message
msg.attach(part)

foundpics = []
for i in xrange(len(found)):
    if "box.jpg" in found[i]:
        foundpics.append(found[i]) 


#can use filename only if in same dir, or full path (note in this case the full path becomes attached file's name) 
for x in xrange(len(foundpics)):
    part = MIMEApplication(open(dir + "/" + foundpics[x],"rb").read()) 
    part.add_header('Content-Disposition', 'attachment', filename=str(foundpics[x])) 
    msg.attach(part)
 

server = smtplib.SMTP("smtp.gmail.com:587")
server.ehlo()
server.starttls()
server.login("me@gmail.com", "password")
 
server.sendmail(msg['From'], emaillist , msg.as_string())
