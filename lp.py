from gurobipy import *

# Create a new Gurobi Model
m = Model("lp")  

# Create two new variables
x = m.addVar(lb=0, name ="x")
y = m.addVar(lb=0, name ="y")
    
# Set the objective function
m.setObjective(10*x + 26*y, GRB.MINIMIZE)
    
#Add Constraints
m.addConstr(11*x + 3*y >= 21, "c0")
m.addConstr(6*x + 20*y >= 39, "c1")
    
# Solve the model
m.optimize()
    
# Print the feasible solution if optimal.
if m.status == GRB.Status.OPTIMAL:
    print('Obj Function:', m.objVal)
    for v in m.getVars():
        print(v.varName, v.x)
# Another way to print the variable
    print("Optimal Solution:")
    print(x.varName, x.x)
    print(y.varName, y.x)        
else:
    print(m.status)
