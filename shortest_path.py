from gurobipy import *
import matplotlib.pyplot as plt
import networkx as nx

# Reading the input file
f = open("AhujaNet.txt", "r")
line = f.readline()
line = line.strip('\n')
data = line.split(':')
num_nodes = int(data[1])
line = f.readline()
line = line.strip('\n')
data = line.split(':')
num_arcs = int(data[1])
line = f.readline()
line = line.strip('\n')
data = line.split(':')
origin = int(data[1])
line = f.readline()
line = line.strip('\n')
data = line.split(':')
destination = int(data[1])
line = f.readline()
line = f.readline()

links = tuplelist()
cost  = {}
while(len(line)):
    line = line.strip('\n')
    data = line.split()
    print(data)
    from_node = int(data[0])
    to_node = int(data[1])
    cost_arc = float(data[2])
    links.append((from_node,to_node))
    cost[from_node, to_node] = cost_arc
    line = f.readline()
f.close() 


#Creating the Gurobi model
m = Model('SP')

#Adding variables to the model
x = m.addVars(links, obj=cost, name ="flow")

#Adding constraints
for i in range(1, num_nodes+1):
    m.addConstr( sum(x[i,j] for i,j in links.select(i, '*')) - sum(x[j,i] for j,i in links.select('*',i)) == 
                     (1 if i==origin else -1 if i==destination else 0 ),'node%s_' % i )

#optimizing the model    
m.optimize() 


if m.status == GRB.Status.OPTIMAL:
   print('The final solution is:')
   for i,j in links:
       if(x[i,j].x > 0):
           print(i, j, x[i,j].x)
           
# Let us now visualize the shortest path
# We use the Networkx and matplotlib package
G=nx.DiGraph()
list_nodes = list(range(1, num_nodes+1))
G.add_nodes_from(list_nodes)
for i,j in links:
    G.add_edge(i,j)

# Adding the position attribute to each node
node_pos = {1: (0, 0), 2: (2, 2), 3: (2, -2), 4: (5, 2), 5: (5, -2), 6: (7, 0)}

# Create a list of edges in shortest path
red_edges = [(i,j) for i,j in links if x[i,j].x > 0]

#Create a list of nodes in shortest path
sp = [ i for i,j in links if x[i,j].x > 0 ]
sp.append(destination)

# If the node is in the shortest path, set it to red, else set it to white color
node_col = ['white' if not node in sp else 'red' for node in G.nodes()]
# If the edge is in the shortest path set it to red, else set it to white color
edge_col = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
# Draw the nodes
nx.draw_networkx(G,node_pos, node_color= node_col, node_size=450)
# Draw the node labels
# nx.draw_networkx_labels(G1, node_pos,node_color= node_col)
# Draw the edges
nx.draw_networkx_edges(G, node_pos,edge_color= edge_col)
# Draw the edge labels
nx.draw_networkx_edge_labels(G, node_pos,edge_color= edge_col, edge_labels=cost)
# Remove the axis
plt.axis('off')

# Show the plot
plt.show()



