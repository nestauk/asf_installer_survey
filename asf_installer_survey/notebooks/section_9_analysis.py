# %% [markdown]
# ## Section 9: Apprenticeships and entry level installer roles
# **Aims:** Generating outputs for Section 9 (RQs 9.01 - 9.26) as planned in [Heat Pump Installer Survey data analysis plan](https://docs.google.com/document/d/1M1nzdf3fyTjipmaKJKViin0EB3e3R1afOQglwMGJaII/edit#heading=h.jzmlm8j0kyve)<br>
# **Author:** Elysia Lucas<br>
# **Date:** 2024-04-19<br>

# %% [markdown]
# ### Importing and pre-processing

# %%
with open("data_setup.py") as file:
    exec(file.read())

with open("free_text_recode.py") as file:
    exec(file.read())

# %%
from matplotlib import pyplot as plt

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# %% [markdown]
# ### RQ 9.01 | What proportion of survey participants currently employs an apprentice who works on heat pump installations, or has done so in the last 12 months?
# - SQ 80
# - Sample:
# - Standard_output
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201

# %%
# Print possible answers
data[col.q80].value_counts()

# %%
# Convert "Not asked" to None
data.loc[data[col.q80] == "Not asked", col.q80] = None

# Specify desired order
ans_80 = ["Yes",
          "No, but I intend on doing so in the next 12 months",
          "No, and I do not intend to do so in the next 12 months",
          "Total"
          ]

# Generate crosstable
df_901 = crosstable("EmploymentType",
                    data,
                    col.q80,
                    ans_80
                    )
df_901 = df_901.fillna(0)
df_901 = df_901.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_901 = df_901.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_901.to_csv("../../outputs/section9/csv/901.csv")
df_901

# Generate figure
groupedbar(df_901,
           "901",
           str(col.q80),
           "section9"
           )

# %%
donut(df_901,
      "901",
     str(col.q80),
     "section9"
     )

# %% [markdown]
# ### RQ 9.02 | How does the number of survey participants who’ve employed an apprentice who works on heat pump installations in the last 12 months differ depending on the length of time they’ve been in the sector?
# - SQ 80
# - Sample:
# - Standard_output
# - Broken down by SQ 4
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201

# %%
# Length of time in sector
# Generate crosstab dataframe
df_902 = crosstable("SectorTime",
                    data,
                    col.q80,
                    ans_80
                    )
df_902 = df_902.fillna(0)
df_902 = df_902.astype(int)

# Save to .csv and display
df_902.to_csv("../../outputs/section9/csv/902.csv")
df_902

# Generate figure
groupedbar(df_902,
           "902_trans",
           str(col.q80),
           "section9"
           )

# %%
df_902 = df_902.transpose()
# Generate figure - transposed version
groupedbar(df_902,
           "902_trans",
           str(col.q80),
           "section9"
           )

# %% [markdown]
# ### RQ 9.03 | How does the number of survey participants who’ve employed an apprentice who works on heat pump installations in the last 12 months differ depending on the size of the company they own?
# - SQ 80
# - Sample:
# - Company_size_owner
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201

# %%
# CompanySizeOwnerV2
# Generate crosstab dataframe
df_903_owner = crosstable("CompanySizeOwnerV2",
                          data,
                          col.q80,
                          ans_80
                          )
df_903_owner = df_903_owner.fillna(0)
df_903_owner = df_903_owner.astype(int)

# Save to .csv and display
df_903_owner.to_csv("../../outputs/section9/csv/903_owner.csv")
df_903_owner

# Generate figure
groupedbar(df_903_owner,
           "903_owner",
           str(col.q80),
           "section9"
           )

# %% [markdown]
# ### RQ 9.04 | How does the number of survey participants who’ve employed an apprentice who works on heat pump installations in the last 12 months differ depending on their business location?
# - SQ 80
# - Sample:
# - Standard_output
# - Broken down by:
# - Q8 - Where is your company located? (Select all that apply)
# - Q9a. 9b, 9c, 9d - In which English/Scottish/Welsh/Northern Irish region/county is your company located?
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201

# %%
df_904_counts = data[[col.q8, col.q80]].copy()
df_904_counts = df_904_counts.dropna()
df_904_counts[col.q8].value_counts().to_frame()

# %%
# Generate crosstable
df_904_stacked, df_904 = location_crosstab(col.q80)

# Save to .csv and display
df_904.to_csv("../../outputs/section9/csv/904.csv")
df_904

# %% [markdown]
# ### RQ 9.05 | How does the number of survey participants who’ve employed an apprentice who works on heat pump installations in the last 12 months differ depending on the number of installations they’ve done in the last 12 months?
# - SQ 80
# - Sample:
# - Standard_output
# - Broken down by Q37 ("NumberInstalls")
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Number of installs
# Generate crosstab dataframe
df_905 = crosstable("NumberInstalls",
                    data,
                    col.q80,
                    ans_80
                    )
df_905 = df_905.fillna(0)
df_905 = df_905.astype(int)

# Save to .csv and display
df_905.to_csv("../../outputs/section9/csv/905.csv")
df_905

# Generate figure
groupedbar(df_905,
           "905",
           str(col.q80),
           "section9"
           )

# %% [markdown]
# ### RQ 9.06 | How does the number of survey participants who’ve employed an apprentice who works on heat pump installations in the last 12 months differ depending on their intention to install more heat pumps?
# - SQ 80
# - Sample:
# - Standard_output
# - Broken down by Q38
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Desired increase in installs
# Generate crosstab dataframe
df_906 = crosstable("DesiredIncrease",
                    data,
                    col.q80,
                    ans_80
                    )
df_906 = df_906.fillna(0)
df_906 = df_906.astype(int)

# Save to .csv and display
df_906.to_csv("../../outputs/section9/csv/906.csv")
df_906

# Generate figure
groupedbar(df_906,
           "906",
           col.q80,
           "section9"
           )

# %%
df_906 = df_906.transpose()
# Generate figure
groupedbar(df_906,
           "906_trans",
           col.q80,
           "section9"
           )

# %% [markdown]
# ### RQ 9.07 | What challenges have survey participants who’ve taken on an apprentice to work on heat pumps faced?
# - SQ 81
# - Sample:
# - Standard_output
# <p>
# Asked if answered "Yes" to SQ 80 -> N = 78 (company owners = 72, sole traders = 6)
# <p>
# N.B. This is a Select all that apply type question

# %%
# Print possible answers
data[col.q81[0]].value_counts()

# %%
# Count checks
n_1 = 0
n_2 = 0
n_3 = 0
for x in data[col.q81[0]]:
    if len(x) == 1:
        n_1 = n_1 + 1
    elif len(x) == 2:
       n_2 = n_2 + 1
    elif len(x) == 3:
        n_3 = n_3 + 1
    else:
        pass
print("One answer: "+ str(n_1),
      "Two answers: "+ str(n_2),
      "Three answers: "+ str(n_3)
      )

print("Total: " + str((n_1) + n_2 + n_3))

# %%
def transform_81(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Tally occurrence of each answer
    if response in x[col.q81[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_81 = ["It was hard to find the right apprentice to fit with the role",
          "I didn’t know where to recruit an apprentice from",
          "There are no colleges delivering apprenticeship training of a high enough quality near me",
          "There were no colleges delivering relevant apprenticeship training near me",
          "Having an apprentice has slowed down my work",
          "Having an apprentice has cost my business too much",
          "It took too long to recruit an apprentice",
          "I needed more guidance on how to properly support an apprentice in their work",
          "I needed more guidance on the administration associated with working with an apprentice",
          "I don’t face any challenges",
          "Other",
          "Total"
          ]

# Create separate dataframe that stacks all answer columns
df_81 = pd.DataFrame()
for n in range(0, len(ans_81) - 1):

    # Create new column for each answer option
    response = ans_81[n]
    new_col = "SQ81Ans"+str(n + 1)
    data[new_col] = data.apply(transform_81, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ81"})
    df_81 = pd.concat([df_81, df])

# Generate crosstab dataframe
df_907 = crosstable("EmploymentType",
                             df_81,
                            "SQ81",
                            ans_81
                            )
df_907 = df_907.fillna(0)
df_907 = df_907.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_907 = df_907.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_907.to_csv("../../outputs/section9/csv/907.csv")
df_907


# %% [markdown]
# ### RQ 9.08 | How do the challenges that survey participants who’ve taken on an apprentice to work on heat pumps differ depending on the length of time they’ve been in the sector?
# - SQ 81
# - Sample:
# - Standard_output
# - Broken down by SQ 4
# <p>
# Asked if answered "Yes" to SQ 80 -> N = 78
# <p>
# N.B. This is a Select all that apply type question

# %%
# Checking counts
# Generate crosstable
df_908_count = crosstable("SectorTime",
                    data,
                    col.q80,
                    ans_80
                    )
df_908_count = df_908_count.fillna(0)
df_908_count = df_908_count.astype(int)

# Save to .csv and display
df_908_count.to_csv("../../outputs/section9/csv/908_count.csv")
df_908_count

# %%
# Create separate dataframe that stacks all answer columns
df_81 = pd.DataFrame()
for n in range(0, len(ans_81) - 1):

    # Create new column for each answer option
    response = ans_81[n]
    new_col = "SQ81Ans"+str(n + 1)
    data[new_col] = data.apply(transform_81, axis=1)

    # Stack columns
    df = data.filter(["SectorTime", new_col])
    df = df.rename(columns={new_col:"SQ81"})
    df_81 = pd.concat([df_81, df])

# Generate crosstab dataframe
df_908 = crosstable("SectorTime",
                             df_81,
                            "SQ81",
                            ans_81
                            )
df_908 = df_908.fillna(0)
df_908 = df_908.astype(int)

# Save to .csv and display
df_908.to_csv("../../outputs/section9/csv/908.csv")
df_908


# %% [markdown]
# ### RQ 9.09 | How do the challenges that survey participants who’ve taken on an apprentice to work on heat pumps differ depending on the size of the company they own?
# - SQ 81
# - Sample:
# - Company_size_owner
# <p>
# Asked if answered "Yes" to SQ 80 -> N = 78
# <p>
# N.B. This is a Select all that apply type question

# %%
# Checking counts
# Generate crosstable
df_909_count = crosstable("CompanySizeOwnerV2",
                    data,
                    col.q80,
                    ans_80
                    )
df_909_count = df_909_count.fillna(0)
df_909_count = df_909_count.astype(int)

# Save to .csv and display
df_909_count.to_csv("../../outputs/section9/csv/909_count.csv")
df_909_count

# %%
# Create separate dataframe that stacks all answer columns
df_81 = pd.DataFrame()
for n in range(0, len(ans_81) - 1):

    # Create new column for each answer option
    response = ans_81[n]
    new_col = "SQ81Ans"+str(n + 1)
    data[new_col] = data.apply(transform_81, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ81"})
    df_81 = pd.concat([df_81, df])

# Generate crosstab dataframe
df_909 = crosstable("CompanySizeOwnerV2",
                             df_81,
                            "SQ81",
                            ans_81
                            )
df_909 = df_909.fillna(0)
df_909 = df_909.astype(int)

# Save to .csv and display
df_909.to_csv("../../outputs/section9/csv/909.csv")
df_909


# %% [markdown]
# ### RQ 9.10 | What challenges do survey participants who haven’t taken on an apprentice to work on heat pumps foresee with doing so?
# - SQ 82
# - Sample:
# - Standard_output
# <p>
# Asked if answered "No, but I intend on doing so in the next 12 months" to SQ 80 -> n = 45 (company owners = 36, sole traders = 9)<br>
# OR<br>
# if answered "No, and I do not intend to do so in the next 12 months" to SQ 80 -> n = 78 (company owners = 55, sole traders = 23)<br>
# Total N = 123
# <p>
# N.B. This is a Select all that apply type question

# %%
# Print possible answers
question_82 = explode_select_all(data.loc[:, col.q82[0]])
print(question_82.sum())
print(question_82.sum().sum())

# %%
def transform_82(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Tally occurrence of each answer
    if response in x[col.q82[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_82 = ["It’s hard to find the right apprentice to fit with the role",
          "I don’t know where to recruit an apprentice from",
          "There are no colleges delivering relevant apprenticeship training near me",
          "There’s no colleges delivering apprenticeship training of a high enough quality near me",
          "Having an apprentice will slow down my work",
          "Having an apprentice will cost my business too much",
          "It takes too long to recruit an apprentice",
          "I need more guidance on how to properly support an apprentice in their work",
          "I need more guidance on the administration associated with working with an apprentice",
          "Other",
          "I don’t forsee any challenges",
          "Total"
          ]

# Create separate dataframe that stacks all answer columns
df_82 = pd.DataFrame()
for n in range(0, len(ans_82) - 1):

    # Create new column for each answer option
    response = ans_82[n]
    new_col = "SQ82Ans"+str(n + 1)
    data[new_col] = data.apply(transform_82, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ82"})
    df_82 = pd.concat([df_82, df])

# Generate crosstab dataframe
df_910 = crosstable("EmploymentType",
                             df_82,
                            "SQ82",
                            ans_82
                            )
df_910 = df_910.fillna(0)
df_910 = df_910.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_910 = df_910.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_910.to_csv("../../outputs/section9/csv/910.csv")
df_910


# %% [markdown]
# ### RQ 9.11 | How do the foreseen challenges that survey participants who haven’t taken on an apprentice to work on heat pumps differ depending on the length of time they’ve been in the sector?
# - SQ 82
# - Sample:
# - Standard_output
#     - Broken down by SQ 4
# <p>
# Asked if answered "No, but I intend on doing so in the next 12 months" to SQ 80 -> n = 45 (company owners = 36, sole traders = 9)<br>
# OR<br>
# if answered "No, and I do not intend to do so in the next 12 months" to SQ 80 -> n = 78 (company owners = 55, sole traders = 23)<br>
# Total N = 123
# <p>
# N.B. This is a Select all that apply type question

# %%
# Checking counts
# Generate crosstable
df_911_count = crosstable("SectorTime",
                    data,
                    col.q80,
                    ans_80
                    )
df_911_count = df_911_count.fillna(0)
df_911_count = df_911_count.astype(int)

# Save to .csv and display
df_911_count.to_csv("../../outputs/section9/csv/911_count.csv")
df_911_count

# %%
# Create separate dataframe that stacks all answer columns
df_82 = pd.DataFrame()
for n in range(0, len(ans_82) - 1):

    # Create new column for each answer option
    response = ans_82[n]
    new_col = "SQ82Ans"+str(n + 1)
    data[new_col] = data.apply(transform_82, axis=1)

    # Stack columns
    df = data.filter(["SectorTime", new_col])
    df = df.rename(columns={new_col:"SQ82"})
    df_82 = pd.concat([df_82, df])

# Generate crosstab dataframe
df_911 = crosstable("SectorTime",
                             df_82,
                            "SQ82",
                            ans_82
                            )
df_911 = df_911.fillna(0)
df_911 = df_911.astype(int)

# Save to .csv and display
df_911.to_csv("../../outputs/section9/csv/911.csv")
df_911

# %% [markdown]
# ### RQ 9.12 | How do the foreseen challenges that survey participants who haven’t taken on an apprentice to work on heat pumps differ depending on the size of the company they own?
# - SQ 82
# - Sample:
# - Company_size_owner
# <p>
# Asked if answered "No, but I intend on doing so in the next 12 months" to SQ 80 -> n = 45 (company owners = 36, sole traders = 9)<br>
# OR<br>
# if answered "No, and I do not intend to do so in the next 12 months" to SQ 80 -> n = 78 (company owners = 55, sole traders = 23)<br>
# Total N = 123
# <p>
# N.B. This is a Select all that apply type question

# %%
# Create separate dataframe that stacks all answer columns
df_82 = pd.DataFrame()
for n in range(0, len(ans_82) - 1):

    # Create new column for each answer option
    response = ans_82[n]
    new_col = "SQ82Ans"+str(n + 1)
    data[new_col] = data.apply(transform_82, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ82"})
    df_82 = pd.concat([df_82, df])

# Generate crosstab dataframe
df_912 = crosstable("CompanySizeOwnerV2",
                             df_82,
                            "SQ82",
                            ans_82
                            )
df_912 = df_912.fillna(0)
df_912 = df_912.astype(int)

# Save to .csv and display
df_912.to_csv("../../outputs/section9/csv/912.csv")
df_912

# %% [markdown]
# ### RQ 9.13 | How confident are survey participants that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work with them?
# - SQ 83
# - Sample:
# - Standard_output
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Print possible answers
data[col.q83].value_counts()

# %%
# Convert "Not asked" to None
data.loc[data[col.q83] == "Not asked", col.q83] = None

# Specify desired order
ans_83 = ["Not at all confident",
          "Not very confident",
          "Somewhat confident",
          "Confident",
          "Very confident",
          "Don't know",
          "Total"
          ]

# Generate crosstable
df_913 = crosstable("EmploymentType",
                    data,
                    col.q83,
                    ans_83
                    )
df_913 = df_913.fillna(0)
df_913 = df_913.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_913 = df_913.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_913.to_csv("../../outputs/section9/csv/913.csv")
df_913

# %% [markdown]
# ### RQ 9.14 | What skills would survey participants prioritise when recruiting a recent graduate from an apprenticeship scheme?
# - SQ 84
# - Sample:
# - Standard_output
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# <p>
# N.B. This is a Select all that apply type question
# 

# %%
# Print possible answers
question_84 = explode_select_all(data.loc[:, col.q84[0]])
print(question_84.sum())
print(question_84.sum().sum())

# %%
# Count checks
n_1 = 0
n_2 = 0
n_3 = 0
for x in data[col.q84[0]]:
    if len(x) == 1:
        n_1 = n_1 + 1
    elif len(x) == 2:
       n_2 = n_2 + 1
    elif len(x) == 3:
        n_3 = n_3 + 1
    else:
        pass
print("One answer: "+ str(n_1),
      "Two answers: "+ str(n_2),
      "Three answers: "+ str(n_3)
      )

print("Total: " + str((n_1) + n_2 + n_3))

# %%
def transform_84(x):
    """
    Function to be applied to dataframe which separates answers selected
    by creating an individual tally column for each possible answer. 

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Tally occurrence of each answer
    if response in x[col.q84[0]]:
        return response
    else:
        return None

# Specifying desired order for outputs
ans_84 = ["Ability to do complete heat loss calculations and surveys",
          "Ability to design heat pump systems",
          "Ability to do a satisfactory install unaccompanied (with a check at the end)",
          "Ability to do individual elements of an install unaccompanied (with a check between each part)",
          "Admin and paperwork related to the project they’re working on",
          "Customer service",
          "Quotes and sales",
          "Other",
          "Other-not relevant",
          "Don’t know",
          "Total"
          ]

# Create separate dataframe that stacks all answer columns
df_84 = pd.DataFrame()
for n in range(0, len(ans_84) - 1):

    # Create new column for each answer option
    response = ans_84[n]
    new_col = "SQ84Ans"+str(n + 1)
    data[new_col] = data.apply(transform_84, axis=1)

    # Stack columns
    df = data.filter(["EmploymentType", new_col])
    df = df.rename(columns={new_col:"SQ84"})
    df_84 = pd.concat([df_84, df])

# Generate crosstab dataframe
df_914 = crosstable("EmploymentType",
                             df_84,
                            "SQ84",
                            ans_84
                            )
df_914 = df_914.fillna(0)
df_914 = df_914.astype(int)

# Save to .csv and display
df_914.to_csv("../../outputs/section9/csv/914.csv")
df_914

# %% [markdown]
# ### RQ 9.15 | How do the skills that survey participants would prioritise when recruiting a recent graduate from an apprenticeship scheme differ depending on the size of company they own?
# - SQ 84
# - Sample:
# - Company_size_owner
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# <p>
# N.B. This is a Select all that apply type question
# 

# %%
# Create separate dataframe that stacks all answer columns
df_84 = pd.DataFrame()
for n in range(0, len(ans_84) - 1):

    # Create new column for each answer option
    response = ans_84[n]
    new_col = "SQ84Ans"+str(n + 1)
    data[new_col] = data.apply(transform_84, axis=1)

    # Stack columns
    df = data.filter(["CompanySizeOwnerV2", new_col])
    df = df.rename(columns={new_col:"SQ84"})
    df_84 = pd.concat([df_84, df])

# Generate crosstab dataframe
df_915 = crosstable("CompanySizeOwnerV2",
                             df_84,
                            "SQ84",
                            ans_84
                            )
df_915 = df_915.fillna(0)
df_915 = df_915.astype(int)

# Save to .csv and display
df_915.to_csv("../../outputs/section9/csv/915.csv")
df_915

# %% [markdown]
# ### RQ 9.16 | What do survey participants think could be most improved from the training that plumbing and heating apprentices receive?
# - SQ 85
# - Sample:
# - Standard_output
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Print possible answers
data[col.q85[0]].value_counts()

# %%
# Convert "Not asked" to None
data.loc[data[col.q85[0]] == "Not asked", col.q85[0]] = None

# Specify desired order
ans_85 = ["Practical general plumbing skills",
          "Theoretical general plumbing knowledge",
          "Practical skills specifically in heat pump installation",
          "Theoretical skills specifically in heat pump installation",
          "General knowledge in heating system design",
          "Specific knowledge in low temperature heating system design",
          "Specific knowledge related to ground source heat pump installation",
          "Ability to do accurate heat loss calculations",
          "Customer service and communication skills",
          "Business and sales skills",
          "Knowledge of equality and diversity",
          "Knowledge of health and safety",
          "Other",
          "Don't know",
          "Total"
          ]

# Generate crosstable
df_916 = crosstable("EmploymentType",
                    data,
                    col.q85[0],
                    ans_85
                    )
df_916 = df_916.fillna(0)
df_916 = df_916.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_916 = df_916.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_916.to_csv("../../outputs/section9/csv/916.csv")
df_916

# %% [markdown]
# ### RQ 9.17 | How likely would survey participants be to take on candidates with paper qualifications but no practical or vocational experience in the field?
# - SQ 86
# - Sample:
# - Standard_output
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# <p>
# Collapsed categories:
# 
# - Unlikely <- Very unlikely; Unlikely
# - Neutral <- Neutral
# - Likely <- Likely; Very likely
# 

# %%
# Print possible answers
data[col.q86].value_counts()

# %% [markdown]
# **Non-collapsed version**

# %%
# Convert "Not asked" to None
data.loc[data[col.q86] == "Not asked", col.q86] = None

# Specify desired order
ans_86 = ["Very unlikely",
          "Unlikely",
          "Neutral",
          "Likely",
          "Very likely",
          "Don't know",
          "Total"
          ]

# Generate crosstable
df_917_uncollapsed = crosstable("EmploymentType",
                    data,
                    col.q86,
                    ans_86
                    )
df_917_uncollapsed = df_917_uncollapsed.fillna(0)
df_917_uncollapsed = df_917_uncollapsed.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_917_uncollapsed = df_917_uncollapsed.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_917_uncollapsed.to_csv("../../outputs/section9/csv/917_uncollapsed.csv")
df_917_uncollapsed

# %% [markdown]
# **Collapsed version**

# %%
def condition_q86(x):
    """
    Function to be applied to dataframe which creates a new column
    merging responses from sub-types of the same question.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Merge responses
    if (x[col.q86] == "Very unlikely") or (x[col.q86] == "Unlikely"):
        return "Unlikely"
    
    elif (x[col.q86] == "Neutral"):
        return "Neutral"
    
    elif (x[col.q86] == "Very likely") or (x[col.q86] == "Likely"):
        return "Likely"
    
    elif(x[col.q86] == "Don't know"):
        return "Don't know"
    
    else:
        return None

# Apply function to each row of dataframe
data["SQ86"] = data.apply(condition_q86,
                          axis=1
                          )

# Specifying desired order for outputs
ans_86_collapsed = ["Unlikely",
          "Neutral",
          "Likely",
          "Don't know",
          "Total"
          ]

# Generate crosstab dataframe
df_917_collapsed = crosstable("EmploymentType",
                             data,
                             "SQ86",
                             ans_86_collapsed
                             )
df_917_collapsed = df_917_collapsed.fillna(0)
df_917_collapsed = df_917_collapsed.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_917_collapsed = df_917_collapsed.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_917_collapsed.to_csv("../../outputs/section9/csv/917_collapsed.csv")
df_917_collapsed


# %% [markdown]
# ### RQ 9.18 | How does the likelihood of survey participants taking on candidates with paper qualifications but no practical or vocational experience in the field differ depending on the size of company they own?
# - SQ 86
# - Sample:
# - Company_size_owner
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# <p>
# Collapsed categories:
# 
# - Unlikely <- Very unlikely; Unlikely
# - Neutral <- Neutral
# - Likely <- Likely; Very likely
# 

# %% [markdown]
# **Non-collapsed version**

# %%
# Convert "Not asked" to None
data.loc[data[col.q86] == "Not asked", col.q86] = None

# Specify desired order
ans_86 = ["Very unlikely",
          "Unlikely",
          "Neutral",
          "Likely",
          "Very likely",
          "Don't know",
          "Total"
          ]

# Generate crosstable
df_918_uncollapsed = crosstable("CompanySizeOwnerV2",
                    data,
                    col.q86,
                    ans_86
                    )
df_918_uncollapsed = df_918_uncollapsed.fillna(0)
df_918_uncollapsed = df_918_uncollapsed.astype(int)

# Save to .csv and display
df_918_uncollapsed.to_csv("../../outputs/section9/csv/918_uncollapsed.csv")
df_918_uncollapsed

# %% [markdown]
# **Collapsed version**

# %%
# Generate crosstab dataframe
df_918_collapsed = crosstable("EmploymentType",
                             data,
                             "SQ86",
                             ans_86_collapsed
                             )
df_918_collapsed = df_918_collapsed.fillna(0)
df_918_collapsed = df_918_collapsed.astype(int)

# Save to .csv and display
df_918_collapsed.to_csv("../../outputs/section9/csv/918_collapsed.csv")
df_918_collapsed

# %% [markdown]
# ### RQ 9.19 | What are the most common reasons why survey participants may take on someone with vocational experience over paper qualifications?
# - SQ 87
# - Sample:
# - Standard_output
# 
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Convert "Not asked" to None
data.loc[data[col.q87[0]] == "Not asked", col.q87[0]] = None

# Specify desired order
ans_87 = ["Shows commitment to the job",
          "I would be more confident in their ability to do the job",
          "I would save time on training them",
          "I would save money on training them",
          "Other",
          "I see no advantages",
          "Total"
          ]

# Generate crosstable
df_919 = crosstable("EmploymentType",
                    data,
                    col.q87[0],
                    ans_87
                    )
df_919 = df_919.fillna(0)
df_919 = df_919.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_919 = df_919.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_919.to_csv("../../outputs/section9/csv/919.csv")
df_919

# %% [markdown]
# ### RQ 9.20 | How do the reasons that survey participants might take on someone with vocational experience over paper qualifications differ depending on the size of the company they own?
# - SQ 87
# - Sample:
# - Company_size_owner
# 
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Generate crosstable
df_920 = crosstable("CompanySizeOwnerV2",
                    data,
                    col.q87[0],
                    ans_87
                    )
df_920 = df_920.fillna(0)
df_920 = df_920.astype(int)

# Save to .csv and display
df_920.to_csv("../../outputs/section9/csv/920.csv")
df_920

# %% [markdown]
# ### RQ 9.21 | What are the most common reasons why survey participants might choose to take on someone with only paper qualifications?
# - SQ 88
# - Sample:
# - Standard_output
# 
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Print possible answers
data[col.q88[0]].value_counts()

# %%
# Convert "Not asked" to None
data.loc[data[col.q88[0]] == "Not asked", col.q88[0]] = None

# Specify desired order
ans_88 = ["There is a shortage of staff with practical experience to recruit",
          "I prefer to train my own staff to get the training right",
          "It is cheaper",
          "I have a personal recommendation as to the quality of this candidate",
          "Other",
          "I would not choose to take on such a person",
          "Total"
          ]

# Generate crosstable
df_921 = crosstable("EmploymentType",
                    data,
                    col.q88[0],
                    ans_88
                    )
df_921 = df_921.fillna(0)
df_921 = df_921.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_921 = df_921.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_921.to_csv("../../outputs/section9/csv/921.csv")
df_921

# %% [markdown]
# ### RQ 9.22 | How do the reasons why survey participants might choose to take on someone with only paper qualifications differ depending on the size of the company they own?
# - SQ 88
# - Sample:
# - Company_size_owner
# 
# <p>
# Only asked company owners (n = 163) and sole traders (n = 38) -> N = 201
# 

# %%
# Generate crosstable
df_922 = crosstable("CompanySizeOwnerV2",
                    data,
                    col.q88[0],
                    ans_88
                    )
df_922 = df_922.fillna(0)
df_922 = df_922.astype(int)

# Save to .csv and display
df_922.to_csv("../../outputs/section9/csv/922.csv")
df_922

# %% [markdown]
# ### RQ 9.23 | What might further encourage survey participants that are likely to take on candidates with paper qualifications but no practical or vocational experience in the field to take on someone with only paper qualifications?
# - SQ 89a
# - Sample:
# - Standard_output
# 
# <p>
# Of company owners and sole traders who were asked SQ 86: 89a was asked if they answered "Very likely" (n=5) or "Likely" (n=9) -> N = 14
# 

# %%
df_917_uncollapsed

# %%
# Print possible answers
data[col.q89a[0]].value_counts()

# %%
# Convert "Not asked" to None
data.loc[data[col.q89a[0]] == "Not asked", col.q89a[0]] = None

# Specify desired order
ans_89 = ["Financial support for salary for a limited period",
          "Financial support for onboarding costs",
          "Financial support for training",
          "Certainty that the person will work with my company for a defined period",
          "Other",
          "I would not choose to take on such a person",
          "Total"
          ]

# Generate crosstable
df_923 = crosstable("EmploymentType",
                    data,
                    col.q89a[0],
                    ans_89
                    )
df_923 = df_923.fillna(0)
df_923 = df_923.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_923 = df_923.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_923.to_csv("../../outputs/section9/csv/923.csv")
df_923

# %% [markdown]
# ### RQ 9.24 | What might encourage survey participants that are unlikely to take on candidates with paper qualifications but no practical or vocational experience in the field to take on someone of that nature?
# - SQ 89b
# - Sample:
# - Standard_output
# 
# <p>
# Of company owners and sole traders who were asked SQ 86: 89b was asked if they answered "Neutral" (n=50), "Unlikely (n=57) or "Very unlikely" (n=77) -> N = 184
# 

# %%
# Print possible answers
data[col.q89b[0]].value_counts()

# %%
# Convert "Not asked" to None
data.loc[data[col.q89b[0]] == "Not asked", col.q89b[0]] = None

# Specify desired order
ans_89 = ["Financial support for salary for a limited period",
          "Financial support for onboarding costs",
          "Financial support for training",
          "Certainty that the person will work with my company for a defined period",
          "Other",
          "Other-not relevant",
          "I would not choose to take on such a person",
          "Total"
          ]

# Generate crosstable
df_924 = crosstable("EmploymentType",
                    data,
                    col.q89b[0],
                    ans_89
                    )
df_924 = df_924.fillna(0)
df_924 = df_924.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_924 = df_924.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_924.to_csv("../../outputs/section9/csv/924.csv")
df_924

# %% [markdown]
# ### RQ 9.25 | Overall, what might most encourage survey participants to take on someone with only paper qualifications?
# - SQ 89a, 89b
# - Sample:
# - Standard_output
# 

# %%
def condition_q89(x):
    """
    Function to be applied to dataframe which creates a new column
    merging responses from sub-types of the same question.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """

    # Merge responses

    if (x[col.q89a[0]] == "Financial support for salary for a limited period") or (x[col.q89b[0]] == "Financial support for salary for a limited period"):
        return "Financial support for salary for a limited period"
    
    elif (x[col.q89a[0]] == "Financial support for onboarding costs") or (x[col.q89b[0]] == "Financial support for onboarding costs"):
        return "Financial support for onboarding costs"
    
    elif (x[col.q89a[0]] == "Financial support for training") or (x[col.q89b[0]] == "Financial support for training"):
        return "Financial support for training"
    
    elif (x[col.q89a[0]] == "Certainty that the person will work with my company for a defined period") or (x[col.q89b[0]] == "Certainty that the person will work with my company for a defined period"):
        return "Certainty that the person will work with my company for a defined period"
    
    elif (x[col.q89a[0]] == "Other") or (x[col.q89b[0]] == "Other"):
        return "Other"
    
    elif (x[col.q89a[0]] == "Other-not relevant") or (x[col.q89b[0]] == "Other-not relevant"):
        return "Other-not relevant"

    elif (x[col.q89a[0]] == "I would not choose to take on such a person") or (x[col.q89b[0]] == "I would not choose to take on such a person"):
        return "I would not choose to take on such a person"
    
    else:
        return None

# Apply function to each row of dataframe
data["SQ89"] = data.apply(condition_q89,
                          axis=1
                          )

# Specifying desired order for outputs
ans_89 = ["Financial support for salary for a limited period",
          "Financial support for onboarding costs",
          "Financial support for training",
          "Certainty that the person will work with my company for a defined period",
          "Other",
          "Other-not relevant",
          "I would not choose to take on such a person",
          "Total"
          ]

# Generate crosstab dataframe
df_925 = crosstable("EmploymentType",
                             data,
                             "SQ89",
                             ans_89
                             )
df_925 = df_925.fillna(0)
df_925 = df_925.astype(int)

# Remove Contractors and Employees index rows because they are not asked
df_925 = df_925.drop(index=['Employee', 'Contractor'])

# Save to .csv and display
df_925.to_csv("../../outputs/section9/csv/925.csv")
df_925

# %% [markdown]
# ### RQ 9.26 | How do the factors that might encourage survey participants to take on someone with only paper qualifications differ depending on the size of the company they own?
# - SQ 89a, 89b
# - Sample:
# - Company_size_owner
# 

# %%
# Generate crosstab dataframe
df_926 = crosstable("CompanySizeOwnerV2",
                             data,
                             "SQ89",
                             ans_89
                             )
df_926 = df_926.fillna(0)
df_926 = df_926.astype(int)

# Save to .csv and display
df_926.to_csv("../../outputs/section9/csv/926.csv")
df_926


