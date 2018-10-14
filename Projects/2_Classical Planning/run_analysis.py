import numpy as np
from run_search import main
import sys
import matplotlib.pyplot as plt

problems = [1]
searches = np.arange(1,12).astype(np.int32).tolist()

problems_field = []
searches_field = []
actions_field = []
expansions_field = []
plength_field = []
time_field = []

stdout = sys.stdout

for p in problems:
    for s in searches:

        problems_field.append(p)
        searches_field.append(s)

        with open('logfile', 'w') as f:
            sys.stdout = f
            main([p], [s])

        with open('logfile', 'r') as f:
            lines = f.readlines()
            actions, expansions = lines[4].split()[:2]
            plength, time = np.asarray(lines[6].split())[[2, -1]]

            actions, expansions, plength, time = float(actions), float(expansions), float(plength), float(time)
            actions_field.append(actions)
            expansions_field.append(expansions)
            plength_field.append(plength)
            time_field.append(time)

sys.stdout = stdout

plt.plot(expansions_field, actions_field)
plt.show()

plt.plot(time_field, actions_field)
plt.show()

plt.plot(plength_field, searches_field)
plt.show()
