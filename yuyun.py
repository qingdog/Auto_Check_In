#!/usr/bin/python3
# -- coding: utf-8 --
# @Time : 2023/6/30 10:23
# -------------------------------
# cron "0 0 6,8,20 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('雨云签到');

import json, requests, os, time


##变量雨云账号密码 注册地址https://www.rainyun.com/NTY1NzY=_   登录后积分中心里面 赚钱积分 (如绑定微信 直接就有2000分）就可以用积分兑换主机 需要每天晚上八点蹲点

# yyusername =os.getenv ("yyusername")#line:12
# yypassword =os.getenv ("yypassword")#line:13
def login_sign(yy_username, yy_password):  # line:17
    session = requests.session()  # line:18
    sign_response = session.post('https://api.v2.rainyun.com/user/login',
                                 headers={"Content-Type": "application/json"}, data=json.dumps(
            {"field": f"{yy_username}", "password": f"{yy_password}"}))  # line:19
    x_csrf_token = None
    if sign_response.text.find("200") > -1:  # line:20
        print("登录成功")  # line:21
        x_csrf_token = sign_response.cookies.get_dict()['X-CSRF-Token']  # line:22
    else:  # line:24
        print(f"登录失败，响应信息：{sign_response.text}")  # line:25
    x_csrf_token_json = {'x-csrf-token': x_csrf_token, }  # line:31
    tasks_response = session.post('https://api.v2.rainyun.com/user/reward/tasks',
                                  headers=x_csrf_token_json,
                                  data=json.dumps({"task_name": "每日签到", "verifyCode": ""}))  # line:32
    print('开始签到：签到结果 ' + tasks_response.text)  # line:33


# if __name__ == '__main__':  # line:44
def sign_in():
    """https://app.rainyun.com/account/reward/earn#获取积分"""
    for i in range(len(os.getenv("YY_USERNAME").split('#'))):
        yy_username = os.getenv("YY_USERNAME").split('#')[i]
        yy_password = os.getenv("YY_PASSWORD").split('#')[i]
        login_sign(yy_username, yy_password)  # line:45
