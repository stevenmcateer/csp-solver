William Schwartz and Steven McAteer

TO RUN:
1. Open a terminal
2. Type "python csp-solver.py test_file.txt"
3. "test_file.txt" is the input file with the values

OUR APPROACH:

We used the following algorithms (in order) in our approach:

1. Trace function:
    - Calls backtracking(csp)
    - Loops until failure or success
    - Records the CSP at each step

2. Backtracking(csp):
    if csp is complete then return global_state // all variables have a value
    next_variable = MinRemainingValue(csp)
    ordered_domain = LeastConstrainedValue(variable)

    for each value in ordered_domain: // values of the domain of the current variable
        if arc_3 of current assignment == False):
            // Assignment is not possible
            Remove the value from ordered_domain
        else:
            Set the variable:value pair as assigned
            Delete the variable from unassigned list
            return csp

3. MRV(csp): //Minimum Remaining Value
    #find lowest domain val for a variable and return it
    for all variable:domain in unassigned:
        record the length of each domain list

    if there is only one minimum domain value:
        return the variable:value
    else:
        for variable in min_values:
            record the degree heuristic for each variable
            // this degree function counts the num of
            // binary constraints for each variable

        return min degree heuristic variable


4. Least Constraining Value(variable, csp):

    for each domain value in variable:
        // check the 3 binary constraints
        Re-compute the binary matrices

        for state in current state items:
            record the number of constraints

        // check the time constraint
        times = knowledge_base.check_time_constraint(variable, current_state)

    least_binary_contraining_list = []
    times_list = []

    // compare the list of domain values with time values
    least_binary_contraining_list.sort(

    ordered_domain = []
    for value in least_binary_contraining_list:
        add value to the ordered domain

    return ordered_domain


5. ARC-3 Consistency(variable, csp):
    queue = [variable]

    while queue is not empty:
        variable = unassigned[queue[0]]

        temp_state = recompute_binary_constraints(variable, temp_state)

        // if a domain is empty
        for state in unassigned items:
            if the state domain is empty:
                // no possible assignments
                return False

        // if the domain changes add it to the queue
        for state in unassigned items:
            domain_change = False
            for value in the state's domain:
                if value not in unassigned[state].domain:
                    domain_change = True

            if domain_change is true:
                add the state to the queue

        remove the fist value because it worked
        return


RESULTS:

Example file 1 (test1.txt):
```bash
$ python csp-solver.py test1.txt
There is no solution
```

Example file 2 (test3.txt):
``` bash
$ python csp-solver.py test3.txt
{'q': {}, 'z': {}, 'p': {}, 'x': {}, 'y': {}, 'r': {}}
arc consistent
{'q': {'D': D, 3, ['q']}, 'z': {}, 'p': {}, 'x': {}, 'y': {}, 'r': {}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {}, 'p': {}, 'x': {}, 'y': {}, 'r': {}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {}, 'p': {'K': K, 4, ['p']}, 'x': {}, 'y': {}, 'r': {}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {}, 'p': {'K': K, 4, ['p']}, 'x': {}, 'y': {}, 'r': {'J': J, 19, ['r']}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {}, 'p': {'K': K, 4, ['p']}, 'x': {'I': I, 7, ['x']}, 'y': {}, 'r': {'J': J, 19, ['r']}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {}, 'p': {'K': K, 4, ['p']}, 'x': {'I': I, 7, ['x']}, 'y': {'H': H, 12, ['y']}, 'r': {'J': J, 19, ['r']}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {'L': L, 9, ['z']}, 'p': {'K': K, 4, ['p']}, 'x': {'I': I, 7, ['x']}, 'y': {'H': H, 12, ['y']}, 'r': {'J': J, 19, ['r']}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {'L': L, 9, ['z']}, 'p': {'G': G, 15, ['p'], 'K': K, 4, ['p']}, 'x': {'I': I, 7, ['x']}, 'y': {'H': H, 12, ['y']}, 'r': {'J': J, 19, ['r']}}
arc consistent
{'q': {'C': C, 6, ['q'], 'D': D, 3, ['q']}, 'z': {'L': L, 9, ['z']}, 'p': {'G': G, 15, ['p'], 'K': K, 4, ['p']}, 'x': {'E': E, 5, ['x'], 'I': I, 7, ['x']}, 'y': {'H': H, 12, ['y']}, 'r': {'J': J, 19, ['r']}}
arc consistent
the final result is
q : (time used 9 of 22,  ['C', 'D'])
z : (time used 9 of 22,  ['L'])
p : (time used 19 of 22,  ['G', 'K'])
x : (time used 20 of 22,  ['E', 'F', 'I'])
y : (time used 12 of 22,  ['H'])
r : (time used 19 of 22,  ['J'])
```
Australian Map Coloring (maptest.txt):
```bash
$ python csp-solver.py maptest.txt
{'r': {}, 'b': {}, 'g': {}}
arc consistent
{'r': {'W': W, 1, ['r']}, 'b': {}, 'g': {}}
arc inconsistent
back_track  V removing: g from domain
('back_track', 'V', 'g')
{'r': {'W': W, 1, ['r']}, 'b': {}, 'g': {}}
arc inconsistent
back_track  V removing: b from domain
('back_track', 'V', 'b')
{'r': {'W': W, 1, ['r']}, 'b': {}, 'g': {}}
arc consistent
{'r': {'W': W, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {}}
arc inconsistent
back_track  Q removing: g from domain
('back_track', 'Q', 'g')
{'r': {'W': W, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {}}
arc inconsistent
back_track  Q removing: b from domain
('back_track', 'Q', 'b')
{'r': {'W': W, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {}}
arc consistent
{'r': {'W': W, 1, ['r'], 'Q': Q, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {}}
arc consistent
{'r': {'W': W, 1, ['r'], 'Q': Q, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {'N': N, 1, ['g']}}
arc inconsistent
back_track  T removing: b from domain
('back_track', 'T', 'b')
{'r': {'W': W, 1, ['r'], 'Q': Q, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {'N': N, 1, ['g']}}
arc consistent
{'r': {'W': W, 1, ['r'], 'Q': Q, 1, ['r'], 'V': V, 1, ['r']}, 'b': {}, 'g': {'N': N, 1, ['g'], 'T': T, 1, ['g']}}
arc consistent
the final result is
r : (time used 3 of 22,  ['W', 'Q', 'V'])
b : (time used 1 of 22,  ['S'])
g : (time used 2 of 22,  ['N', 'T'])
```

STRENGTHS:
- Unary constraints are condensed to inclusive in the read function. We
invert the exclusive unary constraints to create the initial processor lists
for each variable.

WEAKNESSES:
- Our backtracking approach is not as efficient as it could be.
