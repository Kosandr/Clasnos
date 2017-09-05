#!/usr/bin/python3

import sh

import conf
import cutils as utils

from flask import Flask, request
from utiltools import shellutils as shu


app = Flask(__name__)


#if __name__ == "__main__":
#   start_app()



def add_queue(req_data):
   print('adding queue')
   #return conf.mk_succ({'status':'success'})
   data = {
      'url' : req_data['url'],
      'storage_path' : req_data['storage_path'],
      'new_name' : req_data['new_name']
   }


   q = utils.Queue()
   q.start_crit()
   q.add(data)
   q.end_crit()

   return conf.mk_succ({'status':'success'})

def get_queue_len():
   q = utils.Queue()
   return conf.mk_succ({'ret':q.len()})


def upload_script(name, data):
   full_path = conf.SCRIPTS_PATH + name
   sh.touch(full_path)

   shu.write_file(full_path, data)
   sh.chmod('u+x', full_path)
   return conf.mk_succ({'status':'success'})


def queue_script(script_name, url, storage_path, new_name):
   full_path = conf.SCRIPTS_PATH + script_name

   import base64
   url = base64.b64decode(url.encode('utf-8')).decode('utf-8')

   cmd = '%s %s %s %s' % (full_path, url, storage_path, new_name)
   try:
      shu.exec_bash(cmd)
      return conf.mk_succ({'status':'success'})
   except Exception as e:
      pass

   return conf.mk_err(conf.ERR_EXCEPTION, "script exex failed")

def add_key(key):
   keys_path = '/root/.ssh/authorized_keys'
   if not shu.file_exists(keys_path):
      sh.mkdir('-p', '/root/.ssh')
      sh.touch(keys_path)

   auth_keys = str(sh.cat('/root/.ssh/authorized_keys'))

   if key in auth_keys:
      print('!!!!!!!!!!key already added')
   else:
      print('!!!!adding ssh key')
      auth_keys += '\n\n' + key
      shu.write_file(keys_path, auth_keys)

   return conf.mk_succ({'status':'success'})


@app.route("/", methods=['GET', 'POST'])
def req():
   if request.method == 'POST':
      print(request.form)
      #print(request.get_json())
      #req_data = request.get_json()
      req_data = request.form

      if not req_data['pass'] == conf.c['pass']:
         return conf.mk_err(conf.ERR_BAD_PASS, "bad password")

      cmd = req_data['cmd']

      if cmd == 'status':
         return conf.mk_succ({'status' : 'active'})
      elif cmd == 'queue_dw':
         return add_queue(req_data)
      elif cmd == 'queue_len':
         return get_queue_len()
      elif cmd == 'upload_script':
         script_name = req_data['slave_name']
         script_data = req_data['data']
         return upload_script(script_name, script_data)
      elif cmd == 'queue_script':
         script_name = req_data['script_name']
         url = req_data['url']
         storage_path = req_data['storage_path']
         new_name = req_data['new_name']

         print('queueing script!!!!!!!!!!')

         return queue_script(script_name, url, storage_path, new_name)
      elif cmd == 'add_key':
         key = req_data['key']
         return add_key(key)

      return conf.mk_err(conf.ERR_DEFAULT)

   else:
      return conf.mk_err(conf.ERR_BAD_REQUEST, 'need post request')

   return conf.mk_err(conf.ERR_DEFAULT)




