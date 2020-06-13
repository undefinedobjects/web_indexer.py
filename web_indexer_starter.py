import os

for number in range(90,100):
    start = "172." + str(number) + ".0.0"
    end = "172." + str((number + 1)) + ".0.0"
    os.system("start web_indexer.py -s " + start + " -e " + end)
