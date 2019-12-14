# -*- coding:utf-8 -*-

def progress_bar(total_size, current_percent=0, last_percent=0):
    '''进度条功能'''
    while 1:
        received_size = yield current_percent
        current_percent = int(received_size / total_size * 100)
        if current_percent > last_percent:
            print("*" * int(current_percent / 2) + "{percent}%".format(percent=current_percent), end='\r',
                  flush=True)
            # 把本次循环的percent赋值给last
            last_percent = current_percent