#!/usr/local/bin/python

import texttable as TT
import perfcollect as PC

#set here counters, which you need, in format group - list of counters
perf_counters = {	'WBThrottle' : ['bytes_dirtied', 'ios_dirtied'],
					'filestore' : ['journal_latency', 'journal_queue_max_ops', 'commitcycle_interval']	}



def main(): #just for test
  perf_list = PC.get_perf_dump_in_map ()

  tab = TT.Texttable()
  tab.set_deco(tab.HEADER | tab.VLINES | tab.BORDER | tab.HLINES)

  header = ['']
  header.extend (perf_list.keys())
  tab.add_row (header)
  tab.header = header

  for group_name, counters in perf_counters.items():
  	row = [''] * (len(perf_list.keys()) + 1)
  	row[0] = group_name
  	tab.add_row (row)
  	for counter in counters:
	  	row = []
		row.append (counter)
  		for key,value in perf_list.items():
	  		if type(value[group_name][counter]) != type (dict()):
	  			row.append(value[group_name][counter])
	  		else:
	  			s = ""
	  			for key1,value1 in value[group_name][counter].items():
	  				s = s + key1 + " = " + str(value1) + "\n"
	  			row.append (s)
  		tab.add_row (row)



  print tab.draw()


if __name__ == '__main__':
    main()
