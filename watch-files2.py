#!/usr/bin/env python
#coding=utf-8

import os
import logging
import codecs
import smtplib
from email.mime.text import MIMEText
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText as MIMEText2
from email.Utils import COMMASPACE, formatdate
from email import Encoders

tar_dir = '/var/lib/mldonkey/incoming/files/'
temp_dir = '/var/lib/mldonkey/temp/'
log_file = '/var/www/thewawar.tk/notifies/ML-log.txt'
output_file = '/var/www/thewawar.tk/notifies/ML-list.txt'
FILE_ENCODING = 'gbk'

wm = WatchManager()
FLAGS = EventsCodes.ALL_FLAGS
mask = FLAGS['IN_DELETE'] | FLAGS['IN_CREATE'] | FLAGS['IN_MOVED_FROM'] | FLAGS['IN_MOVED_TO'] 

# Logging config
FORMAT = '%(asctime)s - %(message)s'
logger = logging.getLogger('watch_files_log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_file, encoding=FILE_ENCODING)
fh.setFormatter(logging.Formatter(FORMAT))
fh.setLevel(logging.INFO)
logger.addHandler(fh)

# Send Mail config (Common)
##
# Send Mail config (for QQ mail)
mailto_lst = ['thewawar@gmail.com']
mail_host = 'smtp.qq.com'
mail_user = '156970672'
mail_pass = 'yawenmoqingshui0'
mail_postfix = 'qq.com'
me = '%s<%s@%s>' % (mail_user, mail_user, mail_postfix)

# Send Mail config (for postfix)
server_name = 'localhost'
mail_to = ['TheWaWaR <thewawar@gmail.com>']
mail_fro = 'weet <weet@weet-DT>'

def utf8(s):
    return unicode(s, encoding='utf-8')

def sendmail_by_postfix(subject, text, to=mail_to, fro=mail_fro, server=server_name):
    assert type(to)==list
 
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
 
    msg.attach( MIMEText2(text) )
 
    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()


def sendmail_by_qqmail(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = mailto_lst[0]
    s = smtplib.SMTP()
    s.connect(mail_host)
    s.login(mail_user, mail_pass)
    s.sendmail(me, mailto_lst, msg.as_string())
    s.quit()
    s.close()


def update_record():
    tar_files = os.listdir(tar_dir)
    temp_files = os.listdir(temp_dir)
    f = codecs.open(output_file, encoding=FILE_ENCODING, mode='w')

    f.write('Target Files(%d):\n' % len(tar_files))
    f.write('------------\n')
    f.write(utf8('\n'.join(tar_files)))
    f.write('\n\n================================================================================\n\n')
    f.write('Temp Files(%d):\n' % len(temp_files))
    f.write('------------\n')
    f.write(utf8('\n'.join(temp_files)))
    f.close()

    
class PTmp(ProcessEvent):
    def get_path_label(self, event):
	return 'files' if event.path.find('temp') == -1 else 'temp'

    def process_IN_CREATE(self, event):
        logger.info(utf8('Create(%s): %s' % (self.get_path_label(event),
				os.path.join(event.path, event.name))))
        if event.name.split('.')[-1] != 'tmp' and event.path.find('files') > -1:
            sendmail_by_postfix('[Mldonkey-Log]', 'Create file: %s' % event.name)
        update_record()
        
    def process_IN_DELETE(self, event):
        logger.info(utf8('Remove(%s): %s' % (self.get_path_label(event),
				os.path.join(event.path, event.name))))
        if event.name.split('.')[-1] != 'tmp' and event.path.find('files') > -1:
            sendmail_by_postfix('[Mldonkey-Log]', 'Remove file: %s' % event.name)
        update_record()

    def process_IN_MOVED_FROM(self, event):
        logger.info(utf8('Moved from(%s): %s' % (self.get_path_label(event),
				os.path.join(event.path, event.name))))

    def process_IN_MOVED_TO(self, event):
        logger.info(utf8('Moved to(%s): %s' % (self.get_path_label(event),
				os.path.join(event.path, event.name))))
        if event.name.split('.')[-1] != 'tmp' and event.path.find('files') > -1:
            sendmail_by_postfix('[Mldonkey-Log]', 'Add file: %s' % event.name)
        update_record()
        
        
notifier = Notifier(wm, PTmp())
for t_dir in (tar_dir, temp_dir):
    wdd = wm.add_watch(t_dir, mask, rec=True)

update_record()
while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break
