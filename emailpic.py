#!/usr/bin/env python
#Tested on v2.7.14
#
#This headless script is part of my AI face detection project using a raspberry pi + camera mounted on the eyehole of 
#my dorm room door, and is called to notify me when face(s) "detected" past a preset confidence threshold.
#
#Arguments:
#   1) arbitrary email subject
#   2) image path (or just name if same dir)
#   3) detected index/indeces of people array (see example)
#Output:
#   1) message contains detected name(s) and a timestamp
#   2) attached is a picture showing bounding boxes around detected face(s)
#   
#Example usage:
#   ./emailpic.py this_is_the_subject testpic.jpg 0 1 2 3 4
#Example output (message only):
#   "Detected Kevin, roommate1, roommate2, roommate3, Other | 14:03:24"
#
#*At this point "Other" is just a catch-all for non-roommates
#*Timestamp probably unnecessary, but more resolution than email and can reveal delays
#*Obviously embedding the password is a risk but I'm lazy and this will only be on my LAN behind a menacing pfSense firewall

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
from datetime import datetime

count = len(sys.argv) - 3 #people - subject - picture - self = number of people detected
if count < 1: #need at least 1 person
    exit()

sel = [] #array containing args that define detected people according to index in person[]
for i in range(3, 3 + count):
    if sys.argv[i].isdigit(): #barebones half-ass input validation
        sel.append(int(sys.argv[i])) #append person index to selection w/ 3rd arg onward

person = ["Kevin", "roommate1", "roommate2", "roommate3", "Other"]

message = "Detected " + str(person[sel[0]]) #first/only person appended
if count > 1: #make list if > 1 person
    for i in range(1, count): 
        message += ", " + str(person[sel[i]])
            
message += " | " + str(datetime.now().strftime('%H:%M:%S')) #append timestamp to message

#########################################################################################################################
# Below adapted from https://www.linkedin.com/pulse/python-script-send-email-attachment-using-your-gmail-account-singh/ #
#########################################################################################################################

#optionally include other recipients
recipients = ['myemail@gmail.com'] #,'bcc@example.com','bcc2@example.com'] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = str(sys.argv[1])
msg['From'] = 'myemail@gmail.com'
msg['Reply-to'] = 'myemail@gmail.com'
 
msg.preamble = 'Multipart massage.\n'
 
part = MIMEText(str(message)) #email message
msg.attach(part)

#can use filename only if in same dir, or full path (note in this case the full path becomes attached file's name) 
part = MIMEApplication(open(str(sys.argv[2]),"rb").read()) 
part.add_header('Content-Disposition', 'attachment', filename=str(sys.argv[2])) 
msg.attach(part)
 

server = smtplib.SMTP("smtp.gmail.com:587")
server.ehlo()
server.starttls()
server.login("myemail@gmail.com", "mypassword")
 
server.sendmail(msg['From'], emaillist , msg.as_string())
