


# create file with <var> <blank space or bag # if it has high bag centrality or bag_size>

# create 2nd file in form
#	25% high_center : <bag> <percentage within bag> etc.
#	20% high_center : <bag> <percentage within bag> etc.
#	25% high_size : <bag> <percentage within bag> etc.
#	20% high_size : <bag> <percentage within bag> etc.



# Note: use some of these functions to get overleaf subtables


import sys
import networkx as nx
import matplotlib.pyplot as plt


LABEL_TOP_BAGS_SUFF = '.labelled_bags'


def get_num_vars(ub_lines):	
	num_vars = -1
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 's':
			num_vars = int(tokens[-1])
	return num_vars

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
	num_nodes = get_num_bags(ub_lines)
	for i in range(1, num_nodes+1):
		node_sizes.append(-1)
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			bag = int(tokens[1])
			size = ( len(tokens) - 2 )
			node_sizes[bag] = size
	return node_sizes

def get_num_bags(ub_lines):
	num_bags = 0
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			num_bags += 1
	return num_bags

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


def get_sorted_norm_bag_center(centrality):
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

	sorted_norm_bag_center = sorted(norm_bag_center, key=lambda x: x[1]) # sort by 2nd element (i.e center)
	return sorted_norm_bag_center


# outputs sorted_b_bsize[rank] = [bag_i, bag_size]
def get_sorted_b_bsize(td_lines):
	bag_size = []
	for line in td_lines:
		tokens = line.split()
		if tokens and tokens[0] == "b":
			b = int(tokens[1])
			size = len(tokens) - 2
			bag_size.append( [b, size])
	sorted_b_bsize = sorted(bag_size, key=lambda x: x[1]) # sort by 2nd element (i.e size)
	return sorted_b_bsize

# IMPORTANT: vars & bags start numbering at 1!
#	Never use b_bsize_list[0]!
def get_b_bsize(td_lines):
	bag_size = [-100]
	num_bags = get_num_bags(td_lines)
	for i in range(1, num_bags+1):
		bag_size.append(-1)

	for line in td_lines:
		tokens = line.split()
		if tokens and tokens[0] == "b":
			b = int(tokens[1])
			size = len(tokens) - 2
			bag_size[b] = size
	return bag_size


# pre-condition: portion must be decimal number
def get_portion_top_bags(num_all_vars, sorted_bags_score, b_bsize_list, portion):
	num_top_vars = round(num_all_vars * portion)
	num_curr_top_vars = 0
	top_bags_numVars = []	# <bag> <top vars from bag>

	i = -1

	while num_curr_top_vars < num_top_vars:
		
		curr_b = sorted_bags_score[i][0]
		curr_bsize = b_bsize_list[curr_b]
	
		if num_curr_top_vars + curr_bsize > num_top_vars:
			num_added = num_top_vars - num_curr_top_vars
			top_bags_numVars.append( [curr_b, num_added] ) 
			num_curr_top_vars = num_top_vars
		else:
			top_bags_numVars.append( [curr_b, curr_bsize] )
			num_curr_top_vars += curr_bsize
		i -= 1 # won't exceed past length of sorted_bags_score since portion is decimal

	return top_bags_numVars


# IMPORTANT: vars & bags start numbering at 1!
#	Never use top_bags[0]
def get_all_types_top_bags(top_bag_numVars_lists, num_bags):
	top_bags = set()
	for bag_numVars_list in top_bag_numVars_lists:
		for pair in bag_numVars_list:
			curr_b = pair[0]
			top_bags.add(curr_b)
	return sorted(top_bags)
	
def write_labelled_top_bags(label_top_bags_f, all_types_top_bags, num_bags):
	with open(label_top_bags_f, "w") as f:
		for i in range(1, num_bags+1):
			f.write("%d " %i)
			if i in all_types_top_bags:
				f.write("%d\n" %i)
			else:
				f.write(" \n")	


if __name__ == '__main__':
	# create file with <var> <blank space or bag # if it has high bag centrality or bag_size>

	# create 2nd file in form
	#	25% high_center : <bag> <percentage within bag> etc.
	#	OPT - 20% high_center : <bag> <percentage within bag> etc.
	#	25% high_size : <bag> <percentage within bag> etc.
	#	OPT - 20% high_size : <bag> <percentage within bag> etc.

	td_filepath = sys.argv[1] 
	with open(td_filepath, "r") as f:
		td_lines = f.readlines()
	
	edges = get_edges(td_lines)
	node_sizes = get_node_sizes(td_lines)

	graph = nx.Graph()
	build_graph(graph, edges, node_sizes)

	#print nx.info(graph)

	centrality = nx.betweenness_centrality(graph) # edges unweighted
	sorted_norm_bag_center = get_sorted_norm_bag_center(centrality)
	sorted_b_bsize = get_sorted_b_bsize(td_lines)
	
	portion = 0.25
	num_all_vars = get_num_vars(td_lines)
	num_bags = get_num_bags(td_lines)
	b_bsize_list = get_b_bsize(td_lines)

	top_center_bags_numVars = get_portion_top_bags(num_all_vars, sorted_norm_bag_center, b_bsize_list, portion)
	print "top_center"
	print top_center_bags_numVars
	top_size_bags_numVars = get_portion_top_bags(num_all_vars, sorted_b_bsize, b_bsize_list, portion)
	print "top_size"
	print top_size_bags_numVars
	top_bag_numVars_lists = [top_center_bags_numVars, top_size_bags_numVars]
	all_types_top_bags = get_all_types_top_bags(top_bag_numVars_lists, num_bags)


	label_top_bags_f = td_filepath + LABEL_TOP_BAGS_SUFF

	write_labelled_top_bags(label_top_bags_f, all_types_top_bags, num_bags)


	



