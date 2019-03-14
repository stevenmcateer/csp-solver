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
    domain = ["q". "r", "w", ...]

# this gets passed in to trace to start
global_state = [state(), state(), state()]

def cps_backtrack():
    return global_state

def MVR():
    return mvr

def least_constraining_value():
    return value

def ARC_3(): # could also be arc_4
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