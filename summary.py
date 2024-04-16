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




def main():



	#interactive 2022
	dtns = {'dtn-tstat-2022.01-data.json': [91836, 42654, 0, 405841], 'dtn-tstat-2022.02-data.json': [20673, 3394, 0, 75929], 'dtn-tstat-2022.03-data.json': [30606, 12098, 0, 143663], 'dtn-tstat-2022.04-data.json': [226664, 32572, 0, 901531], 'dtn-tstat-2022.05-data.json': [253257, 72489, 0, 1029724], 'dtn-tstat-2022.06-data.json': [249272, 42647, 0, 747812], 'dtn-tstat-2022.07-data.json': [230744, 42248, 0, 586500], 'dtn-tstat-2022.08-data.json': [666962, 97250, 0, 422999], 'dtn-tstat-2022.09-data.json': [457326, 29443, 0, 259363], 'dtn-tstat-2022.10-data.json': [297831, 3830, 0, 194962], 'dtn-tstat-2022.11-data.json': [518923, 17617, 0, 204351], 'dtn-tstat-2022.12-data.json': [69628, 12842, 0, 390379]}

	#interactive 2020

	#dtns = {'dtn-tstat-2020.01-data.json': [2061, 58583, 0, 18156], 'dtn-tstat-2020.02-data.json': [1642, 24138, 0, 26483], 'dtn-tstat-2020.03-data.json': [750, 21506, 0, 36701], 'dtn-tstat-2020.04-data.json': [1181, 41963, 0, 40272], 'dtn-tstat-2020.05-data.json': [7495, 80249, 0, 129601], 'dtn-tstat-2020.06-data.json': [2986, 23341, 0, 64603], 'dtn-tstat-2020.07-data.json': [1413, 7202, 0, 12141], 'dtn-tstat-2020.08-data.json': [1359, 1969, 28, 9242], 'dtn-tstat-2020.09-data.json': [1794, 936, 0, 8185], 'dtn-tstat-2020.10-data.json': [1624, 31472, 0, 1063], 'dtn-tstat-2020.11-data.json': [12014, 24159, 0, 2585], 'dtn-tstat-2020.12-data.json': [2358, 6214, 0, 36933]}

	#interactive 2021
	#dtns ={'dtn-tstat-2021.01-data.json': [2178, 6339, 0, 10070], 'dtn-tstat-2021.02-data.json': [2734, 3311, 1850, 8801], 'dtn-tstat-2021.03-data.json': [6280, 3679, 0, 28812], 'dtn-tstat-2021.04-data.json': [67560, 7406, 0, 143123], 'dtn-tstat-2021.05-data.json': [103623, 22986, 0, 260315], 'dtn-tstat-2021.06-data.json': [89174, 35334, 0, 307734], 'dtn-tstat-2021.07-data.json': [171722, 29281, 0, 326004], 'dtn-tstat-2021.08-data.json': [188395, 28010, 0, 132127], 'dtn-tstat-2021.09-data.json': [148437, 7154, 0, 47472], 'dtn-tstat-2021.10-data.json': [141464, 22051, 0, 7917], 'dtn-tstat-2021.11-data.json': [0, 0, 0, 0], 'dtn-tstat-2021.12-data.json': [0, 0, 0, 0]}
	#globus 2020
	#dtns = {'dtn-tstat-2020.01-data.json': [67173, 45268, 79604, 70968, 49358, 59414, 174800], 'dtn-tstat-2020.02-data.json': [59674, 41079, 31689, 30496, 16904, 47921, 287428], 'dtn-tstat-2020.03-data.json': [69521, 51454, 29173, 39071, 23834, 39508, 128452], 'dtn-tstat-2020.04-data.json': [54238, 34892, 26593, 28531, 35472, 8401, 111313], 'dtn-tstat-2020.05-data.json': [73582, 59234, 50382, 69761, 48598, 32, 205499], 'dtn-tstat-2020.06-data.json': [53889, 39890, 33108, 51174, 26682, 1873, 111971], 'dtn-tstat-2020.07-data.json': [54192, 74587, 46441, 66667, 43304, 5301, 130680], 'dtn-tstat-2020.08-data.json': [47631, 31000, 51658, 39179, 33043, 183, 82660], 'dtn-tstat-2020.09-data.json': [59285, 64429, 45808, 73352, 72601, 148, 200072], 'dtn-tstat-2020.10-data.json': [31952, 22920, 10883, 30286, 24668, 955, 83524], 'dtn-tstat-2020.11-data.json': [47621, 26219, 24388, 34697, 31019, 5657, 100106], 'dtn-tstat-2020.12-data.json': [45385, 57567, 38174, 30919, 25675, 26762, 181265]}
	#globus 2021
	#dtns = {'dtn-tstat-2021.01-data.json': [41777, 39112, 37795, 22147, 33940, 1578, 313384], 'dtn-tstat-2021.02-data.json': [39467, 22875, 80974, 58866, 82780, 6050, 188792], 'dtn-tstat-2021.03-data.json': [59901, 30832, 87835, 48944, 89999, 3217, 10241], 'dtn-tstat-2021.04-data.json': [37327, 15686, 28905, 62638, 27122, 3642, 65663], 'dtn-tstat-2021.05-data.json': [53024, 27993, 39283, 55007, 42536, 1994, 191041], 'dtn-tstat-2021.06-data.json': [63997, 51763, 40502, 45860, 41513, 1192, 87396], 'dtn-tstat-2021.07-data.json': [17762, 2047, 10448, 12563, 9544, 6289, 142861], 'dtn-tstat-2021.08-data.json': [10045, 2857, 4791, 6003, 2860, 8988, 46843], 'dtn-tstat-2021.09-data.json': [8827, 13257, 26049, 5678, 14436, 80, 26386], 'dtn-tstat-2021.10-data.json': [26660, 7851, 25446, 1128, 24362, 612, 15140], 'dtn-tstat-2021.11-data.json': [0, 0, 0, 0, 0, 0, 0], 'dtn-tstat-2021.12-data.json': [0, 0, 0, 0, 0, 0, 0]}

	#globus 2022
	dtns = {'dtn-tstat-2022.01-data.json': [41683, 12873, 28754, 32255, 37555], 'dtn-tstat-2022.02-data.json': [6196, 1711, 2564, 2615, 6034], 'dtn-tstat-2022.03-data.json': [62100, 7161, 17850, 22380, 48906], 'dtn-tstat-2022.04-data.json': [208385, 15176, 52711, 69230, 170995], 'dtn-tstat-2022.05-data.json': [165898, 74060, 69035, 84554, 136242], 'dtn-tstat-2022.06-data.json': [87558, 53938, 62572, 73649, 65914], 'dtn-tstat-2022.07-data.json': [46461, 62427, 33925, 38441, 37173], 'dtn-tstat-2022.08-data.json': [62710,16966, 23701, 39382, 20272], 'dtn-tstat-2022.09-data.json': [62723,48097, 34865, 57732, 30001], 'dtn-tstat-2022.10-data.json': [27259, 58845, 7302, 22331, 5622], 'dtn-tstat-2022.11-data.json': [27159, 38911, 16069, 30595, 15585], 'dtn-tstat-2022.12-data.json': [39908, 19004, 17762, 12821, 18099]}
	df = pd.DataFrame.from_dict(dtns, orient='index', columns=['DTN5', 'DTN6', 'DTN7','DTN8', 'DTN9','DTN10', 'DTN11'])
	#df = pd.DataFrame.from_dict(dtns, orient='index', columns=['DTN1', 'DTN2', 'DTN3','DTN4'])
	print(df)
	labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July','Aug','Sep','Oct', 'Nov','Dec']
	#dtn_names = ['DTN5', 'DTN6', 'DTN7','DTN8', 'DTN9','DTN10', 'DTN11'
	#labels = ['DTN1','DTN2', 'DTN4']
	x = range(0,len(labels))

	# plt.plot(x,df['DTN1'], label = 'dtn01', ls='--', color ='red',marker='D',mfc='red',linewidth=3)
	# plt.plot(x,df['DTN2'], label = 'dtn02', ls='-', color ='green',marker='D',mfc='red',linewidth=3)
	# plt.plot(x,df['DTN4'], label = 'dtn04', ls='dashdot', color ='magenta',marker='D',mfc='red',linewidth=3)

	plt.plot(x,df['DTN5'], label = 'dtn05', ls='--', color ='red',marker='D',mfc='red',linewidth=3)
	plt.plot(x,df['DTN6'], label = 'dtn06', ls='-', color ='green',marker='D',mfc='red',linewidth=3)
	plt.plot(x,df['DTN7'], label = 'dtn07', ls='dashdot', color ='magenta',marker='D',mfc='red',linewidth=3)
	plt.plot(x,df['DTN8'], label = 'dtn08', ls='dotted', color ='blue',marker='D',mfc='red',linewidth=3)
	plt.plot(x,df['DTN9'], label = 'dtn09', ls='dotted', color ='k',marker='D',mfc='red',linewidth=3)
	#plt.plot(x,df['DTN10'], label = 'dtn10', ls='dotted', color ='purple',marker='D',mfc='red',linewidth=3)
	plt.xticks(x,labels,fontsize=18,rotation=45)
	plt.ylim(0,250000)
	#plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.ylabel("Number of transfers", fontsize=18)

	plt.legend(fontsize=18)
	#plt.savefig('non_globus_2022_v3.png', bbox_inches='tight')
	plt.savefig('globus_2021_v3.png', bbox_inches='tight')
	#plt.show()




	


if __name__=="__main__":
	main()