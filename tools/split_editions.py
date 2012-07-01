#!/usr/bin/env python

'''
Read complete dump file (.gz compressed) and export edition records to 100
different files according to the last 2 digits of the primary key (excluding
the letter suffix). For example:

    /books/OL1656966M goes to the edition_66 file
    /books/OL3M       goes to the edition_03 file

Any record with a key that does not match the '/books/OL\d+M' format goes into
a separate file with _NONSTD_KEYS suffix.    

'''

from __future__ import unicode_literals, print_function

import gzip
import sys
import os
import io
import json
import re

RE_EDITION_KEY = re.compile(r'/books/OL(\d+)M')

def shard_key(key, no_match=''):
    '''
        >>> shard_key('/books/OL1656966M') == '66'
        True
        >>> shard_key('/books/OL3M') == '03'
        True
        >>> shard_key('/books/New_Yorker_book_of_lives', '??') == '??'
        True
    '''
    res = RE_EDITION_KEY.match(key)
    if res:
        digits = res.group(1)
        return digits[-2:] if len(digits) > 1 else '0'+digits
    return no_match

def main():
    infile_name = sys.argv[1]
    outfile_base_name, ext = os.path.splitext(infile_name)
    opener = gzip.GzipFile if ext == '.gz' else open

    outfile_names = ['{0}_{1:02d}'.format(outfile_base_name, i) for i in range(100)]
    outfile_names.append(outfile_base_name+'_NONSTD_KEYS')
    outfiles = [io.open(fn, 'wt', encoding='utf-8') for fn in outfile_names]

    editions_ct = 0
    with opener(infile_name) as infile:
        for line_ct, line in enumerate(infile, 1):
            line = line.decode('utf-8')
            rec_type, rec_key, rec_rev, rec_ts, rec_json = line.split('\t')
            if rec_type != '/type/edition':
                continue
            editions_ct += 1
            rec = json.loads(rec_json)
            rec_id = rec_key if rec_rev == '1' else rec_key+'-'+rec_rev
            rec['_id'] = rec_id
            shard = int(shard_key(rec_key, '100'))
            outfiles[int(shard)].write(json.dumps(rec)+'\n')
            if editions_ct % 100000 == 0:
                print(line_ct, editions_ct, shard, rec_id)

    print(line_ct, editions_ct, shard, rec_id)

    for f in outfiles:
        f.close()

if __name__=='__main__':
    main()

