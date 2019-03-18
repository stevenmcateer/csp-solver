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
        # key = ["CG"]
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

class GlobalState:
    def __init__(self):
        self.unassigned = []
        self.assigned = {} # key is processor and val is ordered list of states
        self.ordered_domain = []


# # this gets passed in to trace to start
# global_state = [state(), state(), state()]

# def csp_backtrack(global_state, knowledge_base):

#     # Check if all variables are assigned
#     if len(global_state.unassigned) == 0:
#         return global_state.assigned #exit

#     #might need to make a deepcopy

#     # get the next variable assignment based on mrv
#     variable = mrv(global_state)
#     value = least_constraining_value() # get the next value


#     for value in global_state.ordered_domain:
#         #if value is consistent with assignment
#         if is_consistent(value):
#             global_state.assigned[value] = variable
#             inferences = get_inferences(variable, value)

#             if inferences:
#                 #add inferences to assignment
#                 result = csp_backtrack(global_state, knowledge_base)

#             #success
#             if result:
#                 return result

#             #failure
#             del global_state.assigned[value]
#             #delete inferences from assignment

#     return global_state

# def get_inferences(variable, value):
#     return True

# def is_consistent(value):

#     return True
# def mrv(global_state):
#     min_remaining_val = 0

#     for var in global_state.unassigned:
#         num_remaining_vals = len(var.domain)
#         if num_remaining_vals < min_remaining_val:
#             min_remaining_val = num_remaining_vals
#         #if they equal each other, pick the least constraining val
#         elif num_remaining_vals == min_remaining_val:
#             min_remaining_val = least_constraining_value()

#     return min_remaining_val

# def least_constraining_value(variable, global_state, knowledge_base):
#     # we choose the least constraining value for the variable selected
#     # book 6.3.2
#     return value

# def arc_3(): # could also be arc_4
#     return arc_3

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
                global_state.unassigned.append(state)
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
                print(k_base.unary)
                print()
            elif switch == "exclusive":
                split = line.split(" ")
                k_base.unary[split[0]] = split[1:]
                domain = global_state.ordered_domain
                k_base.unary[split[0]] = k_base.inv_unary(domain, split[0]) 
                print(k_base.unary)
                print()
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
                # TODO: THIS IS NOT IMPLEMENTED THE WAY SHE HAS IT IN THE NOTES HER WAY MAKES NO SENSE
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

    # return knowledge_base, states

if __name__ == "__main__":

    read_input()
    # this gets passed in to trace to start
    # global_state = [state(), state(), state()]

    # trace()
