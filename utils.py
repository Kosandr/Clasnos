
import sh, logging
from utiltools import shellutils
import conf

class Queue:
   def __init__(self, path=None):
      config_dir = conf.c['config_dir']

      if path is None:
         path = config_dir + 'queue.json'

      print(path)
      self.path = path

      self.l = Lock(config_dir + 'queue.lock')
      self.update()


      if not self.data: #shellutils.file_exists(path):
         default_json = {
            'todo' : [],
            'done' : []
         }

         self.data = default_json
         shellutils.write_json(path, default_json)

      pass

   def start_crit(self):
      self.l.lock()

   def end_crit(self):
      self.l.unlock()

   def len(self):
      self.update()
      return len(self.data['todo'])

   def update(self):
      self.data = shellutils.read_json(self.path)

   def add(self, item):
      self.data['todo'].append(item)
      print(self.data)
      shellutils.write_json(self.path, self.data)

   def peak(self):
      self.update()
      if len(self.data['todo']) == 0:
         return None
      return self.data['todo'][0]

   def get(self):

      ret = self.peak()

      if not ret:
         return None

      self.data['todo'] = self.data['todo'][1:]
      self.data['done'].append(ret)

      shellutils.write_json(self.path, self.data)
      return ret



class Lock:
   def __init__(self, path=None):
      if path is None:
         path = conf.c['config_dir'] + 'default.lock'
      self.path = path

      if not shellutils.file_exists(path):
         shellutils.write_file(path, 'free')

   def is_locked(self):

      data = shellutils.read_file(self.path)

      if data == 'locked':
         return True
      elif data == 'free':
         return False
      return None

   def unlock(self):
      shellutils.write_file(self.path, 'free')

   def lock(self, wait_increments=0.1):
      import time
      while self.is_locked():
         time.sleep(wait_increments)

      shellutils.write_file(self.path, 'locked')


'''
q = Queue()
l = Lock()

l.lock()
q.add({'http://sdfdsf', '/tmp/blah/test'})
q.add({'http://sdf', '/tmp/blah/test'})
l.unlock()

'''


def wget(url, args=None):
   ret = None
   try:
      if args is not None:
         ret = sh.wget(url, args)
      else:
         ret = sh.wget(url)
   except Exception as e:
      print('wget error: ' + url)
      logging.error('wget error: ' + url)
   return ret


