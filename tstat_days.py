
#!/usr/bin/env python

import os
import sys
import time
import json
from collections import defaultdict, Counter
from itertools import islice
import datetime
#from datetime import datetime
import dateutil.relativedelta
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.use('Agg')
import matplotlib.dates
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

hfont = {'fontname':'Arial'}

#calculates number of active transfers per hour long bucket over 24h
#plots number of active transfers and corresponding percentage of retransmissions over the same hour long buckets
#input: DTN IP, tstat_cords, busiest day for that DTN, name of file for transfers and retransmissios
#output: 2 plots - active transfers per hour and percentage of retransmissions for that hour




def active_transfers_per_hours(dtn, tstat_records,busiest_day, name):
	active_transfers_per_hour = defaultdict(int, {k:0 for k in range(0,24)})
	transfers = 0
	same_day_transfers = 0
	start_times = []
	retrans_values = []
	percentage = 0
	df = pd.DataFrame(columns=['start_time','end_time', 'retrans'])
	for i in tstat_records:
	#2021 log	#if '.nersc.gov' in i['_source']['dest'] and '.nersc.gov' not in i['_source']['source']:
		if '128.55.' in i['_source']['meta']['src_ip'] and '128.55.' not in i['_source']['meta']['dst_ip']:
			#print('Outgoing transfers')
			#if dtn in str(i['_source']['dest']):
			if dtn in str(i['_source']['meta']['src_ip']):
				#active_transfers = defaultdict(int, {k:0 for k in range(0,24)})
				#print('Looking at incoming transfers to ' + str(i['_source']['dest']))
				#print('Outgoing from ')
				print('Incoming to')
				print(dtn)

				transfers += 1
				print(i['_source'])
				dt_end = datetime.datetime.fromtimestamp(int(i['_source']['end'])/1000)
				dt_start = datetime.datetime.fromtimestamp(int(i['_source']["start"])/1000)
				print(dt_start.day)
				print(dt_end.day)
				#time.sleep(5)
				if dt_start.day == busiest_day:
					print('I found the busiest day')
					print(dt_start.hour)
					print(dt_start.minute)
					print(dt_start.day)
					rd = dateutil.relativedelta.relativedelta(dt_end, dt_start)
					print(rd)


					percentage = 100* (float(i['_source']['values']['tcp_rexmit_bytes'])/float(i['_source']['values']['num_bytes']))
					retrans_values.append(percentage)
					print(int(dt_end.hour))
					print('The transfer lasted for:')
					print(int(rd.hours))
					df.loc[len(df)] = [dt_start,dt_end,percentage]

					hour_key = int(dt_start.hour) + int(rd.hours)
						#time.sleep(1)
					if (rd.hours > 0) and (rd.hours < 24):
						print('Eimai mesa sto if')
						print(hour_key)
						print(active_transfers_per_hour[dt_start.hour])
						print(active_transfers_per_hour[dt_start.hour+hour_key+1])
						for i in range(dt_start.hour,dt_start.hour+rd.hours):
							print(i)
							active_transfers_per_hour[i] += 1
							hours_t = dt_start + dateutil.relativedelta.relativedelta(hours=1)
							print('Value of hours_t')
							print(hours_t)

					elif rd.hours == 0:
						print('The transfer lasted less than an hour')
						print(hour_key)
						same_day_transfers += 1
						active_transfers_per_hour[dt_start.hour] += 1
						hours_t = dt_start + dateutil.relativedelta.relativedelta(hours=rd.hours)
						print(hours_t)
						#time.sleep(5)
					start_times.append(hours_t)
			else:
				print('Not the dtn you are looking for')
				print(dtn)
			#return None
	print(active_transfers_per_hour)

	format_string = "%H"
	new = {}
	for key,value in active_transfers_per_hour.items():
		print(key)
		if key < 24:

		#print(datetime.datetime.strptime(str(key), format_string))
			new[datetime.datetime.strptime(str(key), format_string)] = value
	print(transfers)
	print(busiest_day)
	print(same_day_transfers)






	# ######kanw comment gia na dokimasw me plotly

	print(new)
	print('//////////////////////')
	#exit(0)

	active_transfers_per_hour_sorted = sorted(active_transfers_per_hour.items())
	plt.figure()
	fig, ax = plt.subplots(figsize=(8,8))
	#x, y = zip(*active_transfers_per_hour_sorted)
	#dates = matplotlib.dates.date2num(new)
	new_sorted = sorted(new.items())
	x, y = zip(*new_sorted)
	plt.plot(x,y, marker='D',mfc='red',linewidth=3)
	#plt.bar(x, y,align='center', width=0.7)
	plt.ylabel('Active transfers',fontsize=20,**hfont )
	plt.xlabel('Hour of day',fontsize=20,**hfont)
	#loc =range(0,len(x))
	plt.gca().xaxis.set_major_locator(matplotlib.dates.HourLocator(interval = 3))
	date_format = matplotlib.dates.DateFormatter('%H:%M')
	plt.gca().xaxis.set_major_formatter(date_format)
	ax.tick_params(axis='x', labelrotation=45)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	ax.set_ylim(0,400)
	#plt.xticks(loc,x,rotation=45,fontsize=16)
	#plt.yticks(fontsize=18)

	plt.tick_params(which='both',direction='in', top=True,right=True)
	#plt.tight_layout()
	plt.tight_layout()
	name = dtn+'__'+str(name)+'_active_transfers_hours_new_out_new_line_2.png'
	plt.savefig(name)
	plt.close()
	# #exit(0)
	# plt.figure()
	fig, ax1 = plt.subplots(figsize=(8,8))	
	dates = matplotlib.dates.date2num(start_times)
	#ax1.plot(df.start_time.dt.hour)
	ax1.plot_date(dates, retrans_values,ms=4)
	#ax2 = ax1.twinx()
	#ax2.plot_date(dates, y)

	plt.gca().xaxis.set_major_locator(matplotlib.dates.HourLocator(interval = 3))
	date_format = matplotlib.dates.DateFormatter('%H:%M')
	plt.gca().xaxis.set_major_formatter(date_format)
	ax.tick_params(axis='x', labelrotation=45)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	#plt.xticks(loc,x,rotation=45,fontsize=18)
	#plt.gca().xaxis.set_major_locator(matplotlib.dates.HourLocator(interval = 1))
	#ax1.set_xticks(ticks=[i for i in range(0, 25)])
	#ax1.set_xticklabels([i for i in range(0, 25)])
	ax1.tick_params(axis='x', labelrotation=45)
	ax1.set_ylim(0,6)
	ax1.set_xlabel('Hour of day',fontsize=20,**hfont)
	ax1.set_ylabel('Percentage of Retransmissions',fontsize=20,**hfont)
	name = dtn+'__' +str(name)+'_active_transfers_retrans_new_out__new_overlay.png'
	#plt.show()
	plt.tight_layout()
	plt.savefig(name)
	plt.close()
	#plt.tick_params(which='both',direction='in', top=True,right=True)






	# #ax1.set_xticks(fontsize=18,rotation=45)
	# #ax1.set_yticks(fontsize=18)
	# name = dtn+' ' +str(busiest_day)+' active_transfers_retrans_new_in__new_overlay.png'
	# plt.show()
	# plt.savefig(name)
	# plt.close()
	return active_transfers_per_hour








def main():
	
	interactive = ['128.55.205.18','128.55.205.19','128.55.205.20','128.55.205.21']
	globus_nodes = ['128.55.205.26','128.55.205.27','128.55.205.28','128.55.205.29','128.55.205.36'] ##DTN 10 is excluded due to corrupt logs
	#all_dtns = ['128.55.205.18','128.55.205.19','128.55.205.20','128.55.205.21','128.55.205.26','128.55.205.27','128.55.205.28','128.55.205.29','128.55.205.36']
	for dtn in globus_nodes:
		#active_transfers_days = defaultdict(int, {k:0 for k in range(1,32)})
		#active_transfers_days_in = defaultdict(int, {k:0 for k in range(1,32)})
		#occurs = 0
		#example input dtn-tstat-2022.02-data.json dtn-tstat-2022.03-data.json dtn-tstat-2022.04-data.json ...
		for file in sys.argv[1:]:
			with open(file,'r') as f:
				occurs = 0
				active_transfers_days = defaultdict(int, {k:0 for k in range(1,32)})
				active_transfers_days_in = defaultdict(int, {k:0 for k in range(1,32)})
				throughput_outgoing = defaultdict(list)
				throughput_incoming = defaultdict(list)
				retrans_outgoing = defaultdict(list)
				retrans_incoming = defaultdict(list)
				tstat_data = [json.loads(line) for line in f]

				for i in tstat_data:
					#print(i)
					
					if '128.55.' in i['_source']['meta']['src_ip'] and '128.55.' not in i['_source']['meta']['dst_ip']:
						# print(i['_source'])
						# print(i['_source']['dest'])
						# time.sleep(4)
						print('From NERSC to the outside world')
						if dtn in str(i['_source']['meta']['src_ip']):
						#if 'dtn01.nersc.gov' in str(i['_source']['source']):
							occurs +=1
							print(occurs)
							#time.sleep(2)
				
				# 		#hour_key = active_transfers_per_hour('dtn02.nersc.gov',i)
				# 		#if hour_key is not None:
				# 		#	for i in range(dt.start.hour,dt_end.hour)
				# 		#		active_transfers[i] += 1
				# 	#dtn_active_transfers[dtn] = active_transfers
				# #print(dtn_active_transfers)	
				# #exit(0)
							print('Looking at outgoing transfers from ' + str(i['_source']['source']))
							throughput_outgoing[float(i['_source']['values']['file_size_MB']/1000)] = float(i['_source']['values']['throughput_Mbps'])
							retrans_outgoing[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
							#print(i['_source'])
							dt_end = datetime.datetime.fromtimestamp(int(i['_source']['end'])/1000)
							print(dt_end.day)
							dt_start = datetime.datetime.fromtimestamp(int(i['_source']["start"])/1000)
							print(dt_end.hour)
							print(dt_end.minute)
							rd = dateutil.relativedelta.relativedelta(dt_end, dt_start)
							print(rd)
							print(dt_start)
							print(dt_start.hour)
							print(int(dt_end.hour))
							print(int(rd.days))
							if int(rd.days) == 0: ####flows under 1 day
								if dt_end.day == dt_start.day:
									print('same day')
								#time.sleep(5)
									active_transfers_days[int(dt_end.day)] +=1
								else:
									print('la')
									day_key = int(dt_start.day)
									if int(day_key) <= 30:
								#while int(day_key) + int(rd.days) < 31:
										day_key = int(dt_start.day) +1
									#day_key = int(dt_start.day) + int(rd.days)
									active_transfers_days[day_key] +=1
									print(day_key)
									#if day_key==30:
									#	break
									#print(day_key)
							else: #####flows bigger than 1 day
								#day_key = int(dt_start.day)
								print('Starting from day:')
								day_key = int(dt_start.day)
								#time.sleep(5)
								print('Transfer will go on for ')
								print(int(rd.days))
								while day_key <31:
									if day_key == 30:
										active_transfers_days[day_key] +=1
										break
									for k in range(0,int(rd.days)):
										active_transfers_days[day_key] +=1
										day_key += 1
										print(day_key)
										if day_key == 30:
											break
										#time.sleep(1)
									break
			
							# if dt_end.day == dt_start.day:
							# 	print('same day')
							# 	#time.sleep(5)
							# 	active_transfers_days[int(dt_end.day)] +=1
							# else:
							# 	print('la')
							# 	day_key = int(dt_start.day) + int(rd.days)
							# 	active_transfers_days[day_key] +=1
							# 	active_transfers_days[int(dt_start.day)] += 1

					if '128.55.' not in i['_source']['meta']['src_ip']: #and '.nersc.gov' in i['_source']['source']:   #allazw gia oti erxetai apeksw
						print('Looking at incoming transfers from the outside')
						# print(i['_source'])
						# print(i['_source']['dest'])
						# time.sleep(4)
		# 	# #print('Looking at local incoming transfers')
						#if 'dtn01.nersc.gov' in str(i['_source']['dest']):
						if dtn in str(i['_source']['meta']['dst_ip']):

							occurs += 1
							throughput_incoming[float(i['_source']['values']['file_size_MB']/1000)] = float(i['_source']['values']['throughput_Mbps'])
							retrans_incoming[float(i['_source']['values']['throughput_Mbps'])] = float(i['_source']['values']['file_size_MB']/1000)
							dt_end = datetime.datetime.fromtimestamp(int(i['_source']['end'])/1000)
							print(dt_end.day)
							dt_start = datetime.datetime.fromtimestamp(int(i['_source']["start"])/1000)
							print(dt_end.hour)
							print(dt_end.minute)
							rd = dateutil.relativedelta.relativedelta(dt_end, dt_start)
							print(rd)
							print(dt_start)
							print(dt_start.hour)
							print(int(dt_end.hour))
							print(int(rd.days))
							if int(rd.days) == 0: ####flows under 1 day
								if dt_end.day == dt_start.day:
									print('same day')
								#time.sleep(5)
									active_transfers_days_in[int(dt_end.day)] +=1
								else:
									print('la')
									day_key = int(dt_start.day)
									if int(day_key) <= 30:
								#while int(day_key) + int(rd.days) < 31:
										day_key = int(dt_start.day) +1
									#day_key = int(dt_start.day) + int(rd.days)
									active_transfers_days_in[day_key] +=1
									print(day_key)
									#if day_key==30:
									#	break
									#print(day_key)
							else: #####flows bigger than 1 day
								day_key = int(dt_start.day)
								print('starting from day:')
								print(day_key)
								#time.sleep(5)
								print('Transfer will go on for')
								print(int(rd.days))
								while day_key <31:
									if day_key == 30:
										active_transfers_days_in[day_key] +=1
										break
									for k in range(0,int(rd.days)):
										active_transfers_days_in[day_key] +=1
										day_key += 1
										print(day_key)
										if day_key == 30:
											break
										#time.sleep(1)
									break

								 #int(dt_start.day) + int(rd.days)
								#day_key = int(dt_start.day) +1


			print(active_transfers_days_in)
			print('This is the occurence value')
			print(occurs)
			#exit(0)
			active_transfers_days_sorted = sorted(active_transfers_days.items())
			active_transfers_days_in_sorted = sorted(active_transfers_days_in.items())
			total_transf = sum(active_transfers_days) + sum(active_transfers_days)
			print('total transfers')
			print(total_transf)
			print(active_transfers_days_in_sorted)
			print(active_transfers_days_sorted)
			busiest_day_in = 0
			busiest_day_in = max(active_transfers_days_in, key=active_transfers_days_in.get)
			print(busiest_day_in)
			#active_transfers_per_hour = active_transfers_per_hours(dtn,tstat_data,busiest_day_in,f.name.replace('',''))
			#exit(0)
			busiest_day = 0
			busiest_day = max(active_transfers_days, key=active_transfers_days.get)
			print(busiest_day)
			active_transfers_per_hour = active_transfers_per_hours(dtn,tstat_data,busiest_day,f.name.replace('',''))
			#exit(0)
			# plt.figure()
			throughput_outgoing_sorted = sorted(throughput_outgoing.items())
			throughput_incoming_sorted = sorted(throughput_incoming.items())

			hfont = {'fontname':'Arial'}


			fig, ax = plt.subplots(figsize=(8,8))
			x, y = zip(*active_transfers_days_in_sorted)
			plt.bar(x, y,align='center', width=0.7)
			plt.ylabel('Number of active transfers',fontsize=16)
			plt.xlabel('Day of month',fontsize=16)
			loc =range(1,len(x)+1)
			plt.xticks(loc,x,rotation=45, fontsize=12)
			plt.yticks(fontsize=16)
			y_max = int(active_transfers_days_in[busiest_day_in]) + 500
			#y_max = 4500
			plt.ylim(0,y_max)
			#plt.rcParams['font.size'] = 14
			plt.rc('ytick', labelsize=14)
			plt.tight_layout()
			#dtn = 'dtn01.nersc.gov'
			name =str(file) +dtn+'_active_transfers_days_in_new.png'
			plt.savefig(name)
			plt.clf()


			plt.figure()
			fig, ax = plt.subplots(figsize=(8,8))
			x, y = zip(*active_transfers_days_sorted)
			plt.bar(x, y,align='center', width=0.7)
			plt.ylabel('Number of active transfers',fontsize=16)
			plt.xlabel('Day of month',fontsize=16)
			loc =range(1,len(x)+1)
			plt.xticks(loc,x,rotation=45, fontsize=12)
			plt.yticks(fontsize=16)
			y_max = int(active_transfers_days[busiest_day]) + 500
			#y_max = 50
			plt.ylim(0,y_max)
			#plt.rcParams['font.size'] = 14
			plt.rc('ytick', labelsize=12)
			plt.tight_layout()
			#dtn = 'dtn01.nersc.gov'
			name =str(file) +dtn+'_active_transfers_days_out_new.png'
			plt.savefig(name)
			plt.clf()


if __name__=="__main__":
	main()
