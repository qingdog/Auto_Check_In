import json
import asyncio
import platform
import subprocess

from pyppeteer import launch, browser
from datetime import datetime, timedelta, timezone
import aiofiles
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PIG_URL = os.getenv('PIG_URL')
PIG_USERNAME = os.getenv('PIG_USERNAME')
PIG_PASSWORD = os.getenv('PIG_PASSWORD')
# github秘密环境变量
# ACCOUNTS_JSON = "./accounts.json"
# 如果使用本地指定地址的浏览器
chrome_executable_path = None
is_headless = True

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if TELEGRAM_CHAT_ID == "xxx":
    chrome_executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    is_headless = False
else:
    def find_chrome_path():  # Linux
        try:
            path = subprocess.check_output(['which', 'google-chrome']).decode().strip()
            return path
        except subprocess.CalledProcessError:
            return None


    chrome_executable_path = find_chrome_path()

# 全局浏览器实例
chrome_browser: browser.Browser = None


def format_to_iso(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


async def delay_time(ms):
    await asyncio.sleep(ms / 1000)


async def chrome_init():
    global chrome_browser
    global page1

    # page = None  # 确保 page 在任何情况下都被定义
    if not chrome_browser:
        chrome_browser = await launch(headless=is_headless, args=['--no-sandbox', '--disable-setuid-sandbox'],
                                      executablePath=chrome_executable_path)
    # 获取所有打开的页面
    pages = await chrome_browser.pages()
    for p in pages:
        page1 = p
        break
    # 全局设置导航超时时间为 60 秒
    page1.setDefaultNavigationTimeout(60000 * 3)

    # 等待1s再打开页面
    delay = random.randint(500, 1000)
    await delay_time(delay)

    if page1 is None:
        page1 = await chrome_browser.newPage()
    # page=page
    #    await page1.goto("https://www.baidu.com")
    return page1


async def login(username, password, url):
    try:
        url = f'https://{url}/auth/login'
        await page1.goto(url)

        username_input = await page1.querySelector('#email')
        if username_input:
            # 在浏览器页面的上下文中执行 JavaScript 操作 username_input 作为参数传入清空输入框
            await page1.evaluate('''(input) => input.value = ""''', username_input)

        await page1.type('#email', username)
        await page1.type('#passwd', password)

        login_button = await page1.querySelector('#login')
        if login_button:
            await login_button.click()
        else:
            raise Exception('无法找到登录按钮')

        await page1.content()
        await page1.waitForNavigation()

        checkin_button = await page1.querySelector('a.btn.btn-brand.btn-flat')
        if checkin_button:
            await checkin_button.click()
        else:
            print('无法找到签到按钮')


        is_logged_in = await page1.evaluate('''() => {
            const logoutButton = document.querySelector('a[href="/user/logout"]');
            return logoutButton !== null;
        }''')

        checkin_button = await page1.querySelector('a.btn.btn-brand.btn-flat')
        if checkin_button:
            await checkin_button.click()
        else:
            raise Exception('无法找到签到按钮')

        return is_logged_in

    except Exception as e:
        print(f'{url} 账号 {username} 登录时出现错误: {e}')
        return False
    finally:
        pass


async def main():
    # try:
    #     async with aiofiles.open(f'{ACCOUNTS_JSON}', mode='r', encoding='utf-8') as f:
    #         accounts_json = await f.read()
    #     accounts = json.loads(accounts_json)
    # except Exception as e:
    #     print(f'读取 {ACCOUNTS_JSON} 文件时出错: {e}')
    #     return

    # for account in accounts:
    #     username = account['username']
    #     password = account['password']
    #     url = account['url']

    # ===登录===
    await chrome_init()
    is_logged_in = await login(PIG_USERNAME, PIG_PASSWORD, PIG_URL)

    if page1:
        # await page1.close() # 关闭页面
        pass
    await chrome_browser.close()

    if is_logged_in:
        # 获取当前 UTC 时间
        now_utc = format_to_iso(datetime.now(timezone.utc))
        # 获取当前北京时间（UTC+8）
        now_beijing = format_to_iso(datetime.now(timezone.utc) + timedelta(hours=8))
        print(f' 于北京时间 {now_beijing}（UTC时间 {now_utc}）登录成功！')
    else:
        print(f'请检查{PIG_USERNAME}账号和密码是否正确。')

    delay = random.randint(1000, 8000)
    await delay_time(delay)

    # await send_telegram_message(message)
    print(f'🐖^(*￣(oo)￣)^=================================执行完成！')


async def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '问题反馈❓',
                        'url': 'https://t.me/yxjsjl'
                    }
                ]
            ]
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到Telegram失败: {response.text}")
    except Exception as e:
        print(f"发送消息到Telegram时出错: {e}")


def run(cls, run_main, *args, is_old_run=True):
    """执行异步函数"""
    if is_old_run:
        cls.new_event_loop.run_until_complete(run_main(*args))
    else:
        # 处理win平台 asyncio.run() 执行完所产生的异常
        if platform.system() == 'Windows':
            async def win_shutdown_default_executor():
                await asyncio.BaseEventLoop.shutdown_default_executor()
                await asyncio.sleep(0.25)
                # await asyncio.sleep(3)

            asyncio.BaseEventLoop.originalShutdownFunc = win_shutdown_default_executor
            # asyncio.BaseEventLoop.set_exception_handler(self=cls.new_event_loop, handler=win_shutdown_default_executor)
        # 运行主函数
        asyncio.run(run_main(*args))


if __name__ == '__main__':
    asyncio.run(main())
