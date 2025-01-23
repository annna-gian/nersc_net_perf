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

def main():
    globus_nodes = ['dtn05.nersc.gov', 'dtn06.nersc.gov', 'dtn07.nersc.gov', 'dtn08.nersc.gov', 'dtn09.nersc.gov', 'dtn10.nersc.gov', 'dtn11.nersc.gov']

    total_ew = 0
    total_out_ns = 0
    total_in_ns = 0
    total_size_globus_out = 0
    total_size_globus_in = 0

    interactive = ['128.55.205.18', '128.55.205.19', '128.55.205.20', '128.55.205.21', 
                   'dtn01.nersc.gov', 'dtn02.nersc.gov', 'dtn03.nersc.gov', 'dtn04.nersc.gov']

    
            for file in sys.argv[1:]:
                with open(file, 'r') as f:
                    tstat_data = [json.loads(line) for line in f]
                    if '2022' in f.name:
                        print('Its a 2022 file')
                        for i in tstat_data:
                            if '.nersc.gov' in i['_source']['source'] and '.nersc.gov' in i['_source']['dest']:
                                print('EW traffic DTNs')
                                total_ew += float(i['_source']['values']['file_size_MB'])
                            elif '.nersc.gov' in i['_source']['source'] and '.nersc.gov' not in i['_source']['dest']:
                                print('NS traffic-leaving NERSC')
                                total_out_ns += float(i['_source']['values']['file_size_MB'])
                                if (50000 <= int(i['_source']['meta']['src_port']) <= 51000 and 
                                    50000 <= int(i['_source']['meta']['dst_port']) <= 51000):
                                    print('This is a globus transfer')
                                    total_size_globus_out += float(i['_source']['values']['file_size_MB'])
                            elif '.nersc.gov' in i['_source']['dest'] and '.nersc.gov' not in i['_source']['source']:
                                print('NS traffic-coming NERSC in 2022')
                                total_in_ns += float(i['_source']['values']['file_size_MB'])
                            if (50000 <= int(i['_source']['meta']['src_port']) <= 51000 and 
                                50000 <= int(i['_source']['meta']['dst_port']) <= 51000):
                                print('This is a globus transfer from 2022')
                                total_size_globus_in += float(i['_source']['values']['file_size_MB'])

    print(total_ew)
    print('Border crossing traffic')
    print(total_out_ns / 1024 * 1024)
    print(total_in_ns / 1024 * 1024)
    print(total_out_ns + total_in_ns)
    print('Globus')
    print(total_size_globus_out / 1024 * 1024)
    print(total_size_globus_in / 1024 * 1024)

if __name__ == "__main__":
    main()
