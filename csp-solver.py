import sys

class KnowledgeBase:
    def __init__(self):
        self.deadline = 0
        self.unary = {}
        self.binary_not_simultaneous = {} # dictionary of matrices
         # eg
        # inclusive of G
        # exclusive of C
        # as well as binary not equals from input
        # key = ["C G"]
        self.binary_equals = {}  # dictionary of matrices
        # do the same but different
        self.binary_not_equals = {} # dictionary of matrices

    def inv_unary(self, domain:list, key):
        new_dom = domain.copy()
        inv = self.unary[key]
        for value in inv:
            if value in new_dom:
                new_dom.remove(value)
        return new_dom



# class trace:
#     order = # list of the global state for each step

class State:

    def __init__(self, task_, duration_):
        self.task = task_
        self.duration = duration_
        self.domain = []
    
    def __repr__(self):
        return "{}, {}, {}".format(self.task, self.duration, self.domain)

    def __str__(self):
        return "{}, {}, {}".format(self.task, self.duration, self.domain)

    def __eq__(self, task_):
        return self.task == task_

class GlobalState:
    def __init__(self):
        self.unassigned = {}
        self.assigned = {} # key is processor and val is ordered list of states
        self.ordered_domain = []


def csp_backtrack(global_state, knowledge_base):
    # Check if all variables are assigned
    # this means unassigned is empty
    if global_state.unassigned == False:
        return global_state #exit

    # get the next variable assignment based on mrv
    variable = mrv(global_state, knowledge_base)
    value = least_constraining_value(variable, global_state, knowledge_base) # get the next value

    for value in global_state.ordered_domain:
        # if value is consistent with assignment
        # check that arc-3 domain value lists are not empty for the unassigned variables
        # this might be checked in arc-3, not here
        if arc_3(global_state, knowledge_base).unassigned:
            global_state.assigned[value] = variable
            inferences = arc_3(variable, value)

            if inferences:
                #add inferences to assignment
                result = csp_backtrack(global_state, knowledge_base)

            #success
            if result:
                return result

            #failure
            del global_state.assigned[value]
            #delete inferences from assignment

    return global_state


#find the min remaining value
def mrv(global_state, knowledge_base):
    #find lowest domain val for a variable and return it
    # TODO: fix this do not need
    var_val = {}
    for _, var in global_state.unassigned.items():
        var_val[var.task] = len(var.domain)

    min_values = {}
    for key in var_val.keys():
        if var_val[key] == min(var_val.values()):
            min_values[key] = min(var_val.values())


    print(var_val)
    #dictionary for variable and degree heuristic
    var_degree = {}

    if len(min_values) == 1:
        print(min(var_val, key=lambda x: var_val.get(x)))
        return min(var_val, key=lambda x: var_val.get(x))
    else:
        for var in min_values:
            var_degree[var] = degree_heuristic(var, knowledge_base)

        return min(var_degree, key=lambda x: var_degree.get(x))


def degree_heuristic(variable, knowledge_base):
    # Degree heuristic: assign a value to the variable that is involved in the largest
    # number of constraints on other unassigned variables.

    #TODO: could also weight this
    degree = 0
    for key, _ in knowledge_base.binary_equals.items():
        if key.find(variable) != -1:
            degree += 1

    for key, _ in knowledge_base.binary_not_equals.items():
        if key.find(variable) != -1:
            degree += 1
    
    for key, _ in knowledge_base.binary_not_simultaneous.items():
        if key.find(variable) != -1:
            degree += 1

    return degree

def least_constraining_value(variable, global_state, knowledge_base):
    # we choose the least constraining value for the variable selected
    # book 6.3.2
    value = 0
    return value

#inference
def arc_3(global_state, knowledge_base): # could also be arc_4


    return arc_3


# http://aima.cs.berkeley.edu/python/csp.py
def AC3(csp, queue=None):
    """[Fig. 5.7]"""
    if queue == None:
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
    while queue:
        (Xi, Xj) = queue.pop()
        if remove_inconsistent_values(csp, Xi, Xj):
            for Xk in csp.neighbors[Xi]:
                queue.append((Xk, Xi))

def remove_inconsistent_values(csp, Xi, Xj):
    "Return true if we remove a value."
    removed = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                csp.curr_domains[Xj]):
            csp.curr_domains[Xi].remove(x)
            removed = True
    return removed


def read_input():

    file = sys.argv[1]

    with open(file,'r') as i:
        lines = i.readlines()
        switch = " "
        global_state = GlobalState()
        k_base = KnowledgeBase()
        for line in lines:
            # strip the new line character
            line = line.strip("\n")

            # get the field name of the inputs 
            if line.find("variables") != -1:
                switch = "variables"

            elif line.find("values") != -1:
                switch = "values"

            elif line.find("deadline") != -1:
                switch = "deadline"

            elif line.find("inclusive") != -1:
                switch = "inclusive"

            elif line.find("exclusive") != -1:
                switch = "exclusive"
            
            elif line.find("binary equals") != -1:
                switch = "binary equals"

            elif line.find("binary not equals") != -1:
                switch = "binary not equals"

            elif line.find("not simultaneous") != -1:
                switch = "not simultaneous"
            elif line == '\n' or line == '':
                pass

            # write the values into the appropriate fields
            elif switch == "variables":
                print("variables\n")
                split = line.split(" ", 2)
                state = State(split[0], int(split[1]))
                global_state.unassigned[split[0]] = state
                print(global_state.unassigned)
                print()
            elif switch == "values":
                # TODO: might want to add values to the domain for every varaible
                global_state.ordered_domain.append(line)
                print(global_state.ordered_domain)
                print()
            elif switch == "deadline":
                k_base.deadline = int(line)
                print(k_base.deadline)
                print()
            elif switch == "inclusive":
                split = line.split(" ")
                k_base.unary[split[0]] = split[1:]
                global_state.unassigned[split[0]].domain = split[1:]
                print(k_base.unary)
                print()
            elif switch == "exclusive":
                split = line.split(" ")
                k_base.unary[split[0]] = split[1:]
                domain = global_state.ordered_domain
                k_base.unary[split[0]] = k_base.inv_unary(domain, split[0]) 
                global_state.unassigned[split[0]].domain = k_base.unary[split[0]]
                print(k_base.unary)
                print("lookee here")
                print(global_state.unassigned)
            elif switch == "binary equals":
                print("binary equals\n")
                split = line.split(" ")
                domain = global_state.ordered_domain

                #TODO: might have weird errors not copying lists!!!
                if(split[0] in k_base.unary):
                    left = k_base.unary[split[0]]
                else:
                    left = domain
                
                if(split[1] in k_base.unary):
                    top = k_base.unary[split[1]]
                else:
                    top = domain

                matrix = []
                for value in domain:
                    row = [0] * len(domain)
                    matrix.append(row)

                for iter_, val in enumerate(domain):
                    if val in left and val in top:
                        matrix[iter_][iter_] = 1

                k_base.binary_equals[line] = matrix
                print(k_base.binary_equals)
                print()

            elif switch == "binary not equals":
                print("binary not equals\n")
                split = line.split(" ")
                domain = global_state.ordered_domain

                #TODO: might have weird errors not copying lists!!!
                if(split[0] in k_base.unary):
                    left = k_base.unary[split[0]]
                else:
                    left = domain
                
                if(split[1] in k_base.unary):
                    top = k_base.unary[split[1]]
                else:
                    top = domain

                matrix = []
                for value in domain:
                    row = [0] * len(domain)
                    matrix.append(row)

                print(top)

                # this code is gross but the output is right
                for iter_top, val_top in enumerate(domain):
                    for iter_left, val_left in enumerate(domain):
                        if val_left in left and val_top in top and val_left != val_top:
                            matrix[iter_left][iter_top] = 1

                k_base.binary_not_equals[line] = matrix
                print(k_base.binary_not_equals)
                print()

            elif switch == "not simultaneous":
                print("binary not simultaneous\n")
                split = line.split(" ")
                domain = global_state.ordered_domain

                #TODO: might have weird errors not copying lists!!!
                if(split[0] in k_base.unary):
                    left = k_base.unary[split[0]]
                else:
                    left = domain
                
                if(split[1] in k_base.unary):
                    top = k_base.unary[split[1]]
                else:
                    top = domain
                    
                

                matrix = []
                for value in domain:
                    row = [0] * len(domain)
                    matrix.append(row)

                # this code is gross but the output is right
                for iter_top, val_top in enumerate(domain):
                    for iter_left, val_left in enumerate(domain):
                        if val_left in left and val_top in top:
                            if(val_left != split[2] or val_top != split[3]):
                                matrix[iter_left][iter_top] = 1

                k_base.binary_not_simultaneous[line] = matrix
                print(k_base.binary_not_simultaneous)
                print()


            else:
                print("THIS IS A BIG ERROR IN THE INPUT FILE!!", line)
                print()
    # fill in the domain for the variables that dont have assignments
    for _, value in global_state.unassigned.items():
        if value.domain == []:
            value.domain = global_state.ordered_domain
    return global_state, k_base

if __name__ == "__main__":
    

    #TODO: UNIQUE stuff, check the iniary constrainsts, make sure they are satisfiable before we start backtracking
    #TODO: UNIQUE stuff, check the the timing, make sure we have enough time for all tasks
    #TODO: UNIQUE stuff, make sure no task is longer than the deadline


    global_state, k_base = read_input()

    print(global_state)
    print(k_base)
    # import ipdb; ipdb.set_trace()
    mrv(global_state, k_base)
    # this gets passed in to trace to start
    # global_state = [state(), state(), state()]

    # trace()
