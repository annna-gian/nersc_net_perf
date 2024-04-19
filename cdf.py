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

	#'dtn-tstat-2022.03-data.json','dtn-tstat-2022.04-data.json','dtn-tstat-2022.05-data.json','dtn-tstat-2022.06-data.json','dtn-tstat-2022.07-data.json','dtn-tstat-2022.08-data.json','dtn-tstat-2022.09-data.json','dtn-tstat-2022.10-data.json','dtn-tstat-2022.11-data.json','dtn-tstat-2022.12-data.json']:



def main():
	#globus_nodes = ['dtn05.nersc.gov','dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov','dtn09.nersc.gov']
	#globus_nodes = ['dtn04.nersc.gov']
	#interactive = ['dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']
	interactive = ['128.55.205.18','128.55.205.19','128.55.205.20','128.55.205.21','dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']
	globus_nodes = ['128.55.205.26','128.55.205.27','128.55.205.28','128.55.205.29','128.55.205.36','dtn05.nersc.gov','dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov','dtn09.nersc.gov']
	#all_dtns = ['128.55.205.18','128.55.205.19','128.55.205.20','128.55.205.21','128.55.205.26','128.55.205.27','128.55.205.28','128.55.205.29','128.55.205.36']
	throughput_outgoing = defaultdict(list)
	throughput_incoming = defaultdict(list)
	throughput_outgoing_globus = defaultdict(list)
	throughput_outgoing_interactive = defaultdict(list)
	throughput_incoming_globus = defaultdict(list)
	throughput_incoming_interactive = defaultdict(list)
	throughput_outgoing_globus_21 = defaultdict(list)
	throughput_outgoing_interactive_21 = defaultdict(list)
	throughput_incoming_globus_21 = defaultdict(list)
	throughput_incoming_interactive_21 = defaultdict(list)
	
	for file in sys.argv[1]:
	#'dtn-tstat-2022.03-data.json','dtn-tstat-2022.04-data.json','dtn-tstat-2022.05-data.json','dtn-tstat-2022.06-data.json','dtn-tstat-2022.07-data.json','dtn-tstat-2022.08-data.json','dtn-tstat-2022.09-data.json','dtn-tstat-2022.10-data.json','dtn-tstat-2022.11-data.json','dtn-tstat-2022.12-data.json']:
		with open(file,'r') as f:
			tstat_data = [json.loads(line) for line in f]
			
			if '2022' in f.name:
				print('Its a 2022 file')
				# throughput_outgoing_globus = defaultdict(list)
				# throughput_outgoing_interactive = defaultdict(list)
				# throughput_incoming_globus = defaultdict(list)
				# throughput_incoming_interactive = defaultdict(list)
				#print(interactive)
				for i in tstat_data:
					if i['_source']['meta']['src_ip'] in globus_nodes and i['_source']['meta']['dst_ip'] not in globus_nodes:
						print('Outgoing globus transfer')
						throughput_outgoing_globus[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					elif i['_source']['meta']['src_ip'] in interactive and i['_source']['meta']['dst_ip'] not in interactive:
						print('Outgoing globus transfer')
						throughput_outgoing_interactive[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					elif i['_source']['meta']['dst_ip'] in globus_nodes and i['_source']['meta']['src_ip'] not in globus_nodes:
						print('Incoming globus transfer')
						throughput_incoming_globus[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					elif i['_source']['meta']['dst_ip'] in interactive and i['_source']['meta']['src_ip'] not in interactive:
						print('Incoming interactive transfer')
						throughput_incoming_interactive[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					else:
						print('Nothing to do')
			elif '2021' in f.name:
				print('Its a 2021  file')
				# throughput_outgoing_globus_21 = defaultdict(list)
				# throughput_outgoing_interactive_21 = defaultdict(list)
				# throughput_incoming_globus_21 = defaultdict(list)
				# throughput_incoming_interactive_21 = defaultdict(list)
				#print(interactive)
				for i in tstat_data:
					if i['_source']['meta']['src_ip'] in globus_nodes and i['_source']['meta']['dst_ip'] not in globus_nodes:
						print('Outgoing globus transfer')
						throughput_outgoing_globus_21[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					elif i['_source']['meta']['src_ip'] in interactive and i['_source']['meta']['dst_ip'] not in interactive:
						print('Outgoing globus transfer')
						throughput_outgoing_interactive_21[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					elif i['_source']['meta']['dst_ip'] in globus_nodes and i['_source']['meta']['src_ip'] not in globus_nodes:
						print('Incoming globus transfer')
						throughput_incoming_globus_21[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					elif i['_source']['meta']['dst_ip'] in interactive and i['_source']['meta']['src_ip'] not in interactive:
						print('Incoming interactive transfer')
						throughput_incoming_interactive_21[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
					else:
						print('Nothing to do')

	throughput_outgoing_globus_sorted = sorted(throughput_outgoing_globus.items())
	throughput_outgoing_interactive_sorted = sorted(throughput_outgoing_interactive.items())
	throughput_outgoing_globus_sorted_21 = sorted(throughput_outgoing_globus_21.items())
	throughput_outgoing_interactive_sorted_21 = sorted(throughput_outgoing_interactive_21.items())

	throughput_incoming_globus_sorted = sorted(throughput_incoming_globus.items())
	throughput_incoming_interactive_sorted = sorted(throughput_incoming_interactive.items())
	throughput_incoming_globus_sorted_21 = sorted(throughput_incoming_globus_21.items())
	throughput_incoming_interactive_sorted_21 = sorted(throughput_incoming_interactive_21.items())
	hfont = {'fontname':'Arial'}
	# = plt.subplots()
	import matplotlib.pyplot as plt
	#plt.figure()
	fig, ax1 = plt.subplots()
	z, q = zip(*throughput_outgoing_globus_sorted)
	m, k = zip(*throughput_outgoing_globus_sorted_21)
	sorted_data =np.sort(q)
	sorted_data2 = np.sort(k)
	yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
	ax2 = ax1.twinx()
	yvals2=np.arange(len(sorted_data2))/float(len(sorted_data2)-1)
	ax1.plot(sorted_data,yvals, label = '2022 Globus Traffic',color="red",linewidth=3)
	ax2.plot(sorted_data2,yvals2, label = '2021 Globus Traffic',color="blue", linewidth=3, linestyle="--")
	ax1.set_xscale('log')
	ax2.set_xscale('log')
	ax1.legend(loc='right', frameon=True, fontsize=18)
	ax2.legend(loc='lower right', frameon=True, fontsize=18)
	ax1.set_xlabel('Flow size log(GB)',fontsize=18,**hfont)
	ax1.tick_params(axis='x', labelsize=18)
	ax1.tick_params(axis='y', labelsize=18)
	ax2.tick_params(axis='y', labelsize=18)
	#ax1.set_xticklabels(fontsize=16,**hfont)
	#ax1.set_yticklabels(fontsize=16,**hfont)
	#ax2.set_yticklabels(fontsize=16,**hfont)
	#plt.ylabel('%  of Transfers',fontsize=20,**hfont)
	#plt.xlabel('Flow size',fontsize=20,**hfont)
	#ax1.set_xticklabels('%  of Transfers',fontsize=20,**hfont)
	#ax1.set_yticklabels('Flow size',fontsize=20,**hfont)
	#ax2.set_yticklabels('Flow size',fontsize=20,**hfont)
	ax1.tick_params(which='both',direction='in', top=True,right=True, labelsize=18)
	ax2.tick_params(which='both',direction='in', top=True,right=True, labelsize=18)
	#ax1.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
	name_2 = file + '_cdf_size_globus_outgoing_v3_log_2.png'
	plt.tight_layout()
	fig.savefig(name_2)
	#plt.clf()
	#plt.close()
	#exit(0)



	fig, ax1 = plt.subplots()
	z, q = zip(*throughput_outgoing_interactive_sorted)
	m, k = zip(*throughput_outgoing_interactive_sorted_21)
	sorted_data =np.sort(q)
	sorted_data2 = np.sort(k)
	yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
	ax2 = ax1.twinx()
	yvals2=np.arange(len(sorted_data2))/float(len(sorted_data2)-1)
	ax1.plot(sorted_data,yvals, label = '2022 Non-Globus Traffic',color="red",linewidth=3)
	ax2.plot(sorted_data2,yvals2, label = '2021 Non-Globus Traffic',color="blue", linewidth=3, linestyle="--")
	ax1.set_xscale('log')
	ax2.set_xscale('log')
	ax1.legend(loc='right', frameon=True,fontsize=18)
	ax2.legend(loc='lower right', frameon=True,fontsize=18)
	ax1.set_xlabel('Flow size log(GB)',fontsize=18,**hfont)
	
	#plt.ylabel('%  of Transfers',fontsize=20,**hfont)
	#plt.xlabel('Flow size',fontsize=20,**hfont)
	#ax1.set_xticklabels('%  of Transfers',fontsize=20,**hfont)
	#ax1.set_yticklabels('Flow size',fontsize=20,**hfont)
	#ax2.set_yticklabels('Flow size',fontsize=20,**hfont)
	ax1.tick_params(which='both',direction='in', top=True,right=True, labelsize=18)
	ax2.tick_params(which='both',direction='in', top=True,right=True, labelsize=18)
	#ax1.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
	plt.tight_layout()
	name_2 = file + '_cdf_size_interactive_outgoing_v3_log.png'
	fig.savefig(name_2)


	fig, ax1 = plt.subplots()
	z, q = zip(*throughput_incoming_interactive_sorted)
	m, k = zip(*throughput_incoming_interactive_sorted_21)
	sorted_data =np.sort(q)
	sorted_data2 = np.sort(k)
	yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
	ax2 = ax1.twinx()
	yvals2=np.arange(len(sorted_data2))/float(len(sorted_data2)-1)
	ax1.plot(sorted_data,yvals, label = '2022 Non-Globus Traffic',color="red",linewidth=3)
	ax2.plot(sorted_data2,yvals2, label = '2021 Non-Globus Traffic',color="blue", linewidth=3, linestyle="--")
	ax1.set_xscale('log')
	ax2.set_xscale('log')
	ax1.legend(loc='right', frameon=True,fontsize=18)
	ax2.legend(loc='lower right', frameon=True,fontsize=18)
	ax1.set_xlabel('Flow size log(GB)',fontsize=18,**hfont)
	#plt.ylabel('%  of Transfers',fontsize=20,**hfont)
	#plt.xlabel('Flow size',fontsize=20,**hfont)
	
	ax1.tick_params(which='both',direction='in', top=True,right=True,labelsize=16)
	ax2.tick_params(which='both',direction='in', top=True,right=True, labelsize=16)
	#ax1.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
	name_2 = file + '_cdf_size_interactive_incoming_v3_log.png'
	plt.tight_layout()
	fig.savefig(name_2)	


	fig, ax1 = plt.subplots()
	z, q = zip(*throughput_incoming_globus_sorted)
	m, k = zip(*throughput_incoming_globus_sorted_21)
	sorted_data =np.sort(q)
	sorted_data2 = np.sort(k)
	yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
	ax2 = ax1.twinx()
	yvals2=np.arange(len(sorted_data2))/float(len(sorted_data2)-1)
	ax1.plot(sorted_data,yvals, label = '2022 Globus Traffic',color="red",linewidth=3)
	ax2.plot(sorted_data2,yvals2, label = '2021 Globus Traffic',color="blue", linewidth=3, linestyle="--")
	ax1.set_xscale('log')
	ax2.set_xscale('log')
	ax1.legend(loc='right', frameon=True,fontsize=18)
	ax2.legend(loc='lower right', frameon=True,fontsize=18)
	ax1.set_xlabel('Flow size log(GB)',fontsize=18,**hfont)
	#plt.ylabel('%  of Transfers',fontsize=20,**hfont)
	#plt.xlabel('Flow size',fontsize=20,**hfont)
	#ax1.set_xticklabels('%  of Transfers',fontsize=20,**hfont)
	#ax1.set_yticklabels('Flow size',fontsize=20,**hfont)
	#ax2.set_yticklabels('Flow size',fontsize=20,**hfont)
	ax1.tick_params(which='both',direction='in', top=True,right=True,labelsize=18)
	ax2.tick_params(which='both',direction='in', top=True,right=True, labelsize=18)
	#ax1.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
	name_2 = file + '_cdf_size_globus_incoming_v3_log.png'
	plt.tight_layout()
	fig.savefig(name_2)

		





if __name__=="__main__":
	main()
