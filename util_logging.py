import logging
import os
import sys
import time


class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # 定义颜色
        color_codes = {
            logging.DEBUG: '\033[94m',  # 蓝色
            logging.INFO: '\033[92m',  # 绿色
            logging.WARNING: '\033[93m',  # 黄色
            logging.ERROR: '\033[91m',  # 红色
            logging.CRITICAL: '\033[95m'  # 紫色
        }
        # 添加颜色代码
        record.levelname = color_codes.get(record.levelno, '\033[0m') + record.levelname + '\033[0m'
        return super().format(record)


projectPath = os.path.abspath('.')
logPath = projectPath + '\\logs\\'
# 如果 logs 目录不存在，则创建
if not os.path.exists(logPath):
    os.makedirs(logPath)
log_name = os.path.join(logPath, '%s.log' % (time.strftime('%Y%m%d_%H')))

# LOG日志记录
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] - [%(filename)s:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    # stream=sys.stdout,
                    # filename='my.log',
                    # filemode='a',
                    handlers=[
                        logging.FileHandler(f"{log_name}", encoding="UTF-8", mode='a'),  # 文件日志处理器
                        logging.StreamHandler(sys.stdout)  # 控制台日志处理器
                    ]
                    )
logger = logging.getLogger()
# 获取控制台日志处理器
console_handler = logger.handlers[-1]
# 创建控制台日志格式化器（包含颜色代码）
console_handler.setFormatter(ColoredFormatter(
    fmt='[%(asctime)s] - [%(filename)s:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S'
))