import time
import schedule
import threading

def job():
    print("I'm working... in job1  start")
    time.sleep(15)
    print("I'm working... in job1  end")

def job2():
    print("I'm working... in job2")

def run_threaded(job_func):
     job_thread = threading.Thread(target=job_func)
     job_thread.start()

schedule.every(10).seconds.do(run_threaded,job)
schedule.every(10).seconds.do(run_threaded,job2)


while True:
    schedule.run_pending()
