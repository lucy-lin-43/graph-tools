




intInvNormEdgeF=".clauseCommBrg.graphxcl.int_invSquared_Norm_1_100"

intNormCommsF=".clauseCommBrg.comms_size.int_norm_1_100"

for cnf in /local-scratch/lucy_temp/make_process_metis_files/test/*cnf; do	
	if [ -s $cnf$intInvNormEdgeF ] && [ -s $cnf$intNormCommsF ]; then 
		echo $cnf 

		# cnf_f = sys.argv[1]
		# intInv_edge_f = sys.argv[2]
		# int_comms_f = sys.argv[3]

		python ./generate_metis_input.py $cnf  $cnf$intInvNormEdgeF $cnf$intNormCommsF 

	fi 
done
