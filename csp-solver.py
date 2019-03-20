import sys
import numpy as np
import copy

class KnowledgeBase:
    def __init__(self):
        self.deadline = float("inf")
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

    def make_binary_equals(self, state1, state2, domain):

        left = state1.domain
        top = state2.domain

        matrix = []
        for value in domain:
            row = [0] * len(domain)
            matrix.append(row)

        for iter_, val in enumerate(domain):
            if val in left and val in top:
                matrix[iter_][iter_] = 1
    
        return matrix

    def make_binary_not_equals(self, state1, state2, domain):

        left = state1.domain
        top = state2.domain

        matrix = []
        for value in domain:
            row = [0] * len(domain)
            matrix.append(row)

        # this code is gross but the output is right
        for iter_top, val_top in enumerate(domain):
            for iter_left, val_left in enumerate(domain):
                if val_left in left and val_top in top and val_left != val_top:
                    matrix[iter_left][iter_top] = 1
    
        return matrix

    def make_binary_not_simultaneous(self, line, state1, state2, domain):

        split = line.split(" ")

        left = state1.domain
        top = state2.domain
        matrix = []
        for value in domain:
            row = [0] * len(domain)
            matrix.append(row)

        for iter_top, val_top in enumerate(domain):
                    for iter_left, val_left in enumerate(domain):
                        if val_left in left and val_top in top:
                            if(val_left != split[2] or val_top != split[3]):
                                matrix[iter_left][iter_top] = 1
                            if(val_left == state1.task and val_top == state2.task):
                                print("in the matrix")
                                matrix[iter_left][iter_top] = 0
        return matrix

    def get_domain_from_matrix(self, matrix, ordered_domain):
        # get non empty columns
        matrix = self.transpose_matrix(matrix)

        matrix_1_domain = []
        for i, list_ in enumerate(matrix):
                if(1 in list_):
                    matrix_1_domain.append(ordered_domain[i])
        return matrix_1_domain
        
    def transpose_matrix(self, matrix):
        return  list(map(list, np.transpose(matrix)))

    def check_time_constraint(self, variable, global_state):
        #TODO: UNCHECKED FUNCITON
        times = {}

        for value in global_state.ordered_domain:
            times[value] = global_state.unassigned[variable].duration
        for key, value in global_state.assigned.items():
            for _, state in value.items():
                times[key] += state.duration
        return times

    def get_assigned_variable(self, key, global_state):
        for _, tasks in global_state.assigned.items():
            for id, task in tasks.items():
                if(id == key):
                    return task

    def recompute_binary_constraints(self, variable, global_state):

        # binary_equals
        for key, matrix in self.binary_equals.items():
            location = key.find(variable)
            if location != -1:

                # The Value is missing because the constraint is satisfied
                if key[0] not in global_state.unassigned:
                    first = self.get_assigned_variable(key[0], global_state)
                else:
                    first = global_state.unassigned[key[0]]
                if key[2] not in global_state.unassigned:
                    second = self.get_assigned_variable(key[2], global_state)
                else:
                    second = global_state.unassigned[key[2]]

                # print(key, "bin_=")
                # print(first)
                # print(second)
                matrix = self.make_binary_equals(first, second, global_state.ordered_domain)

                second.domain = self.get_domain_from_matrix(matrix, global_state.ordered_domain)
                first.domain = self.get_domain_from_matrix(self.transpose_matrix(matrix), global_state.ordered_domain)
                # print(first, "after recompute of", variable)
                # print(second, "after recompute of", variable)

        # binary_not_equals
        for key, matrix in self.binary_not_equals.items():
            location = key.find(variable)
            if location != -1:

                # The Value is missing because the constraint is satisfied
                if key[0] not in global_state.unassigned:
                    first = self.get_assigned_variable(key[0], global_state)
                else:
                    first = global_state.unassigned[key[0]]
                if key[2] not in global_state.unassigned:
                    second = self.get_assigned_variable(key[2], global_state)
                else:
                    second = global_state.unassigned[key[2]]

                # print(key, "bin_!=")
                # print(first)
                # print(second)
                matrix = self.make_binary_not_equals(first, second, global_state.ordered_domain)

                second.domain = self.get_domain_from_matrix(matrix, global_state.ordered_domain)
                first.domain = self.get_domain_from_matrix(self.transpose_matrix(matrix), global_state.ordered_domain)
                # print(first, "after recompute of", variable)
                # print(second, "after recompute of", variable)

        # binary_not_simultaneous
        for key, matrix in self.binary_not_simultaneous.items():
            location = key.find(variable)
            if location != -1:

                # The Value is missing because the constraint is satisfied
                if key[0] not in global_state.unassigned:
                    first = self.get_assigned_variable(key[0], global_state)
                else:
                    first = global_state.unassigned[key[0]]
                if key[2] not in global_state.unassigned:
                    second = self.get_assigned_variable(key[2], global_state)
                else:
                    second = global_state.unassigned[key[2]]
                
                

                # print(key, "bin_!same_time")
                # print(first)
                # print(second)
                matrix = self.make_binary_not_simultaneous(key, first, second, global_state.ordered_domain)

                second.domain = self.get_domain_from_matrix(matrix, global_state.ordered_domain)
                first.domain = self.get_domain_from_matrix(self.transpose_matrix(matrix), global_state.ordered_domain)
                # print(first, "after recompute of", variable)
                # print(second, "after recompute of", variable)

        return global_state


class Trace:
    def __init__(self, global_state, knowledge_base):
        self.current_csp = (global_state, knowledge_base)
        self.history = [copy.deepcopy(self.current_csp)]

    def run_trace(self):
        result = csp_backtrack(self.current_csp[0], self.current_csp[1])
        if (result == False):
            print("there is not any solutions present")
        elif (result[0] == "back_track"):
            print("back_track ", result[1], "removing:",result[2], "from domain")
            if("backtracking" not in self.history[0]):
                self.history.insert(0, copy.deepcopy((self.history[0][0], self.history[0][1],self.history[0][2], "backtracking")))
                self.current_csp = self.history[0]
            # still have a back tracking bug!!! # it doesn't jump to the correct block to check
            print(result)
            self.current_csp[0].unassigned[result[1]].domain.remove(result[2])
            if(self.current_csp[0].unassigned[result[1]].domain == []):
                #for csp in self.history:
                print("this needs to be filled in")
                    

            # print("removing from the global")
            #import ipdb; ipdb.set_trace()

        else:
            # all is good
            result_c = copy.deepcopy(result)
            self.history.insert(0,result_c)
            self.current_csp = (result[0], result[1])

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
    # TODO: untested !!!

    if ( not global_state.unassigned):
        print("we are done")
        return global_state, knowledge_base
    # print(global_state.unassigned)
    variable = mrv(global_state, knowledge_base)
    # print("the variable is", variable)
    ordered_domain = least_constraining_value(variable, global_state, knowledge_base) # get the next value
    for value in ordered_domain:

        # if value is consistent with assignment
        # check that arc-3 domain value lists are not empty for the unassigned variables
        # this might be checked in arc-3, not here

        temp_state = copy.deepcopy(global_state)
        temp_state.unassigned[variable].domain = [value]
        if(arc_3(variable, value, temp_state, knowledge_base) == False):
            # BACKTRACK!!!
            return ("back_track", variable, value) 
        else:
            global_state.assigned[value][variable] = temp_state.unassigned[variable]
            if (len(global_state.assigned[value][variable].domain) != 1):
                global_state.assigned[value][variable].domain.remove(value)
            del global_state.unassigned[variable]
            return global_state, knowledge_base, variable
    return False


#find the min remaining value
def mrv(global_state, knowledge_base):
    #find lowest domain val for a variable and return it
    var_val = {}
    # print(global_state.unassigned, "\nHERE ARE THE UNNASSIGNED VARIABLES")
    for _, var in global_state.unassigned.items():
        var_val[var.task] = len(var.domain)

    min_values = {}
    for key in var_val.keys():
        if var_val[key] == min(var_val.values()):
            min_values[key] = min(var_val.values())


    #dictionary for variable and degree heuristic
    var_degree = {}

    if len(min_values) == 1:
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
    
    least_binary_contraining = {}
    for value in global_state.unassigned[variable].domain:

        # check the Binary constraints
        least_binary_contraining[value] = 0
        temp_state = copy.deepcopy(global_state)
        temp_state.unassigned[variable].domain = [value]
        temp_state = knowledge_base.recompute_binary_constraints(variable, temp_state)

        for _, state in temp_state.unassigned.items():
            least_binary_contraining[value] += len(global_state.unassigned[state.task].domain) - len(state.domain)

        # always will be there because of 3 bin constraints, and we assigned G to that aka 3
        # this is a bad comment try to remember
        least_binary_contraining[value] -= 3

        # check the time constraint
        times = knowledge_base.check_time_constraint(variable ,temp_state)

    least_binary_contraining_list = []
    times_list = []
    for value in global_state.unassigned[variable].domain:
        least_binary_contraining_list.append((value, least_binary_contraining[value], times[value]))

    least_binary_contraining_list.sort(key = lambda x: (x[1], x[2]))

    ordered_domain = []
    for value in least_binary_contraining_list:
        ordered_domain.append(value[0])

    return ordered_domain

#inference
def arc_3(variable, value, global_state, knowledge_base): # could also be arc_4
    queue = [variable]
    # TODO: THIS MIGHT HAVE OUR ERROR
    # AttributeError: 'NoneType' object has no attribute 'domain'
    while queue != []:
        variable = global_state.unassigned[queue[0]]


        # print(variable)
        temp_state = copy.deepcopy(global_state)
        #### HERE
        # print("WE ARE STARTING TO GET SOME KNOWLEDGE")
        # print(global_state.unassigned)
        temp_state = knowledge_base.recompute_binary_constraints(variable.task, temp_state)

        # if a domain is empty
        for _, state in temp_state.unassigned.items():
            if state.domain == []:
                print("arc inconsistent")
                return False

        # if the domain changes add it to the queue
        for _, state in global_state.unassigned.items():
            domain_change = False
            for value in state.domain:
                if value not in temp_state.unassigned[state.task].domain:
                    # print(value)
                    domain_change = True

            if domain_change:
                queue.append(state.task)

        # remove the fist value because it worked
        queue.remove(variable.task)
        # print(queue)
        global_state = temp_state
    print("arc consistent")
    return global_state, knowledge_base

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
                split = line.split(" ", 2)
                state = State(split[0], int(split[1]))
                global_state.unassigned[split[0]] = state
            elif switch == "values":
                # TODO: might want to add values to the domain for every varaible
                global_state.ordered_domain.append(line)
            elif switch == "deadline":
                k_base.deadline = int(line)
            elif switch == "inclusive":
                split = line.split(" ")
                k_base.unary[split[0]] = split[1:]
                global_state.unassigned[split[0]].domain = split[1:]
            elif switch == "exclusive":
                split = line.split(" ")
                k_base.unary[split[0]] = split[1:]
                domain = global_state.ordered_domain
                k_base.unary[split[0]] = k_base.inv_unary(domain, split[0]) 
                global_state.unassigned[split[0]].domain = k_base.unary[split[0]]
            elif switch == "binary equals":
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

            elif switch == "binary not equals":
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
                        if val_left in left and val_top in top and val_left != val_top:
                            matrix[iter_left][iter_top] = 1

                k_base.binary_not_equals[line] = matrix

            elif switch == "not simultaneous":
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


            else:
                print("THIS IS A BIG ERROR IN THE INPUT FILE!!", line)
                print()
    # fill in the domain for the variables that dont have assignments
    for _, value in global_state.unassigned.items():
        if value.domain == []:
            value.domain = copy.deepcopy(global_state.ordered_domain)

    # fill assigned with processors
    for processor in global_state.ordered_domain:
        global_state.assigned[processor] = {}

    return global_state, k_base

if __name__ == "__main__":
    

    #TODO: UNIQUE stuff, check the iniary constrainsts, make sure they are satisfiable before we start backtracking
    #TODO: UNIQUE stuff, check the the timing, make sure we have enough time for all tasks
    #TODO: UNIQUE stuff, make sure no task is longer than the deadline


    g_state, knowledge_base = read_input()

    # check the total time we have
    var_time = 0
    for var in g_state.unassigned.values():
        var_time += var.duration
    
    proc_time = 0
    for proc in g_state.ordered_domain:
        proc_time += 1

    if (proc_time * knowledge_base.deadline - var_time) < 0:
        print("There is no solution")
        exit()
    import ipdb; ipdb.set_trace()

    # is the time too long? who knows?
    for i, varable in enumerate(g_state.unassigned.keys()):
        if i == 0:
            ret = knowledge_base.recompute_binary_constraints(varable, g_state)
        else:
            ret = knowledge_base.recompute_binary_constraints(varable, ret)
    
    for value in ret.unassigned.values():
        if (value.domain == []):
            print("There is no solution")
            exit()

    trace = Trace(g_state, knowledge_base)

    while (trace.current_csp[0].unassigned):
        print(trace.current_csp[0].assigned)
        trace.run_trace()
    print("the final result is")
    # assignement of p
    # deadline
    # total lenght for each p
    # total length
    for proc, list_ in trace.current_csp[0].assigned.items():
        time_used = 0
        tasks = []
        for key, value in list_.items():
            time_used += value.duration
            tasks.append(value.task)
        
        print("{} : (time used {} of {},  {})".format(proc, time_used, trace.current_csp[1].deadline, tasks))
