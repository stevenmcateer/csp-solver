# csp-solver
Generic CSP problem solver


Processors (Variables' domains): The m processors will be denoted by m lower case letters (e.g., p, w, f, s, ...). Each of the processors performs the tasks assigned to it in a sequential manner. Processors are independent from each other.  There is no ordering of tasks assigned to a processor, that is, you should not care in what order tasks will be executed, only which processors will execute them. 

Two given tasks cannot be simultaneously assigned to a given pair of processors. For instance, the user can specify that task D cannot be assigned to processor p if task E is assigned to processor u.  To be more specific, this constraint is regardless of time, that is, all assignments take place before any tasks have been executed, at time t = 0.  If D is assigned to p, then E can not be assigned to u, even if the two tasks could be executed at different times. 