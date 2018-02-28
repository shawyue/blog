#_*_ coding: utf-8 _*_

import os
import sys
from logbook import StreamHandler, RotatingFileHandler
from logbook import set_datetime_format

'''
设置日志时间格式 
参数:
    local : 本地时间
    utc   : utc时间
'''
set_datetime_format('local')

def setup_logger(conf):
    """
    设置 logbook
    """
    console = conf['LOGBOOK_CONSOLE']  # 是否终端输出
    console_level = conf['LOGBOOK_CONSOLE_LEVEL']  # 终端打印日志级别
    file = conf['LOGBOOK_FILE']  # 是否文件输出日志
    file_level = conf['LOGBOOK_FILE_LEVEL']  # 文件输出日志级别
    logfile = conf['LOGBOOK_LOG_FILE']  # 文件输出位置
    backup_count = conf['LOGBOOK_BACKUP_COUNT']  # 文件最大保存数量
    max_size = conf['LOGBOOK_MAX_SIZE']  # 文件保存最大大小
    format_string = conf['LOGBOOK_FORMAT_STRING']  # 日志消息格式
    # logbook终端打印输出设置
    if console:
        StreamHandler(sys.stdout, level=console_level, format_string=format_string, bubble=True).push_application()
    # logbook文件输出设置
    if file:
        dir_path = os.path.dirname(logfile)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        RotatingFileHandler(logfile, mode='a', encoding='utf-8', level=file_level,
                            format_string=format_string, delay=False, max_size=max_size,
                            backup_count=backup_count, filter=None, bubble=True
                            ).push_application()

    return None
