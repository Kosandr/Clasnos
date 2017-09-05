import json, re, sh

from utiltools import shellutils


file_data = shellutils.read_file('~/orgs/Kosandr/Clasnos/conf.json')

#file_data = shellutils.read_file('conf.json')
file_data = re.sub(r'[\n\t]', '', file_data)
file_conf = json.loads(file_data)

c = {
   'config_dir' : '~/.clasnos/',
   'pass' : file_conf['pass'],
   'is_master' : False,
   'port' : '7331',
   'master' : file_conf['master'],
   'slaves' : file_conf['slaves']
}


@shellutils.expandhome1
def get_path(x):
   return x

CONFIG_DIR = get_path(c['config_dir']) + '/'
SCRIPTS_PATH = CONFIG_DIR + 'scripts/'

if not shellutils.file_exists(SCRIPTS_PATH):
   print('making scripts path!', SCRIPTS_PATH)
   sh.mkdir('-p', SCRIPTS_PATH)


###Errors

ERR_DEFAULT = 0
ERR_BAD_PASS = 1
ERR_BAD_REQUEST = 2
ERR_EXCEPTION = 3

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

###End Errors


