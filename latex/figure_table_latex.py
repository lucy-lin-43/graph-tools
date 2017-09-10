

# generates latex script with labelled tree-decomposition figure and table on top of it indicating which bags were bumped for each category

# FIXME: some image files have .cnf in them but some don't

import sys
import os.path
import glob
import networkx as nx
import matplotlib.pyplot as plt


IMG_SUFF = ".cnf.eliminated.td.colored.png" # Everything after formula_name (i.e include .cnf!)
IMG_FOLDER = "/local-scratch/lucy_temp/td-latex-cont/final_graph_td_elim_2013"
TD_FOLDER = "/local-scratch/lucy_temp/2013_centrality_formulas"
TD_SUFF = ".cnf.eliminated.gr.TW_flow_cutter.300" # Everything after formula_name (i.e include .cnf!)

TD_OVERLEAF_FOLDER = "Tree_Decompositions"

OUT_F = "2013_td_latex.txt"
CNF_SUFF = ".cnf"

TW = "Treewidth"

INS_PARBOX_SIZE = "insert_parbox_size" # include in ending
INS_PARBOX_TEXT = "insert_parbox_text"
TABLE_PARBOX = '\\parbox[t]{insert_parbox_size in}{\\small insert_parbox_text \\strut}'
TOP_CENTER_25 = "Bumped 25\\% highest center" 
TOP_SIZE_25 = "Bumped 25\\% largest"

HLINE = "\\hline"
NEWL = '\n'

INS_MOD_OVERLEAF_FILEPATH = "insert_mod_overleaf_filepath"
INS_TABLE = "insert_table"
INS_ESC_FORMULA_NAME= "insert_formula_name"
INS_CAPTION = "insert_caption"


CAPTION = "Table indicates, for each bumping scheme, the bag bumped and, in brackets, the fraction of the bag bumped. Coloring corresponds to the bag's betweenness centrality (NetworkX). Labels correspond to bag number. Size correspond to bag size. Tree decomposition produced by Flow-Cutter, PACE 2016 heuristic winner."

FIGURE_TEMPLATE = "\\begin{figure}[!htbp] \n  \\begin{minipage}[b]{0.60\\linewidth} \n    \\centering \n    \\includegraphics[width=10cm, height=8.5cm]{insert_mod_overleaf_filepath} \n  \\end{minipage} \n  \\begin{minipage}[b]{0.20\\linewidth} \n    \\centering \n\\begin{tabular}[b]{ |l|l| } \n\\hline \ninsert_table\\end{tabular} \n\\end{minipage} \n\\caption{\\label{fig: insert_mod_overleaf_filepath }Tree decomposition of insert_formula_name formula, after pre-processing by Glucose. insert_caption} \n\\end{figure} \n \n \n"


FILE_TYPES = [".png", ".jpg"]

def getCnf(formula):
	if (not(".cnf" in formula)):
		formula = formula + ".cnf"
	return formula

# Replacing _ with \\_ during label construction
def escapeLatex(string):
	finalString = string.replace("_", "\\_")
	return finalString

# Replace "." with "_" in includegraphics filename part
# suffix must include "."
def modFileName(filename):
	for i in FILE_TYPES:
		if i in filename:
			trunc = filename.split(i, 1)[0]
			trunc = trunc.replace(".", "_")
			finalname = trunc + i	
	return finalname


# size in inches and as string
def make_parbox(content, size_parbox):
	parbox = TABLE_PARBOX
	parbox = parbox.replace(INS_PARBOX_TEXT, content)
	parbox = parbox.replace(INS_PARBOX_SIZE, size_parbox)
	return parbox		

def addTableContent(curr_table, name, data):
	#print curr_table, col_1, col_2
	col_1 = make_parbox(name, "0.5")
	col_2 = make_parbox(data, "1.5")
	return (curr_table + col_1 + ' & ' + col_2 + '\\\\' + NEWL + HLINE + NEWL)

# input in form: [ [<bumped_bag>, <frac_bumped_in_bag>], etc.]
def buildBumpedCol2(top_bags_frac):
	col2 = ""
	num_top_bags = len(top_bags_frac)
	if num_top_bags > 20:
		col2 = "*%d bags bumped" %num_top_bags
	else:
		for pair in top_bags_frac:
			bag = pair[0]
			frac = pair[1]
			col2 += "\\textbf{%d} (%.2f), " % (bag, frac)
	return col2

def addBumpedContent(curr_table, name, top_bags_frac):
	updatedTable = ""
	#print top_bags_frac
	col2 = buildBumpedCol2(top_bags_frac)
	#print col2
	updatedTable = addTableContent(curr_table, name, col2)
	return updatedTable


def build_graph(td_lines):
	g = nx.Graph()
	edges = get_edges(td_lines)
	node_sizes = get_node_sizes(td_lines)
	add_all_edges(g, edges)
	add_weighted_nodes(g, node_sizes)
	return g

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
	
def add_all_edges(g, edges):
	for e in edges:
		g.add_edge(e[0], e[1])

def add_weighted_nodes(g, node_sizes):
	len_node_sizes = len(node_sizes)
	for i in range(1, len_node_sizes):
		g.add_node(i, weight = node_sizes[i])


def get_sorted_norm_bag_center(td_lines):
	g = build_graph(td_lines)	
	centrality = nx.betweenness_centrality(g)

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
def get_portion_top_bags(td_lines, sorted_bags_score, portion):
	num_all_vars = get_num_vars(td_lines)
	b_bsize_list = get_b_bsize(td_lines)
	num_top_vars = round(num_all_vars * portion)
	num_curr_top_vars = 0
	top_bags_numVars = []	# <bag> <top vars from bag>

	i = -1

	while num_curr_top_vars < num_top_vars:
		
		curr_b = sorted_bags_score[i][0]
		curr_bsize = b_bsize_list[curr_b]
	
		if num_curr_top_vars + curr_bsize > num_top_vars:
			num_added = num_top_vars - num_curr_top_vars
			top_bags_numVars.append( [curr_b, float(num_added)/curr_bsize] ) 
			num_curr_top_vars = num_top_vars
		else:
			top_bags_numVars.append( [curr_b, 1.0] )
			num_curr_top_vars += curr_bsize
		i -= 1 # won't exceed past length of sorted_bags_score since portion is decimal

	return top_bags_numVars

def get_num_vars(ub_lines):	
	num_vars = -1
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 's':
			num_vars = int(tokens[-1])
	return num_vars



def get_num_bags(ub_lines):
	num_bags = 0
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 'b':
			num_bags += 1
	return num_bags

def get_tree_width(ub_lines):
	tw = -1
	for line in ub_lines:
		tokens = line.split()
		if tokens and tokens[0] == 's':
			tw = (int(tokens[-2]) - 1)
	return tw

def make_figure(formula, img_td_filename, table, caption):
	figure = FIGURE_TEMPLATE
	mod_img_overleaf_filepath = modFileName(TD_OVERLEAF_FOLDER + '/' + img_td_filename)
	esc_formula = escapeLatex(formula)

	keyword_list = [INS_ESC_FORMULA_NAME, INS_MOD_OVERLEAF_FILEPATH, INS_TABLE, INS_CAPTION]
	content_list = [esc_formula, mod_img_overleaf_filepath, table, caption]

	num_keys = len(keyword_list)
	for i in range(0, num_keys):
		figure = figure.replace(keyword_list[i], content_list[i])

	return figure 

if __name__ == '__main__':

	# get list of .png from folder
	img_td_filepath_list = glob.glob( os.path.join(IMG_FOLDER, "*" + IMG_SUFF) )
	
	with open(OUT_F, "w") as g:
		for img_td_filepath in img_td_filepath_list:
			img_td_filename = img_td_filepath.rsplit('/', 1)[1]
			formula_name = img_td_filename.split( CNF_SUFF, 1)[0]
			td_filepath = os.path.join(TD_FOLDER, formula_name + TD_SUFF)
			
			if os.path.isfile(td_filepath):
				with open(td_filepath, "r") as f:
					td_lines = f.readlines()
				sorted_norm_bag_center = get_sorted_norm_bag_center(td_lines)
				sorted_b_bsize = get_sorted_b_bsize(td_lines)
				portion = 0.25
				top_center_bags_frac = get_portion_top_bags(td_lines, sorted_norm_bag_center, portion)	
				top_size_bags_frac = get_portion_top_bags(td_lines, sorted_b_bsize, portion)

				# build table
				table = ""
				table = addTableContent(table, TW, str(get_tree_width(td_lines)))
				table = addBumpedContent(table, TOP_CENTER_25, top_center_bags_frac)
				table = addBumpedContent(table, TOP_SIZE_25, top_size_bags_frac)				
				figure = make_figure(formula_name, img_td_filename, table, CAPTION)
				g.write("%s\n\n" %figure)




				




















