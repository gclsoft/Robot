#!/usr/bin/python
import os
import subprocess
import smtplib
import socket
import datetime
import time
from email.mime.text import MIMEText
import re
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

def start( action ):
    os.system( '. /lib/lsb/init-functions; log_begin_msg "' + action  + ' ..."' );
def success():
    os.system( '. /lib/lsb/init-functions; log_progress_msg done; log_end_msg 0');
def fail():
    os.system( '. /lib/lsb/init-functions; log_end_msg 1');

# Mail server settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Mail account settings
configparser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
CONFIG = configparser.ConfigParser()
CONFIG_FILENAME = os.path.splitext(os.path.abspath(__file__))[0]+'.ini'
CONFIG.read(CONFIG_FILENAME)
send_to =  CONFIG.get('set', 'send_to')
mail_user =  CONFIG.get('set', 'mail_user')
mail_password = CONFIG.get('set', 'mail_password')

# Connect to smtp server, try several times
start( 'Connect to [ ' + smtp_server + ' ]' )
try_max = 5
try_times = 0
try_delay = 1
while try_times <= try_max:
    try_times += 1
    try:
        smtpserver = smtplib.SMTP( smtp_server, smtp_port )
        success()
        break
    except Exception, what:
        if try_times > try_max:
            fail()
            exit()
        else:
            time.sleep( try_delay )
            try_delay *= 2

# Login to mail system
#start( 'Login with ( ' + mail_user + ' )' )
#print("mail user:"+mail_user);
start( 'Login with ( ' + mail_user + ' ,password=set in the ini\n' )

try:
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login( mail_user, mail_password )
    print("22mail user:"+mail_user);
    success()
except Exception, what:
    fail()
    exit()

# Build ip mail and send (for Raspberry only)
today = datetime.date.today()
p = subprocess.Popen( 'ip route list', shell = True, stdout = subprocess.PIPE )
data = p.communicate()
split_data = data[ 0 ].split()
ipaddr = split_data[ split_data.index( 'src' ) + 1 ]
my_ip = 'Your ip is %s' % ipaddr
start( 'Send ip mail ( ' + ipaddr + ' )' )
msg = MIMEText( my_ip )
msg[ 'Subject' ] = 'IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg[ 'From' ] = mail_user
msg[ 'To' ] = send_to
try:
    smtpserver.sendmail( mail_user, [send_to], msg.as_string() )
    success()
except Exception, what:
    fail()
smtpserver.quit()
