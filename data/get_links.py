#!/usr/bin/env python

import sys
import bz2
import json
import pickle

try:
	dump_file_name = sys.argv[1]
except IndexError:
	print 'Plase provide the "editions" dump file name (.bz2 format assumed)'
	sys.exit(1)

fields = dict(authors=set(), works=set())

with bz2.BZ2File(dump_file_name) as dump:
	for count, lin in enumerate(dump, 1):
		rec_type, rec_id, revision, modified, document = lin.split('\t')
		record = json.loads(document)
		for field_name in fields:
			if field_name in record:
				# set of keys without the /authors/ or /works/ prefix
				keys = {i['key'].replace('/%s/'%field_name,'') 
				        for i in record[field_name]}
				fields[field_name].update(keys)
		if count % 1000 == 0:
			print '%8d records read' % count

print '%8d records read' % count
		
for field_name in fields:
	file_name = field_name+'.pickle'
	with open(file_name, 'wb') as outfile:
		pickle.dump(fields[field_name], outfile, -1)
		print file_name, 'written'
