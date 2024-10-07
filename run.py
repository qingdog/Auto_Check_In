import logging

import checkIn_Quark
import yuyun

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    checkIn_Quark.sign_in()
    logging.info("----------雨云自动登录开始----------")
    yuyun.sign_in()
