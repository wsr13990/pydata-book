import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np

path = 'ch02\\usagov_bitly_data2012-03-16-1331923249.txt'
open(path).readline()

#Parsing json data acquired from file in the path
records = [json.loads(line) for line in open(path)]

#Create time_zones array containing data in the 'tz' tag
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

#Count the occurence of particular time_zones
def get_counts(sequence):
	counts = {}
	for x in sequence:
		if x in counts:
			counts[x] += 1
		else:
			counts[x] = 1
	return counts

#Alternative method to get_counts
def get_counts2(sequence):
	counts = defaultdict(int) #value will initialize to 0
	for x in sequence:
		counts[x] += 1
	return counts

#Get the top occurence of time_zones	
def top_counts(count_dict, n = 10):
	value_key_pairs = [(count,tz) for tz, count in count_dict.items()]
	value_key_pairs.sort()
	return value_key_pairs[-n:]

counts = Counter(time_zones)

#Put the parsed data int the DataFrame
frame = DataFrame(records)

#Replace the "" and N/A data with missing and unknown
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'

tz_counts = clean_tz.value_counts()

#Display the horizontal bar of time_zones count
#tz_counts[:10].plot(kind = 'barh', rot = 0)
#plot.show()

#Split the data ini dataframe
results = Series([x.split()[0] for x in frame.a.dropna()])
result = results.value_counts()[:8]
#print(result)


#Group the data based on operating_system & time_zones then count its size
#...and display it 
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows')
	,'Windows','Not Windows')
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)

#Select the overall time_zones
indexer = agg_counts.sum(1).argsort()
print(indexer[:10])
