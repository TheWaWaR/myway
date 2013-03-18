#!/usr/bin/env python
#coding=utf-8

import os
import pickle
import time
from datetime import datetime, timedelta
import pytz
from multiprocessing import Process
from flask import Blueprint, request
from weibo import APIClient, APIError

moduleid = 'weibo'
weiboview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

APP_KEY = '781743531'
APP_SECRET = '90849f6986665f841090d2e245e9f31c'
CALLBACK_URL = 'http://ahorn.me/weibo/callback'
TOKENS_FILE = 'tokens'
QUEUE_FILE = 'queue'
PROCESS_STARTED = False

MESSAGES = [u'Good day!',
        u'If you try something again and again and again, one day you\'ll get over it, the delightful sense is worth to fight!',
        u'Happy day, boys!']



def save_token(nt):
    tokens = []
    try:
        input_file = open(TOKENS_FILE, 'rb')
        tokens = pickle.load(input_file)
        input_file.close()
    except IOError:
        print 'INIT tokens file'

    new_token_dict = {}
    for t in tokens + [nt]:
        new_token_dict[t.uid] = t
    new_tokens = new_token_dict.values()
    output_file = open(TOKENS_FILE, 'wb')
    pickle.dump(new_tokens, output_file)
    output_file.close()


def sleep_util_next_day():
    IT = pytz.timezone('Asia/Shanghai')
    dt_day = timedelta(1)
    cn_now = datetime.now(IT)
    next_day = cn_now + dt_day
    next_cn_now = datetime(next_day.year, next_day.month, next_day.day, 2, 0, 0, 0, IT)
    d_secs = int((next_cn_now - cn_now).total_seconds())
    print 'SLEEP <%d> minutes.' % (d_secs/60, )
    time.sleep(d_secs)
    print 'WEAK UP'

def check_queue_OK():
    is_OK = True
    if os.path.isfile(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            l = f.readline()
            if l.startswith('STOP'):
                is_OK = False
    return is_OK

def post_status(client, cont, visb):
    status_ret = None
    try:
        status_ret = client.statuses.update.post(status=cont, visible=visb)
    except APIError, e:
        print e
    return status_ret

def post_comment(client, cont, sid):
    cmt_ret = None
    try:
        cmt_ret = client.comments.create.post(comment=cont, id=sid)
    except APIError, e:
        print e
    return cmt_ret

def update_private_statues():
    count = 0
    while True:
        if not check_queue_OK():
            return
        try:
            try:
                input_file = open(TOKENS_FILE, 'rb')
                tokens = pickle.load(input_file)
                input_file.close()
            except IOError, e:
                print "No Token: ", e
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            status_ids = []
            for t in tokens:
                print 'Update for %s, <%d>' % (str(t.uid), count)
                client.set_access_token(t.access_token, t.expires_in)
                for i in range(3):
                    status_ret = post_status(client, u'Test private update ' + str(i)*5, 2)
                    if status_ret is None:
                        continue
                    print 'POSTED %d' % status_ret.id
                    status_ids.append(status_ret.id)
                    for j in range(3):
                        time.sleep(1)
                        cmt_ret = post_comment(client, u'Good post ' + str(j)*5, status_ret.id)
                        if cmt_ret is None:
                            continue
                    time.sleep(1)
                post_status(client, MESSAGES[count%len(MESSAGES)], 2)
            time.sleep(15)
            print 'POSTED ids %r' % status_ids
            for sid in status_ids:
                client.statuses.destroy.post(id=sid)
                time.sleep(1)
            count += 1
            sleep_util_next_day()
        except IOError, e:
            print "Network Error?: ", e
            time.sleep(60)


def start_process():
    p = Process(target=update_private_statues, args=())
    p.start()


# ==============================================================================
#  Views
# ==============================================================================
@weiboview.route('/')
def register():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return u'''<a href="%s">%s</a>''' % (url, url)

@weiboview.route('/start')
def start():
    global PROCESS_STARTED
    if not PROCESS_STARTED:
        start_process()
        PROCESS_STARTED = True
    return 'OK'


@weiboview.route('/stop')
def stop():
    with open(QUEUE_FILE, 'w') as f:
        f.write('STOP')
    return 'OK'

@weiboview.route('/callback')
def callback():
    code = request.args.get('code', '')
    print 'New CODE: ' + code
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    t = client.request_access_token(code)
    access_token = t.access_token # 新浪返回的token，类似abc123xyz456
    expires_in = t.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4

    # TODO: 在此可保存access token
    client.set_access_token(access_token, expires_in)
    # print client.statuses.update.post(status=u'测试OAuth 2.0发微博')

    save_token(t)
    return 'OK'

