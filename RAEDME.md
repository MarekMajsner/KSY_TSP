# Installation

To install the TSP Human benchmark use `pip install .`.

# Usage
run the main script run_experiment.py
`python3 run_experiment.py`

Input Flags
- n --name runs single experiment with the specified name
- l --nologs (debug option) stops from saving logs into tests_runs
- d --debug does not existm will show optimal path/info???

# Data logging
experiment data saved in tests_runs.
structure example:
```
{
    "10": {
        "experiment": 1,
        "path": [
            {
                "point1": "3",
                "point2": "8"
            },
            {
                "point1": "3",
                "point2": "4"
            },
            {
                "point1": "4",
                "point2": "5"
            },
            {
                "point1": "5",
                "point2": "7"
            },

        "time": 15.975210428237915
    },
    "14": {
        "experiment": 2,
        "path": [
            {
                "point1": "0",
                "point2": "11"
            },
            {
                "point1": "10",
                "point2": "11"
            },

        ],
        "time": 29.374980926513672
    }
}

```

# TODO
 - DATA Logging more info
 - evaluation of data
 - 