#!/bin/bash

gogui-twogtp -size 5 -games 100 -black "Go3/Go3.py --sim 50" -white "Go4/Go4ACAD.py --sim 50" -sgffile test2 -auto -thread 8 -alternate
