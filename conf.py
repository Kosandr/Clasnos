import json, re

from utiltools import shellutils


file_data = shellutils.read_file('conf.json')
file_data = re.sub('[\n\t]', '', file_data)
file_conf = json.loads(file_data)

c = {
   'config_dir' : '~/.clasnos/',
   'pass' : file_conf['pass'],
   'is_master' : False,
   'port' : '7331',
   'master' : file_conf['master'],
   'slaves' : file_conf['slaves']
}



CONFIG_DIR = c['config_dir']
if not shellutils.file_exists(CONFIG_DIR):
   shellutils.mkdir(CONFIG_DIR)


ERR_DEFAULT = 0
ERR_BAD_PASS = 1
ERR_BAD_REQUEST = 1


def mk_err(status, msg_str=''):
   return json.dumps({
      'is_err' : True,
      'err' : ret,
      'err_msg' : msg_str
   })

def mk_succ(ret):
   return json.dumps({
      'is_err' : False,
      'data' : ret
   })


def is_err(x):
   return x.get('is_err', True)


