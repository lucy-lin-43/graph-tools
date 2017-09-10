


partSuffix=".metisInput.part.2"
edgeF=".clauseCommBrg.graphxcl"
commsF=".clauseCommBrg.comms_size"



for cnf in /local-scratch/lucy_temp/make_process_metis_files/test/*cnf; do
	if [ -s $cnf$partSuffix ] && [ -s $cnf$edgeF ] && [ -s $cnf$commsF ]; then

		echo $cnf$partSuffix

		# partitionF = sys.argv[1]
		# intInv_edge_f = sys.argv[2]
		# int_comms_f = sys.argv[3]

		python ./getCutVars.py $cnf$partSuffix $cnf$edgeF $cnf$commsF 
	fi
done
