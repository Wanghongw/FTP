# -*- coding:utf-8 -*-
import os
import sys
from server.core.main import main

# 往sys.path里添加项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    main()
