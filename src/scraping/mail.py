import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import smtplib


def send_mail(sender, receiver, subject, other):
    # sender += "@miamioh.edu"
    # receiver += "@miamioh.edu"
    msg = f"Subject:{subject}\r\nFrom:{sender}\r\nTo:{receiver}\r\nSid says hi --\n{other}"
    server = smtplib.SMTP(host='mailfwd.miamioh.edu', port=25)
    server.set_debuglevel(1)
    server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg)
    server.quit()

send_mail("vahhs@miamioh.edu", 'haidera@miamioh.edu', "HI HUNTER", "HI FROM SID!!! WHY DID YOU EMAIL YOURSELF!!")