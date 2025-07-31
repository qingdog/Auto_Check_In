#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : github@wd210010 https://github.com/wd210010/just_for_happy
# @Time : 2023/3/27 13:23
# -------------------------------
# cron "30 5 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('IKuuu机场签到帐号版')

'''import requests, re

import requests
import os


# import notify

# export ikuuu='邮箱&密码'      多号#号隔开

def main():
    r = 1
    oy = ql_env()
    print("共找到" + str(len(oy)) + "个账号")
    for i in oy:
        print("------------正在执行第" + str(r) + "个账号----------------")
        email = i.split('&')[0]
        passwd = i.split('&')[1]
        sign_in(email, passwd)
        r += 1


def sign_in(email, passwd):
    try:
        body = {"email": email, "passwd": passwd, }
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        res = requests.get('https://ikuuu.club/', headers=headers)
        url = re.findall('target="_blank">(.*?)</a>', res.text, re.S)
        for i in range(len(url)):
            resp = requests.session()
            resp.post(f'{url[i]}auth/login', headers=headers, data=body)
            ss = resp.post(f'{url[i]}user/checkin').json()
            #         print(ss)
            if 'msg' in ss:
                print("ikuuu.club " + ss['msg'])
                # notify.send("IKuuu机场签到", ss['msg'])
                break
    except:
        print('ikuuu.club 请检查帐号配置是否错误')
        # notify.send("IKuuu机场签到", '请检查帐号配置是否错误')


def ql_env():
    # if "ikuuu" in os.environ:
    if os.getenv("IKUUU"):
        token_list = os.environ['IKUUU'].split('#')
        # token_list = os.getenv("ikuuu").split('#')
        if len(token_list) > 0:
            return token_list
        else:
            print("ikuuu变量未启用")
            # sys.exit(1)
    else:
        print("未添加ikuuu变量")
        # sys.exit(0)


if __name__ == '__main__':
    main()'''
    
#document.querySelectorAll("#swal2-content")[0].textContent
import re
import logging
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright, url="https://ikuuu.club") -> None:
    #browser = playwright.chromium.launch(headless=False)
    from find_chrome_util import find_chrome_util
    import platform
    import os
    from dotenv import load_dotenv
    load_dotenv()
    logging.getLogger().setLevel(logging.INFO)
    browser = playwright.chromium.launch(headless=platform.system() != "Windows", executable_path=find_chrome_util())
    context = browser.new_context(color_scheme="dark", viewport={"width": 1920, "height": 1080}) # 为了确定UI整体布局位置
    
    page = context.new_page()
    page.goto(url)
    
    try: 
        with page.expect_popup() as page1_info:
            #page.get_by_role("link", name="https://ikuuu.ch/").click() ikuuu.ch ikuuu.de https://ikuuu.one/
            print(page.locator("a").nth(0).inner_html())
            page.locator("a").nth(0).click()
        page1 = page1_info.value
        page1.locator("html").click()
    except Exception as e: 
        logging.error(e, exc_info=True)
    
    page1.get_by_role("textbox", name="邮箱").click()
    page1.get_by_role("textbox", name="邮箱").fill("qingdoor@gmail.com")
    page1.get_by_role("textbox", name="密码").click()
    page1.get_by_role("textbox", name="密码").fill("qingdoor@gmail.com")
    page1.get_by_role("button", name="登录", exact=True).click()
    
    page1.get_by_role("button", name="Read").click()
    page1.get_by_role("link", name=" 每日签到").click()
    logging.info(page1.locator("#swal2-title").text_content())
    expect(page1.locator("#swal2-title")).to_contain_text("签到成功")
    
    #print(page.query_selector(".row").text_content())
    
    #page.wait_for_timeout(20 * 1000)

    # ---------------------
    context.close()
    browser.close()


def main():
    with sync_playwright() as playwright:
        for url in ["https://ikuuu.club","https://ikuuu.ch","https://ikuuu.de","https://ikuuu.one"]:
            try: 
                run(playwright, url)
                break
            except Exception as e: 
                logging.error(e, exc_info=True)

if __name__ == '__main__':
    main()
