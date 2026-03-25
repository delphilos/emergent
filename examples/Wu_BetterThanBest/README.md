# README: BetterThanBest Simulation

## Overview

This repository contains Python simulation code for the paper:

**"Better than Best" by Jingyi Wu (LSE Philosophy)**

The script implements agent-based simulations on rugged epistemic
landscapes to compare the performance of different social learning
strategies:

-   **Best-response strategy** ("best" agents)
-   **Better-than-current strategy** ("better" agents)
-   **Mixed populations** of both strategies

The goal is to analyze how different updating rules, network structures,
and parameters affect collective epistemic performance.

------------------------------------------------------------------------

## Features

-   Simulates **NK fitness landscapes** (rugged search spaces)
-   Implements **three behavioral strategies**
-   Supports **random directed social networks**
-   Runs **multiple simulations in parallel**
-   Tracks **average normalized performance over time**

------------------------------------------------------------------------

## Requirements

Originally written for **Python 2.7**

### Dependencies

-   numpy
-   scipy

------------------------------------------------------------------------

## Parameters

Key parameters:

-   n = 20 (dimensions)
-   k = 5 (ruggedness)
-   total_agents = 100
-   rounds = 200
-   simulation_runs = 1000

------------------------------------------------------------------------

## Model Description

### Landscape

-   NK model with binary strings
-   Payoffs from random valuation structure

### Network

-   Random directed network
-   Ensured to be strongly connected

### Strategies

-   Best: copy highest-performing neighbor
-   Better: copy any better-performing neighbor
-   Mixed: combination of both

------------------------------------------------------------------------

## Output

Returns time-series performance data normalized by global maximum.

------------------------------------------------------------------------

## How to Run

``` bash
python Wu_BetterThanBest.py
```

------------------------------------------------------------------------

## License

Creative Commons Attribution 4.0 International License

------------------------------------------------------------------------

## Contact

Jingyi Wu\
Jingyi.Wu@uci.edu
