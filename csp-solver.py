class knowledge_base:
    deadline = 0
    unary = # dictionary
    binary_not_simultaneous = # dictionary of matrices
        # eg
        # inclusive of G
        # exclusive of C
        # as well as binary not equals from input
        # key = ["CG"]

    binary_equals = # dictionary of matrices
        # do the same but different
    binary_not_equals = # dictionary of matrices



class trace:
    order = # list of the global state for each step

class state:
    task = "a"
    duration = 6
    domain = ["q", "r", "w", ...]

class global_state:
    unassigned = []
    assigned = {} # key is processor and val is ordered list of states
    ordered_domain = []


# this gets passed in to trace to start
global_state = [state(), state(), state()]

def csp_backtrack(global_state, knowledge_base):

    # Check if all variables are assigned
    if len(global_state.unassigned) == 0:
        return global_state.assigned #exit

    #might need to make a deepcopy

    # get the next variable assignment based on mrv
    variable = mrv(global_state)
    value = least_constraining_value() # get the next value


    for value in global_state.ordered_domain:
        #if value is consistent with assignment
        if is_consistent(value):
            global_state.assigned[value] = variable
            inferences = get_inferences(variable, value)

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

def get_inferences(variable, value):
    return True

def is_consistent(value):

    return True
def mrv(global_state):
    min_remaining_val = 0

    for var in global_state.unassigned:
        num_remaining_vals = len(var.domain)
        if num_remaining_vals < min_remaining_val:
            min_remaining_val = num_remaining_vals
        #if they equal each other, pick the least constraining val
        elif num_remaining_vals == min_remaining_val:
            min_remaining_val = least_constraining_value()

    return min_remaining_val

def least_constraining_value():
    return value

def arc_3(): # could also be arc_4
    return arc_3

def read_input(path):
    states = []
    knowledge_base = knowledge_base()

    return knowledge_base, states

if __name__ == "__main__":

    read_input("path to file")
    # this gets passed in to trace to start
    global_state = [state(), state(), state()]

    trace()
