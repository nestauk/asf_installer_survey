# %% [markdown]
# ### Data setup and pre-processing
# **Aims:** (1) Processing installer survey results dataset and including only analytical sample. (2) Defining categories for sub-populations.<br>
# **Author:** Elysia Lucas<br>
# **Date:** 2024-04-04<br>
# <br>
# **Outline:**
# * Importing packages and data
# * Populating analytical sample
# * Sub-population outputs
# * Functions to generate figures
# 

# %% [markdown]
# #### Importing packages and data

# %%
# Importing packages
import pandas as pd
import nbformat
import numpy as np
from matplotlib import pyplot as plt
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Import questions from lookups class
import sys
sys.path.insert(0,"..")
from utils.lookups import QuestionNumbers as col

# %%
# Load data

data_path_parquet = """/mnt/g/Shared drives/A Sustainable Future/1. Reducing household emissions/\
2. Projects Research Work/36. Installer survey/05 survey data/20240201_Installer_survey_clean_data_anonymised.parquet"""

# To retrieve locally from /asf-installer-survey/data folder:
# data_path_parquet = "../data/20240201_Installer_survey_clean_data_anonymised.parquet"

data = pd.read_parquet(data_path_parquet, engine = 'pyarrow')

# Dataset info
data.info()

# Status of raw dataset
(
    data[col.q0d]
    .value_counts()
    .to_frame()
    .assign(proportion=lambda df: (df["count"] / df["count"].sum() * 100).round(1))
)

# %% [markdown]
# #### Populating analytical sample

# %%
# Populating analytical sample using exclusion criteria 
# (if 0e. Analytical Sample = True)
data = data.loc[lambda df: df[col.q0e] == True, :]

# Status after exclusion
(
    data[col.q0d]
    .value_counts()
    .to_frame()
    .assign(proportion=lambda df: (df["count"] / df["count"].sum() * 100).round(1))
)

# Reset index
data = data.reset_index(drop=True)

# %% [markdown]
# #### Creating sub-populations

# %% [markdown]
# <b>What this section does:</b><br>
# Adds new columns to the dataframe categorising each response by different sub-population types.<br>
# Categorisation is determined as outlined in the 'Pre-analysis: Recurring sub-populations and “outputs"' section in the [Heat Pump Installer Survey data analysis plan](https://docs.google.com/document/d/1M1nzdf3fyTjipmaKJKViin0EB3e3R1afOQglwMGJaII/edit#heading=h.voghu12g248q) document.

# %%
# Create dictionary to store lists specifying desired order
order_dict = {}

# %% [markdown]
# ##### Employment type
# - Sole trader = Answered “The owner or co-owner of a firm” to SQ 5 AND “I'm a sole trader” to SQ 6a
# - Company owner = Answered "The owner or co-owner of a firm” to SQ 5 AND anything other than “I'm a sole trader” to SQ 6a
# - Contractor = Answered "A contractor or freelancer” to SQ 5
# - Employee = Answered "An employee of a firm"

# %%
def condition_employment_type(x):
    """
    Function to be applied to dataframe which creates a new column categorising the employment type of each response.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    
    Returns:
        Dataframe x with new categorisation column.

    """
    
    # Categorising sole traders
    if (x[col.q5] == "The owner or co-owner of a firm") and (x[col.q6a] == "I’m a sole trader"):
        return "Sole trader"
    
    # Categorising company owners
    elif (x[col.q5] == "The owner or co-owner of a firm") and (x[col.q6a] != "I’m a sole trader"):
        return "Company owner"
    
    # Categorising contractors
    elif (x[col.q5] == "A contractor or freelancer"):
        return "Contractor"
    
    # Categorising employees
    else:
        return "Employee"

category = "EmploymentType"

# Apply function to each row of dataframe
data[category] = data.apply(condition_employment_type, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["Company owner",
        "Contractor",
        "Employee",
        "Sole trader",
        "Total"
        ]
order_dict.update({category:order})

# Summary of EmploymentType column
data[category].value_counts()

# %% [markdown]
# ##### Sizes of companies owned
# N.B. There are two versions of the categorisation criteria. As of 11.04.2024, only outputs with version 2 categorisation are generated.

# %% [markdown]
# **Version 1 of collapsed categories**

# %%
def condition_company_size_owner_v1(x):
    """
    Function to be applied to dataframe which creates a new column categorising the company size of each respondent.
    Using Version 1 of categorisation.

    Args:
        x: pandas dataframe containing responses from analytical sample.

    Returns:
        Dataframe x with new categorisation column.

    """
    if (x[col.q6a] == "I’m a sole trader"):
        return "Sole trader"
    
    elif (x[col.q6a] == "I own a company with 5 or fewer employees"):
        return "Small"
    
    elif (x[col.q6a] == "I own a company with 6-25 employees"):
        return "Medium"
    
    elif (x[col.q6a] == "I own a company with 26-100 employees") or (x[col.q6a] == "I own a company with over 100 employees"):
        return "Large"
    
    else:
        return None
    
category = "CompanySizeOwnerV1"

# Apply function to each row of dataframe
data[category] = data.apply(condition_company_size_owner_v1, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["Sole trader",
        "Small",
        "Medium",
        "Large",
        "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# **Version 2 of collapsed categories**

# %%
def condition_company_size_owner_v2(x):
    """
    Function to be applied to dataframe which creates a new column categorising the company size owned by company owners or sole traders.
    Using Version 2 of categorisation.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    
    """
    if (x[col.q6a] == "I’m a sole trader"):
        return "Sole trader"
    
    elif (x[col.q6a] == "I own a company with 5 or fewer employees"):
        return "Small"
    
    elif (x[col.q6a] == "I own a company with 6-25 employees") or (x[col.q6a] == "I own a company with 26-100 employees") or (x[col.q6a] == "I own a company with over 100 employees"):
        return "Medium and large"
    
    else:
        return None
    
category = "CompanySizeOwnerV2"

# Apply function to each row of dataframe
data[category] = data.apply(condition_company_size_owner_v2, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["Sole trader",
        "Small",
        "Medium and large",
        "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# ##### Size of company (employees)
# 
# N.B. There are two versions of the categorisation criteria. As of 11.04.2024, only outputs with version 2 categorisation are generated.)

# %% [markdown]
# **Version 1 of collapsed categories**

# %%
def condition_company_size_employee_v1(x):
    """
    Function to be applied to dataframe which creates a new column categorising the company size of employees.
    Using Version 1 of categorisation.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    
    """
    if (x[col.q6b] == "Don't know"):
        return "Don't know"
    
    elif (x[col.q6b] == "I work for a company with 5 or fewer employees"):
        return "5 or fewer"
    
    elif (x[col.q6b] == "I work for a company with 6-25 employees"):
        return "6-25"
    
    elif (x[col.q6b] == "I work for a company with 26-100 employees"):
        return "26-100"
    
    elif (x[col.q6b] == "I work for a company with over 100 employees"):
        return "Over 100"
    
    else:
        return None
    
category = "CompanySizeEmployeeV1"

# Apply function to each row of dataframe
data[category] = data.apply(condition_company_size_employee_v1, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["5 or fewer",
        "6-25",
        "26-100",
        "Over 100",
        "Don't know",
        "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# **Version 2 of collapsed categories**

# %%
def condition_company_size_employee_v2(x):
    """
    Function to be applied to dataframe which creates a new column categorising the company size of employees.
    Using Version 2 of categorisation.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    
    """
    if (x[col.q6b] == "Don't know"):
        return "Don't know"
    
    elif (x[col.q6b] == "I work for a company with 5 or fewer employees") or (x[col.q6b] == "I work for a company with 6-25 employees"):
        return "25 or fewer"
    
    elif (x[col.q6b] == "I work for a company with 26-100 employees") or (x[col.q6b] == "I work for a company with over 100 employees"):
        return "Over 25"
    
    else:
        return None
    
category = "CompanySizeEmployeeV2"

# Apply function to each row of dataframe
data[category] = data.apply(condition_company_size_employee_v2, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["25 or fewer",
        "Over 25",
        "Don't know",
        "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# ##### Length of time in the heat pump sector
# <p>
# Determined by SQ 4

# %%
def condition_sector_time(x):
    """
    Function to be applied to dataframe which creates a new column categorising the length of time
    respondent has worked in the sector

    Args:
        x: pandas dataframe containing responses from analytical sample.
    
    """
    if (x[col.q4] == "I don’t work with heat pumps and have no plans to do so") or (x[col.q4] == "I don’t work with heat pumps, but plan to do so in the twelve months") or (x[col.q4] == "Don't know"):
        return "Don't work with heat pumps"
    
    elif (x[col.q4] == "Less than 12 months") or (x[col.q4] == "1-3 years"):
        return "Under 3 years"
    
    elif (x[col.q4] == "3-5 years"):
        return "3-5 years"
    
    elif (x[col.q4] == "5-10 years"):
        return "5-10 years"
    
    elif(x[col.q4] == "10-20 years") or (x[col.q4] == "Over 20 years"):
        return "Over 10 years"
    
    else:
        return None
    
category = "SectorTime"

# Apply function to each row of dataframe
data[category] = data.apply(condition_sector_time, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["Don't work with heat pumps",
         "Under 3 years",
         "3-5 years",
         "5-10 years",
         "Over 10 years",
         "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# #### Number of installations in the past year
# Determined by SQs 37a and 37b.

# %%
data[col.q37a].value_counts()

# %%
data[col.q37b].value_counts()

# %%
def condition_q37(x):
    """
    Function to be applied to dataframe which creates a new column
    merging responses from sub-types of the same question.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    """
    
    # Merge responses
    if (x[col.q37a] == "9 or fewer") or (x[col.q37b] == "9 or fewer"):
        return "9 or fewer"
    
    elif (x[col.q37a] == "10 to 24") or (x[col.q37b] == "10 to 24"):
        return "10-24"
    
    elif (x[col.q37a] == "25 to 49") or (x[col.q37b] == "25 to 49"):
        return "25-49"
    
    elif (x[col.q37a] == "50 to 99") or (x[col.q37b] == "50 to 99"):
        return "50 or more"
    
    elif (x[col.q37a] == "100 to 149") or (x[col.q37b] == "100 to 149"):
        return "50 or more"
    
    elif (x[col.q37a] == "150 to 349") or (x[col.q37b] == "150 to 349"):
        return "50 or more"
    
    elif (x[col.q37a] == "350 or more") or (x[col.q37b] == "350 or more"):
        return "50 or more"

    # Check if all are captured
    else:
        return "Flag"

category = "NumberInstalls"

# Apply function to each row of dataframe
data[category] = data.apply(condition_q37, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["9 or fewer",
         "10-24",
         "25-49",
         "50 or more",
         "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# #### Location & Sublocation
# - Q8 - Where is your company located? (Select all that apply)<br>
# - Q9a. 9b, 9c, 9d - In which English/Scottish/Welsh/Northern Irish region/county is your company located?

# %%
data[col.q8].value_counts()

# %%
data[col.q9a].value_counts()
data[col.q9b].value_counts()
data[col.q9c].value_counts()
data[col.q9d].value_counts()

# %% [markdown]
# #### DesiredIncrease
# - SQ 38a. and 38b. "Would you like your business to install more heat pumps each year?/Would you like to install more heat pumps each year? I'd like to install:"

# %%
data[col.q38a].value_counts()
data[col.q38b].value_counts()

# %%
def condition_desired_increase(x):
    """
    Function to be applied to dataframe which creates a new column categorising the respondent's desire
    to increase the number of heat pump installations each year.

    Args:
        x: pandas dataframe containing responses from analytical sample.
    
    """
    if ("fewer" in x[col.q38a]) or ("fewer" in x[col.q38b]):
        return "Fewer installs"
    
    elif ("Fewer" in x[col.q38a]) or ("Fewer" in x[col.q38b]):
        return "Fewer installs"
    
    elif ("same" in x[col.q38a]) or ("same" in x[col.q38b]):
        return "Same amount of installs"
    
    elif ("More" in x[col.q38a]) or ("More" in x[col.q38b]):
        return "More installs"
    
    elif ("more" in x[col.q38a]) or ("more" in x[col.q38b]):
        return "More installs"
    
    elif ("Don't know" in x[col.q38a]) or ("Don't know" in x[col.q38b]):
        return "Don't know"
    
    else:
        return None
    
category = "DesiredIncrease"

# Apply function to each row of dataframe
data[category] = data.apply(condition_desired_increase, axis=1)

# Specify desired order for outputs and add to dictionary
order = ["Fewer installs",
         "Same amount of installs",
         "More installs",
         "Don't know",
         "Total"
        ]
order_dict.update({category:order})

# Summary of category column
data[category].value_counts()

# %% [markdown]
# #### Functions to generate crosstables

# %%
def crosstable(subpop, dataframe, x, ans) -> pd.DataFrame:
    """
    Function to generate a crosstab dataframe for standard_output

    Args:
        subpop: Column heading name for sub-population category e.g. "EmploymentType" or "CompanySizeOwnerV2"
        dataframe: pandas dataframe containing responses from analytical sample with subpop column(s)
        x: Column heading of survey question being analysed with format e.g. "SQ42"
        ans: List specifying the order of answers to the survey question being analysed with format e.g. ans_42
    
    Returns:
        A pandas crosstab dataframe summarising the count for each employment type and answer
    
    """
    # Create pandas crosstab dataframe with Total counts
    df = pd.crosstab(dataframe[subpop], dataframe[x], margins=True, margins_name="Total")

    # Re-order indices and columns according to orders specified in lists
    df = df.reindex(ans, axis='columns')
    df = df.reindex(order_dict[subpop], axis='rows')

    return df

# %%
def location_crosstab(sq_col) -> pd.DataFrame:
    """
    Function that creates crosstable dataframe with location (SQ 8) and
    sublocation (SQ 9a, 9b, 9c, 9d) grouped columns.

    Args:
        sq_col: Column heading for SQ of interest, e.g., col.q80 or "SQ70".
    """

    df_p = pd.DataFrame(columns=[col.q0a, sq_col, 'Location', 'Sublocation'])
    for n in range(0, len(data)):

        # If multiple locations selected
        if len(data[col.q8][n]) > 1:

            for m in range(0, len(data[col.q8][n])):

                if data[col.q8][n][m] == "England":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][m],
                               data[col.q9a][n]
                               ]

                
                elif data[col.q8][n][m] == "Scotland":
                    new_row = [data[col.q0a][n],
                                data[sq_col][n],
                                data[col.q8][n][m],
                                data[col.q9b][n]
                                ]

                elif data[col.q8][n][m] == "Wales":
                    new_row = [data[col.q0a][n],
                                data[sq_col][n],
                                data[col.q8][n][m],
                                data[col.q9c][n]
                                ]

                elif data[col.q8][n][m] == "Northern Ireland":
                    new_row = [data[col.q0a][n],
                                data[sq_col][n],
                                data[col.q8][n][m],
                                data[col.q9d][n]
                                ]

                else:
                    pass
            
                df_p.loc[len(df_p)] = new_row

        else:

            if data[col.q8][n] == "England":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][0],
                               data[col.q9a][n]
                               ]
            
            elif data[col.q8][n] == "Scotland":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][0],
                               data[col.q9b][n]
                               ]
            
            elif data[col.q8][n] == "Wales":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][0],
                               data[col.q9c][n]
                               ]
                    
            elif data[col.q8][n] == "Northern Ireland":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][0],
                               data[col.q9d][n]
                               ]
            
            elif data[col.q8][n] == "UK-wide business":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][0],
                               data[col.q8][n][0]
                               ]
            
            elif data[col.q8][n] == "Don't know":
                    new_row = [data[col.q0a][n],
                               data[sq_col][n],
                               data[col.q8][n][0],
                               data[col.q8][n][0]
                               ]
                    
            else:
                 pass

            df_p.loc[len(df_p)] = new_row
    
    # Generate crosstable
    df_p_crosstab = pd.crosstab(df_p[sq_col],
                     [df_p.Location, df_p.Sublocation],
                     margins=True,
                     margins_name='Total'
                     )
    df_p_crosstab

    df_p_stacked = df_p
    
    return df_p_stacked, df_p_crosstab

# %% [markdown]
# #### Functions to explode multiple response answers 

# %%
def explode_select_all(column: pd.Series) -> pd.DataFrame:
    """Explode Series of lists to boolean dataframe"""
    responses = set([item for items in column for item in items])
    return pd.concat(
        [pd.Series(column.apply(lambda x: response in x), name=response) for response in responses],
        axis=1
    )

# %% [markdown]
# #### Functions to generate figures

# %% [markdown]
# * <code>wrap_labels</code>: To be applied to x-axis to wrap tick labels
# * <code>stackedbar</code>: Stacked bar plot
# * <code>groupedbar</code>: Grouped bar plot
# * <code>donut</code>: Donut chart

# %%
import textwrap
def wrap_labels(ax, width, break_long_words=False):
    """
    Function to wrap text of x-axis tick labels.
    Adapted from https://medium.com/dunder-data/automatically-wrap-graph-labels-in-matplotlib-and-seaborn-a48740bc9ce

    Args:
        ax: Axes object of plot.
        width: Break string at space at given width.
        break_long_words: Boolean for option to break in the middle of a word.
    """
    
    # Create list of x-axis tick labels
    labels = []
    for label in ax.get_xticklabels():

        text = label.get_text()

        labels.append(textwrap.fill(text,
                                    width=width,
                                    break_long_words=break_long_words
                                    ))
        
    ax.set_xticklabels(labels, rotation=0)

# %%
def stackedbar(df, number, question, section="section6"):
    """
    Function to generate stacked bar plot.

    Args:
        df: Crosstab dataframe corresponding to research question, e.g., df_601_crosstab
        number: Research question number ID as string for .png file name, e.g, "601" or "602_owner_V2"
        question: Corresponding survey question as string for title of plot.
    """

    # Manipulate dataframe for plotting compatibility
    df_plot = df.transpose()
    df_plot = df_plot.drop(columns=['Total'],
                           index=['Total']
                           )

    # Generate stacked bar plot
    ax = df_plot.plot(kind="bar",
                      stacked=True,
                      rot=0,
                      fontsize="8"
                      )

    # Format legend
    ax.legend(title=df.index.name,
              title_fontsize="8",
              loc='upper right',
              bbox_to_anchor=(1.35,1),
              fontsize="8",
              frameon=False
              )

    # Wrap x-axis tick labels
    wrap_labels(ax,
                width=13
                )
    ax.figure

    # Format plot title and axes labels
    plt.title(question,
              fontsize="8",
              weight='bold',
              wrap=True
              )
    plt.ylabel("Count",
               fontsize="8",
               weight='bold'
               )
    plt.xlabel("Response",
               fontsize="8",
               weight='bold'
               )

    # Save as .png
    plt.savefig("../../outputs/" + section + "/figures/" + number + "_stacked_plot.png",
                bbox_inches="tight",
                dpi=600
                )

# %%
def groupedbar(df, number, question, section="section6"):
    """
    Function to generate grouped bar plot.

    Args:
        df: Crosstab dataframe corresponding to research question, e.g., df_601_crosstab
        number: Research question number ID as string for .png file name, e.g, "601" or "602_owner_V2"
        question: Corresponding survey question as string for title of plot.
    """

    # Manipulate dataframe for plotting compatibility
    df_plot = df.transpose()
    df_plot = df_plot.drop(columns=['Total'],
                           index=['Total']
                           )

    # Generate grouped bar plot
    ax = df_plot.plot(kind="bar",
                      rot=0,
                      fontsize="8"
                      )

    # Format legend
    ax.legend(title=df.index.name,
              title_fontsize="8",
              loc='upper right',
              bbox_to_anchor=(1.35,1),
              fontsize="8",
              frameon=False
              )
    
    # Wrap x-axis tick labels
    wrap_labels(ax,
                width=13
                )
    ax.figure

    # Format font size of x-axis tick labels
    for container in ax.containers:
        ax.bar_label(container,
                     fontsize="8")

    # Format plot title and axes labels
    plt.title(question,
              fontsize="8",
              weight='bold',
              wrap=True
              )
    plt.ylabel("Count",
               fontsize="8",
               weight='bold'
               )
    plt.xlabel("Response",
               fontsize="8",
               weight='bold'
               )

    # Save as .png
    plt.savefig("../../outputs/" + section + "/figures/" + number + "_grouped_plot.png",
                bbox_inches="tight",
                dpi=600
                )

# %%
def donut(df, number, question, section="section6"):
    """
    Function to generate donut chart.

    Args:
        df: Crosstab dataframe corresponding to research question, e.g., df_601_crosstab
        number: Research question number ID as string for .png file name, e.g, "601" or "602_owner_V2"
        question: Corresponding survey question as string for title of plot.
    """

    # Create list of total counts
    totals = df.loc['Total'].to_list()
    totals = totals[0:-1]

    # Create list of answer labels
    labels = df.columns.to_list()
    labels = labels[0:-1]

    # Wrap text labels
    import textwrap
    label_wrapped=[]
    for label in labels:
        label_wrapped.append(textwrap.fill(label,
                                           width=20,
                                           break_long_words=False
                                           ))
        
    # Set explosion parameters
    explode = (0.05,) * len(labels)

    # Generate pie chart
    plt.pie(totals,
            labels=label_wrapped,
            autopct='%1.1f%%',
            pctdistance=0.85,
            labeldistance=1.15,
            explode=explode,
            textprops={'fontsize': 8}
            )

    # Draw cutout circle to create donut shape
    centre_circle=plt.Circle((0, 0),
                             0.70,
                             fc='white'
                             )
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
 
    # Format plot title
    plt.title(question,
              fontsize="8",
              weight='bold',
              wrap=True
              )

    # Save as .png
    plt.savefig("../../outputs/" + section + "/figures/" + number + "_donut_plot.png",
                dpi=600
                )

    # Display chart
    plt.show()


