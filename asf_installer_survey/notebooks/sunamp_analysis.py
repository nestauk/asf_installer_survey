# %% [markdown]
# ## Analysis for Sunamp
# **Aims:** Generating outputs as outlined in [analysis plan](https://docs.google.com/document/d/1w263o_J1JPLoT1H7tq1Sd43CLylsxCgeVSSqLEbaTLA/edit).
# Run this file as a Jupyter Notebook to inspect each cross tabulation generated - two cross tables are generated for each survey question of interest
# (1 with subpopulation breakdowns by response to SQ 18 and 1 with subpopulation breakdowns by response to SQ 101).<br>
# **Author:** Elysia Lucas<br>
# **Date:** 2024-06-02<br>

# %%
%%capture

# Run pre-processing
#%run data_setup.ipynb
with open("data_setup.py") as file:
    exec(file.read())

from matplotlib import pyplot as plt

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# %% [markdown]
# Define function to create expanded dataframe for select all apply type questions

# %%
def select_all_apply_transformation(response_list, column_of_interest, column_for_breakdown):
    
    stacked_responses = pd.DataFrame()

    for n in range(0, len(response_list)-1):
        response = response_list[n]
        new_col = column_of_interest + str(n+1)
        data[new_col] = data.apply(transform, args = (response, response_list, column_of_interest), axis = 1)

        stacked_responses_individual = data.filter([column_for_breakdown, new_col])
        stacked_responses_individual = stacked_responses_individual.rename(columns={new_col:column_of_interest})
        stacked_responses = pd.concat([stacked_responses, stacked_responses_individual])
    
    return stacked_responses

# %% [markdown]
# Q1

# %%
pd.crosstab(data[col.q1], data[col.q18])
pd.crosstab(data[col.q1], data[col.q101])

# %% [markdown]
# Q3

# %%
pd.crosstab(data[col.q3], data[col.q18])
pd.crosstab(data[col.q3], data[col.q101])

# %% [markdown]
# Q4

# %%
pd.crosstab(data[col.q4], data[col.q18])
pd.crosstab(data[col.q4], data[col.q101])

# %% [markdown]
# Q5

# %%
pd.crosstab(data[col.q5], data[col.q18])
pd.crosstab(data[col.q5], data[col.q101])

# %% [markdown]
# Q6

# %%
# Company owners and sole traders
pd.crosstab(data[col.q6a], data[col.q18])
pd.crosstab(data[col.q6a], data[col.q101])

# %%
# Employees
pd.crosstab(data[col.q6b], data[col.q18])
pd.crosstab(data[col.q6b], data[col.q101])

# %% [markdown]
# Q7 - Select all that apply

# %%
question_7 = pd.DataFrame(explode_select_all(data[col.q7]).sum())
responses_q7 = question_7.index.to_list()
responses_q7.append('Total')

# %%
# SQ 18
response_list = responses_q7
column_of_interest = col.q7

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %% [markdown]
# Q8 - Select all that apply

# %%
question_8 = pd.DataFrame(explode_select_all(data[col.q8]).sum())
responses_q8 = question_8.index.to_list()
responses_q8.append('Total')

# %%
# SQ 18
response_list = responses_q8
column_of_interest = col.q8

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %% [markdown]
# Q10

# %%
pd.crosstab(data[col.q10], data[col.q18])
pd.crosstab(data[col.q10], data[col.q101])

# %% [markdown]
# Q18

# %%
pd.DataFrame(data[col.q18].value_counts())

# %% [markdown]
# Q19

# %%
question_19 = pd.DataFrame(explode_select_all(data[col.q19[0]]).sum())
responses_q19 = question_19.index.to_list()
responses_q19.append('Total')

# %%
# SQ 18
response_list = responses_q19
column_of_interest = col.q19[0]

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %%
# Recording responses to Q18 and Q101 from respondents who gave free text responses
data[[col.q18, col.q101, col.q19[0],col.q19[1]]].dropna()

# %% [markdown]
# Q20

# %%
pd.crosstab(data[col.q20[0]], data[col.q18])
pd.crosstab(data[col.q20[0]], data[col.q101])

# %%
# Recording responses to Q18 and Q101 from respondents who gave free text responses
data[[col.q18, col.q101, col.q20[1]]].dropna()

# %% [markdown]
# Q21

# %%
# Company owners
pd.crosstab(data[col.q21a], data[col.q18])
pd.crosstab(data[col.q21a], data[col.q101])

# %%
# Sole traders and contractors
pd.crosstab(data[col.q21c], data[col.q18])
pd.crosstab(data[col.q21c], data[col.q101])

# %% [markdown]
# Q58

# %%
# Company owners
pd.crosstab(data["58a. In which areas of your business do you think extra support could be most helpful: Thermal store selection"], data[col.q18])
pd.crosstab(data["58a. In which areas of your business do you think extra support could be most helpful: Thermal store selection"], data[col.q101])

# %%
# Employees
pd.crosstab(data["58b. In which areas of your work do you think extra support could be most helpful: Thermal store selection"], data[col.q18])
pd.crosstab(data["58b. In which areas of your work do you think extra support could be most helpful: Thermal store selection"], data[col.q101])

# %%
# Contractors
pd.crosstab(data["58c. In which areas of your work do you think extra support could be most helpful: Thermal store selection"], data[col.q18])
pd.crosstab(data["58c. In which areas of your work do you think extra support could be most helpful: Thermal store selection"], data[col.q101])

# %%
# Sole traders
pd.crosstab(data["58d. In which areas of your business do you think extra support could be most helpful: Thermal store selection"], data[col.q18])
pd.crosstab(data["58d. In which areas of your business do you think extra support could be most helpful: Thermal store selection"], data[col.q101])

# %% [markdown]
# Q70 - Select all that apply

# %%
## Recoding free text responses 

def get_index(recode):
    """
    Function to create dictionary where
    key is response ID and value is dataframe index.

    Args:
        recode: List of response IDs to be recoded
    
    Returns:
        response[id]: dictionary {id:index}
    """
    
    # Get row indices
    indices = []
    for id in recode:
        i = data.index[data[col.q0a]==id]
        indices.append(i)

    # Map lists in dictionary
    return {recode[i]: indices[i] for i in range(len(recode))}

def recode_single_replace_new(ids_for_recoding, column, new_option, dataframe) -> pd.DataFrame:
    """Replace "Other" in answer entry for response ID with new option"""

    response = get_index(ids_for_recoding)

    for id in ids_for_recoding:
        
        for entry in dataframe.loc[response[id], column]:
            entry[entry == "Other"] = new_option
    
    return dataframe

# Recoding "Other" to new option
ids_for_recoding_q70 = [763,
                        133,
                        192,
                        370,
                        529,
                        593,
                        674,
                        689,
                        796,
                        311,
                        352,
                        395,
                        589,
                        649
                        ]
data = recode_single_replace_new(ids_for_recoding_q70, col.q70[0], "Easy MCS", data)

ids_for_recoding_q70 = [331,
                        542,
                        616,
                        751,
                        805,
                        828,
                        300,
                        562,
                        741,
                        533,
                        309,
                        598
                        ]
data = recode_single_replace_new(ids_for_recoding_q70, col.q70[0], "Evergreen", data)

ids_for_recoding_q70 = [79,
                        621,
                        788,
                        750
                        ]
data = recode_single_replace_new(ids_for_recoding_q70, col.q70[0], "H2x", data)

ids_for_recoding_q70 = [115,
                        129,
                        144,
                        574,
                        287,
                        619,
                        821
                        ]
data = recode_single_replace_new(ids_for_recoding_q70, col.q70[0], "Heatpunk", data)

ids_for_recoding_q70 = [345,
                        613,
                        664
                        ]
data = recode_single_replace_new(ids_for_recoding_q70, col.q70[0], "I don't use design software", data)

# %%
question_70 = pd.DataFrame(explode_select_all(data[col.q70[0]]).sum())
responses_q70 = question_70.index.to_list()
responses_q70.append('Total')

# %%
# SQ 18
response_list = responses_q70
column_of_interest = col.q70[0]

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %% [markdown]
# Q97 - Select all that apply

# %%
question_97 = pd.DataFrame(explode_select_all(data[col.q97[0]]).sum())
responses_q97 = question_97.index.to_list()
responses_q97.append('Total')

# %%
# SQ 18
response_list = responses_q97
column_of_interest = col.q97[0]

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %% [markdown]
# Q100

# %%
pd.crosstab(data[col.q100[0]], data[col.q18])
pd.crosstab(data[col.q100[0]], data[col.q101])

# %%
data[col.q100[1]].value_counts()

# %% [markdown]
# Q101

# %%
pd.DataFrame(data[col.q101].value_counts())

# %% [markdown]
# Q102

# %%
pd.crosstab(data[col.q102[0]], data[col.q18])
pd.crosstab(data[col.q102[0]], data[col.q101])

# %%
pd.DataFrame(data[col.q102[1]].value_counts())

# %% [markdown]
# Q104

# %%
pd.crosstab(data[col.q104[0]], data[col.q18])
pd.crosstab(data[col.q104[0]], data[col.q101])

# %%
pd.DataFrame(data[col.q104[1]].value_counts())

# %% [markdown]
# Q107

# %%
question_107 = pd.DataFrame(explode_select_all(data[col.q107[0]]).sum())
responses_q107 = question_107.index.to_list()
responses_q107.append('Total')

# %%
# SQ 18
response_list = responses_q107
column_of_interest = col.q107[0]

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %%
pd.DataFrame(data[col.q107[1]].value_counts())

# %% [markdown]
# Q112

# %%
question_112 = pd.DataFrame(explode_select_all(data[col.q112[0]]).sum())
responses_q112 = question_112.index.to_list()
responses_q112.append('Total')

# %%
# SQ 18
response_list = responses_q112
column_of_interest = col.q112[0]

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %%
pd.DataFrame(data[col.q112[1]].value_counts())

# %% [markdown]
# Q113

# %%
question_113 = pd.DataFrame(explode_select_all(data[col.q113[0]]).sum())
responses_q113 = question_113.index.to_list()
responses_q113.append('Total')

# %%
# SQ 18
response_list = responses_q113
column_of_interest = col.q113[0]

stacked_responses_sq18 = select_all_apply_transformation(response_list, column_of_interest, col.q18)
crosstab_sq18 = pd.crosstab(stacked_responses_sq18[column_of_interest], stacked_responses_sq18[col.q18], margins = True, margins_name = 'Total')
crosstab_sq18 = crosstab_sq18.fillna(0)
crosstab_sq18 = crosstab_sq18.astype(int)
crosstab_sq18

# %%
# SQ 101
stacked_responses_sq101 = select_all_apply_transformation(response_list, column_of_interest, col.q101)
crosstab_sq101 = pd.crosstab(stacked_responses_sq101[column_of_interest], stacked_responses_sq101[col.q101], margins = True, margins_name = 'Total')
crosstab_sq101 = crosstab_sq101.fillna(0)
crosstab_sq101 = crosstab_sq101.astype(int)
crosstab_sq101

# %%
pd.DataFrame(data[col.q113[1]].value_counts())

# %% [markdown]
# Q18 x Q101

# %%
pd.crosstab(data[col.q101], data[col.q18])


