# -*- coding:utf-8 -*-
import logging
from server.conf.settings import LOG_PATH

def my_log():
    #生成logger对象
    whw_logger = logging.getLogger('logs.log')
    whw_logger.setLevel(logging.INFO)
    # 如果handlers属性为空则添加文件操作符，不为空直接写日志
    if not whw_logger.handlers:
        #生成handler对象
        whw_fh = logging.FileHandler(LOG_PATH)
        whw_fh.setLevel(logging.INFO)
        #生成Formatter对象
        file_formatter = logging.Formatter(' %(asctime)s - %(name)s - %(levelname)s - %(message)s ')
        #把formatter对象绑定到handler对象中
        whw_fh.setFormatter(file_formatter)
        # 把handler对象绑定到logger对象中
        whw_logger.addHandler(whw_fh)
    return whw_logger