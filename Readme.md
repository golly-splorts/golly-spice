# golly-spice

Re-simulating every Golly match, with better instrumentation.


## Data Format: Spice Inputs

A standard Golly game is used as the input to the golly-spice simulator.
It contains the following fields:

```
        {
            "gameid"
            "team1Name"
            "team2Name"
            "season"
            "day"
            "league"
            "team1Color"
            "team2Color"
            "team1WinLoss"
            "team2WinLoss"
            "map": {
                "patternName"
                "mapName"
                "mapZone1Name"
                "mapZone2Name"
                "mapZone3Name"
                "mapZone4Name"
                "initialConditions1"
                "initialConditions2"
                "url"
                "rows"
                "columns"
                "cellSize"
            }
            "team1Score"
            "team2Score"
            "generations"
            "isPostseason"
            "team1Abbr"
            "team2Abbr"
        }
```

The `gameid` field contains a UUID that is the unique game ID.

## Data Format: Spice Outputs

When that game is simulated with the instrumented simulator,
it will generate various time series of metrics from during
the match.

These are exported to a file named `<game uuid>.json`.
That json file has the following structure:

```
    {
        "liveCells1": [1, 2, 3, 4, ... ],
        "liveCells2": [5, 6, 7, 8, ... ],
        "last3": [[0.01, 0.02, 0.03], [0.04, 0.05, 0.06], ...]
    }
```

The keys used to save cell counts are the same fields as the
ones in the data structure returned by the GOL simulator's
get live counts method (see gollyx-python library).

## Scripts

Scripts to run simulations of prior games are in the `scripts/` directory.

This is the approach used if you're simulating on a single machine, and just gonna
let it sit and churn through all the calculations with multiple threads.

This is a bit complicated, because have to transfer some code from the backend generator
approach to multithreading, and that code is troublesome to troubleshoot.

