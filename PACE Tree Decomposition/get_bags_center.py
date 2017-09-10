import sys
import networkx as nx
import matplotlib.pyplot as plt




def get_edges(ub_lines):
	edges = []
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0].isdigit():
			edges.append( [int(tokens[0]), int(tokens[1])] )
	return edges

# node_sizes[bag #] = size of bag
# IMPORTANT: ignore index 0! Node numbering starts at 1!
def get_node_sizes(ub_lines):
	node_sizes = [-1000] # 0th index ignored
	num_nodes = get_num_nodes(ub_lines)
	for i in range(1, num_nodes+1):
		node_sizes.append(-1)
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			bag = int(tokens[1])
			size = ( len(tokens) - 2 )
			node_sizes[bag] = size
	return node_sizes

def get_num_nodes(ub_lines):
	num_nodes = 0
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			num_nodes += 1
	return num_nodes

def build_graph(g, edges, node_sizes):		
	add_all_edges(g, edges)
	add_weighted_nodes(g, node_sizes)	

def add_all_edges(g, edges):
	for e in edges:
		g.add_edge(e[0], e[1])

def add_weighted_nodes(g, node_sizes):
	len_node_sizes = len(node_sizes)
	for i in range(1, len_node_sizes):
		g.add_node(i, weight = node_sizes[i])


def get_norm_bag_center(centrality):
	norm_bag_center = []

	min_center = 0.0
	max_key = max(centrality, key=centrality.get)
	max_center = centrality[max_key]

	if max_center == min_center: # prevent division by zero
		for bag, center in centrality.iteritems():
			norm_bag_center.append( [bag, center] )
	else:
		for bag, center in centrality.iteritems():
			norm_center = ( (center - min_center) / (max_center - min_center) )
			norm_bag_center.append( [bag, norm_center] )

	norm_bag_center = sorted(norm_bag_center, key=lambda x: x[0]) # sort by bag
	return norm_bag_center




if __name__ == '__main__':

	td_filepath = sys.argv[1] 
	with open(td_filepath, "r") as f:
		td_lines = f.readlines()

	edges = get_edges(td_lines)
	node_sizes = get_node_sizes(td_lines)

	graph = nx.Graph()
	build_graph(graph, edges, node_sizes)

	#print nx.info(graph)

	centrality = nx.betweenness_centrality(graph) # edges unweighted
	norm_bag_center = get_norm_bag_center(centrality)
	out_f = td_filepath + '.bag_center'

	with open(out_f, "w") as f:
		for pair in norm_bag_center:
			f.write( "%d %f\n" %(pair[0], pair[1]) ) # <bag> <bag_norm>
	


