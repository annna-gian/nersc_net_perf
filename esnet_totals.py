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

#compute total in/out traffic volume (in PB) at the NERSC border- yearly
#to run: python esnet_totals.py border_traffic.csv
#input: border router data from ESnet in csv format
#output: total incoming and outgoing traffic in PB
def main():
	df = pd.read_csv(sys.argv[1])
	print(df.columns.values.tolist())
	print(df.info())
	df['Time'] = pd.to_datetime(df['Time'], format= '%Y-%m-%d %H:%M:%S') 
	df = df.rename(columns={'Total Out': 'total_out', 'Total In':'total_in'})
	df['total_out'] = df['total_out'].astype(str)
	print(df.info())
	start_date = '2022-01-01 00:00:00'
	end_date = '2022-12-31 00:00:00'
	mask = (df['Time'] > start_date) & (df['Time'] <= end_date)
	df_2020 = df.loc[mask]
	#print(df_2020.info())
	df_2020['total_out'] = df_2020['total_out'].map(str)
	df_2020['total_in'] = df_2020['total_in'].map(str)
	print(df_2020.info())
	print('lalalalall')
	print(df_2020[df_2020['total_out'].str.contains("GB")].total_out)
	df_2020[df_2020['total_out'].str.contains("GB")].total_out = df_2020[df_2020['total_out'].str.contains("GB")].total_out.str.replace(r'\D', '', regex=True).astype(int)/1024
	#if df_2020['Total Out'].str.contains('GB').any():
	df_2020[df_2020['total_in'].astype(str).str.contains("GB")].total_in = df_2020[df_2020['total_in'].str.contains("GB")].total_in.str.replace(r'\D', '', regex=True).astype(int)/1024 
	df_2020['total_out'] = df_2020['total_out'].str.replace(r'\D', '', regex=True).astype(int)
	df_2020['total_in'] = df_2020['total_in'].str.replace(r'\D', '', regex=True).astype(int)
	print(df_2020['total_out'].sum())
	print(df_2020['total_in'].sum())







if __name__=="__main__":
	main()