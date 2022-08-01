# gollyx-spice

Re-simulating every Golly match, with better instrumentation.

This library consists of the following parts:

* Instrumented cellular automata simulator classes:
    * these classes extend the simulators from the `gollyx-python` library
    * the extended simulators record the score during the course of the game
    * they only record the score, they do not handle file i/o

* Batch manager classes:
    * handle managing all of the simulations for a given season
    * runs them in parallel using thread pool on local machine
    * handles failures and restarts
    * handles writing time series scores from simulations to files
    * handles collating all information into final data files/structures

