
To generate smaller samples of the dumps, an ``awk`` command was used to skip
every 10 lines of the original dump and of the succesive samples::

  $ awk 'NR % 10 == 1' ol_dump_editions_20120404.txt > ol_dump_editions_20120404_10pct.txt
  $ awk 'NR % 10 == 1' ol_dump_editions_20120404_10pct.txt > ol_dump_editions_20120404_1pct.txt
  $ awk 'NR % 10 == 1' ol_dump_editions_20120404_1pct.txt > ol_dump_editions_20120404_0.1pct.txt

The first command took about 13 minutes to complete on a MacBook Pro 2011
with i7 and 8GB of RAM. The other commands, less than two minutes total. 
The files ``*_10pct.txt``, ``*_1pct.txt`` and ``*0.1pct.txt`` contain 
approximately 10%, 1% and 0.1% of the original records.

Given a sample of editions, the next step is to obtain a matching sample of
authors and works, taking into account that editions contain keys that point
to author and work records.

