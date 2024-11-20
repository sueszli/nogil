# 
# system specs
# 

# macos
system_profiler SPSoftwareDataType SPHardwareDataType

# linux
lscpu
cat /proc/meminfo

# 
# benchmark
# 

hyperfine --export-csv ../data/itertools.csv --export-json ../data/itertools.json --export-markdown ../data/itertools.md "python ./0_plain/itertools.py aaa"
hyperfine --export-csv ../data/lib.csv --export-json ../data/lib.json --export-markdown ../data/lib.md "python ./0_plain/lib.py aaa"
hyperfine --export-csv ../data/plain.csv --export-json ../data/plain.json --export-markdown ../data/plain.md "python ./0_plain/plain.py aaa"

hyperfine --export-csv ../data/imap_unordered.csv --export-json ../data/imap_unordered.json --export-markdown ../data/imap_unordered.md "python ./1_multiprocessing/imap_unordered.py aaa"
hyperfine --export-csv ../data/imap.csv --export-json ../data/imap.json --export-markdown ../data/imap.md "python ./1_multiprocessing/imap.py aaa"
hyperfine --export-csv ../data/map_async.csv --export-json ../data/map_async.json --export-markdown ../data/map_async.md "python ./1_multiprocessing/map_async.py aaa"
hyperfine --export-csv ../data/map.csv --export-json ../data/map.json --export-markdown ../data/map.md "python ./1_multiprocessing/map.py aaa"
