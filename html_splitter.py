#!/usr/bin/env python3

import sys

if len(sys.argv) == 1:
    print ("no input given")
    sys.exit()

with open(sys.argv[1],"r") as f:
    with open("splitted.txt","w") as o:
        for line in f:
            for char in line:
                if char == "<":
                    o.write("\n"+char)
                else:
                    o.write(char)
