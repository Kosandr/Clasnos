#!/usr/bin/python3

import conf, utils
from flask import Flask, request


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

@app.route("/", methods=['GET', 'POST'])
def req():
   if request.method == 'POST':
      print(request.form)
      #print(request.get_json())
      #req_data = request.get_json()
      req_data = request.form

      if not req_data['pass'] == conf.c['pass']:
         return conf.mk_err(conf.ERR_BAD_PASS, "bad password")

      if req_data['cmd'] == 'status':
         return conf.mk_succ({'status' : 'active'})

      if req_data['cmd'] == 'add_dw':
         return add_queue(req_data)

      if req_data['cmd'] == 'queue_len':
         return get_queue_len()

      return conf.mk_err(conf.ERR_DEFAULT)

   else:
      return conf.mk_err(conf.ERR_BAD_REQUEST, 'need post request')

   return conf.mk_err(conf.ERR_DEFAULT)




