from Queue import Queue
from threading import Thread
from datetime import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from obrez.ouser.models import Facebook, Twitter
from obrez.ouser.utils import AvatarLoader, download_service_avatar

class Command(BaseCommand):
    args = ''
    help = 'Update services avatars'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--threads',
            dest='threads',
            default=5,
            help='Number of max worker threads'),
        )

    def handle(self, *args, **options):
        try:
            num_work_threads = int(options['threads'])
        except ValueError:
            self.stdout.write('Error: Threads must be a number\n')
            return

        q = Queue()
        def worker():
            while True:
                try:
                    item = q.get()
                except Exception, e:
                    return
                download_service_avatar(item.avatar_file, item.avatar_url)
                q.task_done()

        for i in xrange(num_work_threads):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        updated = 0
        services = (Facebook.objects.all(), Twitter.objects.all())
        for service in services:
            for i in service:
                updated += 1
                q.put(i)
        q.join()

        print "%s service(s) was accounts was updated" % (updated)
