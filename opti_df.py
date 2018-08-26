import pdb
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

def mem_usage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)



def col_opti(col, col_type, override=None):
	#print(col_type)
	col = col.fillna(0)
	for types in np.sctypes:
		#print types

		if col_type in np.sctypes[types]:
			#print "One of ", np.sctypes[types]
			if types == "int":
				types = "uint"
			for precision in np.sctypes[types]:
				ncol = col.astype(precision).copy()
				if (ncol == col).all():
					#print "Works for ", precision
					return ncol

	raise ValueError("Couldn't detect proper dtypes")


def opti(df):
	ndf = pd.DataFrame()
	print(mem_usage(df))
	for types in set(df.dtypes.tolist()):
		print "Processing type ", types 
		to_conv = df.select_dtypes(include=types)
		if is_numeric_dtype(types):
		    
		    converted_num = pd.DataFrame()

		    for col in to_conv.columns:

		    	num_unique_values = len(to_conv[col].unique())
		    	if num_unique_values <= 2:
		    		converted_num[col]= to_conv[col].astype('bool')
		    	else:
		    		converted_num[col] = col_opti(to_conv[col], types)
		    ndf[converted_num.columns] = converted_num
		else:

			converted_obj = pd.DataFrame()
			dictio = {}
			for col in to_conv.columns:
			    
			    dictio[col] = {}
			    num_unique_values = len(to_conv[col].unique())
			    num_total_values = len(to_conv[col])
			    
			    if num_unique_values / num_total_values < 0.5:

			        converted_obj.loc[:,col] = to_conv[col].astype('category')
			        dictio[col] = dict(enumerate(converted_obj.loc[:,col].cat.categories))
			        converted_obj.loc[:,col] = converted_obj.loc[:,col].cat.codes
			    else:
			        converted_obj.loc[:,col] = to_conv[col].astype('unicode')

			ndf[converted_obj.columns] = converted_obj
	pd.DataFrame(dictio).to_pickle("the_dic.pkl")
	# Set proper order
	ndf = ndf[df.columns]
	return ndf

if __name__ == "__main__":

	files = "games/total_games.txt"
	names="date	number_of_game	day_of_week	v_name	v_league	v_game_number	h_name	h_league	h_game_number	v_score	h_score	length_outs	day_night	completion	forefeit	protest	park_id	attendance	length_minutes	v_line_score	h_line_score	v_at_bats	v_hits	v_doubles	v_triples	v_homeruns	v_rbi	v_sacrifice_hits	v_sacrifice_flies	v_hit_by_pitch	v_walks	v_intentional walks	v_strikeouts	v_stolen_bases	v_caught_stealing	v_grounded_into_double	v_first_catcher_interference	v_left_on_base	v_pitchers_used	v_individual_earned_runs	v_team_earned_runs	v_wild_pitches	v_balks	v_putouts	v_assists	v_errors	v_passed_balls	v_double_plays	v_triple_plays	h_at_bats	h_hits	h_doubles	h_triples	h_homeruns	h_rbi	h_sacrifice_hits	h_sacrifice_flies	h_hit_by_pitch	h_walks	h_intentional walks	h_strikeouts	h_stolen_bases	h_caught_stealing	h_grounded_into_double	h_first_catcher_interference	h_left_on_base	h_pitchers_used	h_individual_earned_runs	h_team_earned_runs	h_wild_pitches	h_balks	h_putouts	h_assists	h_errors	h_passed_balls	h_double_plays	h_triple_plays	hp_umpire_id	hp_umpire_name	1b_umpire_id	1b_umpire_name	2b_umpire_id	2b_umpire_name	3b_umpire_id	3b_umpire_name	lf_umpire_id	lf_umpire_name	rf_umpire_id	rf_umpire_name	v_manager_id	v_manager_name	h_manager_id	h_manager_name	winning_pitcher_id	winning_pitcher_name	losing_pitcher_id	losing_pitcher_name	saving_pitcher_id	saving_pitcher_name	winning_rbi_batter_id	winning_rbi_batter_id_name	v_starting_pitcher_id	v_starting_pitcher_name	h_starting_pitcher_id	h_starting_pitcher_name	v_player_1_id	v_player_1_name	v_player_1_def_pos	v_player_2_id	v_player_2_name	v_player_2_def_pos	v_player_3_id	v_player_3_name	v_player_3_def_pos	v_player_4_id	v_player_4_name	v_player_4_def_pos	v_player_5_id	v_player_5_name	v_player_5_def_pos	v_player_6_id	v_player_6_name	v_player_6_def_pos	v_player_7_id	v_player_7_name	v_player_7_def_pos	v_player_8_id	v_player_8_name	v_player_8_def_pos	v_player_9_id	v_player_9_name	v_player_9_def_pos	h_player_1_id	h_player_1_name	h_player_1_def_pos	h_player_2_id	h_player_2_name	h_player_2_def_pos	h_player_3_id	h_player_3_name	h_player_3_def_pos	h_player_4_id	h_player_4_name	h_player_4_def_pos	h_player_5_id	h_player_5_name	h_player_5_def_pos	h_player_6_id	h_player_6_name	h_player_6_def_pos	h_player_7_id	h_player_7_name	h_player_7_def_pos	h_player_8_id	h_player_8_name	h_player_8_def_pos	h_player_9_id	h_player_9_name	h_player_9_def_pos	additional_info	acquisition_info"

	columns = names.split("\t")

	df = pd.read_csv(files, ',', names=columns, low_memory=False)

	dff = opti(df)
	dff.to_csv('games.tsv', '\t')

	pdb.set_trace()



