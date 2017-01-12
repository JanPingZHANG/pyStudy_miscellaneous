import json

def get_counts(sequence):
	counts = {}
	for x in sequence:
		if x in counts:
			counts[x] += 1
		else:
			counts[x] = 1
	return counts

def top_counts(count_dict,n=10):
	value_key_pairs = [(count,tz) for tz,count in count_dict.items() ]
	value_key_pairs.sort(reverse = True)
	return value_key_pairs[0:n]

path = 'usago_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
time_zones = [elem['tz'] for elem in records if 'tz' in elem]
counts = get_counts(time_zones)
#print 'America/New_York is :', counts['America/New_York']
#print 'time_zones data count is : ',len(time_zones)
#print 'time_zones counts is : ',len(counts)
top10 = top_counts(counts)
#print 'top 10 time_zones is : '
for top in top10:
	print top

from pandas import DataFrame,Series
import pandas as pd
import numpy as np
frame = DataFrame(records)
#print 'DataFrame records is : \n',frame
#print 'DataFrame top10 is : \n',frame['tz'][:10]
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
#print 'DataFrame top10 is : \n',tz_counts[:10]
tz_counts[:10].plot(kind='barh',rot=0)

results = Series([x.split()[0] for x in frame.a.dropna()])
#print results[:10]
#print results.value_counts()[:8]

cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'),'windows','not windows')
#print operating_system[:5]

by_tz_os = cframe.groupby(['tz',operating_system])
#print by_tz_os
#print 'size : ',by_tz_os.size()
agg_counts = by_tz_os.size().unstack()
print agg_counts
