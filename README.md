# Installation
### PIP
To install the TSP Human benchmark use:\
`pip install .`

### Conda env
Create new environment \
`conda create -n KSY python=3.9`\
Activate conda env \
`conda activate KSY` \
Pip install package \
`pip install .`

# Usage
### Experiment gui
run the main script run_experiment.py
`python3 run_experiment.py`

### Graph evaluation

`python3 results`

### Input Flags
- -n --name runs single experiment with the specified name
- -nl --nologs prevents app from saving logs into tests_runs
- -d --debug debug mode for testing

# Data logging
experiment data saved in tests_runs.
structure example:
```
{
  "1_6_9": {
        "path": [
            {
                "point1": "0",
                "point2": "1"
            },
            {
                "point1": "0",
                "point2": "2"
            },
            {
                "point1": "2",
                "point2": "3"
            },
            {
                "point1": "3",
                "point2": "5"
            },
            {
                "point1": "4",
                "point2": "5"
            },
            {
                "point1": "1",
                "point2": "4"
            }
        ],
        "time": 7.496798038482666,
        "path_len": 639.6063456307053,
        "opt_len": 547.2615592479706,
        "num_action": 6
    },
    "1_6_9OPTIMIZE": {
        "path": [
            {
                "point1": "1",
                "point2": "2"
            },
            {
                "point1": "0",
                "point2": "2"
            },
            {
                "point1": "0",
                "point2": "3"
            },
            {
                "point1": "3",
                "point2": "5"
            },
            {
                "point1": "4",
                "point2": "5"
            },
            {
                "point1": "1",
                "point2": "4"
            }
        ],
        "time": 33.83657908439636,
        "path_len": 547.2615814670652,
        "opt_len": 547.2615592479706,
        "num_action": 6
    },
}  
```

# TODO
 - DATA Logging add more info to readme
 - evaluation data scripts to take directory argument where exp. data stored
 - AI evaluation