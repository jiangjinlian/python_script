#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by jiangjinlian on 2017/8/22

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
import requests
import demjson
import json
import time
import datetime
from collections import defaultdict
# from infosys import InfoSysAPI

def get_msg():
    pass



def notify_dd(title=None, msg=None):
    #API_KEY = "13"
    #API_SECRET = "A5D5FD3EC6D041FE977E7131D07D0D8E"
    #infoApi = InfoSysAPI(API_KEY, API_SECRET)
    if title:
        notify_msg = title
    else:
            notify_msg = ''
    if msg and msg != 'None':
        # msg = msg.replace(newLineString, '\n')
        notify_msg += '\n\n%s' % msg
        #infoApi.send_channel_msg(channel_id, notify_msg)
        notify_url = "https://oapi.dingtalk.com/robot/send?access_token=26c4a4be8c2aa3dd08c126c4455525bc4ca51ee47ec55b09e334906be0740265"
        params = dict()
        params["msgtype"] = "text"
        # params["text"] = {"content": "test"}
        params["text"] = {"content": notify_msg}
        
        headers = dict()
        headers["Content-Type"] = "application/json"
        
        # params_json = demjson.encode(params, encoding='utf-8')
        params_json = json.dumps(params)
        print type(params_json)
        #params["text"]["content"] = notify_msg
        response = requests.post(notify_url, data=params_json, headers=headers, verify=False)
        print response.status_code
        print response.text


if __name__ == '__main__':
    
    NOTIFY_MSG = get_msg()
    title = time.strftime("%Y-%m-%d") + " PGC Bugs Statistics"
    notify_dd(title=title, msg=NOTIFY_MSG)

# print "aaaa"
# msg = get_msg()

# get_session_id()
# pass
