
import requests
import conf, cutils
from utiltools import shellutils



def get_slave_ip_from_num(slave_num):
   return conf.c['slaves'][slave_num]

def post_req(ip, port, json_cmd, protocol='http'):

   url = '%s://%s:%s' % (protocol, ip, port)

   json_cmd['pass'] = conf.c['pass']

   resp = requests.post(url, data=json_cmd)
   print(resp.text)
   #return resp.text
   return resp.json() #text

def send_cmd(slave_num, cmd):
   slave_ip = get_slave_ip_from_num(slave_num)
   slave_port = conf.c['port']

   return post_req(slave_ip, slave_port, cmd)


##########MASTER COMMANDS

def s_get_queue_len(slave_num):
   ret = send_cmd(slave_num, {'cmd' : 'queue_len'})
   if conf.is_err(ret):
      return None
   else:
      return ret['data']['ret']

#return down or active
def s_get_status(slave_num):
   ret = send_cmd(slave_num, {'cmd' : 'status'})
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
   json_cmd = {
      'cmd' : 'queue_script',
      'script_name' : script_name,
      'url' : url,
      'storage_path' : storage_path,
      'new_name' : new_name
   }

   return send_cmd(slave_num, json_cmd)


def s_sync(slave_num, slave_dir, master_dir):
   slave_ip = get_slave_ip_from_num(slave_num)

   utils.rsync('root', slave_ip, slave_dir, master_dir)

   return {} #return send_cmd(slave_num, json_cmd)


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

