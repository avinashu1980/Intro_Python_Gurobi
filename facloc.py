from gurobipy import *

# 1040444.375
# J.E.Beasley "An algorithm for solving  
# large capacitated warehouse location problems" European 
# Journal of Operational Research 33 (1988) 314-325.

f = open("cap41.txt", "r")
line = f.readline() 
data = line.split()
num_loc = int(data[0])
num_cust = int(data[1])
loc = list(range(num_loc))
cust = list(range(num_cust))
cap = []
fc = []
dem = []
vc = []
for i in loc:
    line = f.readline() 
    data = line.split()
    cap.append(int(data[0]))
    fc.append(float(data[1]))
for i in cust:
    line = f.readline()
    dem.append(int(line))
    line = f.readline()
    data = line.split()
    for j in loc:
        vc.append([])
        vc[i].append(float(data[j]))
f.close()

m = Model("facility location")



y = []
for i in loc:
    y.append(m.addVar(vtype=GRB.BINARY, obj=fc[i],  name="open[%d]" % i))
    
x = []
for i in cust:
    x.append([])
    for j in loc:
        x[i].append(m.addVar(obj=vc[i][j], lb = 0, ub = 1, name="trans[%d,%d]" % (i, j)))

# Other ways to add variables
#y = m.addVars(num_loc, vtype=GRB.BINARY, obj=fc, name="open")
#x = m.addVars(num_cust, num_loc, obj=vc, lb = 0, ub = 1, name="trans")
#x = []
#for i in cust:
#    for j in loc:
#        x[i][j] = m.addVar(obj=vc[i][j], lb = 0, ub = 1, name="trans[%d,%d]" % (i, j))

m.modelSense = GRB.MINIMIZE

for i in cust:
    m.addConstr(sum(x[i][j] for j in loc) == 1, "Demand[%d]" % i)

for j in loc:
     m.addConstr(sum(dem[i]*x[i][j] for i in cust) <= cap[j]*y[j], "Capacity[%d]" % j)

for i in cust:
    for j in loc:
        m.addConstr(x[i][j] <= y[j], "Feasibility[%d][%d]" %(i,j))

m.optimize()

# Print solution
f = open("output.txt", "w")
f.write('\nTOTAL COSTS: %g' % m.objVal)
f.write('\nSOLUTION:')
for j in loc:
    if y[j].x > 0.99:
        f.write('\nPlant %s open' % j)
        for i in cust:
            if x[i][j].x > 0:
                f.write('\n Transport %g units to customer %s' % (x[i][j].x, i))
    else:
        f.write('\n Plant %s closed!' % i)
f.close()

import networkx as nx
import matplotlib.pyplot as plt
import random

plt.figure(figsize=(10,10))

cust_x = [random.uniform(1,10) for i in cust]
cust_y = [random.uniform(0,10) for i in cust]

fac_x = [random.uniform(0,1) for i in loc]
fac_y = [random.uniform(0,10) for i in loc]

connection = [(i,50+j) for i in cust for j in loc if x[i][j].x > 0]
fac_nodes = [j for j in loc if y[j].x > 0]
cust_nodes = [i for i in cust]

G = nx.Graph()
G.add_edges_from(connection)

for i in cust:
    G.add_node(i, pos = (cust_x[i], cust_y[i]))

print("Number of nodes: ", G.number_of_nodes())
    
for i in loc:
    if y[i].x > 0:
        G.add_node(50+i, pos = (fac_x[i],fac_y[i]) )

print("Number of nodes: ", G.number_of_nodes())       
#node_col = nx.get_node_attributes(G,'color')
node_col = ['white' if node < len(cust) else 'red' for node in G.nodes()]

node_pos=nx.get_node_attributes(G,'pos')

#nx.draw_networkx(G,node_pos, node_color = node_col)
nx.draw(G,node_pos, node_color = node_col)
#nx.draw_networkx_edges(G, node_pos)
#plt.axis('off')
# Show the plot
plt.show()


# The following lines of code involves printing the input to make sure the input is read correctly        
#f.write("\n \n")
#f.write("\n Input Variables")
#f.write("\n Number of Customers: {}".format(num_cust))
#f.write("\n Number of Locations: {}".format(num_loc))
#f.write("\n Facility Fixed Costs, Capacity")
#for i in loc:
#    f.write("\n {}, {}".format(fc[i],cap[i]))
#f.write("\n Demand")
#for i in cust:
#    f.write("\n Customer {} demand : {}".format(i,dem[i]))
#f.write("Transportation Costs \n")
#for i in cust:
#    for j in loc:   
#        f.write("{}   ".format(vc[i][j]))
#    f.write("\n")
#f.close()


