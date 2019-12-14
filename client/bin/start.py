# -*- coding:utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# print(BASE_DIR)
# print(sys.path)
if __name__ == '__main__':
    from client.core.main import main
    main()