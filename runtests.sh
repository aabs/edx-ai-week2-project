#!/bin/bash

# Test Case #1
python3 driver.py bfs 3,1,2,0,4,5,6,7,8
python3 driver.py dfs 3,1,2,0,4,5,6,7,8
python3 driver.py ast 3,1,2,0,4,5,6,7,8
python3 driver.py ida 3,1,2,0,4,5,6,7,8

# Test Case #2
python3 driver.py bfs 1,2,5,3,4,0,6,7,8
python3 driver.py dfs 1,2,5,3,4,0,6,7,8
python3 driver.py ast 1,2,5,3,4,0,6,7,8
python3 driver.py ida 1,2,5,3,4,0,6,7,8