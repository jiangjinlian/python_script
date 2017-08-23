#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lina on 2017/4/14


import requests
import demjson
import json
import time
import datetime
from collections import defaultdict
# from infosys import InfoSysAPI

def get_msg():
    
    msg = "Reminding\n\n"
    
    url = 'https://jira.bytedance.com/rest/api/2/search?jql=project%20=%20TTINTPGC%20and%20status%20in%20(Open,%20%22In%20Progress%22,%20Reopened)AND%20issuetype%20%3D%20Bug%20'
    
    headers = dict()
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
    headers["Cookie"] = "%s; _ga=GA1.2.1001356093.1470803696" % get_session_id()
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            
    response = requests.get(url, verify=False, headers=headers)
            
    data = demjson.decode(response.text)
            
    issues = data.get("issues")
            
    issue_total_count = data.get("total")
    msg += "Total: "
    msg += str(issue_total_count)
    msg += "\n\n"
            
    issue_assignee_count = dict()
            
    for issue in issues:
        assignee = issue.get("fields").get("assignee").get("displayName")
        if assignee in issue_assignee_count.keys():
           issue_assignee_count[assignee] += 1
        else:
           issue_assignee_count[assignee] = 1

    reverse_list = sorted(issue_assignee_count.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    
    count_sort = defaultdict(list)
    for key, value in reverse_list:
        count_sort[value].append(key)

    count_sort_desc = sorted(count_sort.items(), lambda x, y: cmp(x[0], y[0]), reverse=True)
    score_user_count = 0
    score_rank = 1
    
    # user_score = dict()
    
    #with open('user_score.json', 'r') as f:
    #    user_score = json.load(f)
    
    weekday = datetime.datetime.now().weekday()
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    for assignee in reverse_list:
        msg += assignee[0]
        msg += ": "
        msg += str(assignee[1])
        msg += "\n"
    
    msg += "\n"
    if not issues:
        issue_key = issues[0].get("key")
    else:
        issue_key = "TTINTPGC-255"
    msg += "Click to see the detail  https://jira.bytedance.com/browse/%s?filter=13359" % issue_key
    # msg += "Click to see the detail  https://jira.bytedance.com/browse/TTINTPGC-77?filter=13359"

    return msg


def get_session_id():
    login_url = "https://jira.bytedance.com/rest/gadget/1.0/login"
    params = dict()
    params["os_username"] = "lina.02"
    params["os_password"] = "ByteDance2016!"
    
    headers = dict()
    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["Referer"] = "https://jira.bytedance.com/secure/Dashboard.jspa"
    headers["Cookie"] = "atlassian.xsrf.token=B2HT-9ELJ-5A6E-IWUO|af20ecd1c8ad03125335ec3c2d6d5df7bf7e2f2b|lout; JSESSIONID=1E6A7DB996CF256537C89785B08777C1; _ga=GA1.2.1001356093.1470803696; _gat=1"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
    
    response = requests.post(login_url, headers=headers, params=params, verify=False)
    set_cookie = response.headers.get("Set-Cookie")
    set_cookie_new = set_cookie.replace("; Path=/", "").replace("HttpOnly,", "")
    
    return set_cookie_new


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
        #notify_url = "https://oapi.dingtalk.com/robot/send?access_token=9fae5015c71453b3cc28512dafa9c4c5aa51e16ae51fb353b23759564ce9f443"
        notify_url = "https://oapi.dingtalk.com/robot/send?access_token=19429c85aaa167668ab7dbceca0766548294c122b9c1e8916647218271a3edc1"
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
