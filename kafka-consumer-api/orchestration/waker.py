import sys
from time import sleep

try:
    x = int(sys.argv[1])
except Exception:
    x = 696969
sleep(x)
