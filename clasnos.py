#!/usr/bin/python3

import os, sh, time
import conf
import cutils as utils

from utiltools import shellutils



q = utils.Queue()

q.l.unlock()

#QUEUE_NORMAL_SLEEP = 0.1
#QUEUE_EMPTY_SLEEP = 2
QUEUE_EMPTY_SLEEP = 4
QUEUE_NORMAL_SLEEP = 0.8

def queue_processor():
   while True:
      #print('queue tick')
      print('q len: %i lock: %r' % (q.len(), q.l.is_locked()))

      time.sleep(QUEUE_NORMAL_SLEEP)


      q.start_crit()

      q.update()
      print('queue len: %i' % (q.len(),))

      tick_data = q.peak()

      if tick_data is None:
         print('empty queue')
         q.end_crit()
         time.sleep(QUEUE_EMPTY_SLEEP)
         continue

      before_dw = os.getcwd()

      url = tick_data['url']
      storage_path = tick_data['storage_path']
      new_name = tick_data['new_name']

      print('processing: %s' % (url, ))

      sh.mkdir('-p', storage_path)
      sh.cd(storage_path)

      if not new_name == '':
         wget_args = '--output-document=%s' % (new_name,)
         utils.wget(url, wget_args)
      else:
         utils.wget(url)

      sh.cd(before_dw)

      q.get() #remove from TODO queue

      q.end_crit()

      pass

   pass


def main():
   is_master = conf.c['is_master']

   if not is_master:
      def flask_runner():
         cmd = './run.sh ' + conf.c['port']
         shellutils.exec_bash(cmd)

      shellutils.func_thread(flask_runner)

      queue_processor()
   else:
      print('use python repl: python3; import master;')

if __name__ == "__main__":
   main()


