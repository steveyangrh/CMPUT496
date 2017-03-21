#!/bin/bash

gogui-twogtp -size 5 -komi 6.5 -games 100 -black "Go4/Go4.py --sim 50" -white "Go4/Go4AC.py --sim 50" -sgffile test3 -auto -thread 8 -alternate
