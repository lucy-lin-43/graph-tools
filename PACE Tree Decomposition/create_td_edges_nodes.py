

import sys

EDGE_SUFF = '.edges'
NODE_SUFF = '.nodes'


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


if __name__ == '__main__':

	ub_f = sys.argv[1]
	with open(ub_f, "r") as f:
		ub_lines = f.readlines()	

	edges = get_edges(ub_lines)
	node_sizes = get_node_sizes(ub_lines)

	edge_out = ub_f + EDGE_SUFF
	node_out = ub_f + NODE_SUFF

	with open(edge_out, 'w') as f:
		for edge in edges:
			f.write( "%d %d\n" %(edge[0], edge[1]) )

	with open(node_out, 'w') as f:
		node_sizes_len = len(node_sizes)
		for i in range(1, node_sizes_len): # node numbering starts at 1!)
			f.write( "%d %d\n" %(i, node_sizes[i]) )
			if node_sizes[i] < 0:
				print ub_f
				print "Error: num bag error"


		
