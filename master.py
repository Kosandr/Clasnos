
import requests
import conf

def post_req(ip, port, json_cmd, protocol='http'):

   url = '%s://%s:%s' % (protocol, ip, port)

   json_cmd['pass'] = conf.c['pass']

   resp = requests.post(url, data=json_cmd)
   print(resp.text)
   #return resp.text
   return resp.json() #text

def send_cmd(slave_num, cmd):
   slave_ip = conf.c['slaves'][slave_num]
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


def s_add_queue(slave_num, url, storage_path, new_name=''):
   json_cmd = {
      'cmd' : 'add_dw',
      'url' : url,
      'storage_path' : storage_path,
      'new_name' : new_name
   }
   return send_cmd(slave_num, json_cmd)



'''
#post_req('slave-ip', '7331', {'cmd':'hi'})


urls = [
   'url1',
   'url2',
   'url3',
   'url4'
]

#print(s_get_status(0))
#print(s_add_queue(0, url, '/tmp/ha'))
for url in urls:
   print(s_add_queue(0, url, '/tmp/ha'))
'''

