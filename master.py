
import requests, sh
import conf
import cutils
from utiltools import shellutils


def get_slave_num_from_ip(slave_ip):
   for i, x in enumerate(conf.c['slaves']):
      if x == slave_ip:
         return i
   return None

def get_slave_ip_from_num(slave_num):
   print('kk:', slave_num)
   return conf.c['slaves'][int(slave_num)]


def post_req(ip, port, json_cmd, protocol='http', timeout=None):


   url = '%s://%s:%s' % (protocol, ip, port)

   json_cmd['pass'] = conf.c['pass']

   resp = None
   if timeout is not None:
      resp = requests.post(url, data=json_cmd, timeout=timeout)
   else:
      resp = requests.post(url, data=json_cmd)

   print(resp.text)
   #return resp.text
   return resp.json() #text

def send_cmd(slave_num, cmd, timeout=None):
   slave_ip = get_slave_ip_from_num(slave_num)
   slave_port = conf.c['port']

   return post_req(slave_ip, slave_port, cmd, timeout=timeout)


##########MASTER COMMANDS

def s_get_queue_len(slave_num):
   ret = send_cmd(slave_num, {'cmd' : 'queue_len'})
   print('s_get_queue_len ret: ', ret)
   if conf.is_err(ret):
      return None
   else:
      return ret['data']['ret']

#return down or active
def s_get_status(slave_num):
   try:
      ret = send_cmd(slave_num, {'cmd' : 'status'}, timeout=1)
   except:
      return 'down'

   if conf.is_err(ret):
      return 'down'
   else:
      return ret['data']['status']


def s_queue_dw(slave_num, url, storage_path, new_name=''):
   json_cmd = {
      'cmd' : 'queue_dw',
      'url' : url,
      'storage_path' : storage_path,
      'new_name' : new_name
   }
   return send_cmd(slave_num, json_cmd)


#slave_name = script name on slave
def s_upload_script(slave_num, slave_name, master_path):
   data = shellutils.read_file(master_path)

   json_cmd = {
      'cmd' : 'upload_script',
      'slave_name' : slave_name,
      'data' : data
   }

   return send_cmd(slave_num, json_cmd)

def s_queue_script(slave_num, script_name, url, storage_path, new_name=''):

   import base64
   url = base64.b64encode(bytes(url, 'utf-8')).decode('utf-8')
   #import binascii
   #url = binasci.hexlify(url)

   json_cmd = {
      'cmd' : 'queue_script',
      'script_name' : script_name,
      'url' : url,
      'storage_path' : storage_path,
      'new_name' : new_name
   }

   return send_cmd(slave_num, json_cmd)


def s_add_key(slave_num):
   key = str(sh.cat('/root/.ssh/id_rsa.pub'))
   json_cmd = {
      'cmd' : 'add_key',
      'key' : key
   }
   print(key)
   return send_cmd(slave_num, json_cmd)


def s_sync(slave_num, slave_dir, master_dir): #from slaves to master
   slave_ip = get_slave_ip_from_num(slave_num)

   cutils.rsync('root', slave_ip, slave_dir, master_dir)

   return {} #return send_cmd(slave_num, json_cmd)


def cluster_rsync_paths(slave_ips, master_path, slave_path):
   for ip in slave_ips:
      slave_num = get_slave_num_from_ip(ip)
      s_sync(slave_num, slave_path, master_path)
   pass





#initializes, checks every slave status, distributes work
class Worker:

   def __init__(self):
      self.slave_ips = conf.c['slaves']
      self.get_good_slaves()

   def get_good_slaves(self):
      '''Returns ip addresses of good slaves

      '''

      self.good_slave_ips = []

      print(self.slave_ips)

      for slave_ip in self.slave_ips:
         slave_num = get_slave_num_from_ip(slave_ip)
         stat = s_get_status(slave_num)
         if stat == 'active':
            self.good_slave_ips.append(slave_ip)
         print('x')

      print('good slaves:', self.good_slave_ips)

      return self.good_slave_ips

   #returns slave index with least tasks
   def get_slave_min_tasks(self):
      min_tasks = 1000000000

      all_min_indices = []

      curr_slave_index = None

      for slave_ip in self.good_slave_ips:
         slave_index = conf.c['slaves'].index(slave_ip)
         ret = s_get_queue_len(slave_index)

         if ret is None:
            print('get_slave_min_tasks(): Bad slave ', slave_ip)
            continue
         if ret < min_tasks:
            min_tasks = ret
            curr_slave_index = slave_index
            all_min_indices = [slave_index]


         if ret == min_tasks:
            all_min_indices.append(slave_index)

      import random

      print('min_tasks:', min_tasks)
      i = random.randint(0, len(all_min_indices) - 1)
      return all_min_indices[i]

      #return curr_slave_index

#END class Worker



'''
#post_req('slave-ip', '7331', {'cmd':'hi'})


urls = [
   'url1',
   'url2',
   'url3',
   'url4'
]

#print(s_get_status(0))
#print(s_queue_dw(0, url, '/tmp/ha'))
for url in urls:
   print(s_queue_dw(0, url, '/tmp/ha'))

test.py:
   #!/usr/bin/python
   import sys
   print('hi', sys.argv)

master.s_upload_script(0, "ha.py", "/tmp/test.py")
master.s_queue_script(0, "ha.py", "http://", "/tmp/")
'''

