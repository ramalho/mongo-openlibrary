#!/usr/bin/env python

import sys
import bz2
import pickle

try:
	dump_file_name = sys.argv[1]
except IndexError:
	print 'Plase provide the dump file name (.bz2 format assumed)'
	sys.exit(1)
	
if 'works' in dump_file_name:
	field_name = 'works'
elif 'authors' in dump_file_name:
	field_name = 'authors'
else:
	print 'The dump file name must contain either "works" or "authors"'
	sys.exit(1)
	
file_name = field_name+'.pickle'
with open(file_name, 'rb') as infile:
	links = pickle.load(infile)
	print file_name, 'loaded'

linked = 0
with bz2.BZ2File(dump_file_name) as indump:
	outfile_name = dump_file_name.replace('.txt', '_SAMPLE.txt')
	print 'scanning', dump_file_name
	with bz2.BZ2File(outfile_name, 'w') as outfile:
		for count, lin in enumerate(indump, 1):
			rec_type, rec_id, revision, modified, document = lin.split('\t')
			key = rec_id.replace('/%s/'%field_name,'') 
			if key in links:
				outfile.write(lin)
				links.remove(key)
				linked += 1
				if not links:
					break # no more items to find
			if count % 10000 == 0:
				print '%8d %s read, %s linked' % (count, field_name, linked)

print '%8d %s read, %s linked' % (count, field_name, linked)
print outfile_name, 'written'
