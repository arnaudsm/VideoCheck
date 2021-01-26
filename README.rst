==========
videocheck
==========


.. image:: https://img.shields.io/pypi/v/videocheck.svg
        :target: https://pypi.python.org/pypi/videocheck

Automated tool to check consistency of your video library.


* Free software: MIT license


Usage
--------

```bash
videocheck [OPTIONS] [PATHS]...

  Automated tool to check consistency of your video library.

Options:
  -o, --output FILE           Output file path (csv file)
  -e, --extensions TEXT       Video extensions to scan
  -f, --forbidden-hours TEXT  Forbidden hours (useful for multi-day scans),
                              example: 18-23 to forbid scanning between 18h
                              and 23h
  -t, --threads INTEGER       CPU threads for FFmpeg
  -d, --delete                Delete corrupt files after scanning
  --help                      Show this message and exit.
```

Output Example
--------
```bash
🏁 2 files to check
✅ ~/Videos/ok.mp4
❌ ~/Videos/ko.mp4
100%|██████████████████████████| 2/2 [00:00<00:00, 16.99it/s]
##############################
SCAN DONE
1/2 faulty videos detected 🚨 

Report file available: ./videochecked.csv
Tip: Use --delete to delete them
OVER ✅
```
