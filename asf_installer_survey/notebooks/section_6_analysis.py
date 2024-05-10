# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     comment_magics: true
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: installersurvey
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Section 6: Maintenance and servicing
# **Aims:** Generating outputs for Section 6 (RQs 6.01-6.25) as planned in [Heat Pump Installer Survey data analysis plan](https://docs.google.com/document/d/1M1nzdf3fyTjipmaKJKViin0EB3e3R1afOQglwMGJaII/edit#heading=h.jzmlm8j0kyve)<br>
# **Author:** Elysia Lucas<br>
# **Date:** 2024-04-04<br>
# <i>Update:</i> 2024-04-17 (Re-coding of free text responses)
# <p> 
# N.B. As of 11.04.2024, only CompanySizeOwner and CompanySizeEmployee outputs with version 2 categorisation are generated.

# %% [markdown]
# ### Importing and pre-processing

# %%
with open("data_setup.py") as file:
    exec(file.read())

with open("free_text_recode.py") as file:
    exec(file.read())

# %%
from matplotlib import pyplot as plt

# Allow display of all outputs (not just the last output) from each cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# %% [markdown]
# ### RQ 6.01 What proportion of survey participants offer repairs, servicing and maintenance to heat pump customers
# - SQ: 42a, 42b
# - Sample: Standard_output (employment type categorisation)

# %%
# Print possible answers
data[col.q42a].value_counts()
data[col.q42b].value_counts()


# %%
from typing import Dict
def condition_q42(x: Dict[str, str]):
    """
    Function to be applied to dataframe which creates a new column
    merging responses from sub-types of the same question.

    Args:
        x: A dictionary-like object representing a single row from a DataFrame.
    """
    
    # Merge responses
    if (x[col.q42a] == "Yes") or (x[col.q42b] == "Yes"):
        return "Yes"
    
    elif (x[col.q42a] == "No, but I intend to offer it in the next 12 months") or (x[col.q42b] == "No, but we intend to offer it in the next 12 months"):
        return "No, but we/I intend to offer it in the next 12 months"
    
    elif (x[col.q42a] == "No, and I do not intend to start offering this service in the next 12 months") or (x[col.q42b] == "No, and we do not intend to start offering this service in the next 12 months"):
        return "No, and we/I do not intend to start offering this service in the next 12 months"
    
    elif (x[col.q42a] == "Don't know") or (x[col.q42b] == "Don't know"):
        return "We/I don't know"
    
    # Check if all are captured
    else:
        return "Flag" 

# Apply function to each row of dataframe
data["SQ42"] = data.apply(condition_q42,
                          axis=1
                          )

# Specifying desired order for outputs
ans_42 = ["Yes",
           "No, but we/I intend to offer it in the next 12 months",
           "No, and we/I do not intend to start offering this service in the next 12 months",
           "We/I don't know",
           "Total"
           ]

# Generate crosstab dataframe
df_601_crosstab = crosstable("EmploymentType",
                             data,
                             "SQ42",
                             ans_42
                             )

# Save to .csv and display

df_601_crosstab.to_csv("../../outputs/section6/csv/601.csv")
df_601_crosstab

# %%
"""
Alternative function formulation suggested in PR review (https://github.com/nestauk/asf_installer_survey/pull/6#discussion_r1587935315)

# Mapping of input values to output values
    response_mapping = {
        "Yes": "Yes",
        "No, but I intend to offer it in the next 12 months": "No, but we/I intend to offer it in the next 12 months",
        "No, and I do not intend to start offering this service in the next 12 months": "No, and we/I do not intend to start offering this service in the next 12 months",
        "Don't know": "We/I don't know"
    }

    # Get the responses for q42a and q42b
    response_a = x[col.q42a]
    response_b = x[col.q42b]

    # Check if the responses are in the mapping
    if response_a in response_mapping:
        return response_mapping[response_a]
    elif response_b in response_mapping:
        return response_mapping[response_b]
    else:
        raise ValueError(f"Unexpected value: {response_a}, {response_b}")
"""

# %%
# Generate figure
groupedbar(df_601_crosstab,
           "601",
           "SQ 42a. & 42b. Do you/the business you work for offer repairs, servicing and maintenance to heat pump customers?"
           )

# %%
# Generate figure
donut(df_601_crosstab,
           "601",
           "SQ 42a. & 42b. Do you/the business you work for offer repairs, servicing and maintenance to heat pump customers?"
           )

# %% [markdown]
# ### RQ 6.02 How does the proportion of survey participants offering repairs, servicing and maintenance differ depending on the size of the company they work for or own?
# - SQ: 42a, 42b
# - Sample:
# - Company_size_owner
# - Company size_employee

# %%
# Generate crosstab dataframe
df_602_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      data,
                                      "SQ42",
                                      ans_42
                                      )

# Save to .csv and display
df_602_crosstab_owner_V2.to_csv("../../outputs/section6/csv/602_owner_V2.csv")
df_602_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_602_crosstab_owner_V2,
           "602_owner_V2",
           "SQ 42a. Do you offer repairs, servicing and maintenance to heat pump customers?"
           )

# %%
# Generate figure
donut(df_602_crosstab_owner_V2,
           "602_owner_V2",
           "SQ 42a. Do you offer repairs, servicing and maintenance to heat pump customers?"
           )

# %%
# Generate crosstab dataframe
df_602_crosstab_employee_V2 = crosstable("CompanySizeEmployeeV2",
                                        data,
                                        "SQ42",
                                        ans_42
                                        )
# Save to .csv and display
df_602_crosstab_employee_V2.to_csv("../../outputs/section6/csv/602_employee_V2.csv")
df_602_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_602_crosstab_employee_V2,
           "602_employee_V2",
           "SQ 42b. Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
           )

# %%
# Generate figure
donut(df_602_crosstab_employee_V2,
           "602_employee_V2",
           "SQ 42b. Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
           )

# %% [markdown]
# ### RQ 6.03 Do survey participants offer heat pump repairs, servicing and maintenance for all heat pump systems, or just ones they’ve installed?
# - SQ: 43a, 43b, 43c
# - Sample: Standard_output

# %%
# Print possible answers
data[col.q43a].value_counts()
data[col.q43b].value_counts()
data[col.q43c].value_counts()

# %%
def condition_q43(x):
    """
    Function to be applied to dataframe which creates a new column
    merging responses from sub-types of the same question.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Merge responses    
    if "Only" in x[col.q43a] or "Only" in x[col.q43b] or "Only" in x[col.q43c]:
        return "Only for heat pump systems that I/my company/the business has installed"
    
    elif "For all" in x[col.q43a] or "For all" in x[col.q43b] or "For all" in x[col.q43c]:
        return "For all heat pump systems, regardless of who originally installed it"
    
    else:
        return None
    
# Apply function to each row of dataframe
data["SQ43"] = data.apply(condition_q43,
                          axis=1
                          )

# Specifying desired order for outputs
ans_43 = ["Only for heat pump systems that I/my company/the business has installed",
        "For all heat pump systems, regardless of who originally installed it",
        "Total"
        ]

# Generate crosstab dataframe
df_603_crosstab = crosstable("EmploymentType",
                                data,
                                "SQ43",
                                ans_43
                                )

# Save to .csv and display
df_603_crosstab.to_csv("../../outputs/section6/csv/603.csv")
df_603_crosstab  

# %%
# Generate figure
groupedbar(df_603_crosstab,
           "603",
           "SQ 43a, 43b & 43c. My business/I/The business I work for offers heat pump repairs, servicing and maintenance:")

# %%
# Generate figure
donut(df_603_crosstab,
           "603",
           "SQ 43a, 43b & 43c. My business/I/The business I work for offers heat pump repairs, servicing and maintenance:")

# %% [markdown]
# ### RQ 6.04 | How does the offer of repairs, servicing and maintenance for all heat pump
# systems or just ones survey participants have installed differ depending on the size
# of the business they work for or own?
# - SQ: 43a, 43b, 43c
# - Sample:
# - Company_size_owner
# - Company size_employee

# %%
# CompanySizeOwner V2
# Generate crosstab dataframe
df_604_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                        data,
                                        "SQ43",
                                        ans_43
                                        )

# Save to .csv and display
df_604_crosstab_owner_V2.to_csv("../../outputs/section6/csv/604_owner_V2.csv")
df_604_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_604_crosstab_owner_V2,
           "604_owner_V2",
           "SQ 43a. & 43b. I/my business offers heat pump repairs, servicing and maintenance:"
           )

# %%
# Generate figure
donut(df_604_crosstab_owner_V2,
           "604_owner_V2",
           "SQ 43a. & 43b. I/my business offers heat pump repairs, servicing and maintenance:"
           )

# %%
# CompanySizeEmployee V2
# Generate crosstab dataframe
df_604_crosstab_employee_V2 = crosstable("CompanySizeEmployeeV2",
                                         data,
                                        "SQ43",
                                        ans_43
                                        )

# Save to .csv and display
df_604_crosstab_employee_V2.to_csv("../../outputs/section6/csv/604_employee_V2.csv")
df_604_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_604_crosstab_employee_V2,
           "604_employee_V2",
           "SQ 43c. The business I work for offers heat pump repairs, servicing and maintenance:"
           )

# %%
# Generate figure
donut(df_604_crosstab_employee_V2,
           "604_employee_V2",
           "SQ 43c. The business I work for offers heat pump repairs, servicing and maintenance:"
           )

# %% [markdown]
# ### RQ 6.05 | Why do survey participants who only offer repairs, servicing and maintenance for heat pump systems they’ve installed choose not to do so for all other systems?
# - SQ: 44a, 44b
# - Sample
# - Standard_output
# <p>
# N.B. Select all that apply type question
# <p>
# Update: Free text responses recoded on 2024-04-17

# %%
# Print possible answers and check counts
data[col.q44a[0]].value_counts()
data[col.q44b[0]].value_counts()

# %%
def transform_44(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Tally occurrence of each answer
    if response in x[col.q44a[0]] or response in x[col.q44b[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_44 = ["Relationship with existing customers",
          "No demand from other customers",
          "Don’t want to take responsibility for other installers’ heat pump installations",
          "I only work on equipment I understand or have been trained in",
          "Only work with certain heat pump models", # re-coded new option
          "Other",
          "Don't know",
          "Total"
          ]

# Create separate dataframe that stacks all answer columns
df_44 = pd.DataFrame()
for n in range(0, len(ans_44) - 1):

    # Create new column for each answer option
    response = ans_44[n]
    new_col = "SQ44Ans" + str(n + 1)
    data[new_col] = data.apply(transform_44, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ44"})
    df_44 = pd.concat([df_44, df])

# Generate crosstab dataframe
df_605_crosstab = crosstable("EmploymentType",
                             df_44,
                             "SQ44",
                             ans_44
                             )
df_605_crosstab = df_605_crosstab.fillna(0)
df_605_crosstab = df_605_crosstab.astype(int)

# Save to .csv and display
df_605_crosstab.to_csv("../../outputs/section6/csv/recoded/605_recoded.csv")
df_605_crosstab

# %%
# Generate figure
groupedbar(df_605_crosstab,
           "605_recoded",
           "SQ 44a. & 44b. Why do you/does the firm you work for only offer repairs, servicing and maintenance only for heat pump systems you have installed?'")

# %%
# Generate figure
donut(df_605_crosstab,
           "605_recoded",
           "SQ 44a. & 44b. Why do you/does the firm you work for only offer repairs, servicing and maintenance only for heat pump systems you have installed?'")

# %% [markdown]
# ### RQ 6.06 | How do the reasons survey participants give for only offering repairs, servicing and maintenance to heat pump systems they’ve installed differ depending on the size of the company they work for or own?
# - SQ: 44a, 44b
# - Sample:
# - Company_size_owner
# - Company size_employee

# %%
# CompanySizeOwner V2
# Create separate dataframe that stacks all answer columns
df_44 = pd.DataFrame()
for n in range(0, len(ans_44) - 1):

    # Create new column for each answer option
    response = ans_44[n]
    new_col = "SQ44Ans"+str(n + 1)
    data[new_col] = data.apply(transform_44, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ44"})
    df_44 = pd.concat([df_44, df])

# Generate crosstab dataframe
df_606_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      df_44,
                                     "SQ44",
                                     ans_44
                                     )
df_606_crosstab_owner_V2 = df_606_crosstab_owner_V2.fillna(0)
df_606_crosstab_owner_V2 = df_606_crosstab_owner_V2.astype(int)

# Save to .csv and display
df_606_crosstab_owner_V2.to_csv("../../outputs/section6/csv/recoded/606_owner_V2_recoded.csv")
df_606_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_606_crosstab_owner_V2,
           "606_owner_V2_recoded",
           "SQ 44a. Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %%
# Generate figure
donut(df_606_crosstab_owner_V2,
           "606_owner_V2_recoded",
           "SQ 44a. Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %%
# CompanySizeEmployee V2
# Create separate dataframe that stacks all answer columns
df_44 = pd.DataFrame()
for n in range(0, len(ans_44) -1 ):

    # Create new column for each answer option
    response = ans_44[n]
    new_col = "SQ44Ans"+str(n + 1)
    data[new_col] = data.apply(transform_44, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeEmployeeV2", new_col])
    df = df.rename(columns={new_col:"SQ44"})
    df_44 = pd.concat([df_44, df])

# Generate crosstab dataframe
df_606_crosstab_employee_V2 = crosstable("CompanySizeEmployeeV2",
                                         df_44,
                                         "SQ44",
                                         ans_44
                                         )
df_606_crosstab_employee_V2 = df_606_crosstab_employee_V2.fillna(0)
df_606_crosstab_employee_V2 = df_606_crosstab_employee_V2.astype(int)

# Save to .csv and display
df_606_crosstab_employee_V2.to_csv("../../outputs/section6/csv/recoded/606_employee_V2_recoded.csv")
df_606_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_606_crosstab_employee_V2,
           "606_employee_V2_recoded",
           "SQ 44b. Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %%
# Generate figure
donut(df_606_crosstab_employee_V2,
           "606_employee_V2_recoded",
           "SQ 44b. Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %% [markdown]
# ### RQ 6.07 | What challenges have survey participants found with working in repairs, servicing and maintenance?
# - SQ: 45
# - Sample:
# - Standard_output
# <p>
# N.B. Select all that apply type question

# %%
# Print possible answers and check counts
data[col.q45[0]].value_counts()

# %%
def transform_45(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Tally occurrence of each answer
    if response in x[col.q45[0]]:
        return response
    else:
        return None
    
# Specifying desired order for outputs
ans_45 = ["Difficult to find the skills you need",
"Low levels of customer demand",
"Hard to make a profit from this work",
"Difficult to fit this work into your work schedule",
"No challenges", # re-coded new option
"Poor original installations", # re-coded new option
"Not enough manufacturer support", # re-coded new option
"Difficulty sourcing components", # re-coded new option
"Other",
"Don't know",
"Total"
]

# Create separate dataframe that stacks all answer columns
df_45 = pd.DataFrame()
for n in range(0, len(ans_45)-1):

    # Create new column for each answer option
    response = ans_45[n]
    new_col = "SQ45Ans"+str(n+1)
    data[new_col] = data.apply(transform_45, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ45"})
    df_45 = pd.concat([df_45, df])

# Generate crosstab dataframe
df_607_crosstab = crosstable("EmploymentType",
                             df_45,
                             "SQ45",
                             ans_45
                             )
df_607_crosstab = df_607_crosstab.fillna(0)
df_607_crosstab = df_607_crosstab.astype(int)

# Remove Employee index row because they are not asked
df_607_crosstab = df_607_crosstab.drop(index='Employee')

# Save to .csv and display
df_607_crosstab.to_csv("../../outputs/section6/csv/recoded/607_recoded.csv")
df_607_crosstab

# %%
# Generate figure
groupedbar(df_607_crosstab,
           "607_recoded",
           "SQ 45. Have you found any challenges working in heat pump repairs, servicing and maintenance?")

# %%
# Generate figure
donut(df_607_crosstab,
           "607_recoded",
           "SQ 45. Have you found any challenges working in heat pump repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.08 | How do the challenges that survey participants find with working in repairs, servicing and maintenance differ depending on the size of the company they own?
# - SQ: 45
# - Sample:
# - Company_size_owner

# %%
# CompanySizeOwner V2
# Create separate dataframe that stacks all answer columns
df_p = pd.DataFrame()
for n in range(0, len(ans_45) - 1):

    # Create new column for each answer option
    response = ans_45[n]
    new_col = "SQ45Ans"+str(n + 1)
    data[new_col] = data.apply(transform_45, axis=1)
    
    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ45"})
    df_p = pd.concat([df_p, df])

# Generate crosstab dataframe
df_608_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      df_p,
                                     "SQ45",
                                     ans_45
                                     )
df_608_crosstab_owner_V2 = df_608_crosstab_owner_V2.fillna(0)
df_608_crosstab_owner_V2 = df_608_crosstab_owner_V2.astype(int)

# Save to .csv and display
df_608_crosstab_owner_V2.to_csv("../../outputs/section6/csv/recoded/608_owner_V2_recoded.csv")
df_608_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_608_crosstab_owner_V2,
           "608_owner_V2_recoded",
           "SQ 45. Have you found any challenges working in heat pump repairs, servicing and maintenance?")

# %%
# Generate figure
donut(df_608_crosstab_owner_V2,
           "608_owner_V2_recoded",
           "SQ 45. Have you found any challenges working in heat pump repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.09 | Do survey participants who currently work in repairs,servicing and maintenance expect to expand this activity?
# - SQ: 46
# - Sample:
# - Standard_output

# %%
# Print possible answers
data[col.q46].value_counts()

# %%
# Change all Not asked to None
data.loc[data[col.q46] == "Not asked", col.q46] = None

# Specifying desired order for outputs
ans_46 = ["Yes",
          "No",
          "Don't know",
          "Total"
          ]

# Generate crosstab dataframe
df_609_crosstab = crosstable("EmploymentType",
                             data,
                             "46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?",
                             ans_46
                             )
df_609_crosstab = df_609_crosstab.fillna(0)
df_609_crosstab = df_609_crosstab.astype(int)

# Remove Employee index row because they are not asked
df_609_crosstab = df_609_crosstab.drop(index='Employee')

# Save to .csv and display
df_609_crosstab.to_csv("../../outputs/section6/csv/609.csv")
df_609_crosstab

# %%
# Generate figure
groupedbar(df_609_crosstab,
           "609",
           "SQ 46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?")

# %%
# Generate figure
donut(df_609_crosstab,
           "609",
           "SQ 46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.10 | How do survey participant expectations of expanding their work in repairs, servicing and maintenance differ depending on the size of the company they own?
# - SQ: 46
# - Sample:
# - Company_size_owner

# %%
# Generate crosstab dataframe
df_610_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      data,
                                     "46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?",
                                     ans_46
                                     )

# Save to .csv and display
df_610_crosstab_owner_V2.to_csv("../../outputs/section6/csv/610_owner_V2.csv")
df_610_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_610_crosstab_owner_V2,
           "610_owner_V2",
           "SQ 46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?")

# %%
# Generate figure
donut(df_610_crosstab_owner_V2,
           "610_owner_V2",
           "SQ 46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.11 | How often do survey participants that work in repairs, servicing, and maintenance identify bad installation practices that negatively affects heat pump performance?
# - SQ: 47
# - Standard_output

# %%
# Print possible answers
data[col.q47].value_counts()

# %%
# Change all Not asked to None
data.loc[data[col.q47] == "Not asked", col.q47] = None

# Specifying desired order for outputs
ans_47 = ["Never",
"Rarely",
"Sometimes",
"Often",
"Always",
"Don't know",
"Total"
]

# Generate crosstab dataframe
df_611_crosstab = crosstable("EmploymentType",
                             data,
                             "47. When doing repairs, servicing or maintenance to installations by other installers, how often do you identify bad installation practice that negatively affects heat pump performance?",
                             ans_47
                             )
df_611_crosstab = df_611_crosstab.fillna(0)
df_611_crosstab = df_611_crosstab.astype(int)

# Remove Employee index row because they are not asked
df_611_crosstab = df_611_crosstab.drop(index='Employee')

# Save to .csv and display
df_611_crosstab.to_csv("../../outputs/section6/csv/611.csv")
df_611_crosstab

# %%
# Generate figure
groupedbar(df_611_crosstab,
           "611",
           "SQ 47. When doing repairs, servicing or maintenance to installations by other installers, how often do you identify bad installation practice that negatively affects heat pump performance?")

# %%
# Generate figure
donut(df_611_crosstab,
           "611",
           "SQ 47. When doing repairs, servicing or maintenance to installations by other installers, how often do you identify bad installation practice that negatively affects heat pump performance?")

# %% [markdown]
# ### RQ 6.12 | Do survey participants who intend to offer repairs, servicing and maintenance intend to do so for all heat pump systems, or just ones they’ve installed?
# - SQ: 48a, 48b, 48c
# - Sample:
# - Standard_output

# %%
# Print possible answers
data[col.q48a].value_counts()
data[col.q48b].value_counts()
data[col.q48c].value_counts()

# %%
def condition_q48(x):
    """
    Function to be applied to dataframe which creates a new column
    merging responses from sub-types of the same question.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Merge responses
    if "Only" in x[col.q48a] or "Only" in x[col.q48b] or "Only" in x[col.q48c]:
        return "Only for heat pump systems that I/my company/the business has installed"
    
    elif "For all" in x[col.q48a] or "For all" in x[col.q48b] or "For all" in x[col.q48c]:
        return "For all heat pump systems, regardless of who originally installed it"
    
    else:
        return None

# Apply function to each row of dataframe
data["SQ48"] = data.apply(condition_q48,
                          axis=1
                          )

# Specifying desired order for outputs
ans_48 = ["Only for heat pump systems that I/my company/the business has installed",
          "For all heat pump systems, regardless of who originally installed it",
          "Total"
          ]

# Generate crosstab dataframe
df_612_crosstab = crosstable("EmploymentType",
                             data,
                             "SQ48",
                             ans_48
                             )

# Save to .csv and display
df_612_crosstab.to_csv("../../outputs/section6/csv/612.csv")
df_612_crosstab

# %%
# Generate figure
groupedbar(df_612_crosstab,
           "612",
           "SQ 48a., 48b. & 48c. I/the business I work for intends to offer heat pump repairs, servicing and maintenance:")

# %%
# Generate figure
donut(df_612_crosstab,
           "612",
           "SQ 48a., 48b. & 48c. I/the business I work for intends to offer heat pump repairs, servicing and maintenance:")

# %% [markdown]
# ### RQ 6.13 | | How does the intention of offering repairs, servicing and maintenance for all heat pump systems or just ones survey participants have installed differ depending on the size of the business they work for or own?
# - SQ: 48a, 48b, 48c
# - Sample:
# - Company_size_owner
# - Company size_employee

# %%
# CompanySizeOwner V2
# Generate crosstab dataframe
df_613_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      data,
                                     "SQ48",
                                     ans_48
                                     )

# Save to .csv and display
df_613_crosstab_owner_V2.to_csv("../../outputs/section6/csv/613_owner_V2.csv")
df_613_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_613_crosstab_owner_V2,
           "613_owner_V2",
           "SQ 48a. & 48b. I intend to offer heat pump repairs, servicing and maintenance:")

# %%
# Generate figure
donut(df_613_crosstab_owner_V2,
           "613_owner_V2",
           "SQ 48a. & 48b. I intend to offer heat pump repairs, servicing and maintenance:")

# %%
# CompanySizeEmployee V2
# Generate crosstab dataframe
df_613_crosstab_employee_V2 = crosstable("CompanySizeEmployeeV2",
                                         data,
                                         "SQ48",
                                         ans_48
                                         )
df_613_crosstab_employee_V2 = df_613_crosstab_employee_V2.fillna(0)
df_613_crosstab_employee_V2 = df_613_crosstab_employee_V2.astype(int)

# Save to .csv and display
df_613_crosstab_employee_V2.to_csv("../../outputs/section6/csv/613_employee_V2.csv")
df_613_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_613_crosstab_employee_V2,
           "613_employee_V2",
           "SQ 48c. The business I work for intends to offer heat pump repairs, servicing and maintenance:")

# %%
# Generate figure
donut(df_613_crosstab_employee_V2,
           "613_employee_V2",
           "SQ 48c. The business I work for intends to offer heat pump repairs, servicing and maintenance:")

# %% [markdown]
# ### RQ 6.14 | Why do survey participants who intend to only offer repairs, servicing and maintenance to heat pump systems they’ve installed not intend to do so for other systems?
# - SQ: 49a, 49b
# - Sample:
# - Standard_output
# <p>
# N.B. Select all that apply type question

# %%
# Print possible answers and check counts
data[col.q49a[0]].value_counts()
data[col.q49b[0]].value_counts()

# %%
def transform_49(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Tally occurrence of each answer
    if response in x[col.q49a[0]] or response in x[col.q49b[0]]:
        return response
    else:
        return 

# Specifying desired order for outputs
ans_49 = ["Relationship with existing customers",
          "No demand from other customers",
          "Don’t want to take responsibility for other installers’ heat pump installations",
          "I only work on equipment I understand or have been trained in",
          "Other",
          "Don't know",
          "Total"
          ]

# Create separate dataframe that stacks all answer columns
df_49 = pd.DataFrame()

for n in range(0, len(ans_49)-1):

    # Create new column for each answer option
    response = ans_49[n]
    new_col = "SQ49Ans"+str(n+1)
    data[new_col] = data.apply(transform_49, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ49"})
    df_49 = pd.concat([df_49, df])

# Generate crosstab dataframe
df_614_crosstab = crosstable("EmploymentType",
                             df_49,
                             "SQ49",
                             ans_49
                             )
df_614_crosstab = df_614_crosstab.fillna(0)
df_614_crosstab = df_614_crosstab.astype(int)

# Save to .csv and display
df_614_crosstab.to_csv("../../outputs/section6/csv/614.csv")
df_614_crosstab

# %%
# Generate figure
groupedbar(df_614_crosstab,
           "614",
           "SQ 49a. & 49b. Why do you/does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %%
# Generate figure
donut(df_614_crosstab,
           "614",
           "SQ 49a. & 49b. Why do you/does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %% [markdown]
# ### RQ 6.15 | How do the reasons survey participants give for only intending to offer repairs, servicing and maintenance to heat pump systems they’ve installed differ depending on the size of the company they work for or own?
# - SQ: 49a, 49b
# - Sample:
# - Company_size_owner
# - Company size_employee
# <p>
# N.B. Select all that apply type question

# %%
# CompanySizeOwner V2
# Create separate dataframe that stacks all answer columns
df_p = pd.DataFrame()
for n in range(0, len(ans_49) - 1):

    # Create new column for each answer option
    response = ans_49[n]
    new_col = "SQ49Ans"+str(n+1)
    data[new_col] = data.apply(transform_49, axis=1)
    
    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ49"})
    df_p = pd.concat([df_p, df])

# Generate crosstab dataframe
df_615_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      df_p,
                                     "SQ49",
                                     ans_49
                                     )
df_615_crosstab_owner_V2 = df_615_crosstab_owner_V2.fillna(0)
df_615_crosstab_owner_V2 = df_615_crosstab_owner_V2.astype(int)

# Save to .csv and display
df_615_crosstab_owner_V2.to_csv("../../outputs/section6/csv/615_owner_V2.csv")
df_615_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_615_crosstab_owner_V2,
           "615_owner_V2",
           "SQ 49a. Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?"
           )

# %%
# Generate figure
donut(df_615_crosstab_owner_V2,
           "615_owner_V2",
           "SQ 49a. Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?"
           )

# %%
# CompanySizeEmployee V2
# Create separate dataframe that stacks all answer columns
df_p = pd.DataFrame()
for n in range(0, len(ans_49)-1):

    # Create new column for each answer option
    response = ans_49[n]
    new_col = "SQ49Ans"+str(n+1)
    data[new_col] = data.apply(transform_49, axis=1)
    
    # Stack columns
    df = data.filter(["CompanySizeEmployeeV2", new_col])
    df = df.rename(columns={new_col:"SQ49"})
    df_p = pd.concat([df_p, df])

# Generate crosstab dataframe
df_615_crosstab_employee_V2 = crosstable("CompanySizeEmployeeV2",
                                         df_p,
                                         "SQ49",
                                         ans_49
                                         )
df_615_crosstab_employee_V2 = df_615_crosstab_employee_V2.fillna(0)
df_615_crosstab_employee_V2 = df_615_crosstab_employee_V2.astype(int)

# Save to .csv and display
df_615_crosstab_employee_V2.to_csv("../../outputs/section6/csv/615_employee_V2.csv")
df_615_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_615_crosstab_employee_V2,
           "615_employee_V2",
           "SQ 49b. Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %%
# Generate figure
donut(df_615_crosstab_employee_V2,
           "615_employee_V2",
           "SQ 49b. Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?")

# %% [markdown]
# ### RQ 6.16 | Why don’t those who only offer, or only intend to offer, repairs, servicing and maintenance to heat pump systems they’ve installed choose not to do so for other systems?
# - SQ: 49a, 49b (intend to offer); 44a, 44b (offer)
# - Sample:
# - Standard_output
# <p>
# N.B. Merging two Select all that apply type crosstab dataframes
# <p>
# Update: Free text responses recoded for df_605_crosstab (SQ44a, 44b) on 2024-04-17

# %%
# Display dataframes to be merged
df_605_crosstab
df_614_crosstab

# %%
# Create new df_614_crosstab with dummy column to match df_605_crosstab
df_614_crosstab_mapped = df_614_crosstab.copy()
df_614_crosstab_mapped["Only work with certain heat pump models"] = 0

# Merge dataframes
# N.B. Need to rename header of columns - SQ44 should be RQ6.16
df_616_crosstab = df_605_crosstab.add(df_614_crosstab_mapped)

# Save to .csv and display
df_616_crosstab.to_csv("../../outputs/section6/csv/recoded/616_recoded.csv")
df_616_crosstab

# %%
# Generate figure
groupedbar(df_616_crosstab,
           "616",
           "RQ 6.16 Why do those who only offer, or only intend to offer, repairs, servicing and maintenance to heat pump systems they’ve installed choose not to do so for other systems?")

# %%
# Generate figure
donut(df_616_crosstab,
           "616",
           "RQ 6.16 Why do those who only offer, or only intend to offer, repairs, servicing and maintenance to heat pump systems they’ve installed choose not to do so for other systems?")

# %% [markdown]
# ### RQ 6.17 | How do the reasons that survey participants give for only offering, or only intending to offer, repairs, servicing and maintenance to heat pump systems they’ve installed (but not for all other systems) differ depending on the size of the company they work for or own?
# - SQ: 49a, 49b (intend to offer); 44a, 44b (offer)
# - Sample:
# - Company_size_owner
# - Company size_employee
# <p>
# N.B. Merging two Select all that apply type crosstab dataframes
# <p>
# Update: Free text responses recoded for df_605_crosstab (SQ44a, 44b) on 2024-04-17

# %%
# CompanySizeOwner V2
# Display dataframes to be merged
df_606_crosstab_owner_V2
df_615_crosstab_owner_V2

# %%
# CompanySizeOwner V2
# Create new df_615_crosstab_owner_V2 with dummy column to match df_606_crosstab_owner_V2
df_615_crosstab_owner_V2_mapped = df_615_crosstab_owner_V2.copy()
df_615_crosstab_owner_V2_mapped["Only work with certain heat pump models"] = 0

# Merge dataframes
# N.B. Need to rename header of columns - SQ44 should be RQ6.17
df_617_crosstab_owner_V2 = df_606_crosstab_owner_V2.add(df_615_crosstab_owner_V2_mapped)

# Save to .csv and display
df_617_crosstab_owner_V2.to_csv("../../outputs/section6/csv/recoded/617_owner_V2_recoded.csv")
df_617_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_617_crosstab_owner_V2,
           "617_owner_V2",
           "RQ 6.17 How do the reasons that survey participants give for only offering, or only intending to offer, repairs, servicing and maintenance to heat pump systems they’ve installed (but not for all other systems) differ depending on the size of the company they work for or own?")

# %%
# Generate figure
donut(df_617_crosstab_owner_V2,
           "617_owner_V2",
           "RQ 6.17 How do the reasons that survey participants give for only offering, or only intending to offer, repairs, servicing and maintenance to heat pump systems they’ve installed (but not for all other systems) differ depending on the size of the company they work for or own?")

# %%
# CompanySizeEmployee V2
# Display dataframes to be merged
df_606_crosstab_employee_V2
df_615_crosstab_employee_V2

# %%
# CompanySizeEmployee V2
# Create new df_615_crosstab_crosstab_employee_V2 with dummy column to match df_606_crosstab_employee_V2
df_615_crosstab_employee_V2_mapped = df_615_crosstab_employee_V2.copy()
df_615_crosstab_employee_V2_mapped["Only work with certain heat pump models"] = 0

# Merge dataframes
# N.B. Need to rename header of columns - SQ44 should be RQ6.17
df_617_crosstab_employee_V2 = df_606_crosstab_employee_V2.add(df_615_crosstab_employee_V2_mapped)

# Save to .csv and display
df_617_crosstab_employee_V2.to_csv("../../outputs/section6/csv/recoded/617_employee_V2_recoded.csv")
df_617_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_617_crosstab_employee_V2,
           "617_employee_V2",
           "RQ 6.17 How do the reasons that survey participants give for only offering, or only intending to offer, repairs, servicing and maintenance to heat pump systems they’ve installed (but not for all other systems) differ depending on the size of the company they work for or own?")

# %%
# Generate figure
donut(df_617_crosstab_employee_V2,
           "617_employee_V2",
           "RQ 6.17 How do the reasons that survey participants give for only offering, or only intending to offer, repairs, servicing and maintenance to heat pump systems they’ve installed (but not for all other systems) differ depending on the size of the company they work for or own?")

# %% [markdown]
# ### Q 6.18 | Why haven’t survey participants that intend on offering heat pump repairs, servicing and maintenance not done so thus far?
# - SQ: 50
# - Sample:
# - Standard_output
# <p>
# - N.B. Employees don’t answer this question AND this is a Select all that apply type question
# <p>
# Update: Free text responses recoded on 2024-04-18

# %%
# Print possible answers and check counts
data[col.q50[0]].value_counts()

# %%
def transform_50(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Tally occurrence of each answer
    if response in x[col.q50[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_50 = ["Too little demand from customers",
          "Not profitable enough",
          "Lack the necessary skills and expertise",
          "Hard to fit into work schedule",
          "The manufacturer does it",
          "Other",
          "Don't know",
          "Total"
          ]
    
# Create separate dataframe that stacks all answer columns
df_50 = pd.DataFrame()
for n in range(0, len(ans_50) - 1):

    # Create new column for each answer option
    response = ans_50[n]
    new_col = "SQ50Ans"+str(n + 1)
    data[new_col] = data.apply(transform_50, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ50"})
    df_50 = pd.concat([df_50, df])

# Generate crosstab dataframe
df_618_crosstab = crosstable("EmploymentType",
                             df_50,
                            "SQ50",
                            ans_50
                            )
df_618_crosstab = df_618_crosstab.fillna(0)
df_618_crosstab = df_618_crosstab.astype(int)

# Save to .csv and display
df_618_crosstab.to_csv("../../outputs/section6/csv/recoded/618_recoded.csv")
df_618_crosstab

# %%
# Generate crosstab dataframe
groupedbar(df_618_crosstab,
           "618",
           "SQ 50. Why have you previously not offered repairs, servicing and maintenance?")

# %%
# Generate crosstab dataframe
donut(df_618_crosstab,
           "618",
           "SQ 50. Why have you previously not offered repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.19 | How do the reasons that survey participants give for not offering heat pump repairs, servicing and maintenance thus far (despite intending to do so) differ depending on the size of the company they own?
# - SQ: 50
# - Sample:
# - Company_size_owner
# <p>
# N.B. Employees don’t answer this question AND this is a Select all that apply type question
# <p>
# Update: Free text responses recoded on 2024-04-18

# %%
# CompanySizeOwner V2
# Create separate dataframe that stacks all answer columns
df_50 = pd.DataFrame()
for n in range(0, len(ans_50) - 1):

    # Create new column for each answer option
    response = ans_50[n]
    new_col = "SQ50Ans"+str(n+1)
    data[new_col] = data.apply(transform_50, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ50"})
    df_50 = pd.concat([df_50, df])

# Generate crosstab dataframe
df_619_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      df_50,
                                     "SQ50",
                                     ans_50
                                     )
df_619_crosstab_owner_V2 = df_619_crosstab_owner_V2.fillna(0)
df_619_crosstab_owner_V2 = df_619_crosstab_owner_V2.astype(int)

# Save to .csv and display
df_619_crosstab_owner_V2.to_csv("../../outputs/section6/csv/recoded/619_owner_V2_recoded.csv")
df_619_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_619_crosstab_owner_V2,
           "619",
           "SQ 50. Why have you previously not offered repairs, servicing and maintenance?")

# %%
# Generate figure
donut(df_619_crosstab_owner_V2,
           "619",
           "SQ 50. Why have you previously not offered repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.20 | Why do survey participants that intend on offering heat pump repairs, servicing and maintenance plan on moving into the space?
# - SQ: 51
# - Sample:
# - Standard_output
# <p>
# N.B. Employees don’t answer this question AND this is a Select all that apply type question

# %%
# Print possible answers and check counts
data[col.q51[0]].value_counts()

# %%
def transform_51(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Tally occurrence of each answer
    if response in x[col.q51[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_51 = ["Growing demand from customers",
          "Servicing is increasingly profitable work",
          "Now have access to the relevant skills and expertise",
          "Issues getting the manufacturer to sort problems or visit homes",
          "Other",
          "Don't know",
          "Total"
          ]
    
# Create separate dataframe that stacks all answer columns
df_51 = pd.DataFrame()
for n in range(0, len(ans_51)-1):

    # Create new column for each answer option
    response = ans_51[n]
    new_col = "SQ51Ans"+str(n+1)
    data[new_col] = data.apply(transform_51, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ51"})
    df_51 = pd.concat([df_51, df])

# Generate crosstab dataframe
df_620_crosstab = crosstable("EmploymentType",
                             df_51,
                             "SQ51",
                             ans_51
                             )
df_620_crosstab = df_620_crosstab.fillna(0)
df_620_crosstab = df_620_crosstab.astype(int)

# Save to .csv and display
df_620_crosstab.to_csv("../../outputs/section6/csv/620.csv")
df_620_crosstab

# %%
# Generate crosstab dataframe
groupedbar(df_620_crosstab,
           "620",
           "SQ 51. Why do you now intend to move into heat pump repairs, servicing and maintenance?")

# %%
# Generate crosstab dataframe
donut(df_620_crosstab,
           "620",
           "SQ 51. Why do you now intend to move into heat pump repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.21 | How do the reasons that survey participants give for intending to move into heat pump repairs, servicing and maintenance differ depending on the size of the company they own?
# - SQ: 51
# - Sample:
# - Company_size_owner
# <p>
# N.B. Employees don’t answer this question AND this is a Select all that apply type question

# %%
# CompanySizeOwner V2
# Create separate dataframe that stacks all answer columns
df_51 = pd.DataFrame()
for n in range(0, len(ans_51)-1):

    # Create new column for each answer option
    response = ans_51[n]
    new_col = "SQ51Ans"+str(n+1)
    data[new_col] = data.apply(transform_51, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ51"})
    df_51 = pd.concat([df_51, df])

# Generate crosstab dataframe
df_621_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      df_51,
                                     "SQ51",
                                     ans_51
                                     )
df_621_crosstab_owner_V2 = df_621_crosstab_owner_V2.fillna(0)
df_621_crosstab_owner_V2 = df_621_crosstab_owner_V2.astype(int)

# Save to .csv and display
df_621_crosstab_owner_V2.to_csv("../../outputs/section6/csv/621_owner_V2.csv")
df_621_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_621_crosstab_owner_V2,
           "621",
           "SQ 51. Why do you now intend to move into heat pump repairs, servicing and maintenance?")

# %%
# Generate figure
donut(df_621_crosstab_owner_V2,
           "621",
           "SQ 51. Why do you now intend to move into heat pump repairs, servicing and maintenance?")

# %% [markdown]
# ### RQ 6.22 | Why don’t survey participants want to offer, repairs, servicing and maintenance at all?
# - SQ: 52a, 52b
# - Sample:
# - Standard_output
# <p>
# N.B. Select all that apply type question

# %%
# Print possible answers and check counts
data[col.q52a[0]].value_counts()
data[col.q52b[0]].value_counts()

# %%
def transform_52(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Tally occurrence of each answer    
    if response in x[col.q52a[0]] or response in x[col.q52b[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_52 = ["Too little demand from customers",
          "Not profitable enough",
          "Lack the necessary skills and expertise",
          "The manufacturer does it",
          "It’s difficult to manage / schedule",
          "Inadequate or slow support from manufacturers",
          "Other",
          "Don't know",
          "Total"
          ]

# Create separate dataframe that stacks all answer columns
df_52 = pd.DataFrame()
for n in range(0, len(ans_52)-1):

    # Create new column for each answer option
    response = ans_52[n]
    new_col = "SQ52Ans"+str(n+1)
    data[new_col] = data.apply(transform_52, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ52"})
    df_52 = pd.concat([df_52, df])

# Generate crosstab dataframe
df_622_crosstab = crosstable("EmploymentType",
                             df_52,
                             "SQ52",
                             ans_52
                             )
df_622_crosstab = df_622_crosstab.fillna(0)
df_622_crosstab = df_622_crosstab.astype(int)

# Save to .csv and display
df_622_crosstab.to_csv("../../outputs/section6/csv/622.csv")
df_622_crosstab

# %%
# Generate figure
groupedbar(df_622_crosstab,
           "622",
           "SQ 52a. & 52b. Why don’t you/the business you work for currently offer repairs, servicing and maintenance to customers?")

# %%
# Generate figure
donut(df_622_crosstab,
           "622",
           "SQ 52a. & 52b. Why don’t you/the business you work for currently offer repairs, servicing and maintenance to customers?")

# %% [markdown]
# ### RQ 6.23 | How do the reasons why survey participants don’t want to offer repairs,servicing and maintenance at all differ depending on the size of the company they work for or own.
# - SQ: 52a, 52b
# - Sample:
# - Company_size_owner
# - Company size_employee
# <p>
# N.B. Select all that apply type question

# %%
# CompanySizeOwner V2
# Create separate dataframe that stacks all answer columns
df_52 = pd.DataFrame()
for n in range(0, len(ans_52) - 1):

    # Create new column for each answer option
    response = ans_52[n]
    new_col = "SQ52Ans"+str(n + 1)
    data[new_col] = data.apply(transform_52, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ52"})
    df_52 = pd.concat([df_52, df])

# Generate crosstab dataframe
df_623_crosstab_owner_V2 = crosstable("CompanySizeOwnerV2",
                                      df_52,
                                     "SQ52",
                                     ans_52
                                     )
df_623_crosstab_owner_V2 = df_623_crosstab_owner_V2.fillna(0)
df_623_crosstab_owner_V2 = df_623_crosstab_owner_V2.astype(int)

# Save to .csv and display
df_623_crosstab_owner_V2.to_csv("../../outputs/section6/csv/623_owner_V2.csv")
df_623_crosstab_owner_V2

# %%
# Generate figure
groupedbar(df_623_crosstab_owner_V2,
           "623_owner_V2",
           "SQ 52a. Why don’t you currently offer repairs, servicing and maintenance to customers?")

# %%
# Generate figure
donut(df_623_crosstab_owner_V2,
           "623_owner_V2",
           "SQ 52a. Why don’t you currently offer repairs, servicing and maintenance to customers?")

# %%
# CompanySizeEmployee V2
# Create separate dataframe that stacks all answer columns
df_52 = pd.DataFrame()
for n in range(0, len(ans_52) - 1):

    # Create new column for each answer option
    response = ans_52[n]
    new_col = "SQ52Ans"+str(n+1)
    data[new_col] = data.apply(transform_52, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeEmployeeV2", new_col])
    df = df.rename(columns={new_col:"SQ52"})
    df_52 = pd.concat([df_52, df])

# Generate crosstab dataframe
df_623_crosstab_employee_V2 = crosstable("CompanySizeEmployeeV2",
                                         df_52,
                                         "SQ52",
                                         ans_52
                                         )
df_623_crosstab_employee_V2 = df_623_crosstab_employee_V2.fillna(0)
df_623_crosstab_employee_V2 = df_623_crosstab_employee_V2.astype(int)

# Save to .csv and display
df_623_crosstab_employee_V2.to_csv("../../outputs/section6/csv/623_employee_V2.csv")
df_623_crosstab_employee_V2

# %%
# Generate figure
groupedbar(df_623_crosstab_employee_V2,
           "623_employee_V2",
           "SQ 52b. Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?")

# %%
# Generate figure
donut(df_623_crosstab_employee_V2,
            "623_employee_V2",
           "SQ 52b. Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?")

# %% [markdown]
# ### RQ 6.24 | Why don’t survey participants offer repairs, servicing and maintenance (including those who are intending to do so in the next 12 months)?
# - SQ: 50, 52a, 52b
# - Merging the responses from two very similar questions: one which is asked to
# those who intend (but don’t currently) offer repairs, servicing and
# maintenance, and one for those who don’t intend to.
# - Sample:
# - Standard_output
# <p>
# N.B. Merging two Select all that apply type crosstab dataframes
# <p>
# Update: Free text responses recoded for df_618_crosstab on 2024-04-18

# %%
# Display dataframes to be merged
df_618_crosstab
df_622_crosstab

# %%
# Create new df_618_crosstab with dummy column to match df_622_crosstab
df_618_crosstab_mapped = df_618_crosstab.copy()
df_618_crosstab_mapped["Inadequate or slow support from manufacturers"] = 0

# Create new df_622_crosstab with renamed response to match df_618_crosstab
df_622_crosstab_mapped = df_622_crosstab.rename(columns={"It’s difficult to manage / schedule":"Hard to fit into work schedule"})

# Merge dataframes
df_624_crosstab = df_618_crosstab_mapped.add(df_622_crosstab_mapped)

# Save to .csv and display
df_624_crosstab.to_csv("../../outputs/section6/csv/recoded/624_recoded.csv")
df_624_crosstab

# %%
# Generate figure
groupedbar(df_624_crosstab,
           "624",
           "RQ 6.24 Why don’t survey participants offer repairs, servicing and maintenance (including those who are intending to do so in the next 12 months)?")

# %%
# Generate figure
donut(df_624_crosstab,
           "624",
           "RQ 6.24 Why don’t survey participants offer repairs, servicing and maintenance (including those who are intending to do so in the next 12 months)?")

# %% [markdown]
# ### RQ 6.25 | How do the reasons survey participants give for not offering repairs, servicing and maintenance (including those that intend to do so in the next 12 months) differ depending on the size of the company they work for or own?
# - SQ: 50, 52a, 52b
# - Merging the responses from two very similar questions: one which is asked to
# those who intend (but don’t currently) offer repairs, servicing and
# maintenance, and one for those who don’t intend to.
# - Sample:
# - Company_size_owner
# - Company size_employee
# <p>
# N.B. Merging two Select all that apply type crosstab dataframes
# <p>
# Update: Free text responses recoded for df_618_crosstab on 2024-04-18

# %%
# CompanySizeOwner V2
# Display dataframes to be merged
df_619_crosstab_owner_V2
df_623_crosstab_owner_V2

# %%
# Create new df_619_crosstab_owner_V2 with dummy column to match df_623_crosstab_owner_V2
df_619_crosstab_owner_V2_mapped = df_619_crosstab_owner_V2.copy()
df_619_crosstab_owner_V2_mapped["Inadequate or slow support from manufacturers"] = 0

# Create new df_623_crosstab with renamed response to match df_619_crosstab
df_623_crosstab_owner_V2_mapped = df_623_crosstab_owner_V2.rename(columns={"It’s difficult to manage / schedule":"Hard to fit into work schedule"})

# Merge dataframes
df_625_crosstab = df_619_crosstab_owner_V2_mapped.add(df_623_crosstab_owner_V2_mapped)

# Save to .csv and display
df_625_crosstab.to_csv("../../outputs/section6/csv/recoded/625_owner_V2_recoded.csv")
df_625_crosstab

# %%
# Generate figure
groupedbar(df_625_crosstab,
           "625_owner_V2",
           "RQ 6.25 How do the reasons survey participants give for not offering repairs, servicing and maintenance (including those that intend to do so in the next 12 months) differ depending on the size of the company they work for or own?")

# %%
# Generate figure
donut(df_625_crosstab,
           "625_owner_V2",
           "RQ 6.25 How do the reasons survey participants give for not offering repairs, servicing and maintenance (including those that intend to do so in the next 12 months) differ depending on the size of the company they work for or own?")


