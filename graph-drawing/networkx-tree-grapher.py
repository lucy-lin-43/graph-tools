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

# Bags start numbering from 1 NOT 0
# but nodes in graph start numbering from 0! so that sizes show up properly
def get_node_sizes(ub_lines):
	node_sizes = []
	num_nodes = get_num_nodes(ub_lines)
	for i in range(0, num_nodes):
		node_sizes.append(-1)
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			bag = int(tokens[1])
			size = ( len(tokens) - 2 )
			node_sizes[bag-1] = size # so that bag numbering starts at 0
	return node_sizes

def get_num_nodes(ub_lines):
	num_nodes = 0
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			num_nodes += 1
	return num_nodes

def build_graph(g, td_lines):
	edges = get_edges(td_lines)
	node_sizes = get_node_sizes(td_lines)		
	add_all_edges(g, edges)
	add_weighted_nodes(g, node_sizes)	

def add_all_edges(g, edges):
	for e in edges:
		g.add_edge(e[0], e[1])

def add_weighted_nodes(g, node_sizes):
	len_node_sizes = len(node_sizes)
	for i in range(1, len_node_sizes):
		g.add_node(i, weight = node_sizes[i])




if __name__ == '__main__':

	td_filepath = sys.argv[1] 
	with open(td_filepath, "r") as f:
		td_lines = f.readlines()

	graph = nx.Graph()
	build_graph(graph, td_lines)

	#print nx.info(graph)
	#nx.draw(graph)
	#plt.show()


	nx.write_dot(graph,'test.dot')

	node_sizes = get_node_sizes(td_lines)
	
	#pos=nx.pydot_layout(graph,prog='dot')
	#pos=nx.spring_layout(graph)
	#pos=nx.spectral_layout(graph)
	pos=nx.graphviz_layout(graph, prog='fdp')

	# FIXME - node sizes not accurate in graph
	nx.draw(graph, pos, with_labels=False, arrows=False, node_size=node_sizes, width=1)
	plt.savefig('nx_test.pdf')
	








