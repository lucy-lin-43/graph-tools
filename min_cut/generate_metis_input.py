



# IMPORTANT: 
	# 1) MUST USE INTEGER AND INVERTED version of invSquaredNorm_0-100 edge weights graphxcl file!
	# 	use absolute edge weight when inverting
	# 	multiply by a constant to get INTEGERS
	# 2) ALL weights - must be INTEGERS
	#	node weights: use absolute weight NOT capped weight
	# 3) numbering for nodes MUST START AT 1 NOT 0 

# FIXME: consider whether want disconnected nodes in metis input
#	(currently they're ignored)


# TODO: update FMT_PARAM

import sys
import os.path


FMT_PARAM = "011"

# IMPORTANT: don't index 0 for any of these lists (cmty numbering starts at 1)

def findNeighbors(edge_lines, num_cmtys):
	neighbors = [-1] # for n cmtys, has n+1 members (since index corresponds to cmty #)
			
	for i in range(0, num_cmtys):
		neighbors.append(-1)

	for line in edge_lines:
		tokens = line.split()
		if tokens:
			if tokens:
				end1 = int(tokens[0])
				end2 = int(tokens[1])
				weight = int(tokens[2])
		
				curr_neigh1 = [end2, weight]
				if not isinstance(neighbors[end1], list): 
					neighbors[end1] = []
				neighbors[end1].append(curr_neigh1)


				curr_neigh2 = [end1, weight]
				if not isinstance(neighbors[end2], list):
					neighbors[end2] = []
				neighbors[end2].append(curr_neigh2)
	return neighbors


def get_cmty_weights(node_lines, num_cmtys):
	
	node_weights = [-1]

	for i in range(0, num_cmtys):
		node_weights.append(-1)		

	for line in node_lines:
		tokens = line.split()
		if tokens and tokens[0].isdigit():
			node = int(tokens[0])
			weight = int(tokens[1])
			node_weights[node] = weight

	return node_weights

def get_num(flines):
	num = 0
	for line in flines:
		tokens = line.split()
		if tokens:
			if tokens[0].isdigit():
				num += 1
	return num




def num_connected_cmtys(neighbours):
	num_connected = 0

	for neigh in neighbours:
		if isinstance(neigh,list):
			num_connected += 1

	return num_connected

if __name__ == '__main__':

	cnf_f = sys.argv[1]
	intInv_edge_f = sys.argv[2]
	int_comms_f = sys.argv[3]
	
	metis_f = cnf_f + ".metisInput"


	with open(intInv_edge_f, "r") as f:
		edge_lines = f.readlines()

	with open(int_comms_f, "r") as f:
		comms_lines = f.readlines()

	num_edges = get_num(edge_lines)
	num_cmtys = get_num(comms_lines)

	neighbors = findNeighbors(edge_lines, num_cmtys )
	node_weights = get_cmty_weights(comms_lines, num_cmtys)

	#num_conn_cmtys = num_connected_cmtys(neighbors)
	
	with open(metis_f, "w") as f:
		# write header
		f.write( "%d %d %s\n" %(num_cmtys, num_edges, FMT_PARAM) )


		for cmty in range(1, num_cmtys+1 ): # numbering starts at ONE not zero
			f.write("%d " %node_weights[cmty])
			if isinstance(neighbors[cmty], list):
				for neigh in neighbors[cmty]:
					f.write( "%d %d " %(neigh[0], neigh[1]) )
			f.write("\n")	
	
