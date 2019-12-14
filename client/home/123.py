import time
count= 0
for i in range(30):
    time.sleep(1)
    count = i
    print('\r'+'%s*'%count,end=' ',flush=True)
