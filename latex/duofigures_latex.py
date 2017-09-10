
import sys
import glob
import os.path





# with or without pre-processing by glucose

#processed


# Everything after formula name
UN_TD_PNG_SUFF = ".cnf.td.png" 
PROC_TD_PNG_SUFF = ".cnf.eliminated.td.colored.png"

FILE_TYPES = [".png", ".jpg"]

UN_TD_FOLDER = "/local-scratch/lucy_temp/td-latex-cont/td_graphs_2016"
PROC_TD_FOLDER = "/local-scratch/lucy_temp/td-latex-cont/final_graph_td_elim_2016"

OVERLEAF_UN_TD_FOLDER = "Tree_Decompositions"
OVERLEAF_PROC_TD_FOLDER = "Tree_Decompositions"

INS_MOD_TD_FILEPATH = "insert_mod_proc_td_filepath"
INS_MOD_UN_TD_FILEPATH = "insert_mod_un_td_filepath"
INS_ESC_FORMULA_NAME= "insert_esc_formula_name"
INS_FIG_LABEL = "insert_label"

LABEL_DUO_SUFF = ".duo"

DUO_FIGURE_TEMPLATE = "\\begin{figure}[!htbp]\n  \\centering\n  \\begin{minipage}[b]{0.4\\textwidth}\n    \\includegraphics[width=8cm, height=8.5cm]{insert_mod_un_td_filepath}\n  \\end{minipage}\n  \\hfill\n  \\begin{minipage}[b]{0.4\\textwidth}\n    \\includegraphics[width=8cm, height=8.5cm]{insert_mod_proc_td_filepath}\n  \\end{minipage}\n  \\caption{\\label{fig: insert_label }insert_esc_formula_name formula. Left: tree-decomposition of unprocessed formula. Right: tree-decomposition of formula after pre-processing with Glucose (coloring corresponds to bag betweenness centrality). Tree-decompositions produced by Flow-Cutter, PACE 2016 heuristic winner} \n\\end{figure}\n"


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


def make_latex_duofigure(formula, cmty_filename, td_filename):
	figure = DUO_FIGURE_TEMPLATE
	
	mod_cmty_filename = modFileName( OVERLEAF_UN_TD_FOLDER + '/' + cmty_filename)
	mod_td_filename = modFileName( OVERLEAF_PROC_TD_FOLDER + '/' + td_filename)
	esc_formula = escapeLatex(formula)
	fig_label = mod_td_filename + LABEL_DUO_SUFF

	INS_KEY_LIST = [INS_ESC_FORMULA_NAME, INS_MOD_UN_TD_FILEPATH, INS_MOD_TD_FILEPATH, INS_FIG_LABEL] 
	content_list = [esc_formula, mod_cmty_filename, mod_td_filename, fig_label]

	num_keys = len(INS_KEY_LIST)
	for i in range(0, num_keys):
		figure = figure.replace(INS_KEY_LIST[i], content_list[i])

	return figure

if __name__ == '__main__':

	
	un_td_png_filepaths = glob.glob( os.path.join(UN_TD_FOLDER, "*" + UN_TD_PNG_SUFF) )
	
	out_f = sys.argv[1]

	with open(out_f, "w") as g:

		for un_td_png_filepath in un_td_png_filepaths:
			un_td_filename = un_td_png_filepath.rsplit("/", 1)[1]
			raw_formula = un_td_filename.split(UN_TD_PNG_SUFF, 1)[0]
			proc_td_filename = raw_formula + PROC_TD_PNG_SUFF
			proc_td_filepath = os.path.join(PROC_TD_FOLDER, proc_td_filename)
			if os.path.isfile(proc_td_filepath):
				latex_figure = 	make_latex_duofigure(raw_formula, un_td_filename, proc_td_filename)
				g.write("%s\n\n" %latex_figure)




		



