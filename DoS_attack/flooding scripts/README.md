Mavlink Message Generation Test
==
This script will creates `NUM_ITERATION` of messages print out the result in seconds/message to console.

## Set up
Installation

```bash
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo pip2 install -U future lxml
sudo pip2 install -U pymavlink
```

## Running
```bash
python mavlink_frequency_test.py
```
With options.
```bash
python mavlink_frequency_test.py --num_msg 1000 --mavlink_type 1 --signed 0
```
check ```bash python mavlink_frequency_test.py --help for details```

## Result

### Mavlink 1
NUM_ITERATION |  Total Time  | microseconds / message 
--- | --- | ---|
100| 0.011053 | 111
1000 | 0.084941 | 85
10000 | 0.817931 | 82 
100000 | 8.241825 | 82

### Mavlink 2
NUM_ITERATION |  Total Time  | microseconds / message 
--- | --- | ---|
100| 0.010194 | 102
1000 | 0.093157 | 93
10000 | 0.856401 | 86 
100000 | 9.017876 | 90


### Mavlink 2 with signed (secured)

NUM_ITERATION |  Total Time  | microseconds / message 
--- | --- | ---|
100| 0.011264 | 113
1000 | 0.108109 | 108
10000 | 1.127869 | 113
100000 | 11.270218 | 113