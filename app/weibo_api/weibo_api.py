# -*- coding: utf-8 -*-

from weibo.weibo import APIClient

def send_weibo(client, auth_token, user_id, to_name, test_id):
    client.statuses.update.post(status = "@" + to_name + ", I have some questions to ask you, please click http://app.weibo.com/socialfaqfaq/answer?test_id=" + test_id)

def get_name(client, auth_token, user_id):
    list = client.users.show.get(access_token = auth_token, uid = user_id)
    return list['name']

def get_friend(client, auth_token, user_id):
    l = client.friendships.friends.get(access_token = auth_token, uid = user_id)
    l = l['users']
    a = []
    for i in range(len(l)):
        a.append(l[i]['name'])
    return a
