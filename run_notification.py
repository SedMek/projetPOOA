import time
import datetime
while 1:
    runfile('/home/insight/pooa/Local-projet-POOA/projetpooa/observer_pattern.py', wdir='/home/insight/pooa/Local-projet-POOA/projetpooa/venv')
    print(str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second))
    time.sleep(0.5)
