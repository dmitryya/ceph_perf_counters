#!/usr/local/bin/python
#import logging
import json
from fabric import tasks
from fabric.api import env, run
#from fabric.api import env
from fabric.network import disconnect_all


env.user = 'root'
cnt_host = '172.16.54.71' #controller host
#osd_list = []
#env.hosts = [
#    '172.16.54.71',
#     ]
#env.gateway = '172.16.54.71' #controller host


#logger = logging.getLogger('fabric')
#logger.setLevel(logging.WARN)

def osds_list_task():
  #gets list og osds id
  global osd_list
  osd_list = run('ceph osd ls').split('\n') #osd ids list
  return osd_list

def osds_ips_task():
#get osd's ips
  ips = []
  for osd_id in osd_list:
    ips.append (json.loads (run('ceph osd find '+osd_id))["ip"].split(":")[0]) #find hosts
  return ips


def get_perf_dump_task():
  #get perf dump for one osd
  osd_name = run ('ls /var/run/ceph/ |grep .asok')
  perf_list = json.loads (run('ceph --admin-daemon /var/run/ceph/'+osd_name+' perf dump'))
  return perf_list

def get_perf_dump_in_map():
  #go to ceph on controller for osd's ips
  env.hosts = [cnt_host]
  osd_list = tasks.execute(osds_list_task)[env.hosts[0]]
  ip_list = tasks.execute(osds_ips_task)[env.hosts[0]]

  #set hosts for osds and gateway (ips are local)
  env.hosts = ip_list
  env.gateway = cnt_host

  perf_list = tasks.execute(get_perf_dump_task)

  disconnect_all()

  return perf_list

def main():
  perf_list = get_perf_dump_in_map ()
  print perf_list


if __name__ == '__main__':
    main()