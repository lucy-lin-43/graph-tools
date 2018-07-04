Graph-tools
===================
Graph-tools is a collection of scripts for isolating  propositional formula variables that have interesting graph properties, such as min cut variables and variables with high betweenness centrality. Scripts are available for calculating betweenness centrality using the Python NetworkX library and for parsing the output of the [Metis Graph Partitioning software](http://glaros.dtc.umn.edu/gkhome/taxonomy/term/60/0?page=19) and [PACE 2017 Tree-Width softwares](https://pacechallenge.wordpress.com/pace-2017/track-a-treewidth/). Python scripts are also available to automate graph drawing of conjunctive normal form (CNF) formulas using NetworkX. Visual basic scripts use the NodeXL library to automate more complicated graph drawing. To derive the graph, each variable is regarded as a node and an edge exists between two variables if they appear in the same conjunct.

## Authors
Lucy Lin
