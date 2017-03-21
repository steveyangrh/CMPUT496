#!/bin/bash

gogui-twogtp -size 5 -komi 6.5 -games 100 -black "Go4 Origin/Go4.py --sim 50" -white "Go4ACAD/Go4.py --sim 50" -sgffile test4 -auto -threads 8 -alternate
