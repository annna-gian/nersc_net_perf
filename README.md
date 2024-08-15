# nersc_net_perf
Network performance analysis and bottleneck identification for HPC networks

## Volume analysis
Volume towards/from NERSC, towards/from DTNs, using Globus service and comparisons between the three is calculated by running: \
`python totals.py [list of tstat_file.json]` \
`python esnet_totals.py border_router_file.csv`\
To generate bar charts for the results: \
`python total_bars.py`\
example of input list containing tstat records:\
`[dtn-tstat-2022.02-data.json, dtn-tstat-2022.03-data.json, ...]`
## Flow size analysis
To generate CDF graphs for different types of transfers run:\
`python cdf.py [list of tstat_file.json]` \
supported transfer types are: incomming/outgoing, Globus/non-Globus

## Number of flows handled by each DTN
To calculate the number of flows handled per DTN per month run: \
`python tstat_days.py [list of tstat_file.json]` \
To plot the number of flows per DTN over 12 month period (Jan to Dec) run: \
`python summary.py`

## Competing transfer detection
To identify the ten largest (in terms of volume) \
ingress and egress flows for each NERSC DTN per month and detect all \
other incoming competing flows during the active window for each one \
of the 10 largest transfers run: \
`python competing_in.py [ list of tstat_file.json]` \
 The following elements per competing transfer are extracted and stored in `competing_transfer_in_example.txt`: source/destination pair, transfer size, start time, end time, throughput, and number of retransmitted packets. \
 To plot relationship between time,throughout and retransmissions for all competing transfers during active time windows run: \
 `python 3Dplots.py` \
 The same process needs to be repeated for outgoing competing transfers (`python competing_transfers.py [list of tstat_file.json]`

 ## Active transfers and retransmission analysis
To detect the day with the highest number of monthly transfers for each DTN, extract all active transfers for that day and isolate the number of retransmitted packets per transfer run: \
`python tstat_days.py [list of tstat_file.json]` \
The relationship between active transfer retransmission and throughput is depicted in the script's dedicated graphs.


## Copyright
Network performance analysis for HPC data centers (net_perf) Copyright (c) 2024, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.
