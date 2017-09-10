


# Numbering:
#	1) .cnf: vars from 0
#	2) .cmty: vars & cmtys from 0
#	3) .graphxcl, .comms_size: cmtys from 1
#	4) .metisInput: vars from 1
#	5) partitionFile: partitions from 0
#	6) cutCmtysFile: cmtys from 1

# ***IMPORTANT: NEVER index element 0 of any lists (index corresponds to cmty numbering)


# Input: Metis partition file
#	n lines with single number per line
#	ith line of file contains the partition # that the ith vertex belongs to
#	Partition numbers: start from ZERO up to the number of partitions-1
#
# Output: file with 3 numbers per line:
#	<cut_cmty> <weight_of_corresponding_cut_edge> <weight_of_cmty>
#		***cmtys numbered from ONE not zero






import sys

FORMAT = "<cut_cmty> <weight_of_corresponding_cut_edge> <weight_of_cmty>"

def getParts(parts_lines):
	cmtyParts = [-1]

	for line in parts_lines:
		tokens = line.split()
		if tokens:
			cmtyParts.append( int(tokens[0]) )

	return cmtyParts

def getCutCmtys(cmtyParts, edge_lines, numCmtys):
	
	cutCmtys = [-1] # cutCmtys[cmty] = <weight of cut edge it belong to> or -1 if not a cut vertex

	for i in range(0, numCmtys):
		cutCmtys.append(-1)

	for line in edge_lines:
		tokens = line.split()
		if tokens:
			end1 = int(tokens[0])
			end2 = int(tokens[1])
			weight = float(tokens[3])

			if cmtyParts[end1] != cmtyParts[end2]:
				cutCmtys[end1] = weight
				cutCmtys[end2] = weight

	return cutCmtys

def get_cmty_weights(node_lines, num_cmtys):
	
	node_weights = [-1]

	for i in range(0, num_cmtys):
		node_weights.append(-1)		

	for line in node_lines:
		tokens = line.split()
		if tokens and tokens[0].isdigit():
			node = int(tokens[0])
			weight = float(tokens[2])
			node_weights[node] = weight

	return node_weights


if __name__ == '__main__':

	partitionF = sys.argv[1]
	graphxcl_f = sys.argv[2]
	comms_f = sys.argv[3]

	output_f = partitionF + ".cutVertices"

	with open(partitionF, "r") as f:
		parts_lines = f.readlines()

	with open(graphxcl_f, "r") as f:
		edge_lines = f.readlines()

	with open(comms_f, "r") as f:
		node_lines = f.readlines()
 
	# read partitionF, generate list of size n+1 (index 0 is empty) 
	# with index i element containing partition # of cmty i

	#getParts(parts_lines):
	cmtyParts = getParts(parts_lines)

	numCmtys = (len(cmtyParts) - 1) # cmtyParts's length is n+1 since empty 0th element

	# read edge_f, for each pair check partitions[cmty] and mark them as cut cmtys
	# if partition[cmty] are different

	node_weights = get_cmty_weights(node_lines, numCmtys)

	cutCmtys = getCutCmtys(cmtyParts, edge_lines, numCmtys)

	with open(output_f, "w") as f:
		f.write("%s\n" %FORMAT)
		for cmty in range(1, numCmtys+1):
			if cutCmtys[cmty] > 0:
				#	<cut_cmty> <weight_of_corresponding_cut_edge> <weight_of_cmty>
				f.write("%d %f %f\n" %(cmty, cutCmtys[cmty], node_weights[cmty]) )




