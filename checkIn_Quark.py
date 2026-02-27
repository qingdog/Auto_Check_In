"""
new Env('夸克自动签到')
cron: 0 9 * * *

V2版-目前有效
使用移动端接口修复每日自动签到，移除原有的“登录验证”，参数有效期未知

V1版-已失效
受大佬 @Cp0204 的仓库项目启发改编
源码来自 GitHub 仓库：https://github.com/Cp0204/quark-auto-save
提取“登录验证”“签到”“领取”方法封装到下文中的“Quark”类中

Author: BNDou
Date: 2024-03-15 21:43:06
LastEditTime: 2024-08-03 21:07:27
FilePath: /Auto_Check_In/checkIn_Quark.py
Description:
抓包流程：
    【手机端】
    ①打开抓包，手机端访问签到页
    ②找到url为 https://drive-m.quark.cn/1/clouddrive/capacity/growth/info 的请求信息
    ③复制url后面的参数: kps sign vcode 粘贴到环境变量
    环境变量名为 COOKIE_QUARK 多账户用 回车 或 && 分开
    user字段是用户名 (可是随意填写，多账户方便区分)
    例如: user=张三; kps=abcdefg; sign=hijklmn; vcode=111111111;
"""
import asyncio
import datetime
import json
import logging
import os
import re
import sys
import traceback

import aiofiles
import requests

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3 import Retry

# 加载 .env 文件，任务每天早上 9 点触发执行
load_dotenv()
ACCOUNTS_JSON = "./accounts.json"

session = requests.Session()
# 配置重试策略
retries = Retry(
    total=5,  # 最多重试 5 次
    backoff_factor=1,  # 退避因子，重试的间隔时间会按照指数增长，例如 1s, 2s, 4s, 8s, 16s...
    status_forcelist=[500, 502, 503, 504],  # 遇到这些 HTTP 状态码时触发重试
    read=7,  # 读取超时
    redirect=5,  # 最多5次重定向
    connect=7  # 连接超时重试次数 第7次64s
)
# 所有的 HTTPS 请求 都会使用这个 HTTPAdapter，从而启用我们定义的重试策略
session.mount("https://", HTTPAdapter(max_retries=retries))


async def get_secrets_accounts():
    try:
        async with aiofiles.open(f'{ACCOUNTS_JSON}', mode='r', encoding='utf-8') as f:
            accounts_json = await f.read()
        accounts = json.loads(accounts_json)
    except Exception as e:
        print(f'读取 {ACCOUNTS_JSON} 文件时出错: {e}')
        return
    for account in accounts:
        os.environ['SMTP_SERVER'] = account['SMTP_SERVER']
        os.environ['SMTP_SSL'] = account['SMTP_SSL']
        os.environ['SMTP_EMAIL'] = account['SMTP_EMAIL']
        os.environ['SMTP_PASSWORD'] = account['SMTP_PASSWORD']
        os.environ['SMTP_NAME'] = account['SMTP_NAME']
        # 邮件标题兼容处理
        if os.environ['SMTP_NAME'] == "夸克登录失败（自己发送给自己）":
            os.environ['SMTP_NAME'] = "夸克自动登录脚本通知"


asyncio.run(get_secrets_accounts())

# 测试用环境变量
# os.environ['COOKIE_QUARK'] = ''

try:  # 异常捕捉
    from utils.notify import send  # 导入消息通知模块
except Exception as err:  # 异常捕捉
    print('%s\n❌加载通知服务失败~' % err)


# 获取环境变量
def get_env():
    # 判断 COOKIE_QUARK是否存在于环境变量
    if "COOKIE_QUARK" in os.environ:
        # 读取系统变量以 \n 或 && 分割变量
        cookie_list = re.split('\n|&&', os.environ.get('COOKIE_QUARK'))
    else:
        # 标准日志输出
        print('❌未添加COOKIE_QUARK变量')
        send('夸克自动签到', '❌未添加COOKIE_QUARK变量')
        # 脚本退出
        sys.exit(0)

    return cookie_list


class Quark:
    """
    Quark类封装了签到、领取签到奖励的方法
    """

    def __init__(self, user_data):
        """
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        """
        self.param = user_data

    def convert_bytes(self, b):
        """
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回 MB GB TB
        """
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024
            i += 1
        return f"{b:.2f} {units[i]}"

    def get_growth_info(self):
        """
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        """
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        response = session.get(url=url, params=querystring).json()
        # print(response)
        if response.get("data"):
            return response["data"]
        else:
            logging.error(f"----------夸克网盘开始签到----------于北京时间 {get_utc8_beiji_time()}失败！！！{response}")
            return False

    def get_growth_sign(self):
        """
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        """
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        data = {"sign_cyclic": True}
        response = session.post(url=url, json=data, params=querystring).json()
        # print(response)
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def queryBalance(self):
        """
        查询抽奖余额
        """
        url = "https://coral2.quark.cn/currency/v1/queryBalance"
        querystring = {
            "moduleCode": "1f3563d38896438db994f118d4ff53cb",
            "kps": self.param.get('kps'),
        }
        response = session.get(url=url, params=querystring).json()
        # print(response)
        if response.get("data"):
            return response["data"]["balance"]
        else:
            return response["msg"]

    def do_sign(self):
        """
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        """
        msg, log = "", ""
        # 每日领空间
        growth_info = self.get_growth_info()
        if growth_info:
            log += (
                f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
                f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
                f"签到累计容量：")
            if "sign_reward" in growth_info['cap_composition']:
                log += f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
            else:
                log += "0 MB\n"
            if growth_info["cap_sign"]["sign_daily"]:
                log += (
                    f"✅ 签到日志: 今日已签到+{self.convert_bytes(growth_info['cap_sign']['sign_daily_reward'])}，"
                    f"连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})\n"
                )
            else:
                sign, sign_return = self.get_growth_sign()
                if sign:
                    log += (
                        f"✅ 执行签到: 今日签到+{self.convert_bytes(sign_return)}，"
                        f"连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})\n"
                    )
                else:
                    log += f"❌ 签到异常: {sign_return}\n"
        else:
            log += f"❌ 签到异常: 获取成长信息失败\n"

        # 查询抽奖余额
        balance = self.queryBalance()
        if isinstance(balance, int):
            if balance > 0:
                log += f"还剩{balance}次抽奖"
            else:
                log += f"暂无抽奖次数"
            msg += log + ", 抽奖功能暂未开发\n"
        else:
            msg += log + balance + "\n"

        return msg


msg = ""


def main():
    """
    主函数
    :return: 返回一个字符串，包含签到结果
    """
    global msg
    # msg = ""
    global cookie_quark
    cookie_quark = get_env()

    print("✅ 检测到共", len(cookie_quark), "个夸克账号\n")

    i = 0
    while i < len(cookie_quark):
        # 获取user_data参数
        user_data = {}  # 用户信息
        for a in cookie_quark[i].replace(" ", "").split(';'):
            if not a == '':
                user_data.update({a[0:a.index('=')]: a[a.index('=') + 1:]})
        # print(user_data)
        # 开始任务
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        # 登录
        log = Quark(user_data).do_sign()
        msg += log + "\n"

        i += 1

    send_notify_if_friday('夸克自动签到', msg)
    # 手动输出（不使用通知py模块进行打印到控制台）
    logging.info(msg)
    # print(msg)
    # try:
    #     send('夸克自动签到', msg)
    # except Exception as err:
    #     print('%s\n❌ 错误，请查看运行日志！' % err)

    return msg[:-1]


def send_notify_if_friday(m, mm):
    """发送成功通知，在周五"""
    today = datetime.datetime.today().weekday()
    #if today == 4:  # 周五
    #    send(m, mm)
    today = datetime.datetime.today()

    # 判断日期是否为每月的1号
    if today.day == 1:
        print("今天是每月1号，执行任务...")
        send(m, mm)


def get_utc8_beiji_time():
    return (datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')


def get_utc0_time():
    return (datetime.datetime.now(tz=datetime.timezone.utc)).strftime('%Y-%m-%d %H:%M:%S')


try:  # 异常捕捉
    import util_logging
except Exception as err:
    logging.error(f"\n❌加载日志失败~ {err}", exc_info=True)


def sign_in():
    """夸克登录签到"""
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"----------夸克网盘开始签到----------于北京时间 {get_utc8_beiji_time()}（UTC时间 {get_utc0_time()}）")

    ms = None
    try:
        ms = main()
    except Exception as err:
        logging.error(err, exc_info=True)
        stack_info = traceback.format_exc()  # 获取完整堆栈信息
        send("登录异常", f"{msg}\n❌ 错误，请查看运行日志！：{stack_info}")
    print("----------夸克网盘签到完毕----------")
