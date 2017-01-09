#include <MEME.spec>
/* 
	Module KBaseCmonkey version 1.0
	This module provides a set of methods for work with cMonkey biclustering tool.
	
	Data types summary
	Input data types: 
	ExpressionSeries from KBaseExpression service.
	ExpressionSample from KBaseExpression service.
	KBaseGenomes.Genome
	Networks.InterationSet with operons data
	Networks.InterationSet with STRING data
	Output data types:
	CmonkeyRun data type represents data generated by a single run of cMonkey (run_infos table of cMonkey results)
	CmonkeyNetwork data type represents bicluster network
	CmonkeyCluter data type represents a single bicluster from cMonkey network, with links to genes, experimental conditions and motifs
	CmonkeyMotif data type represents a single motif identifed for a bicluster

	Methods summary
	run_cmonkey - Starts cMonkey server run for a series of expression data stored in workspace and returns job ID of the run
*/



module Cmonkey
{


	/* Represents KBase gene identifier
		@id external
	*/
	typedef string gene_id;

	/* Represents WS expression data sample identifier
		id ws KBaseExpression.ExpressionSample
	*/
	typedef string expression_sample_ws_ref;

	/* Represents WS expression data series identifier
		@id ws KBaseExpression.ExpressionSeries
	*/
	typedef string expression_series_ws_ref;

	/* Represents WS genome identifier
		@id ws KBaseGenomes.Genome
	*/
	typedef string genome_ws_ref;

	/* Represents WS operome identifier
		@id ws KBaseNetworks.InteractionSet
	*/
	typedef string operons_ws_ref;

	/* Represents WS network identifier
		@id ws KBaseNetworks.InteractionSet
	*/
	typedef string network_ws_ref;

	/* Represents WS cMonkey motif identifier
		id subws Cmonkey.CmonkeyMotif
	*/
	typedef string cmonkey_motif_id;

	/* Represents WS cMonkey cluster identifier
		id subws Cmonkey.CmonkeyCluster
	*/
	typedef string cmonkey_cluster_id;

	/* Represents WS cMonkey network identifier
		id subws Cmonkey.CmonkeyNetwork
	*/
	typedef string cmonkey_network_id;

	/* Represents WS cMonkey run result identifier
		id ws Cmonkey.CmonkeyRunResult
	*/
	typedef string cmonkey_run_result_id;

	/* Represents motif generated by cMonkey with a list of hits in upstream sequences
		string id - identifier of MotifCmonkey
		string seq_type - type of sequence
		int pssm_id - number of motif
		float evalue - motif e-value
		list<list<float>> pssm_rows - PSSM 
		list<MEME.HitMast> hits - hits (motif annotations)
		list<MEME.SiteMeme> sites - training set
		
		@optional seq_type pssm_id evalue pssm_rows hits sites
	*/
	typedef structure{
		string id;
		string seq_type;
		int pssm_id;
		float evalue;
		list<list<float>> pssm_rows;
		list<MEME.MastHit> hits;
		list<MEME.MemeSite> sites;
	} CmonkeyMotif;

	/* Represents bicluster generated by cMonkey
		string id - identifier of bicluster
		float residual - residual
		list<expression_sample_ws_id> sample_ws_ids - list of experimental conditions 
		list<gene_id> gene_ids - list of genes from bicluster
		list<CmonkeyMotif> motifs - list of motifs identified for the bicluster, converted to MEME format
		
		@optional motifs
	*/
	typedef structure{
		string id;
		float residual;
		list<expression_sample_ws_ref> sample_ws_ids;
		list<gene_id> gene_ids;
		list<CmonkeyMotif> motifs;
	} CmonkeyCluster;
	
	/* Represents network generated by a single run of cMonkey
		string id - identifier of cMonkey-generated network
		int iteration - number of the last iteration
		string genome_name - organism name
		int rows_number - number of rows
		int columns_number - number of columns
		int clusters_number - number of clusters
		list<CmonkeyCluster> clusters - list of biclusters
		
		@optional genome_name rows_number columns_number clusters_number clusters
	*/
	typedef structure{
		string id;
		int iteration;
		string genome_name;
		int rows_number;
		int columns_number;
		int clusters_number;
		list<CmonkeyCluster> clusters;
	} CmonkeyNetwork;
	
	/* Contains parameters of a cMonkey run
		int networks_scoring = <0|1> - if 1, Network scoring will be used
		int motifs_scoring = <0|1> - if 1, Motif scoring will be used
		expression_series_ws_ref series_id - workspace id of expression data series;
		genome_ws_ref genome_id - workspace id of genome;
		operons_ws_ref operome_id - workspace id of operome;
		network_ws_ref network_id - workspace id of network;
		
		@optional genome_ref operome_ref network_ref
	*/
	typedef structure{
		expression_series_ws_ref series_ref;
		genome_ws_ref genome_ref;
		operons_ws_ref operome_ref;
		network_ws_ref network_ref;
		int networks_scoring;
		int motifs_scoring;
	} CmonkeyRunParameters;

	/* Represents data from a single run of cMonkey
		string id - identifier of cMonkey run
		string start_time - start time of cMonkey run
		string finish_time - end time of cMonkey run
		int iterations_number - number of iterations
		int last_iteration - last iteration
		CmonkeyRunParameters parameters - run parameters
		CmonkeyNetwork network;
	*/
	typedef structure{
		string id;
		string start_time;
		string finish_time;
		int iterations_number;
		int last_iteration;
		CmonkeyRunParameters parameters;
		CmonkeyNetwork network;
	} CmonkeyRunResult;

	/*	Starts cMonkey server run for a series of expression data stored in workspace and returns job ID of the run
		string ws_id - workspace id
		CmonkeyRunParameters params - parameters of cMonkey run
		string job_id - identifier of cMonkey job
	*/
	funcdef run_cmonkey(string ws_id, CmonkeyRunParameters params) returns(string cmonkey_run_result_job_id) authentication required;
};


