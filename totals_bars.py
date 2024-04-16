#!/usr/bin/env python 

import matplotlib.pyplot as plt
import numpy as np

species = ("2020", "2021", "2022")
penguin_means = {
   #'Total ingress traffic' : (171,156.7, 158.5),
   #'Globus ingress traffic' : (101,65.2,46.1),
    'Total egress traffic': (137.1,164.7,186.5),
    'Globus egress traffic': (43.6, 30.8, 31.5),
    
}
colors = {"Total egress traffic":"royalblue",
     "Globus egress traffic":"lightsteelblue"}


#'DTN egress traffic' : (44.7,34.2,32.7),
x = np.arange(len(species))  # the label locations
width = 0.45  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(figsize=(8,8))

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    print(attribute)
    #print(colors['Globus egress traffic'])
    print(colors[attribute])
    c = colors[attribute]
    rects = ax.bar(x + offset, measurement, width, label=attribute,color=c)
    ax.bar_label(rects, padding=2,fontsize=18)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Traffic Volume (PB)',fontsize=18)
#ax.set_title('Penguin attributes by species')
ax.set_xticks(x + 0.5*width, species)
ax.legend(loc='upper left', ncols=1, fontsize=18)
ax.tick_params(axis='both', labelsize=18)
ax.set_ylim(0, 250)
plt.tight_layout()

name_2 = 'total_dtn_test_out_2.png'
plt.savefig(name_2)
plt.clf()