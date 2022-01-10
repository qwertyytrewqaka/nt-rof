from apscheduler.schedulers.blocking import BlockingScheduler
import main

sched = BlockingScheduler()


def timed_job():
    main.main()

sched.add_job(timed_job, 'interval', seconds=20, jitter=1, max_instances=2)


sched.start()
