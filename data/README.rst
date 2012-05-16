The Open Library dump files can be obtained from:
http://openlibrary.org/developers/dumps

Compressed (bz2) samples of Open Library dumps are available from:
http://turing.com.br/datasets/

To generate smaller samples of the dumps, an ``awk`` command was used to
select one in every 10 lines of the original dump and of the succesive
samples::

  $ awk 'NR % 10 == 1' ol_dump_editions_20120404.txt > \ 
                       ol_dump_editions_20120404_10pct.txt
  $ awk 'NR % 10 == 1' ol_dump_editions_20120404_10pct.txt > \
                       ol_dump_editions_20120404_1pct.txt
  $ awk 'NR % 10 == 1' ol_dump_editions_20120404_1pct.txt > \
                       ol_dump_editions_20120404_0.1pct.txt

The files ``*_10pct.txt``, ``*_1pct.txt`` and ``*0.1pct.txt`` contain 
approximately 10%, 1% and 0.1% of the original records.

The first command took about 13 minutes to complete on a MacBook Pro 
2011 (i7, 8GB of RAM). The other commands, less than two minutes total. 

Given a sample of editions, the next step is to obtain a matching sample
of authors and works, taking into account that editions contain keys 
that point to author and work records. To do that, first run
``get_links.py`` against an ``ol_dump_editions_*`` file::

  $ python get_links ol_dump_editions_20120404_0.1pct.txt
  
This will generate an ``authors.pickle`` and a ``works.pickle`` file,
containing sets of all authors and works ids referenced in the editions
dump. 

Then, run ``select_linked.py`` against the full authors and works
dumps, to select only the records referenced by the chosen editions
dump::

  $ python select_linked.py ol_dump_authors_20120404.txt.bz2

The command above generates a file named 
``ol_dump_authors_20120404_SAMPLE.txt.bz2``. Do the same for the works
dump::

  $ python select_linked.py ol_dump_works_20120404.txt.bz2
