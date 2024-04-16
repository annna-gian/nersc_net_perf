#!/usr/bin/env python

import os
import sys
import time
import json
from collections import defaultdict, Counter
from itertools import islice
import datetime
import dateutil.relativedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import pandas as pd
from operator import itemgetter


#detect competing incoming transfers for 10 largest flows per DTN 
#store source,destination,size, throughput, start_time, end_time, retransmission per competing transfer 
#input: list of json files containing tstat traffic rerords
#output: .txt files containing competing transfer info
#to run: python competing_transfers ['dtn-tstat-2021.01-data.json','dtn-tstat-2021.02-data.json','dtn-tstat-2021.03-data.json','dtn-tstat-2021.04-data.json','dtn-tstat-2021.05-data.json', 'dtn-tstat-2021.06-data.json', 'dtn-tstat-2021.07-data.json','dtn-tstat-2021.08-data.json','dtn-tstat-2021.09-data.json','dtn-tstat-2021.10-data.json','dtn-tstat-2021.11-data.json','dtn-tstat-2021.12-data.json','dtn-tstat-2022.01-data.json','dtn-tstat-2022.02-data.json','dtn-tstat-2022.03-data.json','dtn-tstat-2022.04-data.json','dtn-tstat-2022.05-data.json','dtn-tstat-2022.06-data.json','dtn-tstat-2022.07-data.json','dtn-tstat-2022.08-data.json','dtn-tstat-2022.09-data.json','dtn-tstat-2022.10-data.json','dtn-tstat-2022.11-data.json','dtn-tstat-2022.12-data.json','dtn-tstat-2020.01-data.json', 'dtn-tstat-2020.02-data.json','dtn-tstat-2020.03-data.json','dtn-tstat-2020.04-data.json','dtn-tstat-2020.05-data.json','dtn-tstat-2020.06-data.json', 'dtn-tstat-2020.07-data.json', 'dtn-tstat-2020.08-data.json','dtn-tstat-2020.09-data.json','dtn-tstat-2020.10-data.json','dtn-tstat-2020.11-data.json','dtn-tstat-2020.12-data.json']

def main():
	globus_nodes = ['dtn05.nersc.gov','dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov','dtn09.nersc.gov']
	#globus_nodes = ['dtn04.nersc.gov']
	total_ew = 0
	total_out_ns = 0
	total_in_ns = 0
	total_size_globus_out = 0
	total_size_globus_in = 0
	interactive = ['dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']
	#interactive = ['128.55.205.18','128.55.205.19','128.55.205.20','128.55.205.21','dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']
	#globus_nodes = ['128.55.205.26','128.55.205.27','128.55.205.28','128.55.205.29','128.55.205.36','dtn05.nersc.gov','dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov','dtn09.nersc.gov']
	for dtn in globus_nodes:
		for file in sys.argv[1]:
				with open(file,'r') as f:
					current_directory = os.getcwd()
					final_directory =dtn + f.name +'_dir_in'
					if not os.path.exists(final_directory):
   						os.makedirs(final_directory)
					tstat_data = [json.loads(line) for line in f]
					print(dtn)
					dtnlist = [x for x in tstat_data if x['_source']['dest'].startswith(dtn) and '.nersc.gov' not in x['_source']['source']]
					dtnlist_sorted = sorted(dtnlist, key=lambda x: float(x['_source']['values']['file_size_MB']), reverse=True)
					#print(dtnlist_sorted[:4])
					for i in dtnlist_sorted[:10]:
						start_time  = datetime.datetime.fromtimestamp(int(i['_source']["start"])/1000)
						end_time = datetime.datetime.fromtimestamp(int(i['_source']["end"])/1000)
						duration = dateutil.relativedelta.relativedelta(end_time, start_time)
						print(start_time)
						print(duration)
						print(i['_source']['source'])
						print('one entry')
						with open(os.path.join(final_directory,i['_source']['source']+'_in.txt') ,'a+') as fd:
							fd.write('{0} {1} {2} {3} {4} {5}\n'.format(i['_source']['source'], float(i['_source']['values']['file_size_MB']),i['_source']['values']['throughput_Mbps'],start_time, end_time,100* (float(i['_source']['values']['tcp_rexmit_bytes'])/float(i['_source']['values']['num_bytes'])) ))
						#time.sleep(1)
							for x in dtnlist_sorted[11:]:
								if (datetime.datetime.fromtimestamp(int(x['_source']["end"])/1000) < (start_time + duration) and datetime.datetime.fromtimestamp(int(x['_source']["start"])/1000) > start_time):
									print('Found competing transfer')
									print(x['_source']['source'], x['_source']['values']['throughput_Mbps'],datetime.datetime.fromtimestamp(int(x['_source']["start"])/1000), datetime.datetime.fromtimestamp(int(x['_source']["end"])/1000),100* (float(x['_source']['values']['tcp_rexmit_bytes'])/float(x['_source']['values']['num_bytes'])))
									fd.write('{0} {1} {2} {3} {4} {5}\n'.format(x['_source']['source'],float(x['_source']['values']['file_size_MB']), x['_source']['values']['throughput_Mbps'],datetime.datetime.fromtimestamp(int(x['_source']["start"])/1000), datetime.datetime.fromtimestamp(int(x['_source']["end"])/1000),100* (float(x['_source']['values']['tcp_rexmit_bytes'])/float(x['_source']['values']['num_bytes']))))

									#time.sleep(1)



if __name__=="__main__":
	main()