from django_cron import CronJobBase, Schedule
from jiaquan import *
from jiaquan import *
from ywbserver.settings import CIRCLE_IDLE_DAYS
from django.utils import timezone

class DelCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,)
    #RUN_AT_TIMES = ['2:30']
    #schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'jiaquan.cron'    # a unique code

    def do(self):
        print('this is a cron job.')
        now = timezone.now()
        for circle in Circle.objects.all():
            print(now - circle.last_access)
            if (now - circle.last_access).days >= now - circle.last_access:
                circle.not_deleted = False
                circle.save()
        return    # do your thing here