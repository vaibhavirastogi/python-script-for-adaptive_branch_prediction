# adaptive_branch_prediction
Code for two-level adaptive branch prediction project for CSCE 614

This repository currently contains a Python script. 
The project is implementing A2/A3 branch prediction automatons and running simulations on 9 separate benchmarks in ZSIM simulator. 
The Python script goes into each benchmark directory and extracts total cycles, total instructions, total branch mispredictions, and total conditional branches for 8 cores,
for each benchmark.
It then computes CPI and misprediction rate and gives it as output. It allows me to compare performance between different benchmarks and different prediction automatons.
