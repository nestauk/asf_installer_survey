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
# ### Re-coding free text 'Other' responses 
# **Aim:** Address free text responses to <i>Select all that apply</i> type questions by re-writing them as a new/existing answer or keep as 'Other'<br>
# **Author:** Elysia Lucas<br>
# **Date:** 2024-04-17<br>
# <br>
# Responses are recoded as outlined in the [Free responses re-coding](#https://docs.google.com/document/d/1wWXNAikUtgrT_ZY3pCLF1FIVBt-FlYToVygo8Apk6Ok/edit#heading=h.4bf7bxjgagav) document.
#

# %%
with open("data_setup.py") as file:
    exec(file.read())


# %% [markdown]
# ### Functions

# %%
def get_index(recode):
    """
    Function to create dictionary where
    key is response ID and value is dataframe index.

    Args:
        recode: List of response IDs to be recoded
    
    Returns:
        response[id]: dictionary {id:index}
    """

    # %run data_setup.py
    # Get row indices
    indices = []
    for id in recode:
        i = data.index[data[col.q0a]==id]
        indices.append(i)

    # Map lists in dictionary
    return {recode[i]: indices[i] for i in range(len(recode))}


# %% [markdown]
# ### Section 6

# %% [markdown]
# #### SQ44a and SQ44b
# Affected RQs:
# * 6.05
# * 6.06
# * 6.16
# * 6.17

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [641,
          759,
          781,
          824
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q44b[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q44b[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Only work with certain heat pump models"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q44b[0]] = "Only work with certain heat pump models"

# %% [markdown]
# #### SQ45 (Company owners, sole traders and contractors only)
# Affected RQs:
# * 6.07
# * 6.08

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [630,
          741,
          779
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q45[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q45[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "No challenges"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q45[0]] = "No challenges"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [79,
          192,
          287,
          529,
          554
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q45[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q45[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Poor original installations"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q45[0]] = "Poor original installations"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [198,
          328,
          413,
          463,
          532,
          535
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q45[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q45[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Not enough manufacturer support"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q45[0]] = "Not enough manufacturer support"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [106,
          145,
          624
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q45[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q45[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Difficulty sourcing components"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q45[0]] = "Difficulty sourcing components"

 # %%
 ## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [345,
          677
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q45[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q45[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Difficult to find the skills you need" in i:
            ans_old = data.loc[response[id], col.q45[0]].tolist()[0]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.loc[response[id], col.q45[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "Difficult to find the skills you need"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q45[0]] = "Difficult to find the skills you need"

# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [415,
          810
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q45[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q45[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Low levels of customer demand" in i:
            ans_old = data.loc[response[id], col.q45[0]].tolist()[0]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.loc[response[id], col.q45[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "Low levels of customer demand"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q45[0]] = "Low levels of customer demand"

# %% [markdown]
# #### SQ50
# Affected RQs:
# * 6.18
# * 6.19
# * 6.24
# * 6.25

# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [496
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q50[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q50[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Lack the necessary skills and expertise" in i:
            ans_old = data.loc[response[id], col.q50[0]].tolist()[0]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.loc[response[id], col.q50[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "Lack the necessary skills and expertise"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q50[0]] = "Lack the necessary skills and expertise"

# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [264,
          160
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q50[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q50[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Too little demand from customers" in i:
            ans_old = data.loc[response[id], col.q50[0]].tolist()[0]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.loc[response[id], col.q50[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "Too little demand from customers"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q50[0]] = "Too little demand from customers"

# %% [markdown]
# #### SQ60a
# Affected RQs:
# * 7.80
# * 7.81
# * 7.82
# * 7.83

# %%
## NEW OPTION AND SINGLE CHOICE ONLY
# Response IDs responses to be recoded
recode = [410,
          451
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Add new category
data[col.q60a[0]] = data[col.q60a[0]].cat.add_categories("I haven't done any installations")

# Re-write responses
for id in recode:
    data.loc[response[id], col.q60a[0]] = "I haven't done any installations"

# %% [markdown]
# #### SQ70
# Affected RQs:
# * 7.84
# * 7.85
# * 7.86
# * 7.87

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [763,
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

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q70[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q70[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Easy MCS"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q70[0]] = "Easy MCS"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [331,
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

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q70[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q70[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Evergreen"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q70[0]] = "Evergreen"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [79,
          621,
          788,
          750
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q70[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q70[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "H2x"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q70[0]] = "H2x"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [115,
          129,
          144,
          574,
          287,
          619,
          821
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q70[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q70[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Heatpunk"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q70[0]] = "Heatpunk"

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [345,
          613,
          664
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q70[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q70[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "I don't use design software"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id], col.q70[0]] = "I don't use design software"

# %% [markdown]
# #### SQ81
# Affected RQs:
# * 9.07
# * 9.08
# * 9.09

# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [417
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q81[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q81[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Having an apprentice has cost my business too much" in i:
            ans_old = data.at[response[id].item(), col.q81[0]]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.at[response[id].item(), col.q81[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "Having an apprentice has cost my business too much"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id].item(), col.q81[0]] = np.array([["Having an apprentice has cost my business too much"]])


# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [176
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q81[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q81[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "It was hard to find the right apprentice to fit with the role" in i:
            ans_old = data.at[response[id].item(), col.q81[0]]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.at[response[id].item(), col.q81[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "It was hard to find the right apprentice to fit with the role"

    # Re-coding if only 'Other' is selected
    else:
        data.loc[response[id].item(), col.q81[0]] = np.array([["It was hard to find the right apprentice to fit with the role"]])


# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [325,
          346,
          755
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q81[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q81[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "There are no colleges delivering apprenticeship training of a high enough quality near me" in i:
            ans_old = data.at[response[id].item(), col.q81[0]]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.at[response[id].item(), col.q81[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0][0]] = "There are no colleges delivering apprenticeship training of a high enough quality near me"

    # Re-coding if only 'Other' is selected
    else:
        data.at[response[id].item(), col.q81[0]] = np.array([["There are no colleges delivering apprenticeship training of a high enough quality near me"]])


# %% [markdown]
# #### SQ84
# Affected RQs:
# * 9.14
# * 9.15

# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [352
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q84[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q84[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Ability to do individual elements of an install unaccompanied (with a check between each part)" in i:
            ans_old = data.loc[response[id], col.q84[0]].tolist()[0]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.at[response[id].item(), col.q84[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0]] = "Ability to do individual elements of an install unaccompanied (with a check between each part)"

    # Re-coding if only 'Other' is selected
    else:
        data.at[response[id].item(), col.q84[0]] = ["Ability to do individual elements of an install unaccompanied (with a check between each part)"]

# %%
## EXISTING OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [328
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q84[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q84[0]].tolist()[0]

        # Avoiding double counting if re-coded option already selected
        if "Ability to do a satisfactory install unaccompanied (with a check at the end)" in i:
            ans_old = data.loc[response[id], col.q84[0]].tolist()[0]
            ans_new = ans_old.tolist()
            ans_new.remove("Other")
            data.at[response[id].item(), col.q84[0]] = ans_new
        
        else:
            i[np.where(i == 'Other')[0]] = "Ability to do a satisfactory install unaccompanied (with a check at the end)"

    # Re-coding if only 'Other' is selected
    else:
        data.at[response[id].item(), col.q84[0]] = ["Ability to do a satisfactory install unaccompanied (with a check at the end)"]

# %%
## NEW OPTION AND SELECT ALL THAT APPLY TYPE QUESTION
# Response IDs responses to be recoded
recode = [141,
          198
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:

    # Re-coding if 'Other' is selected AND other option(s)
    if len(data.loc[response[id], col.q84[0]].tolist()[0]) > 1:
        i = data.loc[response[id], col.q84[0]].tolist()[0]
        i[np.where(i == 'Other')[0][0]] = "Other-not relevant"

    # Re-coding if only 'Other' is selected
    else:
        data.at[response[id].item(), col.q84[0]] = ["Other-not relevant"]

# %% [markdown]
# #### SQ87
# Affected RQs:
# * 9.19
# * 9.20
# * 9.21

# %%
## EXISTING OPTION AND SINGLE CHOICE ONLY
# Response IDs responses to be recoded
recode = [417,
          726
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:
    data.loc[response[id], col.q87[0]] = "Shows commitment to the job"

# %%
## EXISTING OPTION AND SINGLE CHOICE ONLY
# Response IDs responses to be recoded
recode = [141,
          198,
          345,
          489,
          516
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:
    data.loc[response[id], col.q87[0]] = "I would be more confident in their ability to do the job"

# %% [markdown]
# #### SQ89b
# Affected RQs:
# * 9.24
# * 9.25
# * 9.26

# %%
## EXISTING OPTION AND SINGLE CHOICE ONLY
# Response IDs responses to be recoded
recode = [198
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Re-write responses
for id in recode:
    data.loc[response[id], col.q89b[0]] = "I would not choose to take on such a person"

# %%
## NEW OPTION AND SINGLE CHOICE ONLY
# Response IDs responses to be recoded
recode = [141,
          366
          ]

# Create dictionary {response ID:dataframe index}
response = get_index(recode)

# Add new category
data[col.q89b[0]] = data[col.q89b[0]].cat.add_categories("Other-not relevant")

# Re-write responses
for id in recode:
    data.loc[response[id], col.q89b[0]] = "Other-not relevant"
