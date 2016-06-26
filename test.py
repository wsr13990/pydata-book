import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plot

path = 'ch02\\usagov_bitly_data2012-03-16-1331923249.txt'
open(path).readline()

records = [json.loads(line) for line in open(path)]

time_zones = [rec['tz'] for rec in records if 'tz' in rec]

def get_counts(sequence):
	counts = {}
	for x in sequence:
		if x in counts:
			counts[x] += 1
		else:
			counts[x] = 1
	return counts
	
def get_counts2(sequence):
	counts = defaultdict(int) #value will initialize to 0
	for x in sequence:
		counts[x] += 1
	return counts
	
def top_counts(count_dict, n = 10):
	value_key_pairs = [(count,tz) for tz, count in count_dict.items()]
	value_key_pairs.sort()
	return value_key_pairs[-n:]
	
counts = Counter(time_zones)
frame = DataFrame(records)

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'

tz_counts = clean_tz.value_counts()
tz_counts[:10].plot(kind = 'barh', rot = 0)
plot.show()
