import pandas as pd
from datetime import datetime
import dateutil.relativedelta
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
import os
import time
import numpy as np
import matplotlib
import matplotlib.dates as mdates
hfont = {'fontname':'Arial'}


#produces 3D plots between retransmissions,time and throughput for competing transfers over a pre-determined time window
#to produce the graphs the .txt files containing the list of competing transfers need to be present
#to generate the .txt files competing_transfers.py needs to be run first
#to run: python 3Dplots.py path_to_txt_files
#output: 3D plot 
#for the 3D plot to be generated there needs to be at least 3 competing transfers


def main():
	dirs = [d for d in os.listdir(os.getcwd()) if d.startswith(sys.argv[1]) and os.path.isdir(d)]
	
	print(dirs)
	for d in dirs:
		#print(os.getcwd())
		os.chdir(os.path.join(sys.argv[1],d))
		print(os.getcwd())
		for file in os.listdir(os.getcwd()):

			if file.endswith('.txt') and os.path.getsize(file) > 1000:
				print(file)
				print(os.path.getsize(file))
		#os.chdir('../')
	#exit(0)
				df = pd.read_csv(file, sep=" ", header=None)
				print(df)
				#fig = plt.figure('scatter dates')
				#fig = plt.figure(figsize=plt.figaspect(0.5))
				#ax = fig.add_subplot(1, 2, 1, projection='3d')
				#ax = fig.add_subplot(projection='3d')
				fig = plt.figure(figsize=(9,8))
				ax = fig.add_subplot(projection='3d')
				#dates = pd.to_datetime(df.iloc[:,4], format= '%H:%M:%S.%f')
				dates = pd.to_datetime(df.iloc[:,4], format= 'mixed')
				date_range = dates.iloc[-1] - dates.iloc[0]
				print(date_range.total_seconds())

			#to_pydatetime
				print(dates)

			
				dates2 = matplotlib.dates.date2num(dates)
				x = np.arange(len(dates2))
				y = df.iloc[:,2]
				z = df.iloc[:,7]
			

				ax.scatter3D(dates2, y, z,s=20)
			
			
			#ax.set_xticks(x)
			#ax.xaxis.set_ticks(x)
				plt.xticks(rotation=25,fontsize=18, va='top')
				#ax.xaxis.set_ticklabels(dates2)
				if date_range.total_seconds() > 1800 and date_range.total_seconds() < 3600:

					f = 30
					xlocator = mdates.SecondLocator(interval=f)
					print(int(date_range.total_seconds()/3600))
				elif int(date_range.total_seconds()/3600) > 1:
					f = 1
					#xlocator = mdates.MinuteLocator(byminute=[0, 15, 30, 45], interval = 1)	
					xlocator = mdates.HourLocator(interval=2)
				else:
					f = 15
					xlocator= mdates.MinuteLocator(interval=f)
				print(int(f))
				#xlocator = mdates.MinuteLocator(byminute=[0, 15, 30, 45], interval = 1)	
				#ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=f))
				ax.xaxis.set_major_locator(xlocator)
				xfmt = mdates.DateFormatter('%H:%M:%S')
				ax.xaxis.set_major_formatter(xfmt)
				#ax.set_xlabel('Time of day', fontweight ='bold', fontsize = 8, va='bottom')
				ax.set_ylabel('\n'+'\n'+'Throughput MB/s', fontsize=18,**hfont) 
				#ax.yaxis.set_label_coords(-.1, .1)
				ax.set_zlabel('\n'+'\n'+'Retransmission %', fontsize=18,**hfont) 
				#ax.yaxis.set_label_coords(-.1, .1)
				ax.tick_params(axis='both', which='major', labelsize=15,pad=10)
				#plt.show()
				name_2 = file+ '_competing_new.png'
				fig.savefig(name_2)
				plt.clf()
			else:
				print('Small file')
		os.chdir('../../..')






if __name__=="__main__":
	main()