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
import seaborn as sns

#input:json file containing tstat traffic rerords
#output: volume totals (in PB) for different types of NERSC traffic:
#types of traffic:
#intra-NERSC: both source/destination in NERSC network
#incoming: source IP/hostname outside the NERSC network
#outgoing: destination IP/hostname outside the NERSC network
#Globus: source or destination port >5000
#to run: python totals.py tstat_file.json
#e.g. of tstat records per month: 'dtn-tstat-2021.01-data.json','dtn-tstat-2021.02-data.json','dtn-tstat-2021.03-data.json','dtn-tstat-2021.04-data.json','dtn-tstat-2021.05-data.json', 'dtn-tstat-2021.06-data.json', 'dtn-tstat-2021.07-data.json','dtn-tstat-2021.08-data.json','dtn-tstat-2021.09-data.json','dtn-tstat-2021.10-data.json','dtn-tstat-2021.11-data.json' 'dtn-tstat-2021.12-data.json', 'dtn-tstat-2022.01-data.json','dtn-tstat-2022.02-data.json','dtn-tstat-2022.03-data.json','dtn-tstat-2022.04-data.json','dtn-tstat-2022.05-data.json','dtn-tstat-2022.06-data.json','dtn-tstat-2022.07-data.json','dtn-tstat-2022.08-data.json','dtn-tstat-2022.09-data.json','dtn-tstat-2022.10-data.json','dtn-tstat-2022.11-data.json','dtn-tstat-2022.12-data.json','dtn-tstat-2020.01-data.json', 'dtn-tstat-2020.02-data.json','dtn-tstat-2020.03-data.json','dtn-tstat-2020.04-data.json','dtn-tstat-2020.05-data.json','dtn-tstat-2020.06-data.json', 'dtn-tstat-2020.07-data.json', 'dtn-tstat-2020.08-data.json','dtn-tstat-2020.09-data.json','dtn-tstat-2020.10-data.json','dtn-tstat-2020.11-data.json','dtn-tstat-2020.12-data.json'

def main():
	globus_nodes = ['dtn05.nersc.gov','dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov','dtn09.nersc.gov','dtn10.nersc.gov','dtn11.nersc.gov']

	total_ew = 0
	total_out_ns = 0
	total_in_ns = 0
	total_size_globus_out = 0
	total_size_globus_in = 0
	#interactive = ['dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']
	interactive = ['128.55.205.18','128.55.205.19','128.55.205.20','128.55.205.21','dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']
	##globus_nodes = ['128.55.205.26','128.55.205.27','128.55.205.28','128.55.205.29','128.55.205.36','dtn05.nersc.gov','dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov','dtn09.nersc.gov']
	for dtn in interactive:
		for file in sys.argv[1:]:
			with open(file,'r') as f:
				tstat_data = [json.loads(line) for line in f]
				if '2022' in f.name:
					print('Its a 2022 file')
					for i in tstat_data:
						if '.nersc.gov' in i['_source']['source'] and '.nersc.gov' in i['_source']['dest']:
							print('EW traffic DTNs')
							total_ew += float(i['_source']['values']['file_size_MB'])
						elif  '.nersc.gov' in i['_source']['source'] and '.nersc.gov' not in i['_source']['dest']:
							print('NS traffic-leaving NERSC')
							total_out_ns += float(i['_source']['values']['file_size_MB'])
							if int(i['_source']['meta']['src_port']) >= 50000 or int(i['_source']['meta']['src_port']) <= 60000:
								#print('This is a globus transfer')
	# # 						total_globus += 1
								total_size_globus_out += float(i['_source']['values']['file_size_MB'])
						elif  '.nersc.gov' in i['_source']['dest'] and '.nersc.gov' not in i['_source']['source']:
							print('NS traffic-coming NERSC')
							total_in_ns += float(i['_source']['values']['file_size_MB'])
							if int(i['_source']['meta']['src_port']) >= 50000 or int(i['_source']['meta']['src_port']) <= 60000:
								#print('This is a globus transfer')
	# # 						total_globus += 1
								total_size_globus_in += float(i['_source']['values']['file_size_MB'])
	print(total_ew)
	print('Border crossing traffic')
	print(total_out_ns/1024*1024)
	print(total_in_ns/1024*1024)
	print(total_out_ns+total_in_ns)
	print('Globus')
	print(total_size_globus_out/1024*1024)
	print(total_size_globus_in/1024*1024)






if __name__=="__main__":
	main()
