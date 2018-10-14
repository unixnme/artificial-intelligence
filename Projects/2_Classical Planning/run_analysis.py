from run_search import main
import sys

problems = [2]
searches = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

problems_field = ['problem']
searches_field = ['search']
actions_field = ['action']
expansions_field = ['expansion']
plength_field = ['plength']
time_field = ['time']

stdout = sys.stdout

for p in problems:
    for s in searches:

        problems_field.append(p)
        searches_field.append(s)
        sys.stdout = stdout
        print('problem %d search %d' % (p, s))
        sys.stdout.flush()

        with open('logfile', 'w') as f:
            sys.stdout = f
            main([p], [s])

        with open('logfile', 'r') as f:
            lines = f.readlines()
            actions, expansions = lines[4].split()[:2]
            plength = lines[6].split()[2]
            time = lines[6].split()[-1]

            actions, expansions, plength, time = float(actions), float(expansions), float(plength), float(time)
            actions_field.append(actions)
            expansions_field.append(expansions)
            plength_field.append(plength)
            time_field.append(time)

sys.stdout = stdout

for array in [problems_field, searches_field, actions_field, expansions_field, plength_field, time_field]:
    print(array[0] + '\t', end='')
    for elem in array[1:]:
        print('%f\t' % elem, end='')
    print()
