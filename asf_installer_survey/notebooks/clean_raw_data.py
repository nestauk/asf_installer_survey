# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     comment_magics: true
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas

from datetime import datetime

from asf_installer_survey.utils.cleaning import (
    collapse_select_all,
    merge_two_questions,
    set_not_asked_responses,
)

# %% [markdown]
# ## Load raw data

# %%
raw_data_path = """/mnt/g/Shared drives/A Sustainable Future/1. Reducing household emissions/\
2. Projects Research Work/36. Installer survey/05 survey data/Installer survey raw data anonymised (CSV).csv"""

# %%
data = pandas.read_csv(raw_data_path)

# %% [markdown]
# ### Filters for Exclusion Criteria

# %%
# Consistent 'not asked' response to insert.
not_asked = "Not asked"

# %%
# In this filter, owners/co-owners and contractors are excluded/not asked.
exclusion_col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""

employees_only = {
    "filters": [
        [(exclusion_col, "==", "The owner or co-owner of a firm")],
        [(exclusion_col, "==", "A contractor or freelancer")],
    ],
    "columns": [exclusion_col],
}

# %%
# In this filter, employees and contractors are excluded/not asked.
exclusion_col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
owners_only = {
    "filters": [
        [(exclusion_col, "==", "An employee of a firm")],
        [(exclusion_col, "==", "A contractor or freelancer")],
    ],
    "columns": [exclusion_col],
}

# %%
# In this filter, employees and owners/co-owners are excluded/not asked.
exclusion_col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
contractors_only = {
    "filters": [
        [(exclusion_col, "==", "An employee of a firm")],
        [(exclusion_col, "==", "The owner or co-owner of a firm")],
    ],
    "columns": [exclusion_col],
}

# %%
# In this filter owners/co-owners are excluded/not asked but soletraders are included.
exclusion_col = "What size company do you own?"

employees_contractors_soletraders = {
    "filters": [
        [(exclusion_col, "==", "I own a company with 5 or fewer employees")],
        [(exclusion_col, "==", "I own a company with 6-25 employees")],
        [(exclusion_col, "==", "I own a company with 26-100 employees")],
        [(exclusion_col, "==", "I own a company with over 100 employees")],
    ],
    "columns": [exclusion_col],
}

# %%
# In this filter employees, contractors and soletraders are excluded/not asked
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "What size company do you own?"

owners_no_soletraders = {
    "filters": [
        [(exclusion_col_1, "==", "An employee of a firm")],
        [(exclusion_col_1, "==", "A contractor or freelancer")],
        [(exclusion_col_2, "==", "I’m a sole trader")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2],
}

# %%
# In this filter employees are excluded/not asked but soletraders are included as owners.
exclusion_col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""

owners_contractors = {
    "filters": [
        [(exclusion_col, "==", "An employee of a firm")],
    ],
    "columns": [exclusion_col],
}

# %%
# In this filter employees and owners are excluded/not asked but soletraders are included with contractors.
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "What size company do you own?"

contractors_soletraders = {
    "filters": [
        [(exclusion_col_1, "==", "An employee of a firm")],
        [(exclusion_col_2, "==", "I own a company with 5 or fewer employees")],
        [(exclusion_col_2, "==", "I own a company with 6-25 employees")],
        [(exclusion_col_2, "==", "I own a company with 26-100 employees")],
        [(exclusion_col_2, "==", "I own a company with over 100 employees")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2],
}

# %%
# In this filter sole traders only
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "What size company do you own?"

soletraders_only = {
    "filters": [
        [(exclusion_col_1, "==", "An employee of a firm")],
        [(exclusion_col_1, "==", "A contractor or freelancer")],
        [(exclusion_col_2, "==", "I own a company with 5 or fewer employees")],
        [(exclusion_col_2, "==", "I own a company with 6-25 employees")],
        [(exclusion_col_2, "==", "I own a company with 26-100 employees")],
        [(exclusion_col_2, "==", "I own a company with over 100 employees")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2],
}

# %%
# In this filter owners and employees
exclusion_col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
owners_employees = {
    "filters": [
        [(exclusion_col, "==", "A contractor or freelancer")],
    ],
    "columns": [exclusion_col],
}

# %% [markdown]
# # System Info
#
# ### Response ID
# Describe: integer; min: 69; max: 837; na: 0.
# Cleaning: Convert from Int64 to int16.

# %%
# Response ID
data["Response ID"] = data["Response ID"].astype("int16")

# %% [markdown]
# ### Time Started
# Describe: text; na: 0.
# Cleaning: Convert to datetime object.

# %%
data["Time Started"] = pandas.to_datetime(data["Time Started"], format="%d/%m/%Y %H:%M")

# %% [markdown]
# ### Date Submitted
# Describe: text; na: 0.
# Cleaning: Convert to datetime object.

# %%
data["Date Submitted"] = pandas.to_datetime(
    data["Date Submitted"], format="%d/%m/%Y %H:%M"
)

# %% [markdown]
# ### Status
# Describe: text; na: 0.
# Cleaning: Convert to categorical object.

# %%
data["Status"] = pandas.Categorical(
    data["Status"], categories=["Complete", "Partial"], ordered=False
)

# %% [markdown]
# # Page 1: Demographics

# %% [markdown]
# ### How old are you?
# Describe: text; na: 8.
# Cleaning: Convert to categorical object.

# %%
data["How old are you?"] = pandas.Categorical(
    data["How old are you?"],
    categories=[
        "Prefer not to say",
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65-74",
        "Over 75",
    ],
    ordered=True,
)

# %% [markdown]
# ### How would you describe your gender?
# Describe: text; na: 8.
# Cleaning: Convert to categorical object.

# %%
data["How would you describe your gender?"] = pandas.Categorical(
    data["How would you describe your gender?"],
    categories=["Prefer not to say", "Male", "Female"],
    ordered=False,
)

# %% [markdown]
# ### Prefer to self describe: How would you describe your gender?
# Describe: text: na: 768
# Cleaning: Dropping field as no responses present.

# %%
data = data.drop(columns="Prefer to self describe:How would you describe your gender?")

# %% [markdown]
# ### How long have you worked in the plumbing and heating sector?
# Describe: text: na: 7.
# Cleaning: Convert to categorical object.

# %%
data[
    "How long have you worked in the plumbing and heating sector?"
] = pandas.Categorical(
    data["How long have you worked in the plumbing and heating sector?"],
    categories=[
        "Don't know",
        "Less than 12 months",
        "1-3 years",
        "3-5 years",
        "5-10 years",
        "10-20 years",
        "Over 20 years",
    ],
    ordered=True,
)

# %% [markdown]
# ### How long have you been working with heat pumps?
# Describe: text; na: 7.
# Cleaning: Convert to categorical object.

# %%
data["How long have you been working with heat pumps?"] = pandas.Categorical(
    data["How long have you been working with heat pumps?"],
    categories=[
        "I don’t work with heat pumps and have no plans to do so",
        "I don’t work with heat pumps, but plan to do so in the twelve months",
        "Don't know",
        "Less than 12 months",
        "1-3 years",
        "3-5 years",
        "5-10 years",
        "10-20 years",
        "Over 20 years",
    ],
    ordered=False,
)

# %% [markdown]
# ### Are you responding to this survey as…If multiple answers apply to you, select the option in which you’ve done the most heat pump installations in the last year.
# Describe: text; na: 7.
# Cleaning: Convert to categorical object.

# %%
col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""

data[col] = pandas.Categorical(
    data[col],
    categories=[
        "The owner or co-owner of a firm",
        "An employee of a firm",
        "A contractor or freelancer",
    ],
    ordered=False,
)

# %% [markdown]
# ### 'Other (please specify):Are you responding to this survey as…If multiple answers apply to you, select the option in which you’ve done the most heat pump installations in the last year.'
# Describe: text: na: 768
# Cleaning: Dropping field as no responses present.

# %%
col = """Other (please specify):Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""

data = data.drop(columns=col)

# %% [markdown]
# ### What size company do you work for?
# Describe: text: na: 533, effective na: 7 (only asked if 'An employee of a firm').
# Cleaning: Convert to categorical object;
# Add 'Not Asked' response for "The owner or co-owner of a firm" and "A contractor or freelancer";
# Recode "I don't know" to "Don't know" for consistency.

# %%
data["What size company do you work for?"] = (
    set_not_asked_responses(
        data,
        "What size company do you work for?",
        employees_only["filters"],
        employees_only["columns"],
        not_asked,
    )["What size company do you work for?"]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "I don’t know",
            "I work for a company with 5 or fewer employees",
            "I work for a company with 6-25 employees",
            "I work for a company with 26-100 employees",
            "I work for a company with over 100 employees",
        ],
        ordered=False,
    )
    .rename_categories({"I don’t know": "Don't know"})
)

# %% [markdown]
# ### What size company do you own?
# Describe: text: na: 330, effective na: 7 (only asked if 'The owner or co-owner of a firm').
# Cleaning: Convert to categorical object
# Add 'Not Asked' response for "An employee of a firm" and "A contractor or freelancer".

# %%
data["What size company do you own?"] = set_not_asked_responses(
    data,
    "What size company do you own?",
    owners_only["filters"],
    owners_only["columns"],
    not_asked,
)["What size company do you own?"].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "I’m a sole trader",
        "I own a company with 5 or fewer employees",
        "I own a company with 6-25 employees",
        "I own a company with 26-100 employees",
        "I own a company with over 100 employees",
    ],
    ordered=False,
)

# %% [markdown]
# ### Do you work with family members in any of the following ways? Select all that apply.
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: I don’t work with family members; Employ family directly; Own the business in partnership; Operate a limited company; Receive informal, ad hoc, help; Subcontract family members; Don’t know
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question asked to owners only, question not asked to 'An employee of a firm', 'A contractor or freelancer'). The redundant columns are removed.

# %%
# In this filter small owners only
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "What size company do you own?"

small_owners_only = {
    "filters": [
        [(exclusion_col_1, "==", "An employee of a firm")],
        [(exclusion_col_1, "==", "A contractor or freelancer")],
        [(exclusion_col_2, "==", "I own a company with 6-25 employees")],
        [(exclusion_col_2, "==", "I own a company with 26-100 employees")],
        [(exclusion_col_2, "==", "I own a company with over 100 employees")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2],
}

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Do you work with family members in any of the following ways?",
    collapsed_column_name="Do you work with family members in any of the following ways? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Do you work with family members in any of the following ways? Select all that apply.",
    small_owners_only["filters"],
    small_owners_only["columns"],
    [not_asked],
)

# %% [markdown]
# ### Where is your company located?
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: UK-wide business; England; Wales; Scotland; Northern Ireland; Don't know; I don't work in the UK.
#
# Asked to all respondents.
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA. The redundant columns are removed.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Where is your company located?",
    collapsed_column_name="Where is your company located?",
    remove_collapsed_columns=True,
)

# %% [markdown]
# ### In which English region is your company located?
# Describe: text; na: 352.
# Cleaning: Convert to categorical object. Set not asked for non-'England' responses. Not asked is a bit different as set on a question that was a select all that apply.

# %%
# Set conditional response for English region
data["In which English region is your company located?"] = (
    data["Where is your company located?"]
    .apply(
        lambda x: True
        if ("England" in x) | ("UK-wide business" in x) | (len(x) == 0)
        else False
    )  # England, uk-wide or empty (to preserve missing)
    .map({False: not_asked})  #
    .fillna(data["In which English region is your company located?"])
    .pipe(
        pandas.Categorical,
        categories=[
            "South East",
            "South West",
            "East of England",
            "North West",
            "Yorkshire and the Humber",
            "East Midlands",
            "London",
            "West Midlands",
            "North East",
            "England-wide business",
            not_asked,
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### In which Scottish region is your company located?
# Describe: text; na: 694.
# Cleaning: Convert to categorical object. Set not asked for non-'Scotland' responses.

# %%
# Set conditional response for Scottish region
data["In which Scottish region is your company located?"] = (
    data["Where is your company located?"]
    .apply(
        lambda x: True
        if ("Scotland" in x) | ("UK-wide business" in x) | (len(x) == 0)
        else False
    )  # Scotland, uk-wide or empty (to preserve missing)
    .map({False: not_asked})  #
    .fillna(data["In which Scottish region is your company located?"])
    .pipe(
        pandas.Categorical,
        categories=[
            "Central Belt",
            "Highlands & Islands",
            "Southern Scotland",
            "North of Scotland",
            "Scotland-wide business",
            not_asked,
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### In which Welsh region is your company located?
# Describe: text; na: 723.
# Cleaning: Convert to categorical object. Set not asked for non-'Wales' responses. Remove non-breaking space from field name.

# %%
# Fix field name
data = data.rename(
    columns={
        "\xa0In which Welsh region is your company located?": "In which Welsh region is your company located?"
    }
)

# %%
# Set conditional response for Scottish region
data["In which Welsh region is your company located?"] = (
    data["Where is your company located?"]
    .apply(
        lambda x: True
        if ("Wales" in x) | ("UK-wide business" in x) | (len(x) == 0)
        else False
    )  # Wales, uk-wide or empty (to preserve missing)
    .map({False: not_asked})  #
    .fillna(data["In which Welsh region is your company located?"])
    .pipe(
        pandas.Categorical,
        categories=[
            "South West Wales",
            "South East Wales",
            "North Wales",
            "Mid Wales",
            "Wales-wide business",
            "Don't know",
            not_asked,
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### In which Northern Irish county is your company located?
# Describe: text; na: 761.
# Cleaning: Convert to categorical object. Set not asked for non-'Northern Ireland' responses.

# %%
# Set conditional response for Scottish region
data["In which Northern Irish county is your company located?"] = (
    data["Where is your company located?"]
    .apply(
        lambda x: True
        if ("Northern Ireland" in x) | ("UK-wide business" in x) | (len(x) == 0)
        else False
    )  # NI, uk-wide or empty (to preserve missing)
    .map({False: not_asked})  #
    .fillna(data["In which Northern Irish county is your company located?"])
    .pipe(
        pandas.Categorical,
        categories=[
            "Tyrone",
            "Fermanagh",
            "Armagh",
            "Northern Ireland-wide business",
            not_asked,
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### How far from your business location would you typically travel for jobs, approximately?
# Describe: text; na: 79.
# Cleaning: Convert to categorical object.

# %%
data[
    "How far from your business location would you typically travel for jobs, approximately?"
] = pandas.Categorical(
    data[
        "How far from your business location would you typically travel for jobs, approximately?"
    ],
    categories=[
        "Don't know",
        "Less than 25 miles",
        "25 to 50 miles",
        "50 to 100 miles",
        "100 to 200 miles",
        "200 to 300 miles",
        "More than 300 miles",
    ],
    ordered=True,
)

# %% [markdown]
# ### What type of work do you do for the company you work for?
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: Installation of heat pump system (including heat pump unit, pipes, emitters); Heat pump servicing and maintenance; Heat pump commissioning; Heat pump system survey - on site; Heat pump system design - office based; Ordering materials and supplies, and monitoring stock levels; Sales/customer relations; Business management (eg. recruitment, planning future of business and strategy); Business administration (eg. finances, paperwork, reporting); Other; Don’t know
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question not asked to 'The owner or co-owner of a firm', 'A contractor or freelancer'). The redundant columns are removed.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="What type of work do you do for the company you work for?",
    collapsed_column_name="What type of work do you do for the company you work for? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "What type of work do you do for the company you work for? Select all that apply.",
    employees_only["filters"],
    employees_only["columns"],
    [not_asked],
)

# %% [markdown]
# ### What aspects of the company you own are you involved with?
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: Installation of heat pump system (including heat pump unit, pipes, emitters); Heat pump servicing and maintenance; Heat pump commissioning; Heat pump system survey - on site; Heat pump system design - office based; Ordering materials and supplies, and monitoring stock levels; Sales/customer relations; Business management (eg. recruitment, planning future of business and strategy); Business administration (eg. finances, paperwork, reporting); Other; Don’t know
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question not asked An employee of a firmfirm', 'A contractor or freelancer'). The redundant columns are removed.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="What aspects of the company you own are you involved with?",
    collapsed_column_name="What aspects of the company you own are you involved with? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "What aspects of the company you own are you involved with? Select all that apply.",
    owners_only["filters"],
    owners_only["columns"],
    [not_asked],
)

# %% [markdown]
# ### What type of work do you do when you’re contracted for a job?
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: Installation of heat pump system (including heat pump unit, pipes, emitters); Heat pump servicing and maintenance; Heat pump commissioning; Heat pump system survey - on site; Heat pump system design - office based; Ordering materials and supplies, and monitoring stock levels; Sales/customer relations; Business management (eg. recruitment, planning future of business and strategy); Business administration (eg. finances, paperwork, reporting); Other; Don’t know
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question not asked to 'An employee of a firm', 'The owner or co-owner of a firm'). The redundant columns are removed.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="What type of work do you do when you’re contracted for a job?",
    collapsed_column_name="What type of work do you do when you’re contracted for a job? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "What type of work do you do when you’re contracted for a job? Select all that apply.",
    contractors_only["filters"],
    contractors_only["columns"],
    [not_asked],
)

# %% [markdown]
# ## Page 2: The work you do
#
# ### Thinking of your overall heating work, what does it currently consist of?
# Describe: text; na: 447 (342 not asked).
# Cleaning: Convert to categorical object
#
# Exclusion criteria - sole traders included, other business owners not-included..

# %%
data[
    "Thinking of your overall heating work, what does it currently consist of?"
] = set_not_asked_responses(
    data,
    "Thinking of your overall heating work, what does it currently consist of?",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    not_asked,
)[
    "Thinking of your overall heating work, what does it currently consist of?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Entirely commercial heating work, and no domestic heating work",
        "Mostly commercial heating work, and some domestic heating work",
        "An even amount of domestic and commercial heating work",
        "Mostly domestic heating work, and some commercial heating work",
        "Entirely domestic heating work, and no commercial heating work",
    ],
    ordered=False,
)

# %% [markdown]
# ### Thinking of your overall heating work in 12 months time, what do you intend it to consist of?
# Describe: text; na: 447 (342 not asked).
# Cleaning: Convert to categorical object.
#
# Exclusion criteria - sole traders included, other business owners not-included.

# %%
data[
    "Thinking of your overall heating work in 12 months time, what do you intend it to consist of?"
] = set_not_asked_responses(
    data,
    "Thinking of your overall heating work in 12 months time, what do you intend it to consist of?",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    not_asked,
)[
    "Thinking of your overall heating work in 12 months time, what do you intend it to consist of?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Entirely commercial heating work, and no domestic heating work",
        "Mostly commercial heating work, and some domestic heating work",
        "An even amount of domestic and commercial heating work",
        "Mostly domestic heating work, and some commercial heating work",
        "Entirely domestic heating work, and no commercial heating work",
    ],
    ordered=False,
)

# %% [markdown]
# ### Thinking of the heating systems you install, do you work on:
#
# Describe: text; na: 447 (342 not asked).
# Cleaning: Convert to categorical object Fix double space in category..
#
# Exclusion criteria - sole traders included, other business owners not-included.

# %%
data["Thinking of the heating systems you install, do you work on:"] = (
    set_not_asked_responses(
        data,
        "Thinking of the heating systems you install, do you work on:",
        employees_contractors_soletraders["filters"],
        employees_contractors_soletraders["columns"],
        not_asked,
    )["Thinking of the heating systems you install, do you work on:"]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Only heat pumps",
            "Mostly heat pumps, and some other systems",
            "An equal number of heat pumps and other systems",
            "Mostly other systems, and some heat pumps",
            "Almost entirely other systems, and the occasional heat pump",
            "I don't install any heat pumps, but I  plan to do so in the next 12 months",
            "I don't install any heat pumps and have no plans to do so",
        ],
        ordered=False,
    )
    .rename_categories(
        {
            "I don't install any heat pumps, but I  plan to do so in the next 12 months": "I don't install any heat pumps, but I plan to do so in the next 12 months"
        }
    )
)

# %% [markdown]
# ### Thinking of the heating systems you service and maintain, do you work on:
# Describe: text; na: 447 (342 not asked).
# Cleaning: Convert to categorical object.
#
# Exclusion criteria - sole traders included, other business owners not-included.

# %%
data[
    "Thinking of the heating systems you service and maintain, do you work on:"
] = set_not_asked_responses(
    data,
    "Thinking of the heating systems you service and maintain, do you work on:",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    not_asked,
)[
    "Thinking of the heating systems you service and maintain, do you work on:"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Only heat pumps",
        "Mostly heat pumps, and some other systems",
        "An equal number of heat pumps and other systems",
        "Mostly other systems and some heat pumps",
        "Almost entirely other systems and the occasional heat pump",
        "I don’t service and maintain any heat pumps, but plan to do so in the next year",
        "I don’t service and maintain any heat pumps and have no plans to do so",
    ],
    ordered=False,
)

# %% [markdown]
# ### What types of heat pump have you installed over the last 12 months?
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: Air-source (air-to-water) heat pump; Air-to-air heat pump; Ground-source heat pump; Hybrid air-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate); Hybrid ground-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate); Heat pumps for shared ground loops; Heat pumps for communal heating systems (air source or ground source); Water-source heat pump; Other.
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question not asked to 'The owner or co-owner of a firm' except for sole traders). The redundant columns are removed.
#
# As there are 'Other' responses, we'll create an Other column for any text.

# %%
responses = [
    "Air-source (air-to-water) heat pump",
    "Air-to-air heat pump",
    "Ground-source heat pump",
    "Hybrid air-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
    "Hybrid ground-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
    "Heat pumps for shared ground loops",
    "Heat pumps for communal heating systems (air source or ground source)",
    "Water-source heat pump",
]

data = collapse_select_all(
    df=data,
    select_all_columns="What types of heat pump have you installed over the last 12 months?",
    collapsed_column_name="What types of heat pump have you installed over the last 12 months? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="What types of heat pump have you installed over the last 12 months? Other.",
).pipe(
    set_not_asked_responses,
    "What types of heat pump have you installed over the last 12 months? Select all that apply.",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    [not_asked],
)

# %% [markdown]
# ### What type of heat pump have you installed most often over the last 12 months?
# Describe: text; na: 448 (342 not asked).
# Cleaning: Convert to categorical object Rename Other category..
#
# Exclusion criteria - sole traders included, other business owners not-included.

# %%
data[
    "What type of heat pump have you installed most often over the last 12 months?Please select one option"
] = set_not_asked_responses(
    data,
    "What type of heat pump have you installed most often over the last 12 months?Please select one option",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    not_asked,
)[
    "What type of heat pump have you installed most often over the last 12 months?Please select one option"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Air-source (air-to-water) heat pump",
        "Other (please specify)",
        "Air-to-air heat pump",
        "Hybrid air-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
        "Ground-source heat pump",
        "Hybrid ground-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
        "Heat pumps for shared ground loops",
        "Water-source heat pump",
        "Heat pumps for communal heating systems (air source or ground source)",
    ],
    ordered=False,
)

# %%
# Rename 'Other' field
data = data.rename(
    columns={
        "Other (please specify):What type of heat pump have you installed most often over the last 12 months?Please select one option": "What type of heat pump have you installed most often over the last 12 months? Other."
    }
)

# %% [markdown]
# ### Thinking of your company's overall heating work, what does it currently consist of?
# Describe: text; na: 475 (419 not asked).
# Cleaning: Convert to categorical object. Fix column name with non-breaking space.
#
# Exclusion criteria - business owners only, sole traders excluded.

# %%
data[
    "Thinking of your company's overall heating work, what does it currently consist of?"
] = set_not_asked_responses(
    data,
    "Thinking of your company's\xa0overall heating work, what does it currently consist of?",
    owners_no_soletraders["filters"],
    owners_no_soletraders["columns"],
    not_asked,
)[
    "Thinking of your company's\xa0overall heating work, what does it currently consist of?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Entirely commercial heating work, and no domestic heating work",
        "Mostly commercial heating work, and some domestic heating work",
        "An even amount of domestic and commercial heating work",
        "Mostly domestic heating work, and some commercial heating work",
        "Entirely domestic heating work, and no commercial heating work",
    ],
    ordered=False,
)

# Drop column with non-breaking space.
data = data.drop(
    columns="Thinking of your company's\xa0overall heating work, what does it currently consist of?"
)

# %% [markdown]
# ### Thinking of your company's overall heating work in 12 months time, what do you intend it to consist of?
# Describe: text; na: 475 (419 not asked).
# Cleaning: Convert to categorical object. Fix column name with non-breaking space.
#
# Exclusion criteria - business owners only, sole traders excluded.

# %%
data[
    "Thinking of your company's overall heating work in 12 months time, what do you intend it to consist of?"
] = set_not_asked_responses(
    data,
    "Thinking of your company's\xa0overall heating work in 12 months time, what do you intend it to consist of?",
    owners_no_soletraders["filters"],
    owners_no_soletraders["columns"],
    not_asked,
)[
    "Thinking of your company's\xa0overall heating work in 12 months time, what do you intend it to consist of?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Entirely commercial heating work, and no domestic heating work",
        "Mostly commercial heating work, and some domestic heating work",
        "An even amount of domestic and commercial heating work",
        "Mostly domestic heating work, and some commercial heating work",
        "Entirely domestic heating work, and no commercial heating work",
    ],
    ordered=False,
)

# Drop column with non-breaking space.
data = data.drop(
    columns="Thinking of your company's\xa0overall heating work in 12 months time, what do you intend it to consist of?"
)

# %% [markdown]
# ### Thinking of the heating systems your company installs, do you work on:
#
# Describe: text; na: 475 (419 not asked).
# Cleaning: Convert to categorical object. Fix 1 wrong category name.
#
# Exclusion criteria - business owners only, sole traders excluded.

# %%
data["Thinking of the heating systems your company installs, do you work on:"] = (
    set_not_asked_responses(
        data,
        "Thinking of the heating systems your company installs, do you work on:",
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )["Thinking of the heating systems your company installs, do you work on:"]
    .replace(
        to_replace="My company doesn't install any heat pumps, but plan to do so in the next year",
        value="My company doesn't install any heat pumps, but plans to do so in the next 12 months",
    )
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Only heat pumps",
            "Mostly heat pumps, and some other systems",
            "An equal number of heat pumps and other systems",
            "Mostly other systems, and some heat pumps",
            "Almost entirely other systems and the occasional heat pump",
            "My company doesn't install any heat pumps, but plans to do so in the next 12 months",
            "My company doesn't install any heat pumps, and has no plans to do so",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### Thinking of the heating systems your company services and maintains, do you work on:
# Describe: text; na: 475 (419 not asked).
# Cleaning: Convert to categorical object. Fix non-breaking space in column name. Fix errant category.
#
# Exclusion criteria - business owners only, sole traders excluded.

# %%
data[
    "Thinking of the heating systems your company services and maintains, do you work on:"
] = (
    set_not_asked_responses(
        data,
        "Thinking of the heating systems your company\xa0services and maintains, do you work on:",
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )[
        "Thinking of the heating systems your company\xa0services and maintains, do you work on:"
    ]
    .replace(
        to_replace="My company doesn't service and maintain any heat pumps, but plan to do so in the next year",
        value="My company doesn't service and maintain any heat pumps, but plans to do so in the next 12 months",
    )
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Only heat pumps",
            "Mostly heat pumps, and some other systems",
            "An equal number of heat pumps and other systems",
            "Mostly other systems and some heat pumps",
            "Almost entirely other systems and the occasional heat pump",
            "My company doesn't service and maintain any heat pumps, but plans to do so in the next 12 months",
            "My company doesn't service and maintain any heat pumps and has no plans to do so",
        ],
        ordered=False,
    )
)

# Drop column with non-breaking space.
data = data.drop(
    columns="Thinking of the heating systems your company\xa0services and maintains, do you work on:"
)

# %% [markdown]
# ### What types of heat pump has your company installed over the last 12 months?
#
# Because this is a 'select all that apply' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: Air-source (air-to-water) heat pump; Air-to-air heat pump; Ground-source heat pump; Hybrid air-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate); Hybrid ground-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate); Heat pumps for shared ground loops; Heat pumps for communal heating systems (air source or ground source); Water-source heat pump; Other.
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question only asked to business owners only, sole traders excluded.). The redundant columns are removed.
#
# As there are 'Other' responses, we'll create an Other column for any text.

# %%
responses = [
    "Air-source (air-to-water) heat pump",
    "Air-to-air heat pump",
    "Ground-source heat pump",
    "Hybrid air-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
    "Hybrid ground-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
    "Heat pumps for communal heating systems (air source or ground source)",
    "Heat pumps for shared ground loops",
    "Water-source heat pump",
]

data = collapse_select_all(
    df=data,
    select_all_columns="What types of heat pump has your company installed over the last 12 months?",
    collapsed_column_name="What types of heat pump has your company installed over the last 12 months? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="What types of heat pump has your company installed over the last 12 months? Other.",
).pipe(
    set_not_asked_responses,
    "What types of heat pump has your company installed over the last 12 months? Select all that apply.",
    owners_no_soletraders["filters"],
    owners_no_soletraders["columns"],
    [not_asked],
)

# Remove redundant columns
data = data.drop(
    columns=data.columns[
        data.columns.str.contains(
            ".+What types of heat pump has your company installed over the last 12 months?"
        )
    ]
)

# %% [markdown]
# ### What type of heat pump has your company installed most often over the last 12 months?Please select one option.
#
# Describe: text; na: 475 (419 not asked).
# Cleaning: Convert to categorical object Rename Other category
#
# Exclusion criteria - business owners only, sole traders excluded.ed.

# %%
data[
    "What type of heat pump has your company installed most often over the last 12 months?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "What type of heat pump has your company installed most often over the last 12 months?Please select one option.",
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )[
        "What type of heat pump has your company installed most often over the last 12 months?Please select one option."
    ]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Air-source (air-to-water) heat pump",
            "Other (please specify)",
            "Air-to-air heat pump",
            "Hybrid air-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
            "Ground-source heat pump",
            "Hybrid ground-source heat pump (e.g. a heat pump and gas/oil powered unit(s), combined or separate)",
            "Heat pumps for shared ground loops",
            "Water-source heat pump",
            "Heat pumps for communal heating systems (air source or ground source)",
        ],
        ordered=False,
    )
    .rename_categories({"Other (please specify)": "Other"})
)

# %% [markdown]
# ### Do you offer heat batteries to accompany your heat pump installations?
#
# NB This question is separated by the survey branch, so the two questions have to be merged first. Everyone is asked.
#
# Describe: text. na: 154.
# Cleaning: Merge questions, convert to categorical object.

# %%
data[
    "Do you offer heat batteries to accompany your heat pump installations?"
] = merge_two_questions(
    data,
    merge_column_1="Do you offer heat batteries to accompany your heat pump installations?",
    merge_column_2="Do you offer heat batteries to accompany your heat pump installations?.1",
    merge_column_name="Do you offer heat batteries to accompany your heat pump installations?",
)[
    "Do you offer heat batteries to accompany your heat pump installations?"
].pipe(
    pandas.Categorical, categories=["Yes", "No", "Don't know"], ordered=False
)

# Remove dedundant column
data = data.drop(
    columns="Do you offer heat batteries to accompany your heat pump installations?.1"
)

# %% [markdown]
# ### What barriers prevent you from offering heat batteries?
#
# Because this is a 'select up to 3' question, we need to clean the possible responses, which are otherwise individual fields.
#
# Responses: Lack of customer demand; I don’t have the required knowledge or training; Installation difficulties; Cost of the heat battery and associated materials; Time it takes to install a heat battery; Compatibility with government funding; Don't know; Other
#
# Cleaning: The data are collapsed rowwise into lists. An empty list corresponds to NA, and a list containing "Not asked" representing the not asked response (question only asked to respondant who said they did not offer heat battery installations). The redundant columns are removed.
#
# As there are 'Other' responses, we'll create an Other column for any text.

# %%
# Bespoke exclusion filter for heat battery responses.
exclusion_col = "Do you offer heat batteries to accompany your heat pump installations?"
heat_battery_no = {
    "filters": [[(exclusion_col, "==", "Yes")], [(exclusion_col, "==", "Don't know")]],
    "columns": [exclusion_col],
}

responses = [
    "Lack of customer demand",
    "I don’t have the required knowledge or training",
    "Installation difficulties",
    "Cost of the heat battery and associated materials",
    "Time it takes to install a heat battery",
    "Compatibility with government funding",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="What barriers prevent you from offering heat batteries?",
    collapsed_column_name="What barriers prevent you from offering heat batteries? You can select up to 3 options.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="What barriers prevent you from offering heat batteries? Other.",
).pipe(
    set_not_asked_responses,
    "What barriers prevent you from offering heat batteries? You can select up to 3 options.",
    heat_battery_no["filters"],
    heat_battery_no["columns"],
    [not_asked],
)

# %% [markdown]
# ### If a customer doesn’t specify what they want with their heat pump, what is the most important factor for you when choosing which thermal store or hot water system to fit?
#
# NB This question is separated by the survey branch, so the two questions have to be merged first. Everyone is asked.
#
# Describe: text. na: 154.
# Cleaning: Merge questions, convert to categorical object.

# %%
# Main Question
data[
    """If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit? Please select one option."""
] = (
    merge_two_questions(
        data,
        merge_column_1="""If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option.""",
        merge_column_2="""If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option..1""",
        merge_column_name="""If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit? Please select one option.""",
    )[
        """If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit? Please select one option."""
    ]
    .pipe(
        pandas.Categorical,
        categories=[
            "Size/space required in the home",
            "Unit made by manufacturer I trust/regularly use",
            "Efficiency/energy rating",
            "Heat loss rate",
            "Price of the unit/system",
            "Other (please specify)",
            "Don’t know",
        ],
        ordered=False,
    )
    .rename_categories({"Other (please specify)": "Other", "Don’t know": "Don't know"})
)

# Remove dedundant columns
data = data.drop(
    columns=[
        """If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option.""",
        """If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option..1""",
    ]
)

# %%
# Merge Other responses.
data = merge_two_questions(
    data,
    merge_column_1="""Other (please specify):If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option.""",
    merge_column_2="""Other (please specify):If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option..1""",
    merge_column_name="""If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit? Other.""",
)

# Remove redundant columns
data = data.drop(
    columns=[
        """Other (please specify):If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option.""",
        """Other (please specify):If a customer doesn’t specify what they want with their heat pump, \
what is the most important factor for you when choosing which thermal store or hot water system to fit?Please select one option..1""",
    ]
)

# %% [markdown]
# # Page 3: The work you do pt. 2
#
# ### Is you business MCS certified for heat pump installations?
# Describe: text; na: 477 (419 not asked).
# Cleaning: Convert to categorical object. Replace unicode apostrophe.
#
# Exclusion criteria - business owners only, sole traders excluded.

# %%
data["Is your business MCS certified for heat pump installations?"] = (
    set_not_asked_responses(
        data,
        "Is your business MCS certified for heat pump installations?",
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )["Is your business MCS certified for heat pump installations?"]
    .replace(
        "Not yet, but we’re in the process of certification",
        "Not yet, but we're in the process of certification",
    )
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Yes",
            "No, we were previously MCS certified but decided to cease to be so",
            "No, we were previously MCS certified but the Nominated Technical Person has left the firm",
            "No, we have never been MCS certified",
            "Not yet, but we're in the process of certification",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### Which heat pump technologies is your business MCS certified to install? Select all that apply.
#
# Although there are 3 responses in the survey data, the 'both' response is empty.
#
# Describe: text; 624 na (566 not asked).
# Cleaning: Collapse select all that apply data.
#
# Exclusion criteria- Responded no or not yet to 'Is your business MCS certified for heat pump installations?'.

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Is your business MCS certified for heat pump installations?"
mcs_yes = {
    "filters": [
        [
            (
                exclusion_col,
                "==",
                "No, we were previously MCS certified but decided to cease to be so",
            )
        ],
        [
            (
                exclusion_col,
                "==",
                "No, we were previously MCS certified but the Nominated Technical Person has left the firm",
            )
        ],
        [(exclusion_col, "==", "No, we have never been MCS certified")],
        [(exclusion_col, "==", "Not yet, but we're in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward 'not asked' exclusion
    ],
    "columns": [exclusion_col],
}

# %%
responses = ["Air source heat pumps", "Ground or water source heat pumps"]

data = collapse_select_all(
    df=data,
    select_all_columns="Which heat pump technologies is your business MCS certified to install?",
    collapsed_column_name="Which heat pump technologies is your business MCS certified to install? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Which heat pump technologies is your business MCS certified to install? Select all that apply.",
    mcs_yes["filters"],
    mcs_yes["columns"],
    [not_asked],
)

# %% [markdown]
# ### How long has your business been MCS certified for heat pump installations?
#
# Describe: text; na: 624 (566 not asked).
# Cleaning: Convert to categorical variable. Replace unicode apostrope in don't know.
#
# Exclusion criteria - Responded no or not yet to 'Is your business MCS certified for heat pump installations?'

# %%
data["How long has your business been MCS certified for heat pump installations?"] = (
    set_not_asked_responses(
        data,
        "How long has your business been MCS certified for heat pump installations?",
        mcs_yes["filters"],
        mcs_yes["columns"],
        not_asked,
    )["How long has your business been MCS certified for heat pump installations?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Less than 1 year",
            "1 to 3 years",
            "3-5 years",
            "5-10 years",
            "Over 10 years",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### How long did the certification process take from application to certification?
#
# Note, this exact question is asked to a different branch, so we'll have to disambiguate here.
#
# Describe: text; na: 624 (566 not asked).
# Cleaning: Convert to categorical variable. Replace unicode apostrope in don't know Drop old column..
#
# Exclusion criteria - Responded no or not yet to 'Is your business MCS certified for heat pump installations?'

# %%
data[
    "How long did the certification process take from application to certification? (Business)"
] = (
    set_not_asked_responses(
        data,
        "How long did the certification process take from application to certification?.1",
        mcs_yes["filters"],
        mcs_yes["columns"],
        not_asked,
    )[
        "How long did the certification process take from application to certification?.1"
    ]
    .replace("Don’t know / can't remember", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "1-3 months",
            "4-6 months",
            "6-9 months",
            "10-12 months",
            "More than 12 months",
        ],
        ordered=True,
    )
)

# Drop old column
data = data.drop(
    columns="How long did the certification process take from application to certification?.1"
)

# %% [markdown]
# ### Why isn’t your business MCS certified? Select all that apply.
#
# Describe: text; na: 678 (620 not asked).
# Cleaning: Collapse multiple options.
#
# NB other column created, but no other text observed.
#
# Exclusion criteria - Responded yes, no, but previously or not yet to 'Is your business MCS certified for heat pump installations?'

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Is your business MCS certified for heat pump installations?"
mcs_no_never = {
    "filters": [
        [
            (
                exclusion_col,
                "==",
                "No, we were previously MCS certified but decided to cease to be so",
            )
        ],
        [
            (
                exclusion_col,
                "==",
                "No, we were previously MCS certified but the Nominated Technical Person has left the firm",
            )
        ],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not yet, but we're in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

responses = [
    "It is too expensive",
    "There is too much paperwork",
    "There is too much required training",
    "My company doesn’t work in retrofit",
    "I prefer to work through an MCS umbrella scheme",
    "I prefer to do retrofit outside the MCS scheme",
    "I prefer to have a colleague from another company sign off my installations for MCS certification.",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why isn’t your business MCS certified?",
    collapsed_column_name="Why isn't your business MCS certified? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why isn't your business MCS certified? Other.",
).pipe(
    set_not_asked_responses,
    "Why isn't your business MCS certified? Select all that apply.",
    mcs_no_never["filters"],
    mcs_no_never["columns"],
    [not_asked],
)

# %% [markdown]
# ### Which heat pump technologies was your business MCS certified to install? Select all that apply.
#
# Describe: text; na: 757 (699 not asked).
# Cleaning: Collapse multiple options.
#
# Exclusion criteria - Responded yes, no, never or not yet to 'Is your business MCS certified for heat pump installations?'

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Is your business MCS certified for heat pump installations?"
mcs_no_previously = {
    "filters": [
        [(exclusion_col, "==", "No, we have never been MCS certified")],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not yet, but we're in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = ["Air source heat pumps", "Ground or water source heat pumps"]

data = collapse_select_all(
    df=data,
    select_all_columns="Which heat pump technologies was your business MCS certified to install?",
    collapsed_column_name="Which heat pump technologies was your business MCS certified to install? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Which heat pump technologies was your business MCS certified to install? Select all that apply.",
    mcs_no_previously["filters"],
    mcs_no_previously["columns"],
    [not_asked],
)

# %% [markdown]
# ### How long was your business MCS certified for heat pump installations?
#
# Describe: text; na: 757 (699 not asked).
# Cleaning: Cast to categorical variables.
#
# Exclusion criteria - Responded yes, no, never or not yet to 'Is your business MCS certified for heat pump installations?'

# %%
data["How long was your business MCS certified for heat pump installations?"] = (
    set_not_asked_responses(
        data,
        "How long was your business MCS certified for heat pump installations?",
        mcs_no_previously["filters"],
        mcs_no_previously["columns"],
        not_asked,
    )["How long was your business MCS certified for heat pump installations?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Less than 1 year",
            "1 to 3 years",
            "3-5 years",
            "5-10 years",
            "Over 10 years",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### Do you intend to reinstate your MCS certification with a new Nominated Technical Person?
#
# Describe: text; na: 767 (709 not asked).
# Cleaning: Cast to categorical variables.
#
# Exclusion criteria - Responded yes, no never, no previously ceased, or not yet to 'Is your business MCS certified for heat pump installations?'

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Is your business MCS certified for heat pump installations?"
mcs_no_ceased = {
    "filters": [
        [
            (
                exclusion_col,
                "==",
                "No, we were previously MCS certified but decided to cease to be so",
            )
        ],
        [(exclusion_col, "==", "No, we have never been MCS certified")],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not yet, but we're in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # Carry forward not asked
    ],
    "columns": [exclusion_col],
}

data[
    "Do you intend to reinstate your MCS certification with a new Nominated Technical Person?"
] = set_not_asked_responses(
    data,
    "Do you intend to reinstate your MCS certification with a new Nominated Technical Person?",
    mcs_no_ceased["filters"],
    mcs_no_ceased["columns"],
    not_asked,
)[
    "Do you intend to reinstate your MCS certification with a new Nominated Technical Person?"
].pipe(
    pandas.Categorical,
    categories=["Not asked", "Don't know", "Yes", "No"],
    ordered=True,
)

# %% [markdown]
# ### Are you personally registered as an MCS-certified heat pump installer?
#
# Describe: text; na: 636 (577 not asked).
# Cleaning: Cast to categorical variables. Fix unicode apostrophe.
#
# Exclusion criteria - Sole trader and contractor only.

# %%
data["Are you personally registered as an MCS-certified heat pump installer?"] = (
    set_not_asked_responses(
        data,
        "Are you personally registered as an MCS-certified heat pump installer?",
        contractors_soletraders["filters"],
        contractors_soletraders["columns"],
        not_asked,
    )["Are you personally registered as an MCS-certified heat pump installer?"]
    .replace(
        "Not yet, but I’m in the process of certification",
        "Not yet, but I'm in the process of certification",
    )
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Yes",
            "No, I have never been MCS certified",
            "Not yet, but I'm in the process of certification",
            "I was previously MCS certified but decided to cease to be so",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### Which heat pump technologies are you MCS certified to install? Select all that apply.
#
# Although there are 3 responses in the survey data, the 'both' response is empty.
#
# Describe: text; na: 755 (696 not asked).
# Cleaning: Collapse select all that apply data.
#
# Exclusion criteria- Responded no or not yet to 'Are you personally registered as an MCS-certified heat pump installer?'.

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Are you personally registered as an MCS-certified heat pump installer?"
mcs_yes = {
    "filters": [
        [
            (
                exclusion_col,
                "==",
                "I was previously MCS certified but decided to cease to be so",
            )
        ],
        [(exclusion_col, "==", "No, I have never been MCS certified")],
        [(exclusion_col, "==", "Not yet, but I'm in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = ["Air source heat pumps", "Ground or water source heat pumps"]

data = collapse_select_all(
    df=data,
    select_all_columns="Which heat pump technologies are you MCS certified to install?",
    collapsed_column_name="Which heat pump technologies are you MCS certified to install? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Which heat pump technologies are you MCS certified to install? Select all that apply.",
    mcs_yes["filters"],
    mcs_yes["columns"],
    [not_asked],
)

# %% [markdown]
# ### How long have you been MCS certified for heat pump installations?
#
# Describe: text; na: 755 (696 not asked).
# Cleaning: Convert to categorical variable.
#
# Exclusion criteria - Responded no or not yet to 'Are you personally registered as an MCS-certified heat pump installer?'

# %%
data["How long have you been MCS certified for heat pump installations?"] = (
    set_not_asked_responses(
        data,
        "How long have you been MCS certified for heat pump installations?",
        mcs_yes["filters"],
        mcs_yes["columns"],
        not_asked,
    )["How long have you been MCS certified for heat pump installations?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Less than 1 year",
            "1 to 3 years",
            "3-5 years",
            "5-10 years",
            "Over 10 years",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### How long did the certification process take from application to certification?
#
# Describe: text; na: 755 (696 not asked).
# Cleaning: Convert to categorical variable.
#
# Exclusion criteria - Responded no or not yet to 'Are you personally registered as an MCS-certified heat pump installer?'

# %%
data[
    "How long did the certification process take from application to certification? (Sole trader/contractor)"
] = set_not_asked_responses(
    data,
    "How long did the certification process take from application to certification?",
    mcs_yes["filters"],
    mcs_yes["columns"],
    not_asked,
)[
    "How long did the certification process take from application to certification?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "1-3 months",
        "4-6 months",
        "6-9 months",
        "10-12 months",
        "More than 12 months",
    ],
    ordered=True,
)

# Drop old column
data = data.drop(
    columns="How long did the certification process take from application to certification?"
)

# %% [markdown]
# ### Why aren’t you MCS certified? Select all that apply. (Sole Trader)
#
# This question has been split by sole traders and contractors, but the question asked is identical, making this difficult to deal with.
#
# The key difference is that sole treaders get the option "I prefer to have a colleague from another company sign off my installations for MCs certification", while contractors get the option "The companies for which I work have their own MCS certification".

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Are you personally registered as an MCS-certified heat pump installer?"
mcs_no_never = {
    "filters": [
        [
            (
                exclusion_col,
                "==",
                "I was previously MCS certified but decided to cease to be so",
            )
        ],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not yet, but I'm in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

responses = [
    "It is too expensive",
    "There is too much paperwork",
    "There is too much required training",
    "I don't work in retrofit",
    "I prefer to work through an MCS umbrella scheme",
    "I prefer to do retrofit outside the MCS scheme",
    "I prefer to have a colleague from another company sign off my installations for MCS certification.",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why aren’t you MCS certified?",
    collapsed_column_name="Why aren't you (Sole Trader) MCS certified? Select all that apply.",
    remove_collapsed_columns=False,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why aren't you (Sole Trader) MCS certified? Other.",
).pipe(
    set_not_asked_responses,
    "Why aren't you (Sole Trader) MCS certified? Select all that apply.",
    mcs_no_never["filters"],
    mcs_no_never["columns"],
    [not_asked],
)

# Set Contractor fields to not asked (empty list)
exclusion_col = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
# Main variable
data.loc[
    lambda df: df[exclusion_col] == "A contractor or freelancer",
    "Why aren't you (Sole Trader) MCS certified? Select all that apply.",
] = data.loc[
    lambda df: df[exclusion_col] == "A contractor or freelancer", "Response ID"
].apply(
    lambda _: [not_asked]
)

# Other variables
data.loc[
    lambda df: df[exclusion_col] == "A contractor or freelancer",
    "Why aren't you (Sole Trader) MCS certified? Other.",
] = data.loc[
    lambda df: df[exclusion_col] == "A contractor or freelancer", "Response ID"
].apply(
    lambda _: not_asked
)

# %% [markdown]
# ### Why aren’t you MCS certified? Select all that apply. (Contractor)
# This question has been split by sole traders and contractors, but the question asked is identical, making this difficult to deal with.
#
# The key difference is that sole treaders get the option "I prefer to have a colleague from another company sign off my installations for MCs certification", while contractors get the option "The companies for which I work have their own MCS certification".

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Are you personally registered as an MCS-certified heat pump installer?"
mcs_no_never = {
    "filters": [
        [
            (
                exclusion_col,
                "==",
                "I was previously MCS certified but decided to cease to be so",
            )
        ],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not yet, but I'm in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

responses = [
    "It is too expensive",
    "There is too much paperwork",
    "There is too much required training",
    "I don't work in retrofit",
    "I prefer to work through an MCS umbrella scheme",
    "I prefer to do retrofit outside the MCS scheme",
    "The companies for which I work have their own MCS certification",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why aren’t you MCS certified?",
    collapsed_column_name="Why aren't you (Contractor) MCS certified? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why aren't you (Contractor) MCS certified? Other.",
).pipe(
    set_not_asked_responses,
    "Why aren't you (Contractor) MCS certified? Select all that apply.",
    mcs_no_never["filters"],
    mcs_no_never["columns"],
    [not_asked],
)

# Set sole trader fields to null (empty list)
exclusion_col = "What size company do you own?"
# Main variable
data.loc[
    lambda df: df[exclusion_col] == "I’m a sole trader",
    "Why aren't you (Contractor) MCS certified? Select all that apply.",
] = data.loc[lambda df: df[exclusion_col] == "I’m a sole trader", "Response ID"].apply(
    lambda _: [not_asked]
)

# Other variables
data.loc[
    lambda df: df[exclusion_col] == "I’m a sole trader",
    "Why aren't you (Contractor) MCS certified? Other.",
] = data.loc[lambda df: df[exclusion_col] == "I’m a sole trader", "Response ID"].apply(
    lambda _: not_asked
)

# %% [markdown]
# ### Which heat pump technologies were you MCS certified to install?
#
# Although there are 3 responses in the survey data, the 'both' response is empty.
#
# Describe: text; na: 760 (700 not asked).
# Cleaning: Collapse select all that apply data.
#
# Exclusion criteria- Responded no, but previously to 'Are you personally registered as an MCS-certified heat pump installer?'.

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Are you personally registered as an MCS-certified heat pump installer?"
mcs_no_previously = {
    "filters": [
        [(exclusion_col, "==", "No, I have never been MCS certified")],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not yet, but I'm in the process of certification")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = ["Air source heat pumps", "Ground or water source heat pumps"]

data = collapse_select_all(
    df=data,
    select_all_columns="Which heat pump technologies were you MCS certified to install?",
    collapsed_column_name="Which heat pump technologies were you MCS certified to install? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Which heat pump technologies were you MCS certified to install? Select all that apply.",
    mcs_no_previously["filters"],
    mcs_no_previously["columns"],
    [not_asked],
)

# %% [markdown]
# ### How long were you MCS certified for heat pump installations?
#
# Describe: text; na: 760 (700 not asked).
# Cleaning: Cast to categorical variable.
#
# Exclusion criteria- Responded no, but previously to 'Are you personally registered as an MCS-certified heat pump installer?'.

# %%
data[
    "How long were you MCS certified for heat pump installations?"
] = set_not_asked_responses(
    data,
    "How long were you MCS certified for heat pump installations?",
    mcs_no_previously["filters"],
    mcs_no_previously["columns"],
    not_asked,
)[
    "How long were you MCS certified for heat pump installations?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "Less than 1 year",
        "1 to 3 years",
        "3-5 years",
        "5-10 years",
        "Over 10 years",
    ],
    ordered=True,
)

# %% [markdown]
# ### Is the firm you work for MCS certified for heat pump installations?
#
# Describe: text; na: 583 (526 not asked).
# Cleaning: Cast to categorical variable. Fix unicode don't know.
#
# Exclusion criteria- Employees only

# %%
data["Is the firm you work for MCS certified for heat pump installations?"] = (
    set_not_asked_responses(
        data,
        "Is the firm you work for MCS certified for heat pump installations?",
        employees_only["filters"],
        employees_only["columns"],
        not_asked,
    )["Is the firm you work for MCS certified for heat pump installations?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Yes",
            "No, it has never been MCS certified",
            "Not yet, but it is in the process of certification",
            "No, it was previously MCS certified but decided to cease to be so",
            "No, it was previously MCS certified but the Nominated Technical Person has left the firm",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### Which heat pump technologies is the firm you work for you MCS certified to install?
#
# Describe: text; na: 631 (574 not asked).
# Cleaning: Collapse categorical.
#
# NB 'both' field is empty and not used.
#
# Exclusion criteria- responded yes to "Is the firm you work for MCS certified for heat pump installations?"

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Is the firm you work for MCS certified for heat pump installations?"
mcs_yes = {
    "filters": [
        [(exclusion_col, "==", "Don't know")],
        [(exclusion_col, "==", "No, it has never been MCS certified")],
        [(exclusion_col, "==", "Not yet, but it is in the process of certification")],
        [
            (
                exclusion_col,
                "==",
                "No, it was previously MCS certified but decided to cease to be so",
            )
        ],
        [
            (
                exclusion_col,
                "==",
                "No, it was previously MCS certified but the Nominated Technical Person has left the firm",
            )
        ],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = ["Air source heat pumps", "Ground or water source heat pumps"]

data = collapse_select_all(
    df=data,
    select_all_columns="Which heat pump technologies is the firm you work for you MCS certified to install?",
    collapsed_column_name="Which heat pump technologies is the firm you work for you MCS certified to install? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Which heat pump technologies is the firm you work for you MCS certified to install? Select all that apply.",
    mcs_yes["filters"],
    mcs_yes["columns"],
    [not_asked],
)

# %% [markdown]
# ### Which heat pump technologies was the firm you work for you MCS certified to install?
#
# Describe: text; na: 760 (703 not asked).
# Cleaning: Collapse categorical.
#
# NB 'both' field is empty and not used.
#
# Exclusion criteria- responded no, previously... to "Is the firm you work for MCS certified for heat pump installations?"

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col = "Is the firm you work for MCS certified for heat pump installations?"
mcs_no_previously = {
    "filters": [
        [(exclusion_col, "==", "Don't know")],
        [(exclusion_col, "==", "No, it has never been MCS certified")],
        [(exclusion_col, "==", "Not yet, but it is in the process of certification")],
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not asked")],  # cary forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = ["Air source heat pumps", "Ground or water source heat pumps"]

data = collapse_select_all(
    df=data,
    select_all_columns="Which heat pump technologies was the firm you work for MCS certified to install?",
    collapsed_column_name="Which heat pump technologies was the firm you work for MCS certified to install? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Which heat pump technologies was the firm you work for MCS certified to install? Select all that apply.",
    mcs_no_previously["filters"],
    mcs_no_previously["columns"],
    [not_asked],
)


# %% [markdown]
# ### Why do you prefer to remain without MCS certification? Select all that apply.
#
# This is a tricky conditional that merges the 'no, previously...' responses for owners (excluding sole traders) and for contractors and soletraders.
#
# Cleaning: Collapse select all variables.
#
# Exclusion: owners responding to 'is your business mcs-certified for heat pump installations' as yes, no never or not yet, contractors and soletraders responding to 'are you personally registered as an MCS-certified for heat pump installations' as yes, no never or not yet.
#
# NB We can't easily carry forward not asked responses from exclusion cols 1 and 2 as they overlap so we need a temporary variable to manage not asked repsonses)


# %%
# Temporary variable to manage joint exclusion criteria
def joint_exclusion(row):
    if (
        row["Are you personally registered as an MCS-certified heat pump installer?"]
        == "Not asked"
    ) & (
        row["Is your business MCS certified for heat pump installations?"]
        not in [
            "No, we were previously MCS certified but decided to cease to be so",
            "No, we were previously MCS certified but the Nominated Technical Person has left the firm",
        ]
    ):
        return "Not asked"
    elif (
        row["Are you personally registered as an MCS-certified heat pump installer?"]
        != "I was previously MCS certified but decided to cease to be so"
    ) & (
        row["Is your business MCS certified for heat pump installations?"]
        == "Not asked"
    ):
        return "Not asked"


data["temp_joint_exclusion"] = data[
    [
        "Are you personally registered as an MCS-certified heat pump installer?",
        "Is your business MCS certified for heat pump installations?",
    ]
].apply(joint_exclusion, axis=1)

# %%
# Bespoke exclusion filter for mcs certification
exclusion_col_1 = "Is your business MCS certified for heat pump installations?"
exclusion_col_2 = (
    "Are you personally registered as an MCS-certified heat pump installer?"
)
exclusion_col_3 = "temp_joint_exclusion"

mcs_no_previously_collected = {
    "filters": [
        [(exclusion_col_1, "==", "Yes")],
        [(exclusion_col_1, "==", "No, we have never been MCS certified")],
        [(exclusion_col_1, "==", "Not yet, but we're in the process of certification")],
        [(exclusion_col_2, "==", "Yes")],
        [(exclusion_col_2, "==", "Not yet, but I'm in the process of certification")],
        [(exclusion_col_2, "==", "No, I have never been MCS certified")],
        [(exclusion_col_3, "==", "Not asked")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2, exclusion_col_3],
}

# %%
responses = [
    "It is too expensive",
    "There is too much paperwork",
    "There is too much required training",
    "My company doesn't work in retrofit",
    "I prefer to work through an MCS umbrella scheme",
    "I prefer to do retrofit outside the MCS scheme",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why do you prefer to remain without MCS certification?",
    collapsed_column_name="Why do you prefer to remain without MCS certification? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why do you prefer to remain without MCS certification? Other.",
).pipe(
    set_not_asked_responses,
    "Why do you prefer to remain without MCS certification? Select all that apply.",
    mcs_no_previously_collected["filters"],
    mcs_no_previously_collected["columns"],
    [not_asked],
)

# %%
# Remove temporary exclusion question
data = data.drop(columns="temp_joint_exclusion")

# %% [markdown]
# # Page 4: The work you do pt. 3
#
# ### Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.
#
# Describe: 483 null (419 Not asked)
# Cleaning: Collapse categories.
#
# Exclusion: Business owners excluding sole traders only.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Has your business done any retrofit or new build heat pump installations over the last 12 months?",
    collapsed_column_name="Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.",
    owners_no_soletraders["filters"],
    owners_no_soletraders["columns"],
    [not_asked],
)

# %% [markdown]
# ### Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties?
# Describe: 518 Null (454 not asked).
# Cleaning: Collapse categories.
#
# Exclusion: must have answered 'retrofit' to "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties?",
    collapsed_column_name="Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Select all that apply.",
    remove_collapsed_columns=True,
    responses=["Individual private homes", "Social housing", "Commercial properties"],
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Other.",
)
# Apply exclusion criteria
exclusion_col = "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Select all that apply."
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("Retrofit" in x) | (len(x) == 0) else False)
    .map({False: [not_asked]})
    .fillna(
        data[
            "Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Select all that apply."
        ]
    )
)

# %% [markdown]
# ### Over the past 12 months, has your business done any new build heat pump installations in any of the following properties?
#
# Describe: 583 Null (519 not asked).
# Cleaning: Collapse categories.
#
# Exclusion: must have answered 'New build' to "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Over the past 12 months, has your business done any new build heat pump installations in any of the following properties?",
    collapsed_column_name="Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Select all that apply.",
    remove_collapsed_columns=True,
    responses=[
        "Individual private homes",
        "Private developments of multiple homes",
        "Social housing developments",
        "Commercial properties",
    ],
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Other.",
)
# Apply exclusion criteria
exclusion_col = "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Select all that apply."
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("New build" in x) | (len(x) == 0) else False)
    .map({False: [not_asked]})
    .fillna(
        data[
            "Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Select all that apply."
        ]
    )
)

# %% [markdown]
# ### Over the past 12 months, where has the majority of the heat pump installations your business has done been?
# Describe: 618 Null (554 not asked).
# Cleaning:Cast to categorical variable..
#
# Exclusion: must have answered 'New bui and 'Retrofit'ld' to "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that appl"
#
#

# %%
exclusion_col = "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, where has the majority of the heat pump installations your business has done been?"
] = (
    data[exclusion_col]
    .apply(
        lambda x: True
        if (("New build" in x) & ("Retrofit" in x)) | (len(x) == 0)
        else False
    )
    .map({False: not_asked})
    .fillna(
        data[
            "Over the past 12 months, where has the majority of the heat pump installations your business has done been?"
        ]
    )
    .pipe(
        pandas.Categorical,
        categories=["Not asked", "New build", "Retrofit"],
        ordered=False,
    )
)

# %% [markdown]
# ### Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done?
#
# Describe: 518 Null (454 not asked).
# Cleaning: Cast to categorical variable.
#
# Exclusion:  must have answered 'Retrofit' to 'Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.'

# %%
# Apply exclusion criteria
exclusion_col = "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done?"
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("Retrofit" in x) | (len(x) == 0) else False)
    .map({False: not_asked})
    .fillna(
        data[
            "Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done?"
        ]
    )
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Individual private homes",
            "Social housing",
            "Commercial properties",
            "Other",
        ],
        ordered=False,
    )
)

# Rename other column
data = data.rename(
    columns={
        "Other (please specify):Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done?": "Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done? Other."
    }
)

# %% [markdown]
# ### Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done?
#
# Describe: 583 Null (519 not asked).
# Cleaning: Collapse categories.
#
# Exclusion: must have answered 'New build' to "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
# Apply exclusion criteria
exclusion_col = "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done?"
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("New build" in x) | (len(x) == 0) else False)
    .map({False: not_asked})
    .fillna(
        data[
            "Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done?"
        ]
    )
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Individual private homes",
            "Private developments of multiple homes",
            "Social housing developments",
            "Commercial properties",
            "Other",
        ],
        ordered=False,
    )
)

# Rename other column
data = data.rename(
    columns={
        "Other (please specify):Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done?": "Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done? Other."
    }
)

# %% [markdown]
# ### In your business’s retrofit work, does your business install heat pumps through
#
# Describe: 518 Null (454 not asked).
# Cleaning: Collapse variables.
#
# Exclusion: must have answered 'Retrofit' to 'Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.'

# %%
responses = [
    "My firm’s MCS certification",
    "With sign off from another MCS certified firm",
    "An MCS umbrella scheme",
    "Without MCS certification",
    "Don’t know",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="In your business’s retrofit work, does your business install heat pumps through:",
    collapsed_column_name="In your business's retrofit work, does your business install heat pumps through: Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="In your business's retrofit work, does your business install heat pumps through: Other.",
)
# Apply exclusion criteria
exclusion_col = "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "In your business's retrofit work, does your business install heat pumps through: Select all that apply."
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("Retrofit" in x) | (len(x) == 0) else False)
    .map({False: [not_asked]})
    .fillna(
        data[
            "In your business's retrofit work, does your business install heat pumps through: Select all that apply."
        ]
    )
)

# %% [markdown]
# ### Have you done any retrofit or new build heat pump installations over the last 12 months?
#
# Describe: 476 null (342 not asked)
# Cleaning: Collapse variables.
#
# Exclusion: employees, contractors and sole traders only.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Have you done any retrofit or new build heat pump installations over the last 12 months?",
    collapsed_column_name="Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    [not_asked],
)

# %% [markdown]
# ### Over the past 12 months, have you done retrofit heat pump installations in any of the following properties?
#
# Describe: 500 null (365 not asked)
# Cleaning: Collapse categories.
#
# Exclusion: must have answered 'Retrofit' to "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Over the past 12 months, have you done retrofit heat pump installations in any of the following properties?",
    collapsed_column_name="Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Select all that apply.",
    remove_collapsed_columns=True,
    responses=["Individual private homes", "Social housing", "Commercial properties"],
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Other.",
)
# Apply exclusion criteria
exclusion_col = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Select all that apply."
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("Retrofit" in x) | (len(x) == 0) else False)
    .map({False: [not_asked]})
    .fillna(
        data[
            "Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Select all that apply."
        ]
    )
)

# %% [markdown]
# ### Over the past 12 months, have you done any new build heat pump installations in any of the following properties?
#
# Describe: 602 null (467 not asked)
# Cleaning: Collapse categories
#
# Exclusion: must have answered 'New build' to "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Over the past 12 months, have you done any new build heat pump installations in any of the following properties?",
    collapsed_column_name="Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Select all that apply.",
    remove_collapsed_columns=True,
    responses=[
        "Individual private homes",
        "Private developments of multiple homes",
        "Social housing developments",
        "Commercial properties",
    ],
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Other.",
)
# Apply exclusion criteria
exclusion_col = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Select all that apply."
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("New build" in x) | (len(x) == 0) else False)
    .map({False: [not_asked]})
    .fillna(
        data[
            "Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Select all that apply."
        ]
    )
)

# %% [markdown]
# ### Over the past 12 months, where has the majority of your heat pump installation work been?
#
# Describe: 625 null (490 not asked)
# Cleaning: cast to categorical.
#
# Exclusion: must have answered 'New build' and 'Retrofit' to "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
exclusion_col = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, where has the majority of your heat pump installation work been?"
] = (
    data[exclusion_col]
    .apply(
        lambda x: True
        if (("New build" in x) & ("Retrofit" in x)) | (len(x) == 0)
        else False
    )
    .map({False: not_asked})
    .fillna(
        data[
            "Over the past 12 months, where has the majority of your heat pump installation work been?"
        ]
    )
    .pipe(
        pandas.Categorical,
        categories=["Not asked", "New build", "Retrofit"],
        ordered=False,
    )
)

# %% [markdown]
# ### Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations?
#
# Describe: 500 null (365 not asked)
# Cleaning: Cast to categorical
#
# Exclusion: Exclusion: must have answered 'Retrofit' to "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
# Apply exclusion criteria
exclusion_col = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations?"
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("Retrofit" in x) | (len(x) == 0) else False)
    .map({False: not_asked})
    .fillna(
        data[
            "Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations?"
        ]
    )
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Individual private homes",
            "Social housing",
            "Commercial properties",
            "Other",
        ],
        ordered=False,
    )
)

# Rename other column
data = data.rename(
    columns={
        "Other (please specify):Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations?": "Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations? Other."
    }
)

# %% [markdown]
# ### Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations?
#
# Describe: 602 null (467 not asked)
# Cleaning: Cast to categorical variable.
#
# Exclusion: must have answered 'New build' to "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

# %%
# Apply exclusion criteria
exclusion_col = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."

data[
    "Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations?"
] = (
    data[exclusion_col]
    .apply(lambda x: True if ("New build" in x) | (len(x) == 0) else False)
    .map({False: not_asked})
    .fillna(
        data[
            "Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations?"
        ]
    )
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Individual private homes",
            "Private developments of multiple homes",
            "Social housing developments",
            "Commercial properties",
            "Other",
        ],
        ordered=False,
    )
)

# Rename other column
data = data.rename(
    columns={
        "Other (please specify):Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations?": "Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations? Other."
    }
)

# %% [markdown]
# ### In your retrofit work, do you install heat pumps through: Select all that apply. (Sole trader)
#
# There are 3 identical questions for different subpopulations, making this a tricky one to clean.
#
# Cleaning: Collapse values.
#
# Exclusion Sole trader and retrofit only.

# %%
responses = [
    "My own MCS certification",
    "With sign off from another MCS certified person or firm",
    "An MCS umbrella scheme",
    "Without MCS certification",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="In your retrofit work, do you install heat pumps through",
    collapsed_column_name="In your (Sole trader) retrofit work, do you install heat pumps through: Select all that apply.",
    remove_collapsed_columns=False,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="In your (Sole trader) retrofit work, do you install heat pumps through: Other.",
)

# Set Contractor and employee fields and New build responses to not asked
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."
# Main variable
data.loc[
    lambda df: df[exclusion_col_1].isin(
        ["A contractor or freelancer", "An employee of a firm"]
    )
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "In your (Sole trader) retrofit work, do you install heat pumps through: Select all that apply.",
] = data.loc[
    lambda df: df[exclusion_col_1].isin(
        ["A contractor or freelancer", "An employee of a firm"]
    )
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "Response ID",
].apply(
    lambda _: [not_asked]
)

# Other variables
data.loc[
    lambda df: df[exclusion_col_1].isin(
        ["A contractor or freelancer", "An employee of a firm"]
    )
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "In your (Sole trader) retrofit work, do you install heat pumps through: Other.",
] = data.loc[
    lambda df: df[exclusion_col_1].isin(
        ["A contractor or freelancer", "An employee of a firm"]
    )
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "Response ID",
].apply(
    lambda _: not_asked
)

# %% [markdown]
# ### In your retrofit work, do you install heat pumps through: Select all that apply. (Employee)
# There are 3 identical questions for different subpopulations, making this a tricky one to clean.
#
# Cleaning: Collapse values.
#
# Exclusion employee and retrofit only.

# %%
responses = [
    "My own MCS certification (I am the firm's Nominated Technical Person)",
    "My firm's MCS certification (someone else is the firm's Nominated Technical Person)",
    "An MCS umbrella scheme",
    "Without MCS certification",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="In your retrofit work, do you install heat pumps through",
    collapsed_column_name="In your (Employee) retrofit work, do you install heat pumps through: Select all that apply.",
    remove_collapsed_columns=False,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="In your (Employee) retrofit work, do you install heat pumps through: Other.",
)

# Set Contractor fields, sole trader fields and New build responses to not asked
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."
exclusion_col_3 = "What size company do you own?"
# Main variable
data.loc[
    lambda df: df[exclusion_col_1].isin(["A contractor or freelancer"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "In your (Employee) retrofit work, do you install heat pumps through: Select all that apply.",
] = data.loc[
    lambda df: df[exclusion_col_1].isin(["A contractor or freelancer"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "Response ID",
].apply(
    lambda _: [not_asked]
)

# Other variables
data.loc[
    lambda df: df[exclusion_col_1].isin(["A contractor or freelancer"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "In your (Employee) retrofit work, do you install heat pumps through: Other.",
] = data.loc[
    lambda df: df[exclusion_col_1].isin(["A contractor or freelancer"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "Response ID",
].apply(
    lambda _: not_asked
)

# %% [markdown]
# ### In your retrofit work, do you install heat pumps through: Select all that apply. (Contractors)
# There are 3 identical questions for different subpopulations, making this a tricky one to clean.
#
# Cleaning: Collapse values.
#
# Exclusion Contractors and retrofit only.

# %%
responses = [
    "My own MCS certification",
    "The MCS certification of the business I’m working for",
    "The MCS umbrella scheme of the business I’m working for",
    "Without MCS certification",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="In your retrofit work, do you install heat pumps through",
    collapsed_column_name="In your (Contractor) retrofit work, do you install heat pumps through: Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="In your (Contractor) retrofit work, do you install heat pumps through: Other.",
)

# Set Contractor fields, sole trader fields and New build responses to not asked
exclusion_col_1 = """Are you responding to this survey as…If multiple answers apply to you, \
select the option in which you’ve done the most heat pump installations in the last year."""
exclusion_col_2 = "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply."
exclusion_col_3 = "What size company do you own?"
# Main variable
data.loc[
    lambda df: df[exclusion_col_1].isin(["An employee of a firm"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "In your (Contractor) retrofit work, do you install heat pumps through: Select all that apply.",
] = data.loc[
    lambda df: df[exclusion_col_1].isin(["An employee of a firm"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "Response ID",
].apply(
    lambda _: [not_asked]
)

# Other variables
data.loc[
    lambda df: df[exclusion_col_1].isin(["An employee of a firm"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "In your (Contractor) retrofit work, do you install heat pumps through: Other.",
] = data.loc[
    lambda df: df[exclusion_col_1].isin(["An employee of a firm"])
    | df[exclusion_col_3].isin(["I’m a sole trader"])
    | df[exclusion_col_2].apply(
        lambda x: True if ("Retrofit" not in x) & ("New build" in x) else False
    ),
    "Response ID",
].apply(
    lambda _: not_asked
)

# %% [markdown]
# # Page 5: Productivity
#
# ### Approximately how many heat pumps did your business install in the past twelve months?
#
# Describe: 558 null (419 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Business owners excluding sole traders.

# %%
data[
    "Approximately how many heat pumps did your business install in the past twelve months?"
] = set_not_asked_responses(
    data,
    "Approximately how many heat pumps did your business install in the past twelve months?",
    owners_no_soletraders["filters"],
    owners_no_soletraders["columns"],
    not_asked,
)[
    "Approximately how many heat pumps did your business install in the past twelve months?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "None",
        "9 or fewer",
        "10 to 24",
        "25 to 49",
        "50 to 99",
        "100 to 149",
        "150 to 349",
        "350 or more",
    ],
    ordered=True,
)

# %% [markdown]
# ### Would you like your business to install more heat pumps each year?I'd like to install:
#
# Describe: 558 null (419 not asked)
# Cleaning: Cast to categorical Standardise Don't know..
#
# Exclusion: Business owners excluding sole traders.

# %%
data[
    "Would you like your business to install more heat pumps each year?I'd like to install:"
] = (
    set_not_asked_responses(
        data,
        "Would you like your business to install more heat pumps each year?I'd like to install:",
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )[
        "Would you like your business to install more heat pumps each year?I'd like to install:"
    ]
    .replace("I don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Far fewer heat pumps",
            "Fewer heat pumps",
            "The same amount of heat pumps",
            "More heat pumps",
            "Far more heat pumps",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option.
#
# Describe: 761 null (648 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Only those who answered 'far fewer' or fewer to "Would you like your business to install more heat pumps each year?I'd like to install:"

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "Would you like your business to install more heat pumps each year?I'd like to install:"
fewer_installs = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "The same amount of heat pumps")],
        [(exclusion_col_1, "==", "More heat pumps")],
        [(exclusion_col_1, "==", "Far more heat pumps")],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

data[
    "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option. (Owners)"
] = (
    set_not_asked_responses(
        data,
        "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option.",
        fewer_installs["filters"],
        fewer_installs["columns"],
        not_asked,
    )[
        "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Heat pumps are less profitable than other work",
            "Heat pump installations are harder jobs than other kinds of work",
            "I am unable to find suitable staff to work with on heat pump installations",
            "I am unable to source the hardware I need, or I am unable to source it in a timely fashion",
            "I don’t believe there is sufficient government support for the heat pump sector",
            "I believe that other renewable technologies are currently better",
            "I believe that other fossil fuel technologies are currently better",
            "Other",
        ],
        ordered=False,
    )
)

## Rename Other column
data = data.rename(
    columns={
        "Other (please specify):What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option.": "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install? Other. (Owners)"
    }
)


# drop original column
data = data.drop(
    columns="What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option."
)

# %% [markdown]
# ### What’s the biggest barrier to you installing more heat pumps?Please select one option.
#
# Describe: 563 null (450 not asked)
# Cleaning: cast to categorical
#
# Exclusion: Only those who answered more or far more to "Would you like your business to install more heat pumps each year?I'd like to install:"

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "Would you like your business to install more heat pumps each year?I'd like to install:"
more_installs = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "The same amount of heat pumps")],
        [(exclusion_col_1, "==", "Fewer heat pumps")],
        [(exclusion_col_1, "==", "Far fewer heat pumps")],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

data[
    "What’s the biggest barrier to you installing more heat pumps? Please select one option. (Owners)"
] = (
    set_not_asked_responses(
        data,
        "What’s the biggest barrier to you installing more heat pumps?Please select one option.",
        more_installs["filters"],
        more_installs["columns"],
        not_asked,
    )[
        "What’s the biggest barrier to you installing more heat pumps?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "I have too little customer demand",
            "Other work in my business’s repertoire is more attractive (e.g. bathrooms, batteries, etc.)",
            "I am not able to source the hardware I need, or I am not able to source it in a timely fashion",
            "I am unable to find additional suitable staff",
            "I find that ‘unnecessary’ elements of installation or admin take up so much time that my business is prevented from doing more jobs",
            "Other",
        ],
        ordered=False,
    )
)

## Rename Other column
data = data.rename(
    columns={
        "Other (please specify):What’s the biggest barrier to you installing more heat pumps?Please select one option.": "What’s the biggest barrier to you installing more heat pumps? Other. (Owners)"
    }
)

# drop original column
data = data.drop(
    columns="What’s the biggest barrier to you installing more heat pumps?Please select one option."
)

# %% [markdown]
# ### Please indicate how you feel about the amount of time your business spends on these tasks.
#
# This is an answer grid question. We'll loop over the questions and assign answers to categories, adpating the column name.
#
# Cleaning: Cast to categorical.
#
# Exclusion: Business owners excluding sole traders.

# %%
columns = data.columns[
    data.columns.str.contains(
        "Please indicate how you feel about the amount of time your business spends on these tasks."
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"Please indicate how you feel about the amount of time your business spends on: {task}"
    ] = set_not_asked_responses(
        data,
        col,
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )[
        col
    ].pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "I spend too long doing this (and it could be quicker)",
            "I spend the right amount of time on this",
            "I don’t get as much time on this as I should",
            "This isn’t part of my job",
        ],
        ordered=False,
    )

data = data.drop(columns=columns)

# %% [markdown]
# ### Approximately how many heat pumps did you install in the past twelve months?
#
# Describe: 534 null (342 not asked)
# Cleaning = cast to categorical
#
# Exclusion: employees, contractors and sole traders.

# %%
data["Approximately how many heat pumps did you install in the past twelve months?"] = (
    set_not_asked_responses(
        data,
        "Approximately how many heat pumps did you install in the past twelve months?",
        employees_contractors_soletraders["filters"],
        employees_contractors_soletraders["columns"],
        not_asked,
    )["Approximately how many heat pumps did you install in the past twelve months?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "None",
            "9 or fewer",
            "10 to 24",
            "25 to 49",
            "50 to 99",
            "100 to 149",
            "150 to 349",
            "350 or more",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### Would you like to install more heat pumps each year?I'd like to install:
#
# Describe: 534 null (342 not asked)
# Cleaning: cast to categorical
#
# Exclusion: employees, contractors and sole traders only.

# %%
data["Would you like to install more heat pumps each year?I'd like to install:"] = (
    set_not_asked_responses(
        data,
        "Would you like to install more heat pumps each year?I'd like to install:",
        employees_contractors_soletraders["filters"],
        employees_contractors_soletraders["columns"],
        not_asked,
    )["Would you like to install more heat pumps each year?I'd like to install:"]
    .replace("I don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Far fewer heat pumps",
            "Fewer heat pumps",
            "The same amount of heat pumps",
            "More heat pumps",
            "Far more heat pumps",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### What’s the biggest barrier to you installing more heat pumps?Please select one option.
#
# Describe: 726 null (387 not asked)
# Cleaning: cast to categorical.
#
# Exclusion: Answered more or far more to 'Would you like to install more heat pumps each year?I'd like to install:' and soletraders only.

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = (
    "Would you like to install more heat pumps each year?I'd like to install:"
)
more_installs = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "The same amount of heat pumps")],
        [(exclusion_col_1, "==", "Fewer heat pumps")],
        [(exclusion_col_1, "==", "Far fewer heat pumps")],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

data[
    "What’s the biggest barrier to you installing more heat pumps?Please select one option. (Employees, contractors, sole traders)"
] = (
    set_not_asked_responses(
        data,
        "What’s the biggest barrier to you installing more heat pumps?Please select one option..1",
        more_installs["filters"],
        more_installs["columns"],
        not_asked,
    )
    .pipe(
        set_not_asked_responses,
        column="What’s the biggest barrier to you installing more heat pumps?Please select one option..1",
        filters=soletraders_only["filters"],
        exclusion_cols=soletraders_only["columns"],
        not_asked_value=not_asked,
    )[
        "What’s the biggest barrier to you installing more heat pumps?Please select one option..1"
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "I have too little customer demand",
            "Other work in my business’s repertoire is more attractive (e.g. bathrooms, batteries, etc.)",
            "I am not able to source the hardware I need, or I am not able to source it in a timely fashion",
            "I am unable to find additional suitable staff",
            "I find that ‘unnecessary’ elements of installation or admin take up so much time that my business is prevented from doing more jobs",
            "Other",
        ],
        ordered=False,
    )
)

# Rename Other column
data = data.rename(
    columns={
        "Other (please specify):What’s the biggest barrier to you installing more heat pumps?Please select one option..1": "What’s the biggest barrier to you installing more heat pumps? Other. (Employees, contractors, sole traders)"
    }
)

# Drop redundant column
data = data.drop(
    columns="What’s the biggest barrier to you installing more heat pumps?Please select one option..1"
)

# %% [markdown]
# ### What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?
#
# Describe: 763 null (585 not asked)
# Cleaning: cast to categorical.
#
# Exclusion: Answered fewer or far fewer to 'Would you like to install more heat pumps each year?I'd like to install:'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = (
    "Would you like to install more heat pumps each year?I'd like to install:"
)
fewer_installs = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "The same amount of heat pumps")],
        [(exclusion_col_1, "==", "More heat pumps")],
        [(exclusion_col_1, "==", "Far more heat pumps")],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

data[
    "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option. (Employees, contractors, sole traders)"
] = (
    set_not_asked_responses(
        data,
        "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option..1",
        fewer_installs["filters"],
        fewer_installs["columns"],
        not_asked,
    )
    .pipe(
        set_not_asked_responses,
        column="What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option..1",
        filters=soletraders_only["filters"],
        exclusion_cols=soletraders_only["columns"],
        not_asked_value=not_asked,
    )[
        "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option..1"
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Heat pumps are less profitable than other work",
            "Heat pump installations are harder jobs than other kinds of work",
            "I am unable to find suitable staff to work with on heat pump installations",
            "I am unable to source the hardware I need, or I am unable to source it in a timely fashion",
            "I don’t believe there is sufficient government support for the heat pump sector",
            "I believe that other renewable technologies are currently better",
            "I believe that other fossil fuel technologies are currently better",
            "Other",
        ],
        ordered=False,
    )
)

## Rename Other column
data = data.rename(
    columns={
        "Other (please specify):What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option..1": "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install? Other. (Employees, contractors, sole traders)"
    }
)


# drop original column
data = data.drop(
    columns="What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option..1"
)

# %% [markdown]
# ### Please indicate how you feel about the amount of time you spend on these tasks.
#
# This is an answer grid question. We'll loop over the questions and assign answers to categories, adpating the column name.
#
# Cleaning: Cast to categorical.
#
# Exclusion: Employees, contreactors and sole traders.

# %%
columns = data.columns[
    data.columns.str.contains(
        "Please indicate how you feel about the amount of time you spend on these tasks."
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"Please indicate how you feel about the amount of time you spend on: {task}"
    ] = set_not_asked_responses(
        data,
        col,
        employees_contractors_soletraders["filters"],
        employees_contractors_soletraders["columns"],
        not_asked,
    )[
        col
    ].pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "I spend too long doing this (and it could be quicker)",
            "I spend the right amount of time on this",
            "I don’t get as much time on this as I should",
            "This isn’t part of my job",
        ],
        ordered=False,
    )

# Remove raw fields.
data = data.drop(columns=columns)

# %% [markdown]
# # Page 6 - Maintenance and servicing
#
# ### Do you offer repairs, servicing and maintenance to heat pump customers?
#
# Describe: 436 null (235 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: employees excluded.

# %%
data["Do you offer repairs, servicing and maintenance to heat pump customers?"] = (
    set_not_asked_responses(
        data,
        "Do you offer repairs, servicing and maintenance to heat pump customers?",
        owners_contractors["filters"],
        owners_contractors["columns"],
        not_asked,
    )["Do you offer repairs, servicing and maintenance to heat pump customers?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Yes",
            "No, but I intend to offer it in the next 12 months",
            "No, and I do not intend to start offering this service in the next 12 months",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### My business offers heat pump repairs, servicing and maintenance:
#
# Describe: 612 null (489 not asked)
# Cleaning: cast to categorical.
#
# Exclusion: Answered yes to 'Do you offer repairs, servicing and maintenance to heat pump customers?' AND is a business owner (excluding sole traders)

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = (
    "Do you offer repairs, servicing and maintenance to heat pump customers?"
)
yes_maintain = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "No, but I intend to offer it in the next 12 months")],
        [
            (
                exclusion_col_1,
                "==",
                "No, and I do not intend to start offering this service in the next 12 months",
            )
        ],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

# %%
data["My business offers heat pump repairs, servicing and maintenance:"] = (
    set_not_asked_responses(
        data,
        "My business offers heat pump repairs, servicing and maintenance:",
        yes_maintain["filters"],
        yes_maintain["columns"],
        not_asked,
    )
    .pipe(
        set_not_asked_responses,
        column="My business offers heat pump repairs, servicing and maintenance:",
        filters=owners_no_soletraders["filters"],
        exclusion_cols=owners_no_soletraders["columns"],
        not_asked_value=not_asked,
    )["My business offers heat pump repairs, servicing and maintenance:"]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "For all heat pump systems, regardless of who originally installed it",
            "Only for heat pump systems that my company has installed",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### I offer heat pump repairs, servicing and maintenance:
#
# Describe: 714 null (624 not asked)
# Cleaning: cast to categorical
#
# Exclusion: Answered yes to 'Do you offer repairs, servicing and maintenance to heat pump customers?' AND is a contractor or soletrader.

# %%
data["I offer heat pump repairs, servicing and maintenance:"] = (
    set_not_asked_responses(
        data,
        "I offer heat pump repairs, servicing and maintenance:",
        yes_maintain["filters"],
        yes_maintain["columns"],
        not_asked,
    )
    .pipe(
        set_not_asked_responses,
        column="I offer heat pump repairs, servicing and maintenance:",
        filters=contractors_soletraders["filters"],
        exclusion_cols=contractors_soletraders["columns"],
        not_asked_value=not_asked,
    )["I offer heat pump repairs, servicing and maintenance:"]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "For all heat pump systems, regardless of who originally installed it",
            "Only for heat pump systems that I have installed",
        ],
        ordered=False,
    )
)


# %% [markdown]
# ### Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?You can select up to 2 reasons.
#
# Cleaning: Collapse columns.
#
# Exclusion: Answered 'Only for heat pump systems that I have installed' to 'I offer heat pump repairs, servicing and maintenance:' OR 'Only for heat pump systems that my company has installed' to 'My business offers heat pump repairs, servicing and maintenance:'.


# %%
def joint_exclusion(row):
    if (
        row["My business offers heat pump repairs, servicing and maintenance:"]
        == "Not asked"
    ) & (
        row["I offer heat pump repairs, servicing and maintenance:"]
        != "Only for heat pump systems that I have installed"
    ):
        return "Not asked"
    elif (
        row["My business offers heat pump repairs, servicing and maintenance:"]
        != "Only for heat pump systems that my company has installed"
    ) & (row["I offer heat pump repairs, servicing and maintenance:"] == "Not asked"):
        return "Not asked"


data["temp_joint_exclusion"] = data[
    [
        "My business offers heat pump repairs, servicing and maintenance:",
        "I offer heat pump repairs, servicing and maintenance:",
    ]
].apply(joint_exclusion, axis=1)

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "My business offers heat pump repairs, servicing and maintenance:"
exclusion_col_2 = "I offer heat pump repairs, servicing and maintenance:"
exclusion_col_3 = "temp_joint_exclusion"

repair_my_systems = {
    "filters": [
        [
            (
                exclusion_col_1,
                "==",
                "For all heat pump systems, regardless of who originally installed it",
            )
        ],
        [
            (
                exclusion_col_2,
                "==",
                "For all heat pump systems, regardless of who originally installed it",
            )
        ],
        [
            (
                exclusion_col_3,
                "==",
                "Not asked",
            )
        ],
    ],
    "columns": [exclusion_col_1, exclusion_col_2, exclusion_col_3],
}

# %%
responses = [
    "Relationship with existing customers",
    "No demand from other customers",
    "Don’t want to take responsibility for other installers’ heat pump installations",
    "I only work on equipment I understand or have been trained in",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    collapsed_column_name="Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
).pipe(
    set_not_asked_responses,
    "Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    repair_my_systems["filters"],
    repair_my_systems["columns"],
    [not_asked],
)

# %%
# remove temp variable
data = data.drop(columns="temp_joint_exclusion")

# %% [markdown]
# ### Have you found any challenges working in heat pump repairs, servicing and maintenance?You can select up to 2 reasons.
#
# Cleaning: Collapse columns.
# Exclusion: Answered yes to 'Do you offer repairs, servicing and maintenance to heat pump customers?':

# %%
responses = [
    "Difficult to find the skills you need",
    "Low levels of customer demand",
    "Hard to make a profit from this work",
    "Difficult to fit this work into your work schedule",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Have you found any challenges working in heat pump repairs, servicing and maintenance?",
    collapsed_column_name="Have you found any challenges working in heat pump repairs, servicing and maintenance?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Have you found any challenges working in heat pump repairs, servicing and maintenance? Other.",
).pipe(
    set_not_asked_responses,
    "Have you found any challenges working in heat pump repairs, servicing and maintenance?",
    yes_maintain["filters"],
    yes_maintain["columns"],
    [not_asked],
)

# %% [markdown]
# ### Do you expect to expand your work in heat pump repairs, servicing and maintenance?
#
# Describe: 558 null (352 not asked)
# Cleaning: cast to categorical.
#
# Exclusion: Answered yes to 'Do you offer repairs, servicing and maintenance to heat pump customers?'

# %%
data[
    "Do you expect to expand your work in heat pump repairs, servicing and maintenance?"
] = (
    set_not_asked_responses(
        data,
        "Do you expect to expand your work in heat pump repairs, servicing and maintenance?",
        yes_maintain["filters"],
        yes_maintain["columns"],
        not_asked,
    )[
        "Do you expect to expand your work in heat pump repairs, servicing and maintenance?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=["Not asked", "Yes", "No", "Don't know"],
        ordered=False,
    )
)


# %% [markdown]
# ### When doing repairs, servicing or maintenance to installations by other installers, how often do you identify bad installation practice that negatively affects heat pump performance?
#
# Describe: 609 null (602 not asked)
# Cleaning: cast to categorical.
#
# Exclusion:  Must have answered "for all heat pump systems" for I/My business offer heat pump repairs, servicing and maintenance.


# %%
# Temporary variable to manage joint exclusion criteria
def joint_exclusion(row):
    if (
        row["My business offers heat pump repairs, servicing and maintenance:"]
        == "Not asked"
    ) & (
        row["I offer heat pump repairs, servicing and maintenance:"]
        != "For all heat pump systems, regardless of who originally installed it"
    ):
        return "Not asked"
    elif (
        row["My business offers heat pump repairs, servicing and maintenance:"]
        != "For all heat pump systems, regardless of who originally installed it"
    ) & (row["I offer heat pump repairs, servicing and maintenance:"] == "Not asked"):
        return "Not asked"


data["temp_joint_exclusion"] = data[
    [
        "My business offers heat pump repairs, servicing and maintenance:",
        "I offer heat pump repairs, servicing and maintenance:",
    ]
].apply(joint_exclusion, axis=1)

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "My business offers heat pump repairs, servicing and maintenance:"
exclusion_col_2 = "I offer heat pump repairs, servicing and maintenance:"
exclusion_col_3 = "temp_joint_exclusion"

all_systems = {
    "filters": [
        [
            (
                exclusion_col_1,
                "==",
                "Only for heat pump systems that my company has installed",
            )
        ],
        [(exclusion_col_2, "==", "Only for heat pump systems that I have installed")],
        [(exclusion_col_3, "==", "Not asked")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2, exclusion_col_3],
}

# %%
data[
    "When doing repairs, servicing or maintenance to installations by other installers, \
how often do you identify bad installation practice that negatively affects heat pump performance?"
] = set_not_asked_responses(
    data,
    "When doing repairs, servicing or maintenance to installations by other installers, \
how often do you identify bad installation practice that negatively affects heat pump performance?",
    all_systems["filters"],
    all_systems["columns"],
    not_asked,
)[
    "When doing repairs, servicing or maintenance to installations by other installers, \
how often do you identify bad installation practice that negatively affects heat pump performance?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "Never",
        "Rarely",
        "Sometimes",
        "Often",
        "Always",
    ],
    ordered=True,
)

# %%
# Remove temporary column
data = data.drop(columns="temp_joint_exclusion")

# %% [markdown]
# ### I intend to offer heat pump repairs, servicing and maintenance:
#
# Describe: 729 null (610 not asked)
# Cleaning: Cast to categorical
#
# Exclusion: Answered No, but I intend to... to 'Do you offer repairs, servicing and maintenance to heat pump customers?' AND is a business owner (excluding sole traders)

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = (
    "Do you offer repairs, servicing and maintenance to heat pump customers?"
)
intend_maintain = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "Yes")],
        [
            (
                exclusion_col_1,
                "==",
                "No, and I do not intend to start offering this service in the next 12 months",
            )
        ],
        [(exclusion_col_1, "==", "Not asked")],
    ],
    "columns": [exclusion_col_1],
}

# %%
data["I intend to offer heat pump repairs, servicing and maintenance: (Owners)"] = (
    set_not_asked_responses(
        data,
        "I intend to offer heat pump repairs, servicing and maintenance:",
        intend_maintain["filters"],
        intend_maintain["columns"],
        not_asked,
    )
    .pipe(
        set_not_asked_responses,
        column="I intend to offer heat pump repairs, servicing and maintenance:",
        filters=owners_no_soletraders["filters"],
        exclusion_cols=owners_no_soletraders["columns"],
        not_asked_value=not_asked,
    )["I intend to offer heat pump repairs, servicing and maintenance:"]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "For all heat pump systems, regardless of who originally installed it",
            "Only for heat pump systems that my company has installed",
        ],
        ordered=False,
    )
)

# drop redundant column
data = data.drop(
    columns="I intend to offer heat pump repairs, servicing and maintenance:"
)

# %% [markdown]
# ### I intend to offer heat pump repairs, servicing and maintenance:
#
# Describe: 738 null (648 not asked)
# Cleaning: Cast to categorical
#
# Exclusion: Answered No, but I intend to... to 'Do you offer repairs, servicing and maintenance to heat pump customers?' AND is a contractor or sole trader.

# %%
data[
    "I intend to offer heat pump repairs, servicing and maintenance: (Contractor/Soletrader)"
] = (
    set_not_asked_responses(
        data,
        "I intend to offer heat pump repairs, servicing and maintenance:.1",
        intend_maintain["filters"],
        intend_maintain["columns"],
        not_asked,
    )
    .pipe(
        set_not_asked_responses,
        column="I intend to offer heat pump repairs, servicing and maintenance:.1",
        filters=contractors_soletraders["filters"],
        exclusion_cols=contractors_soletraders["columns"],
        not_asked_value=not_asked,
    )["I intend to offer heat pump repairs, servicing and maintenance:.1"]
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "For all heat pump systems, regardless of who originally installed it",
            "Only for heat pump systems that I have installed",
        ],
        ordered=False,
    )
)

# drop redundant column
data = data.drop(
    columns="I intend to offer heat pump repairs, servicing and maintenance:.1"
)


# %% [markdown]
# ### Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?You can select up to 2 reasons.
#
# Cleaning: Collapse categories.
#
# Exclusion: Answered 'Only for heat pumps I/my company have/has installed' to 'I intend to offer heat pump repairs, servicing and maintenance'.


# %%
# Temporary variable to manage joint exclusion criteria
def joint_exclusion(row):
    if (
        row["I intend to offer heat pump repairs, servicing and maintenance: (Owners)"]
        == "Not asked"
    ) & (
        row[
            "I intend to offer heat pump repairs, servicing and maintenance: (Contractor/Soletrader)"
        ]
        != "Only for heat pump systems that I have installed"
    ):
        return "Not asked"
    elif (
        row["I intend to offer heat pump repairs, servicing and maintenance: (Owners)"]
        != "Only for heat pump systems that my company has installed"
    ) & (
        row[
            "I intend to offer heat pump repairs, servicing and maintenance: (Contractor/Soletrader)"
        ]
        == "Not asked"
    ):
        return "Not asked"


data["temp_joint_exclusion"] = data[
    [
        "I intend to offer heat pump repairs, servicing and maintenance: (Owners)",
        "I intend to offer heat pump repairs, servicing and maintenance: (Contractor/Soletrader)",
    ]
].apply(joint_exclusion, axis=1)

# %%
# Bespoke exclusion filter for intended heat pump installs
exclusion_col_1 = (
    "I intend to offer heat pump repairs, servicing and maintenance: (Owners)"
)
exclusion_col_2 = "I intend to offer heat pump repairs, servicing and maintenance: (Contractor/Soletrader)"
exclusion_col_3 = "temp_joint_exclusion"

intend_repair_my_systems = {
    "filters": [
        [
            (
                exclusion_col_1,
                "==",
                "For all heat pump systems, regardless of who originally installed it",
            )
        ],
        [
            (
                exclusion_col_2,
                "==",
                "For all heat pump systems, regardless of who originally installed it",
            )
        ],
        [
            (
                exclusion_col_3,
                "==",
                "Not asked",
            )
        ],
    ],
    "columns": [exclusion_col_1, exclusion_col_2, exclusion_col_3],
}

# %%
responses = [
    "Relationship with existing customers",
    "No demand from other customers",
    "Don’t want to take responsibility for other installers’ heat pump installations",
    "I only work on equipment I understand or have been trained in",
    "Don’t know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    collapsed_column_name="Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
).pipe(
    set_not_asked_responses,
    "Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    intend_repair_my_systems["filters"],
    intend_repair_my_systems["columns"],
    [not_asked],
)

# %%
# Remove temp variable
data = data.drop(columns="temp_joint_exclusion")

# %% [markdown]
# ### Why have you previously not offered repairs, servicing and maintenance?
#
# Cleaning: Collapse categories.
#
# Exclusion: Answered No, but I intend to... to 'Do you offer repairs, servicing and maintenance to heat pump customers?'.

# %%
responses = [
    "Too little demand from customers",
    "Not profitable enough",
    "Lack the necessary skills and expertise",
    "Hard to fit into work schedule",
    "The manufacturer does it",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why have you previously not offered repairs, servicing and maintenance?",
    collapsed_column_name="Why have you previously not offered repairs, servicing and maintenance?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why have you previously not offered repairs, servicing and maintenance? Other.",
).pipe(
    set_not_asked_responses,
    "Why have you previously not offered repairs, servicing and maintenance?",
    intend_maintain["filters"],
    intend_maintain["columns"],
    [not_asked],
)

# %% [markdown]
# ### Why do you now intend to move into heat pump repairs, servicing and maintenance?
#
# Cleaning: Collapse categories.
#
# Exclusion: Answered No, but I intend to... to 'Do you offer repairs, servicing and maintenance to heat pump customers?'

# %%
responses = [
    "Growing demand from customers",
    "Servicing is increasingly profitable work",
    "Now have access to the relevant skills and expertise",
    "Issues getting the manufacturer to sort problems or visit homes",
    "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why do you now intend to move into heat pump repairs, servicing and maintenance?",
    collapsed_column_name="Why do you now intend to move into heat pump repairs, servicing and maintenance?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why do you now intend to move into heat pump repairs, servicing and maintenance? Other.",
).pipe(
    set_not_asked_responses,
    "Why do you now intend to move into heat pump repairs, servicing and maintenance?",
    intend_maintain["filters"],
    intend_maintain["columns"],
    [not_asked],
)

# %% [markdown]
# ### Why don’t you currently offer repairs, servicing and maintenance to customers?
#
# Cleaning: collapse categories.
#
# Exclusion: Responded 'no, and I do not intend...' to 'Do you offer repairs, servicing and maintenance to heat pump customers' and owners, soletrader or contractor.

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = (
    "Do you offer repairs, servicing and maintenance to heat pump customers?"
)
no_maintain = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "Yes")],
        [(exclusion_col_1, "==", "No, but I intend to offer it in the next 12 months")],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

# %%
responses = [
    "Too little demand from customers",
    "Not profitable enough",
    "Lack the necessary skills and expertise",
    "The manufacturer does it",
    "It’s difficult to manage / schedule",
    "Inadequate or slow support from manufacturers" "Don't know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why don’t you currently offer repairs, servicing and maintenance to customers?",
    collapsed_column_name="Why don’t you currently offer repairs, servicing and maintenance to customers?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why don’t you currently offer repairs, servicing and maintenance to customers? Other.",
).pipe(
    set_not_asked_responses,
    "Why don’t you currently offer repairs, servicing and maintenance to customers?",
    no_maintain["filters"],
    no_maintain["columns"],
    [not_asked],
)

# %% [markdown]
# ### Does the business you work for offer repairs, servicing and maintenance to heat pump customers?
#
# Describe: 619 null (562 not asked)
# Cleaning: cast to categorical
#
# Exclusion: Employees only.

# %%
data[
    "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
] = (
    set_not_asked_responses(
        data,
        "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?",
        employees_only["filters"],
        employees_only["columns"],
        not_asked,
    )[
        "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
    ]
    .replace("I don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Yes",
            "No, but we intend to offer it in the next 12 months",
            "No, and we do not intend to start offering this service in the next 12 months",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### The business I work for offers heat pump repairs, servicing and maintenance:
#
# Describe: 649 null (555 not asked)
# Cleaning: Cast to categorical
#
# Exclusion: Responded 'yes' to 'Does the business you work for offer repairs, servicing and maintenance to heat pump customers?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
yes_maintain = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [
            (
                exclusion_col_1,
                "==",
                "No, but we intend to offer it in the next 12 months",
            )
        ],
        [
            (
                exclusion_col_1,
                "==",
                "No, and we do not intend to start offering this service in the next 12 months",
            )
        ],
        [
            (
                exclusion_col_1,
                "==",
                "Not asked",  # carry forward not asked
            )
        ],
    ],
    "columns": [exclusion_col_1],
}

# %%
data[
    "The business I work for offers heat pump repairs, servicing and maintenance:"
] = set_not_asked_responses(
    data,
    "The business I work for offers heat pump repairs, servicing and maintenance:",
    yes_maintain["filters"],
    yes_maintain["columns"],
    not_asked,
)[
    "The business I work for offers heat pump repairs, servicing and maintenance:"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "For all heat pump systems, regardless of who originally installed it",
        "Only for heat pump systems that the business has installed",
    ],
    ordered=False,
)

# %% [markdown]
# ### Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?
#
# Cleaning: Collapse categories.
#
# Exclusion: Responded 'Only for heat pump systems that the business has installed' to 'The business I work for offers heat pump repairs, servicing and maintenance:'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = (
    "The business I work for offers heat pump repairs, servicing and maintenance:"
)

repair_my_systems = {
    "filters": [
        [
            (
                exclusion_col_1,
                "==",
                "For all heat pump systems, regardless of who originally installed it",
            )
        ],
        [
            (
                exclusion_col_1,
                "==",
                "Not asked",  # carry forward not asked
            )
        ],
    ],
    "columns": [exclusion_col_1],
}

# %%
responses = [
    "Relationship with existing customers",
    "No demand from other customers",
    "Don’t want to take responsibility for other installers’ heat pump installations",
    "Don’t know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    collapsed_column_name="Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
).pipe(
    set_not_asked_responses,
    "Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    repair_my_systems["filters"],
    repair_my_systems["columns"],
    [not_asked],
)

# %% [markdown]
# ### The business I work for intends to offer heat pump repairs, servicing and maintenance:
#
# Describe: 756 null (663 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Responded 'no, but we intend to...' to 'Does the business you work for offer repairs, servicing and maintenance to heat pump customers?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
intend_maintain = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "Yes")],
        [
            (
                exclusion_col_1,
                "==",
                "No, and we do not intend to start offering this service in the next 12 months",
            )
        ],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

# %%
data[
    "The business I work for intends to offer heat pump repairs, servicing and maintenance:"
] = set_not_asked_responses(
    data,
    "The business I work for intends to offer heat pump repairs, servicing and maintenance:",
    intend_maintain["filters"],
    intend_maintain["columns"],
    not_asked,
)[
    "The business I work for intends to offer heat pump repairs, servicing and maintenance:"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "For all heat pump systems, regardless of who originally installed it",
        "Only for heat pump systems that the business has installed",
    ],
    ordered=False,
)

# %% [markdown]
# ### Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?
#
# Cleaning: Collapse categories.
#
# Exclusion: Responded 'Only for heat pump systems that the business has installed' to 'The business I work for intends to offer heat pump repairs, servicing and maintenance:'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "The business I work for intends to offer heat pump repairs, servicing and maintenance:"

intend_repair_my_systems = {
    "filters": [
        [
            (
                exclusion_col_1,
                "==",
                "For all heat pump systems, regardless of who originally installed it",
            )
        ],
        [
            (
                exclusion_col_1,
                "==",
                "Not asked",
            )
        ],
    ],
    "columns": [exclusion_col_1],
}

# %%
responses = [
    "Relationship with existing customers",
    "No demand from other customers",
    "Don’t want to take responsibility for other installers’ heat pump installations",
    "Don’t know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    collapsed_column_name="Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
).pipe(
    set_not_asked_responses,
    "Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    intend_repair_my_systems["filters"],
    intend_repair_my_systems["columns"],
    [not_asked],
)

# %% [markdown]
# ### Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?
#
# Cleaning: Collapse categories.
#
# Exclusion:  Responded 'no, and we do not intend to...' to 'Does the business you work for offer repairs, servicing and maintenance to heat pump customers?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col_1 = "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?"
no_maintain = {
    "filters": [
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_1, "==", "Yes")],
        [
            (
                exclusion_col_1,
                "==",
                "No, but we intend to offer it in the next 12 months",
            )
        ],
        [(exclusion_col_1, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col_1],
}

# %%
responses = [
    "Relationship with existing customers",
    "No demand from other customers",
    "Don’t want to take responsibility for other installers’ heat pump installations",
    "Don’t know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?",
    collapsed_column_name="Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers? Other.",
).pipe(
    set_not_asked_responses,
    "Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?",
    no_maintain["filters"],
    no_maintain["columns"],
    [not_asked],
)

# %% [markdown]
# # Page 7 - On the job and business tools
#
# ### How often is your business unable to complete work related to a heat pump installation to the standard that you would like?
#
# Describe: 555 null (419 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: owners excluding soletraders.

# %%
data[
    "How often is your business unable to complete work related to a heat pump installation to the standard that you would like?"
] = (
    set_not_asked_responses(
        data,
        "How often is your business unable to complete work related to a heat pump installation to the standard that you would like?",
        owners_no_soletraders["filters"],
        owners_no_soletraders["columns"],
        not_asked,
    )[
        "How often is your business unable to complete work related to a heat pump installation to the standard that you would like?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Always",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### In which areas could you improve the standard of your heat pump installations?
#
# Cleaning: Collapse categories.
#
# Exclusion: Didn't answer 'Never' to 'How often is your business unable to complete work related to a heat pump installation to the standard that you would like?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col = "How often is your business unable to complete work related to a heat pump installation to the standard that you would like?"
not_never = {
    "filters": [
        [(exclusion_col, "==", "Never")],
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "More accurate heat loss calculations",
    "More accurate emitter output calculations",
    "Better or more personalised system design",
    "Speed of installation",
    "Neatness of pipework",
    "Customer education/handover",
    "Commissioning",
    "MCS, BUS DNO and other post-installation paperwork",
    "More accurate noise assessments",
    "Don't know",
    "Don’t know",
]

data = (
    collapse_select_all(
        df=data,
        select_all_columns="In which areas could you improve the standard of your heat pump installations?",
        collapsed_column_name="In which areas could you (Owners) improve the standard of your heat pump installations?",
        remove_collapsed_columns=False,
        responses=responses,
        recode_other=True,
        save_other_as_new_column=True,
        new_other_column_name="In which areas could you (Owners) improve the standard of your heat pump installations? Other.",
    )
    .pipe(
        set_not_asked_responses,
        "In which areas could you (Owners) improve the standard of your heat pump installations?",
        not_never["filters"],
        not_never["columns"],
        [not_asked],
    )
    .pipe(
        set_not_asked_responses,
        column="In which areas could you (Owners) improve the standard of your heat pump installations?",
        filters=owners_no_soletraders["filters"],
        exclusion_cols=owners_no_soletraders["columns"],
        not_asked_value=[not_asked],
    )
)

# %% [markdown]
# ### How often do you, or others in your business, use software apps and digital tools to support the business's activity?
#
# Describe: 555 null (419 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Owners excluding sole traders.

# %%
data[
    "How often do you, or others in your business, use software apps and digital tools to support the business's activity?"
] = set_not_asked_responses(
    data,
    "How often do you, or others in your business, use software apps and digital tools to support the business's activity?",
    owners_no_soletraders["filters"],
    owners_no_soletraders["columns"],
    not_asked,
)[
    "How often do you, or others in your business, use software apps and digital tools to support the business's activity?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "Never",
        "Rarely",
        "Sometimes",
        "Often",
        "Always",
    ],
    ordered=True,
)

# %% [markdown]
# ### In which areas of your business do you use software, apps or digital tools?
#
# Cleaning: Collapse categories.
#
# Exclusion:  Didn't answer 'Never' to 'How often do you, or others in your business, use software apps and digital tools to support the business's activity?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col = "How often do you, or others in your business, use software apps and digital tools to support the business's activity?"
not_never = {
    "filters": [
        [(exclusion_col, "==", "Never")],
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "Lead/job generation or sales",
    "Customer management/relations",
    "Heat loss calculations",
    "Emitter output calculations",
    "System design",
    "Generating quotes",
    "Ordering materials/equipment",
    "Adhering to building regulations",
    "Practical installation",
    "Practical aspect of commissioning",
    "Paperwork related to commissioning",
    "Handover to householders",
    "DNO registration",
    "Invoicing",
    "BUS grant application",
    "Generating documents for MCS",
    "None of the above",
]

data = (
    collapse_select_all(
        df=data,
        select_all_columns="In which areas of your business do you use software, apps or digital tools?",
        collapsed_column_name="In which areas of your business do you use software, apps or digital tools?",
        remove_collapsed_columns=True,
        responses=responses,
        recode_other=True,
        save_other_as_new_column=True,
        new_other_column_name="In which areas of your business do you use software, apps or digital tools? Other.",
    )
    .pipe(
        set_not_asked_responses,
        "In which areas of your business do you use software, apps or digital tools?",
        not_never["filters"],
        not_never["columns"],
        [not_asked],
    )
    .pipe(
        set_not_asked_responses,
        column="In which areas of your business do you use software, apps or digital tools?",
        filters=owners_no_soletraders["filters"],
        exclusion_cols=owners_no_soletraders["columns"],
        not_asked_value=[not_asked],
    )
)

# %% [markdown]
# ### How often are you unable to complete work related to a heat pump installation to the standard that you would like?
#
# Describe: 555 null (342 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Contractors, employees and soletraders only.

# %%
data[
    "How often are you unable to complete work related to a heat pump installation to the standard that you would like?"
] = (
    set_not_asked_responses(
        data,
        "How often are you unable to complete work related to a heat pump installation to the standard that you would like?",
        employees_contractors_soletraders["filters"],
        employees_contractors_soletraders["columns"],
        not_asked,
    )[
        "How often are you unable to complete work related to a heat pump installation to the standard that you would like?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Always",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### In which areas could you improve the standard of your heat pump installations?
#
# Cleaning: Collapse categories.
#
# Exclusion: Didn't answer 'Never' to 'How often is your business unable to complete work related to a heat pump installation to the standard that you would like?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col = "How often are you unable to complete work related to a heat pump installation to the standard that you would like?"
not_never = {
    "filters": [
        [(exclusion_col, "==", "Never")],
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "More accurate heat loss calculations",
    "More accurate emitter output calculations",
    "Better or more personalised system design",
    "Speed of installation",
    "Neatness of pipework",
    "Customer education/handover",
    "Commissioning",
    "MCS, BUS DNO and other post-installation paperwork",
    "More accurate noise assessments",
    "Don't know",
    "Don’t know",
]

data = (
    collapse_select_all(
        df=data,
        select_all_columns="In which areas could you improve the standard of your heat pump installations?",
        collapsed_column_name="In which areas could you (Employee, Contractor, Sole trader) improve the standard of your heat pump installations?",
        remove_collapsed_columns=True,
        responses=responses,
        recode_other=True,
        save_other_as_new_column=True,
        new_other_column_name="In which areas could you (Employee, Contractor, Sole trader) improve the standard of your heat pump installations? Other.",
    )
    .pipe(
        set_not_asked_responses,
        "In which areas could you (Employee, Contractor, Sole trader) improve the standard of your heat pump installations?",
        not_never["filters"],
        not_never["columns"],
        [not_asked],
    )
    .pipe(
        set_not_asked_responses,
        column="In which areas could you (Employee, Contractor, Sole trader) improve the standard of your heat pump installations?",
        filters=employees_contractors_soletraders["filters"],
        exclusion_cols=employees_contractors_soletraders["columns"],
        not_asked_value=[not_asked],
    )
)

# %% [markdown]
# ### How often do you use software, apps and digital tools to support you with your work?
#
# Describe: 555 null (342 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Contractors, employees and soletraders only.

# %%
data[
    "How often do you use software, apps and digital tools to support you with your work?"
] = set_not_asked_responses(
    data,
    "How often do you use software, apps and digital tools to support you with your work?",
    employees_contractors_soletraders["filters"],
    employees_contractors_soletraders["columns"],
    not_asked,
)[
    "How often do you use software, apps and digital tools to support you with your work?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "Never",
        "Rarely",
        "Sometimes",
        "Often",
        "Always",
    ],
    ordered=True,
)

# %% [markdown]
# ### In which areas of your work do you use software, apps or digital tools?
#
# Cleaning: Collapse categories.
#
# Exclusion:  Didn't answer 'Never' to How often do you use software, apps and digital tools to support you with your work?'

# %%
# Bespoke exclusion filter for heat pump installs
exclusion_col = "How often do you use software, apps and digital tools to support you with your work?"
not_never = {
    "filters": [
        [(exclusion_col, "==", "Never")],
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "Lead/job generation or sales",
    "Customer management/relations",
    "Heat loss calculations",
    "Emitter output calculations",
    "System design",
    "Generating quotes",
    "Ordering materials/equipment",
    "Adhering to building regulations",
    "Practical installation",
    "Practical aspect of commissioning",
    "Paperwork related to commissioning",
    "Handover to householders",
    "DNO registration",
    "Invoicing",
    "BUS grant application",
    "Generating documents for MCS",
    "None of the above",
]

data = (
    collapse_select_all(
        df=data,
        select_all_columns="In which areas of your work do you use software, apps or digital tools?",
        collapsed_column_name="In which areas of your work do you use software, apps or digital tools?",
        remove_collapsed_columns=True,
        responses=responses,
        recode_other=True,
        save_other_as_new_column=True,
        new_other_column_name="In which areas of your work do you use software, apps or digital tools? Other.",
    )
    .pipe(
        set_not_asked_responses,
        "In which areas of your work do you use software, apps or digital tools?",
        not_never["filters"],
        not_never["columns"],
        [not_asked],
    )
    .pipe(
        set_not_asked_responses,
        column="In which areas of your work do you use software, apps or digital tools?",
        filters=employees_contractors_soletraders["filters"],
        exclusion_cols=employees_contractors_soletraders["columns"],
        not_asked_value=[not_asked],
    )
)

# %% [markdown]
# ### How would you describe existing software, apps and digital tools in terms of the following?
#
# Cleaning: Cast to categorical for each row of grid.
#
# Exclusion: All asked.

# %%
columns = data.columns[
    data.columns.str.contains(
        "How would you describe existing software, apps and digital tools in terms of the following?"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"How would you describe existing software, apps and digital tools in terms of: {task}"
    ] = (
        data[col]
        .replace("Don’t know", "Don't know")
        .pipe(
            pandas.Categorical,
            categories=[
                "Don't know",
                "Very poor",
                "Poor",
                "Fair/Neutral",
                "Good",
                "Very good",
            ],
            ordered=True,
        )
    )

data = data.drop(columns=columns)

# %% [markdown]
# ### In which areas of your business do you think extra support could be most helpful?
#
# Cleaning: Cast to categorical for each row of grid.
#
# Exclusion: Only owners asked (excluding sole traders)

# %%
columns = data.columns[
    data.columns.str.contains(
        "In which areas of your business do you think extra support could be most helpful\?$"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"In which areas of your business (owners) do you think extra support could be most helpful: {task}"
    ] = (
        set_not_asked_responses(
            data, col, owners_only["filters"], owners_only["columns"], not_asked
        )[col]
        .replace("Don’t know", "Don't know")
        .replace("Don’t need support", "Don't need support")
        .pipe(
            pandas.Categorical,
            categories=[
                "Not asked",
                "Digital tools",
                "Staff",
                "Digital tools and staff",
                "Don't need support",
                "Don't know",
            ],
            ordered=False,
        )
    )

# Remove raw fields.
data = data.drop(columns=columns)

# %% [markdown]
# ### In which areas of your business do you think extra support could be most helpful?
#
# Cleaning: Cast to categorical for each row of grid.
#
# Exclusion: Only sole traders.

# %%
columns = data.columns[
    data.columns.str.contains(
        "In which areas of your business do you think extra support could be most helpful\?"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"In which areas of your business (sole traders) do you think extra support could be most helpful: {task}"
    ] = (
        set_not_asked_responses(
            data,
            col,
            soletraders_only["filters"],
            soletraders_only["columns"],
            not_asked,
        )[col]
        .replace("Don’t know", "Don't know")
        .replace("Don’t need support", "Don't need support")
        .pipe(
            pandas.Categorical,
            categories=[
                "Not asked",
                "Digital tools",
                "Staff",
                "Digital tools and staff",
                "Don't need support",
                "Don't know",
            ],
            ordered=False,
        )
    )

# Remove raw fields.
data = data.drop(columns=columns)

# %% [markdown]
# ### In which areas of your work do you think extra support could be most helpful?
#
# Cleaning: Cast to categorical for each row of grid.
#
# Exclusion: Only employees.

# %%
# NB regex has to additionally exclude the contractor job ops response which is not asked to employees
columns = data.columns[
    data.columns.str.contains(
        "(?<!Finding contractor job opportunities:)In which areas of your work do you think extra support could be most helpful\?$"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"In which areas of your work (employee) do you think extra support could be most helpful: {task}"
    ] = (
        set_not_asked_responses(
            data, col, employees_only["filters"], employees_only["columns"], not_asked
        )[col]
        .replace("Don’t know", "Don't know")
        .replace("Don’t need support", "Don't need support")
        .pipe(
            pandas.Categorical,
            categories=[
                "Not asked",
                "Digital tools",
                "Staff",
                "Digital tools and staff",
                "Don't need support",
                "Don't know",
            ],
            ordered=False,
        )
    )

# Remove raw fields.
data = data.drop(columns=columns)

# %% [markdown]
# ### In which areas of your work do you think extra support could be most helpful?
#
# Cleaning: Cast to categorical for each row of grid.
#
# Exclusion: Only contractors.

# %%
columns = data.columns[
    data.columns.str.contains(
        "In which areas of your work do you think extra support could be most helpful\?"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"In which areas of your work (contractor) do you think extra support could be most helpful: {task}"
    ] = (
        set_not_asked_responses(
            data,
            col,
            contractors_only["filters"],
            contractors_only["columns"],
            not_asked,
        )[col]
        .replace("Don’t know", "Don't know")
        .replace("Don’t need support", "Don't need support")
        .pipe(
            pandas.Categorical,
            categories=[
                "Not asked",
                "Digital tools",
                "Staff",
                "Digital tools and staff",
                "Don't need support",
                "Don't know",
            ],
            ordered=False,
        )
    )

# Remove raw fields.
data = data.drop(columns=columns)

# %% [markdown]
# ### What do you find most challenging about the final stages of the installation and the customer handover?
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="What do you find most challenging about the final stages of the installation and the customer handover?",
    collapsed_column_name="What do you find most challenging about the final stages of the installation and the customer handover? You can select up to 3 responses.",
    remove_collapsed_columns=True,
)

# %% [markdown]
# ### How do you manage the design for the majority of your heat pump installations?
#
# Describe: 383 null (88 not asked)
# Cleaning: Cast to categorical
#
# Exclusion: All except contractors.

# %%
data[
    "How do you (owners and employees) manage the design for the majority of your heat pump installations?"
] = (
    set_not_asked_responses(
        data,
        "How do you manage the design for the majority of your heat pump installations?",
        owners_employees["filters"],
        owners_employees["columns"],
        not_asked,
    )["How do you manage the design for the majority of your heat pump installations?"]
    .replace("Don’t know", "Don't know")
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Other",
            "Done in house",
            "Outsourced to external designers",
            "Outsourced to umbrella scheme",
        ],
        ordered=False,
    )
)

data = data.drop(
    columns="How do you manage the design for the majority of your heat pump installations?"
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):How do you manage the design for the majority of your heat pump installations?": "How do you (owners and employees) manage the design for the majority of your heat pump installations? Other"
    }
)

# %% [markdown]
# ### How do you manage the design for the majority of your heat pump installations?
#
# Describe: 733 null (673 not asked)
# Cleaning: Cast to categorical
#
# Exclusion: Contractors only.

# %%
data[
    "How do you (contractors) manage the design for the majority of your heat pump installations?"
] = (
    set_not_asked_responses(
        data,
        "How do you manage the design for the majority of your heat pump installations?.1",
        contractors_only["filters"],
        contractors_only["columns"],
        not_asked,
    )[
        "How do you manage the design for the majority of your heat pump installations?.1"
    ]
    .replace("I’m", "I'm", regex=True)
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Other",
            "I do it",
            "The company for which I'm working does it in house",
            "The company for which I'm working outsources it to external designers",
            "The company for which I'm working outsources it to an umbrella scheme",
        ],
        ordered=False,
    )
)

data = data.drop(
    columns="How do you manage the design for the majority of your heat pump installations?.1"
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):How do you manage the design for the majority of your heat pump installations?.1": "How do you (contractors) manage the design for the majority of your heat pump installations? Other"
    }
)

# %% [markdown]
# ### Which design software or platform do you use?
#
# Cleaning: Collapse categories.
#
# Exclusion: Must have answered 'in house' to 'How do you (owners and employees) manage the design for the majority of your heat pump installations?' or 'I do it' to 'How do you (contractors) manage the design for the majority of your heat pump installations?'

# %%
# Bespoke exclusion filter for in house design
exclusion_col_1 = "How do you (owners and employees) manage the design for the majority of your heat pump installations?"
exclusion_col_2 = "How do you (contractors) manage the design for the majority of your heat pump installations?"

design_in_house = {
    "filters": [
        [(exclusion_col_1, "==", "Outsourced to external designers")],
        [(exclusion_col_1, "==", "Outsourced to umbrella scheme")],
        [(exclusion_col_1, "==", "Other")],
        [(exclusion_col_1, "==", "Don't know")],
        [(exclusion_col_2, "==", "The company for which I'm working does it in house")],
        [
            (
                exclusion_col_2,
                "==",
                "The company for which I'm working outsources it to external designers",
            )
        ],
        [
            (
                exclusion_col_2,
                "==",
                "The company for which I'm working outsources it to an umbrella scheme",
            )
        ],
        [(exclusion_col_2, "==", "Other")],
        [(exclusion_col_2, "==", "Don't know")],
    ],
    "columns": [exclusion_col_1, exclusion_col_2],
}

# %%
responses = [
    "Heat Engineer",
    "Heat Geek",
    "MCS sizing calculator",
    "Manufacturer-specific tools",
    "Own bespoke",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Which design software or platform do you use?",
    collapsed_column_name="Which design software or platform do you use? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Which design software or platform do you use? Other.",
).pipe(
    set_not_asked_responses,
    "Which design software or platform do you use? Select all that apply.",
    design_in_house["filters"],
    design_in_house["columns"],
    [not_asked],
)

# %% [markdown]
# # Page 8 - Staffing and expansion
#
# NB This page of questions is only asked to owners including sole traders.
#
# ### We want to understand how you obtain the skills you need. How do you source the following skills?
#
# Cleaning: This is a checkbox matrix. We want to collapse categories row-wise.
#
# Exclusion: Owners and soletraders only.
#
# The survey item has a conditional for the 'family' response, however because we're not capturing the boxes that people don't check there's no useful way of capturing when people were eligible but didn't check the box. If relevant, we'll capture or adjust in the analysis.

# %%
rows = [
    "Business administration",
    "System design",
    "Installation of the heat pump system \(including heat pump unit, pipes, emitters\)",
    "Commissioning",
    "MCS and post install documentation",
    "Service and maintenance on site",
    "Customer support off site",
]

for row in rows:
    data = collapse_select_all(
        df=data,
        select_all_columns=f"{row}:We want to understand how you obtain the skills you need. How do you source the following skills?",
        collapsed_column_name=f"How do you source the following skills? {row}",
        remove_collapsed_columns=True,
    ).pipe(
        set_not_asked_responses,
        f"How do you source the following skills? {row}",
        owners_only["filters"],
        owners_only["columns"],
        [not_asked],
    )
    # deduplicate responses
    data[f"How do you source the following skills? {row}"] = data[
        f"How do you source the following skills? {row}"
    ].apply(lambda x: list(set(x)))

# %% [markdown]
# ### If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?
#
# Describe: 542 null (323 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and Soletraders only.

# %%
data[
    "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?Please select one option.",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?Please select one option."
    ]
    .replace("Don’t know", "Don't know")
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Other",
            "Heat loss surveying and calculations",
            "Heating system designer",
            "Plumbing skills",
            "Electrical skills",
            "F-Gas skills",
            "Gas heating skills",
            "Administration skills",
            "Sales and marketing skills",
            "Customer service skills",
        ],
        ordered=False,
    )
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?Please select one option.": "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this? Other."
    }
)

# %% [markdown]
# ### For the role you selected above, what experience level would you most like to recruit?
#
# Describe: 554 null (335 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Must have answered other than "Don't know" to previous question: 'If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?''

# %%
# Bespoke exclusion filter for don't knows
exclusion_col = "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?Please select one option."

dont_know = {
    "filters": [
        [(exclusion_col, "==", "Don't know")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
data[
    "For the role you selected above, what experience level would you most like to recruit?"
] = set_not_asked_responses(
    data,
    "For the role you selected above, what experience level would you most like to recruit?",
    dont_know["filters"],
    dont_know["columns"],
    not_asked,
)[
    "For the role you selected above, what experience level would you most like to recruit?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Don't know",
        "An apprentice",
        "First job applicants",
        "Junior level staff (1-3 years work experience)",
        "Mid-level staff (3-5 years work experience)",
        "Experienced staff (over 5 years experience)",
    ],
    ordered=False,
)

# %% [markdown]
# ### How likely are you to directly employ new staff in the next 12 months?
#
# Describe: 542 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion:  Owners including soletraders.

# %%
data["How likely are you to directly employ new staff in the next 12 months?"] = (
    set_not_asked_responses(
        data,
        "How likely are you to directly employ new staff in the next 12 months?",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )["How likely are you to directly employ new staff in the next 12 months?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Very unlikely",
            "Unlikely",
            "Neutral",
            "Likely",
            "Very likely",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### How likely are you to subcontract new staff in the next 12 months?
#
# Describe: 542 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion:  Owners including soletraders.

# %%
data["How likely are you to subcontract new staff in the next 12 months?"] = (
    set_not_asked_responses(
        data,
        "How likely are you to subcontract new staff in the next 12 months?",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )["How likely are you to subcontract new staff in the next 12 months?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Very unlikely",
            "Unlikely",
            "Neutral",
            "Likely",
            "Very likely",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?
#
# Describe: 659 null (453 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Owners including soletraders. Additionally, respondents must have indicated that they work with family members via "Do you work with family members in any of the following ways? Select all that apply." Qualifying responses are any of: Employ family directly;
# Own the business in partnership
# Operate a limited compa; y
# Receive informal, ad hoc, h; lp
# Subcontract family mem.
#
# Notably, 21 responses include "I don't work with family members" and at least 1 other response that suggests they do. Of these, 10 then gave a response to this question (+ 11 missing responses). These are included as they will have been asked the question, however a small amount of missing data is introduced.bers

# %%
data[
    "How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?"
] = (
    set_not_asked_responses(
        data,
        "How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Very unlikely",
            "Unlikely",
            "Neutral",
            "Likely",
            "Very likely",
        ],
        ordered=True,
    )
)

# %%
# Add family-based exclusion information
data.loc[
    lambda df: ~(
        df[
            "Do you work with family members in any of the following ways? Select all that apply."
        ].apply(
            lambda x: True
            if (
                ("Employ family directly" in x)
                | ("Own the business in partnership" in x)
                | ("Operate a limited company" in x)
                | ("Receive informal, ad hoc, help" in x)
                | ("Subcontract family members" in x)
                | (len(x) == 0)
            )
            else False
        )
    ),
    "How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?",
] = data.loc[
    lambda df: ~(
        df[
            "Do you work with family members in any of the following ways? Select all that apply."
        ].apply(
            lambda x: True
            if (
                ("Employ family directly" in x)
                | ("Own the business in partnership" in x)
                | ("Operate a limited company" in x)
                | ("Receive informal, ad hoc, help" in x)
                | ("Subcontract family members" in x)
                | (len(x) == 0)
            )
            else False
        )
    ),
    "Response ID",
].apply(
    lambda _: not_asked
)

# %% [markdown]
# ### If you were looking for new staff, which of the following would you prefer?Please select one option.
#
# Describe: 542 null (323 not asked) Cleaning: Cast to categorical.
#
# Exclusion: Owners including soletraders.

# %%
data[
    "If you were looking for new staff, which of the following would you prefer?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "If you were looking for new staff, which of the following would you prefer?Please select one option.",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "If you were looking for new staff, which of the following would you prefer?Please select one option."
    ]
    .replace(
        "I wouldn’t want to increase my staff capacity",
        "I wouldn't want to increase my staff capacity",
    )
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Recruit new permanent staff",
            "Recruit new temporary staff (1-12 month contract)",
            "Subcontract a contractor for specific projects",
            "Recruit immediate family members",
            "Other",
            "I wouldn't want to increase my staff capacity",
        ],
        ordered=False,
    )
)

# Rename other category
data = data.rename(
    columns={
        "Other (please specify):If you were looking for new staff, which of the following would you prefer?Please select one option.": "If you were looking for new staff, which of the following would you prefer? Other."
    }
)

# %% [markdown]
# ### If you were looking for new staff, what are the biggest barriers to taking on new directly employed staff?
#
# Cleaning: Collapse categories.
#
# Exclusion: owners and soletraders only.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="If you were looking for new staff, what are the biggest barriers to taking on new directly employed staff?",
    collapsed_column_name="If you were looking for new staff, what are the biggest barriers to taking on new directly employed staff?",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "If you were looking for new staff, what are the biggest barriers to taking on new directly employed staff?",
    owners_only["filters"],
    owners_only["columns"],
    [not_asked],
)

# %% [markdown]
# ### If you were looking for new staff, what are the biggest barriers to subcontracting staff?
#
# Cleaning: Collapse categories.
#
# Exclusion: owners and soletraders only.

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="If you were looking for new staff, what are the biggest barriers to subcontracting staff?",
    collapsed_column_name="If you were looking for new staff, what are the biggest barriers to subcontracting staff?",
    remove_collapsed_columns=True,
).pipe(
    set_not_asked_responses,
    "If you were looking for new staff, what are the biggest barriers to subcontracting staff?",
    owners_only["filters"],
    owners_only["columns"],
    [not_asked],
)

# %% [markdown]
# # Page 9 - Apprenticeships and entry level installer roles
#
# NB This page of questions is only asked to owners including sole traders.
#
# ### Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?
#
# Describe: 549 null (323 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and soletraders only.

# %%
data[
    "Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?"
] = set_not_asked_responses(
    data,
    "Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?",
    owners_only["filters"],
    owners_only["columns"],
    not_asked,
)[
    "Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?"
].pipe(
    pandas.Categorical,
    categories=[
        "Not asked",
        "Yes",
        "No, but I intend on doing so in the next 12 months",
        "No, and I do not intend to do so in the next 12 months",
    ],
    ordered=False,
)

# %% [markdown]
# ### What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations?
#
# Cleaning: Collapse categories.
#
# Exclusion: Must have answered 'Yes' to 'Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?'.

# %%
# Bespoke exclusion filter for apprentices
exclusion_col = "Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?"

yes_apprentice = {
    "filters": [
        [(exclusion_col, "==", "No, but I intend on doing so in the next 12 months")],
        [
            (
                exclusion_col,
                "==",
                "No, and I do not intend to do so in the next 12 months",
            )
        ],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "It was hard to find the right apprentice to fit with the role",
    "I didn’t know where to recruit an apprentice from",
    "There were no colleges delivering relevant apprenticeship training near me",
    "There are no colleges delivering apprenticeship training of a high enough quality near me",
    "Having an apprentice has slowed down my work",
    "Having an apprentice has cost my business too much",
    "It took too long to recruit an apprentice",
    "I needed more guidance on how to properly support an apprentice in their work",
    "I needed more guidance on the administration associated with working with an apprentice",
    "I don’t face any challenges",
]

data = collapse_select_all(
    df=data,
    select_all_columns="What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations?",
    collapsed_column_name="What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations? Other.",
).pipe(
    set_not_asked_responses,
    "What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations?",
    yes_apprentice["filters"],
    yes_apprentice["columns"],
    [not_asked],
)

# %% [markdown]
# ### What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations?
#
# Cleaning: Collapse categories.
#
# Exclusion: Must have answered 'No...' to 'Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?'.

# %%
# Bespoke exclusion filter for apprentices
exclusion_col = "Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?"

no_apprentice = {
    "filters": [
        [(exclusion_col, "==", "Yes")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "It’s hard to find the right apprentice to fit with the role",
    "I don’t know where to recruit an apprentice from",
    "There are no colleges delivering relevant apprenticeship training near me",
    "There’s no colleges delivering apprenticeship training of a high enough quality near me",
    "Having an apprentice will slow down my work",
    "Having an apprentice will cost my business too much",
    "It takes too long to recruit an apprentice",
    "I need more guidance on how to properly support an apprentice in their work",
    "I need more guidance on the administration associated with working with an apprentice",
    "I don’t forsee any challenges",
]

data = collapse_select_all(
    df=data,
    select_all_columns="What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations?",
    collapsed_column_name="What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations? Other.",
).pipe(
    set_not_asked_responses,
    "What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations?",
    no_apprentice["filters"],
    no_apprentice["columns"],
    [not_asked],
)

# %% [markdown]
# ### How confident are you that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work for you?
#
# Describe: 549 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and soletraders only.

# %%
data[
    "How confident are you that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work for you?"
] = (
    set_not_asked_responses(
        data,
        "How confident are you that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work for you?",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "How confident are you that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work for you?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Not at all confident",
            "Not very confident",
            "Somewhat confident",
            "Confident",
            "Very confident",
        ],
        ordered=True,
    )
)

# %% [markdown]
# ### If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations?
#
# Cleaning: Collapse categories.
#
# Exclusion: Owners and soletraders only.

# %%
responses = [
    "Ability to do complete heat loss calculations and surveys",
    "Ability to design heat pump systems",
    "Ability to do a satisfactory install unaccompanied (with a check at the end)",
    "Ability to do individual elements of an install unaccompanied (with a check between each part)",
    "Admin and paperwork related to the project they’re working on",
    "Customer service",
    "Quotes and sales",
    "Don’t know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations?",
    collapsed_column_name="If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations? Other.",
).pipe(
    set_not_asked_responses,
    "If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations?",
    owners_only["filters"],
    owners_only["columns"],
    [not_asked],
)

# %% [markdown]
# ### What do you think could be most improved from the training that plumbing and heating apprentices receive?Please select one option.
#
# Describe: 550 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and sole traders only.

# %%
data[
    "What do you think could be most improved from the training that plumbing and heating apprentices receive?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "What do you think could be most improved from the training that plumbing and heating apprentices receive?Please select one option.",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "What do you think could be most improved from the training that plumbing and heating apprentices receive?Please select one option."
    ]
    .replace("Don’t know", "Don't know")
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Other",
            "Practical general plumbing skills",
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
        ],
        ordered=False,
    )
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):What do you think could be most improved from the training that plumbing and heating apprentices receive?Please select one option.": "What do you think could be most improved from the training that plumbing and heating apprentices receive? Other."
    }
)

# %% [markdown]
# ### If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?
#
# Describe: 550 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and soletraders only.

# %%
data[
    "If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?"
] = (
    set_not_asked_responses(
        data,
        "If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Don't know",
            "Very unlikely",
            "Unlikely",
            "Neutral",
            "Likely",
            "Very likely",
        ],
        ordered=False,
    )
)

# %% [markdown]
# ### Why might you choose to take on someone with vocational experience over paper qualifications?Please select one option.
#
# Describe: 550 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and sole traders only.

# %%
data[
    "Why might you choose to take on someone with vocational experience over paper qualifications?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "Why might you choose to take on someone with vocational experience over paper qualifications?Please select one option.",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "Why might you choose to take on someone with vocational experience over paper qualifications?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Other",
            "Shows commitment to the job",
            "I would be more confident in their ability to do the job",
            "I would save time on training them",
            "I would save money on training them",
            "I see no advantages",
        ],
        ordered=False,
    )
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):Why might you choose to take on someone with vocational experience over paper qualifications?Please select one option.": "Why might you choose to take on someone with vocational experience over paper qualifications? Other."
    }
)

# %% [markdown]
# ### Why might you choose to take on someone with only paper qualifications?Please select one option.
#
# Describe: 550 null (323 not asked).
# Cleaning: Cast to categorical.
#
# Exclusion: Owners and sole traders only.

# %%
data[
    "Why might you choose to take on someone with only paper qualifications?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "Why might you choose to take on someone with only paper qualifications?Please select one option.",
        owners_only["filters"],
        owners_only["columns"],
        not_asked,
    )[
        "Why might you choose to take on someone with only paper qualifications?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Other",
            "There is a shortage of staff with practical experience to recruit",
            "I prefer to train my own staff to get the training right",
            "It is cheaper",
            "I have a personal recommendation as to the quality of this candidate",
            "I would not choose to take on such a person",
        ],
        ordered=False,
    )
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):Why might you choose to take on someone with only paper qualifications?Please select one option.": "Why might you choose to take on someone with only paper qualifications? Other."
    }
)

# %% [markdown]
# ### What might further encourage you most to take on someone with only paper qualifications?Please select one option.
#
# Describe: 753 null (446 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Must have answered likely or very likely to 'If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?'

# %%
# Bespoke exclusion filter for paper quals
exclusion_col = "If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?"

likely_paper_quals = {
    "filters": [
        [(exclusion_col, "==", "Don't know")],
        [(exclusion_col, "==", "Neutral")],
        [(exclusion_col, "==", "Unlikely")],
        [(exclusion_col, "==", "Very Unlikely")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
data[
    "What might further encourage you most to take on someone with only paper qualifications?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "What might further encourage you most to take on someone with only paper qualifications?Please select one option.",
        likely_paper_quals["filters"],
        likely_paper_quals["columns"],
        not_asked,
    )[
        "What might further encourage you most to take on someone with only paper qualifications?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Other",
            "Financial support for salary for a limited period",
            "Financial support for onboarding costs",
            "Financial support for training",
            "Certainty that the person will work with my company for a defined period",
            "I would not choose to take on such a person",
        ],
        ordered=False,
    )
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):What might further encourage you most to take on someone with only paper qualifications?Please select one option.": "What might further encourage you most to take on someone with only paper qualifications? Other."
    }
)

# %% [markdown]
# ### What might encourage you most to take on someone with only paper qualifications?Please select one option.
#
# Describe: 571 null (344 not asked)
# Cleaning: Cast to categorical.
#
# Exclusion: Must have answered neutral or unlikely very unlikely to 'If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?'

# %%
# Bespoke exclusion filter for paper quals
exclusion_col = "If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?"

unlikely_paper_quals = {
    "filters": [
        [(exclusion_col, "==", "Don't know")],
        [(exclusion_col, "==", "Likely")],
        [(exclusion_col, "==", "Very likely")],
        [(exclusion_col, "==", "Not asked")],  # carry forward not asked
    ],
    "columns": [exclusion_col],
}

# %%
data[
    "What might encourage you most to take on someone with only paper qualifications?Please select one option."
] = (
    set_not_asked_responses(
        data,
        "What might encourage you most to take on someone with only paper qualifications?Please select one option.",
        unlikely_paper_quals["filters"],
        unlikely_paper_quals["columns"],
        not_asked,
    )[
        "What might encourage you most to take on someone with only paper qualifications?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Not asked",
            "Other",
            "Financial support for salary for a limited period",
            "Financial support for onboarding costs",
            "Financial support for training",
            "Certainty that the person will work with my company for a defined period",
            "I would not choose to take on such a person",
        ],
        ordered=False,
    )
)

# Rename the other column
data = data.rename(
    columns={
        "Other (please specify):What might encourage you most to take on someone with only paper qualifications?Please select one option.": "What might encourage you most to take on someone with only paper qualifications? Other."
    }
)

# %% [markdown]
# # Page 10 - Customer demand/interest
#
# NB All respondents asked.
#
# ### What proportion of heat pump enquiries result in generating a comprehensive quote for works?
#
# Describe: 397 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "What proportion of heat pump enquiries result in generating a comprehensive quote for works?"
] = (
    data[
        "What proportion of heat pump enquiries result in generating a comprehensive quote for works?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Don't know",
            "Very few (10% or under)",
            "Less than half",
            "More than half",
            "Almost all (90-100%)",
        ],
    )
)

# %% [markdown]
# ### What proportion of comprehensive quotes for works result in installations?
#
# Describe: 397 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data["What proportion of comprehensive quotes for works result in installations?"] = (
    data["What proportion of comprehensive quotes for works result in installations?"]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Don't know",
            "Very few (10% or under)",
            "Less than half",
            "More than half",
            "Almost all (90-100%)",
        ],
    )
)

# %% [markdown]
# ### What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote?Please select one option.
#
# Describe: 397 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote?Please select one option."
] = (
    data[
        "What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote?Please select one option."
    ]
    .replace("Don’t know", "Don't know")
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Don't know",
            "Other",
            "Cheaper quote from another installer",
            "Cost is too high across all quotes so the customer abandons their heat pump project",
            "Running cost estimates are too high",
            "Inconvenience of works",
            "Planning permission challenges",
            "Issues with the DNO",
            "Supply chain delays or equipment availability",
            "Inability to do the installation to meet client timescales",
        ],
    )
)

# rename other column
data = data.rename(
    columns={
        "Other (please specify):What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote?Please select one option.": "What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote? Other."
    }
)

# %% [markdown]
# ### How frequently do you have to decline viable heat pump installation work because you don’t have the capacity to do it?
#
# Describe: 397 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "How frequently do you have to decline viable heat pump installation work because you don’t have the capacity to do it?"
] = (
    data[
        "How frequently do you have to decline viable heat pump installation work because you don’t have the capacity to do it?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Don't know",
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Very often",
        ],
    )
)

# %% [markdown]
# ### Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it?Select all that apply.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "Believe the cost will put the customer off",
    "Do not believe a heat pump will sufficiently heat their home",
    "Believe the customer will not like the necessary radiator upgrades",
    "Believe the job will take you too long",
    "Believe the job will be too risky for your company",
    "Do not wish to work with this customer",
    "I have never declined work in this way",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it?",
    collapsed_column_name="Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it? Other.",
)

# %% [markdown]
# ### Do you ever feel your customer service is of a lower quality than you would like?
#
# Describe: 398 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "Do you ever feel your customer service is of a lower quality than you would like?"
] = (
    data[
        "Do you ever feel your customer service is of a lower quality than you would like?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=["Don't know", "Never", "Rarely", "Sometimes", "Often", "Always"],
    )
)

# %% [markdown]
# ### In which areas could you improve your standards to help you provide a better service to your customers?You can select up to 3 options.
#
# Cleaning: Collapse categories.
#
# Exclusion: Gave answer other than 'never' to 'Do you ever feel your customer service is of a lower quality than you would like?'

# %%
# Bespoke exclusion filter for customer service
exclusion_col = (
    "Do you ever feel your customer service is of a lower quality than you would like?"
)
cust_service = {
    "filters": [
        [(exclusion_col, "==", "Never")],
    ],
    "columns": [exclusion_col],
}

# %%
responses = [
    "Improve my responses to customer queries",
    "Provide better information on potential heat pump installation costs upfront",
    "Help potential customers to better understand how heat pumps work",
    "Give customers clearer information on the installation duration",
    "Give customers clearer information on the installation process",
    "Give customers clearer information on estimated running costs",
    "Improve my commissioning and handover processes",
    "Improve my aftercare and annual servicing offer",
    "Don’t know",
]

data = collapse_select_all(
    df=data,
    select_all_columns="In which areas could you improve your standards to help you provide a better service to your customers?",
    collapsed_column_name="In which areas could you improve your standards to help you provide a better service to your customers?",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="In which areas could you improve your standards to help you provide a better service to your customers? Other.",
).pipe(
    set_not_asked_responses,
    "In which areas could you improve your standards to help you provide a better service to your customers?",
    cust_service["filters"],
    cust_service["columns"],
    [not_asked],
)

# %% [markdown]
# # Page 11 - Your own training
#
# NB All asked.
#
# ### What training or certification do you have?Select all that apply.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "Full Apprenticeship in Related Industry (Heating & Plumbing etc.)",
    "Level 2 NVQ/SVQ in related industry",
    "On the job experience / Journey Man / Grandfather Rights",
    "Level 3 BPEC",
    "LCL in Heat Pumps",
    "Low Temperature Systems qualifications",
    "Part L",
    "Installer-led training online (such as Heat Geek)",
    "Installer-led training in person (such as Kimbo Betty)",
    "Manufacturer-led Training - Online",
    "Manufacturer-led Training - In Person",
    "F-Gas",
    "Water regulations",
    "Qualified Electrician - 18th Edition",
    "Part P",
    "Gas Safe Registered",
    "Oftec certified",
    "G3 building regs qualification",
    "CSCS card or similar",
    "JIB card",
    "NAPIT",
    "SNIPEF",
    "HETAS",
]

data = collapse_select_all(
    df=data,
    select_all_columns="What training or certification do you have?",
    collapsed_column_name="What training or certification do you have? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="What training or certification do you have? Other.",
)

# %% [markdown]
# ### With the skills you’ve gained from the formal training you’ve done so far, how prepared do you feel for your current heat pump installation work?
#
# Describe: 402 null
# Cleaning: cast to categorical.
#
# Exclusion: All Asked.

# %%
data[
    "With the skills you’ve gained from the formal training you’ve done so far, how prepared do you feel for your current heat pump installation work?"
] = (
    data[
        "With the skills you’ve gained from the formal training you’ve done so far, how prepared do you feel for your current heat pump installation work?"
    ]
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Don't know",
            "Very unprepared",
            "Unprepared",
            "Neutral",
            "Prepared",
            "Very prepared",
        ],
    )
)

# %% [markdown]
# ### If there are areas in which your formal training has not been sufficient, how have you addressed these gaps?Select all that apply.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "I find further training courses",
    "I seek informal advice from colleagues",
    "I learn on the job through trial and error",
    "I find information on social media eg on Facebook, YouTube or Twitter",
    "I get knowledge from industry magazines, websites or email lists",
    "I speak to exhibitors at trade shows and conferences",
    "Manufacturers’ technical support via website or phone",
    "I haven’t found a solution",
    "My formal training was sufficient",
]

data = collapse_select_all(
    df=data,
    select_all_columns="If there are areas in which your formal training has not been sufficient, how have you addressed these gaps?",
    collapsed_column_name="If there are areas in which your formal training has not been sufficient, how have you addressed these gaps? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="If there are areas in which your formal training has not been sufficient, how have you addressed these gaps? Other.",
)

# %% [markdown]
# ### In which of these areas would you most like to improve your skills?Please select one option.
#
# Describe: 402 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All Asked.

# %%
data[
    "In which of these areas would you most like to improve your skills?Please select one option."
] = (
    data[
        "In which of these areas would you most like to improve your skills?Please select one option."
    ]
    .replace("Don’t know", "Don't know")
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Don't know",
            "Other",
            "Business management",
            "Administration and paperwork",
            "Tech and IT skills",
            "Sales and marketing",
            "Customer service and communication",
            "Heat loss surveying and calculations",
            "Emitter design",
            "System design",
            "Plumbing skills",
            "Electrical skills",
            "F-Gas skills",
            "How to train and support an apprentice",
            "How to take on new staff",
            "None, I don’t need to improve my skills",
            "None, the current training options are good enough",
        ],
    )
)

# rename other column
data = data.rename(
    columns={
        "Other (please specify):In which of these areas would you most like to improve your skills?Please select one option.": "In which of these areas would you most like to improve your skills? Other."
    }
)

# %% [markdown]
# ### Are you interested in completing training on new technologies (e.g. heat batteries)?
#
# Describe: 402 null.
# Cleaning: cast to cateogrical.
#
# Exclusion: All asked.

# %%
data[
    "Are you interested in completing training on new technologies (e.g. heat batteries)?"
] = data[
    "Are you interested in completing training on new technologies (e.g. heat batteries)?"
].pipe(
    pandas.Categorical, categories=["Yes", "No"]
)

# %% [markdown]
# ### What is your preferred way of doing training?
#
# Describe: 402 null.
# Cleaning: cast to cateogrical.
#
# Exclusion: All asked.

# %%
data["What is your preferred way of doing training?"] = (
    data["What is your preferred way of doing training?"]
    .replace("Other (please specify)", "Other")
    .pipe(
        pandas.Categorical,
        categories=[
            "Other",
            "Face to face, less than an hour travel",
            "Face to face, willing to travel more than one hour",
            "Online, delivered live",
            "Online, available on-demand",
            "Don't know",
        ],
    )
)

# rename other column
data = data.rename(
    columns={
        "Other (please specify):What is your preferred way of doing training?": "What is your preferred way of doing training? Other."
    }
)

# %% [markdown]
# ### How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation?Select all that apply.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "From official websites like MCS or the UK government",
    "From information on social media (eg forums, Facebook, YouTube or Twitter)",
    "From industry magazines, websites or email lists",
    "From trade shows and conferences",
    "Manufacturer or supplier websites or newsletters",
    "From informal conversations with colleagues",
    "I find it hard to find this information",
]

data = collapse_select_all(
    df=data,
    select_all_columns="How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation?",
    collapsed_column_name="How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation? Other.",
)

# %% [markdown]
# ### Where do you think training should be most improved in order to best support the next generation?Please select one option.
#
# Describe: 402 null.
# Cleaning: cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "Where do you think training should be most improved in order to best support the next generation?Please select one option."
] = (
    data[
        "Where do you think training should be most improved in order to best support the next generation?Please select one option."
    ]
    .replace("Other (please specify)", "Other")
    .replace("Don’t know", "Don't know")
    .pipe(
        pandas.Categorical,
        categories=[
            "Other",
            "Don't know",
            "Business management",
            "Administration and paperwork",
            "Tech and IT skills",
            "Sales and marketing",
            "Customer service and communication",
            "Heat loss surveying and calculations",
            "Emitter design",
            "System design",
            "Plumbing skills",
            "Electrical skills",
            "F-Gas skills",
            "Maintenance, repairs, servicing and troubleshooting",
            "None, the current training options are good enough",
        ],
    )
)

# rename other column
data = data.rename(
    columns={
        "Other (please specify):Where do you think training should be most improved in order to best support the next generation?Please select one option.": "Where do you think training should be most improved in order to best support the next generation? Other."
    }
)

# %% [markdown]
# # Page 12 - representation and connection
#
# NB - All asked these questions.
#
# ### Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work?
#
# Cleaning: Iterate over rows and cast to categorical.
#
# Exclusion: All asked.

# %%
columns = data.columns[
    data.columns.str.contains(
        "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work?"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? {task}"
    ] = (
        data[col]
        .replace(
            "N/A / I don’t want to communicate with this body",
            "N/A / I don't want to communicate with this body",
        )
        .pipe(
            pandas.Categorical,
            categories=[
                "N/A / I don't want to communicate with this body",
                "Not at all",
                "A little",
                "A lot",
            ],
            ordered=True,
        )
    )

data = data.drop(columns=columns)

# %% [markdown]
# ### To what extent could the following organisations act on your opinions on how your job and the industry could be improved?
#
# Cleaning: Iterate over rows and cast to categorical.
#
# Exclusion: All asked.

# %%
columns = data.columns[
    data.columns.str.contains(
        "To what extent could the following organisations act on your opinions on how your job and the industry could be improved?"
    )
]

for col in columns:
    task, _ = col.split(":")

    data[
        f"To what extent could the following organisations act on your opinions on how your job and the industry could be improved? {task}"
    ] = (
        data[col]
        .replace("Don’t know", "Don't know")
        .pipe(
            pandas.Categorical,
            categories=["Don't know", "Not at all", "A little", "A lot"],
            ordered=True,
        )
    )

data = data.drop(columns=columns)

# %% [markdown]
# ### Which bodies are you a member of?Select all that apply.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "APHC",
    "HHIC",
    "HPF",
    "GSHPA",
    "HPA",
    "Gas Safe",
    "Oftec",
    "HETAS",
    "Cibse",
    "CIPHE",
    "I'm not a member of any industry bodies",
]

data = collapse_select_all(
    df=data,
    select_all_columns="Which bodies are you a member of?",
    collapsed_column_name="Which bodies are you a member of?Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="Which bodies are you a member of? Other.",
)

# %% [markdown]
# ### To what extent does your membership(s) meet your needs for formal industry representation?
#
# Describe: 447 null.
# Cleaning: cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "To what extent does your membership(s) meet your needs for formal industry representation?"
] = (
    data[
        "To what extent does your membership(s) meet your needs for formal industry representation?"
    ]
    .replace(
        "I don’t expect this from my formal industry representation",
        "I don't expect this from my formal industry representation",
    )
    .pipe(
        pandas.Categorical,
        categories=[
            "I don't expect this from my formal industry representation",
            "A very small amount",
            "A small amount",
            "A moderate amount",
            "A large amount",
            "A very large amount",
        ],
    )
)

# %% [markdown]
# ### To what extent does your membership(s) meet your needs for the sharing of technical knowledge, industry information, and experiences from your work?
#
# Describe: 447 null.
#
# Exclusion: All asked.

# %%
data[
    "To what extent does your membership(s) meet your needs for the sharing of technical knowledge, industry information, and experiences from your work?"
] = (
    data[
        "To what extent does your membership(s) meet your needs for the sharing of technical knowledge, industry information, and experiences from your work?"
    ]
    .replace(
        "I don’t expect this from my formal industry representation",
        "I don't expect this from my formal industry representation",
    )
    .pipe(
        pandas.Categorical,
        categories=[
            "I don't expect this from my formal industry representation",
            "A very small amount",
            "A small amount",
            "A moderate amount",
            "A large amount",
            "A very large amount",
        ],
    )
)

# %% [markdown]
# ### Which certification bodies for MCS do you use?
#
# Cleaning: Collapse categories.
#
# Exclusion: Complex exclusion based on MCS questions in 'work you do' and retrofit work. inclusion based on:
# 'Is your business MCS certified for heat pump installations?' responds 'Yes' OR 'Are you personally registered as an MCS-certified heat pump installer?' responds 'Yes' OR 'In your (Employee) retrofit work, do you install heat pumps through: Select all that apply.' includes the response "My own MCS certification (I am the firm's Nominated Technical Person)"

# %%
data = collapse_select_all(
    df=data,
    select_all_columns="Which certification bodies for MCS do you use?",
    collapsed_column_name="Which certification bodies for MCS do you use? Select all that apply.",
    remove_collapsed_columns=True,
)

# %%
# Add not asked logic to question
data.loc[
    ~(
        (data["Is your business MCS certified for heat pump installations?"] == "Yes")
        | data["Is your business MCS certified for heat pump installations?"].isna()
        | (
            data[
                "Are you personally registered as an MCS-certified heat pump installer?"
            ]
            == "Yes"
        )
        | data[
            "Are you personally registered as an MCS-certified heat pump installer?"
        ].isna()
        | (
            data[
                "In your (Employee) retrofit work, do you install heat pumps through: Select all that apply."
            ].apply(
                lambda x: True
                if (
                    (
                        "My own MCS certification (I am the firm's Nominated Technical Person)"
                        in x
                    )
                    | (len(x) == 0)
                )
                else False
            )
        )
    ),
    "Which certification bodies for MCS do you use? Select all that apply.",
] = data.loc[
    ~(
        (data["Is your business MCS certified for heat pump installations?"] == "Yes")
        | data["Is your business MCS certified for heat pump installations?"].isna()
        | (
            data[
                "Are you personally registered as an MCS-certified heat pump installer?"
            ]
            == "Yes"
        )
        | data[
            "Are you personally registered as an MCS-certified heat pump installer?"
        ].isna()
        | (
            data[
                "In your (Employee) retrofit work, do you install heat pumps through: Select all that apply."
            ].apply(
                lambda x: True
                if (
                    (
                        "My own MCS certification (I am the firm's Nominated Technical Person)"
                        in x
                    )
                    | (len(x) == 0)
                )
                else False
            )
        )
    ),
    "Response ID",
].apply(
    lambda _: [not_asked]
)

# %% [markdown]
# ### To what extent do you want to feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?
#
# Describe: 409 null.
# Cleaning: Cast to categorical.
#
# Exclusion; All asked.

# %%
data[
    "To what extent do you want to feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?"
] = data[
    "To what extent do you want to feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?"
].pipe(
    pandas.Categorical,
    categories=[
        "Don't know",
        "A very small amount",
        "A small amount",
        "A moderate amount",
        "A large amount",
        "A very large amount",
    ],
)

# %% [markdown]
# ### To what extent do you currently feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?
#
# Describe: 409 null.
# Cleaning: Cast to categorical.
#
# Exclusion; All asked.

# %%
data[
    "To what extent do you currently feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?"
] = data[
    "To what extent do you currently feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?"
].pipe(
    pandas.Categorical,
    categories=[
        "Don't know",
        "A very small amount",
        "A small amount",
        "A moderate amount",
        "A large amount",
        "A very large amount",
    ],
)

# %% [markdown]
# ### How do you share knowledge and experiences with other heat pump installers?Select all that apply.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "WhatsApp groups",
    "Social media (eg forums, Facebook, YouTube or Twitter)",
    "Informal conversations with colleagues",
    "Trade shows and conferences",
    "I don’t share knowledge or experiences",
]

data = collapse_select_all(
    df=data,
    select_all_columns="How do you share knowledge and experiences with other heat pump installers?",
    collapsed_column_name="How do you share knowledge and experiences with other heat pump installers? Select all that apply.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="How do you share knowledge and experiences with other heat pump installers? Other.",
)

# %% [markdown]
# ### How do you think manufacturers can better support heat pump installers?You can select up to three options.
#
# Cleaning: Collapse categories.
#
# Exclusion: All asked.

# %%
responses = [
    "Greater number of training courses",
    "Greater variety of training courses",
    "Better quality training courses",
    "General business support",
    "Sales and marketing support",
    "Quality of technical support",
    "Timeliness of the technical support",
    "Service and maintenance support",
    "Clear warranty information",
    "Better customer support offer to the end user",
    "Easier to understand user manuals for customers",
    "Access to finance for their products",
    "Greater involvement of  installers with product development",
    "None of the above",
]

data = collapse_select_all(
    df=data,
    select_all_columns="How do you think manufacturers can better support heat pump installers?",
    collapsed_column_name="How do you think manufacturers can better support heat pump installers? You can select up to three options.",
    remove_collapsed_columns=True,
    responses=responses,
    recode_other=True,
    save_other_as_new_column=True,
    new_other_column_name="How do you think manufacturers can better support heat pump installers? Other.",
)

# %% [markdown]
# # Page 13 - mental health question
#
# NB - Section is asked to all, but is optional.
#
# ### Have you experienced and/or have you been diagnosed with a mental health condition?
#
# Describe: 420 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    "Have you experienced and/or have you been diagnosed with a mental health condition?"
] = data[
    "Have you experienced and/or have you been diagnosed with a mental health condition?"
].pipe(
    pandas.Categorical, categories=["Yes", "No", "Decline to answer"]
)

# %% [markdown]
# ### To what extent do you agree with this statement? "My work in the heat pump sector negatively affects my mental health."
#
# Describe: 424 null.
# Cleaning: Cast to categorical.
#
# Exclusion: All asked.

# %%
data[
    'To what extent do you agree with this statement? "My work in the heat pump sector negatively affects my mental health."'
] = data[
    'To what extent do you agree with this statement? "My work in the heat pump sector negatively affects my mental health."'
].pipe(
    pandas.Categorical,
    categories=[
        "Decline to answer",
        "Strongly disagree",
        "Disagree",
        "Neither agree nor disagree",
        "Agree",
        "Strongly agree",
    ],
)

# %% [markdown]
# # Order Questions
#
# In this section, we'll add question numbers and reorder to match the survey flow.

# %%
column_dict = {
    "Response ID": "0a. Response ID",
    "Time Started": "0b. Time Started",
    "Date Submitted": "0c. Date Submitted",
    "Status": "0d. Status",
    "How old are you?": "1. How old are you?",
    "How would you describe your gender?": "2. How would you describe your gender?",
    "How long have you worked in the plumbing and heating sector?": "3. How long have you worked in the plumbing and heating sector?",
    "How long have you been working with heat pumps?": "4. How long have you been working with heat pumps?",
    "Are you responding to this survey as…If multiple answers apply to you, select the option in which you’ve done the most heat pump installations in the last year.": "5. Are you responding to this survey as…",
    "What size company do you own?": "6a. What size company do you own?",
    "What size company do you work for?": "6b. What size company do you work for?",
    "Do you work with family members in any of the following ways? Select all that apply.": "7. Do you work with family members in any of the following ways? Select all that apply.",
    "Where is your company located?": "8. Where is your company located?",
    "In which English region is your company located?": "9a. In which English region is your company located?",
    "In which Scottish region is your company located?": "9b. In which Scottish region is your company located?",
    "In which Welsh region is your company located?": "9c. In which Welsh region is your company located?",
    "In which Northern Irish county is your company located?": "9d. In which Northern Irish county is your company located?",
    "How far from your business location would you typically travel for jobs, approximately?": "10. How far from your business location would you typically travel for jobs, approximately?",
    "What aspects of the company you own are you involved with? Select all that apply.": "11a. What aspects of the company you own are you involved with? Select all that apply.",
    "What type of work do you do when you’re contracted for a job? Select all that apply.": "11b. What type of work do you do when you’re contracted for a job? Select all that apply.",
    "What type of work do you do for the company you work for? Select all that apply.": "11c. What type of work do you do for the company you work for? Select all that apply.",
    "Thinking of your company's overall heating work, what does it currently consist of?": "12a. Thinking of your company's overall heating work, what does it currently consist of?",
    "Thinking of your overall heating work, what does it currently consist of?": "12b. Thinking of your overall heating work, what does it currently consist of?",
    "Thinking of your company's overall heating work in 12 months time, what do you intend it to consist of?": "13a. Thinking of your company's overall heating work in 12 months time, what do you intend it to consist of?",
    "Thinking of your overall heating work in 12 months time, what do you intend it to consist of?": "13b. Thinking of your overall heating work in 12 months time, what do you intend it to consist of?",
    "Thinking of the heating systems your company installs, do you work on:": "14a. Thinking of the heating systems your company installs, do you work on:",
    "Thinking of the heating systems you install, do you work on:": "14b. Thinking of the heating systems you install, do you work on:",
    "Thinking of the heating systems your company services and maintains, do you work on:": "15a. Thinking of the heating systems your company services and maintains, do you work on:",
    "Thinking of the heating systems you service and maintain, do you work on:": "15b. Thinking of the heating systems you service and maintain, do you work on:",
    "What types of heat pump has your company installed over the last 12 months? Select all that apply.": "16a. What types of heat pump has your company installed over the last 12 months? Select all that apply.",
    "What types of heat pump has your company installed over the last 12 months? Other.": "16ao. What types of heat pump has your company installed over the last 12 months? Other.",
    "What types of heat pump have you installed over the last 12 months? Select all that apply.": "16b. What types of heat pump have you installed over the last 12 months? Select all that apply.",
    "What types of heat pump have you installed over the last 12 months? Other.": "16bo. What types of heat pump have you installed over the last 12 months? Other.",
    "What type of heat pump has your company installed most often over the last 12 months?Please select one option.": "17a. What type of heat pump has your company installed most often over the last 12 months? Please select one option.",
    "Other (please specify):What type of heat pump has your company installed most often over the last 12 months?Please select one option.": "17ao. What type of heat pump has your company installed most often over the last 12 months? Other.",
    "What type of heat pump have you installed most often over the last 12 months?Please select one option": "17b. What type of heat pump have you installed most often over the last 12 months? Please select one option",
    "What type of heat pump have you installed most often over the last 12 months? Other.": "17bo. What type of heat pump have you installed most often over the last 12 months? Other.",
    "Do you offer heat batteries to accompany your heat pump installations?": "18. Do you offer heat batteries to accompany your heat pump installations?",
    "What barriers prevent you from offering heat batteries? You can select up to 3 options.": "19. What barriers prevent you from offering heat batteries? You can select up to 3 options.",
    "What barriers prevent you from offering heat batteries? Other.": "19o. What barriers prevent you from offering heat batteries? Other.",
    "If a customer doesn’t specify what they want with their heat pump, what is the most important factor for you when choosing which thermal store or hot water system to fit? Please select one option.": "20. If a customer doesn’t specify what they want with their heat pump, what is the most important factor for you when choosing which thermal store or hot water system to fit? Please select one option.",
    "If a customer doesn’t specify what they want with their heat pump, what is the most important factor for you when choosing which thermal store or hot water system to fit? Other.": "20o. If a customer doesn’t specify what they want with their heat pump, what is the most important factor for you when choosing which thermal store or hot water system to fit? Other.",
    "Is your business MCS certified for heat pump installations?": "21a. Is your business MCS certified for heat pump installations?",
    "Are you personally registered as an MCS-certified heat pump installer?": "21b. Are you personally registered as an MCS-certified heat pump installer?",
    "Is the firm you work for MCS certified for heat pump installations?": "21c. Is the firm you work for MCS certified for heat pump installations?",
    "Which heat pump technologies is your business MCS certified to install? Select all that apply.": "22a. Which heat pump technologies is your business MCS certified to install? Select all that apply.",
    "Which heat pump technologies are you MCS certified to install? Select all that apply.": "22b. Which heat pump technologies are you MCS certified to install? Select all that apply.",
    "Which heat pump technologies is the firm you work for you MCS certified to install? Select all that apply.": "22c. Which heat pump technologies is the firm you work for you MCS certified to install? Select all that apply.",
    "How long has your business been MCS certified for heat pump installations?": "23a. How long has your business been MCS certified for heat pump installations?",
    "How long have you been MCS certified for heat pump installations?": "23b. How long have you been MCS certified for heat pump installations?",
    "How long did the certification process take from application to certification? (Business)": "24a. How long did the certification process take from application to certification?",
    "How long did the certification process take from application to certification? (Sole trader/contractor)": "24b. How long did the certification process take from application to certification?",
    "Why isn't your business MCS certified? Select all that apply.": "25a. Why isn't your business MCS certified? Select all that apply.",
    "Why isn't your business MCS certified? Other.": "25ao. Why isn't your business MCS certified? Other.",
    "Why aren't you (Sole Trader) MCS certified? Select all that apply.": "25b. Why aren't you MCS certified? Select all that apply.",
    "Why aren't you (Sole Trader) MCS certified? Other.": "25bo. Why aren't you MCS certified? Other.",
    "Why aren't you (Contractor) MCS certified? Select all that apply.": "25c. Why aren't you MCS certified? Select all that apply.",
    "Why aren't you (Contractor) MCS certified? Other.": "25co. Why aren't you (Contractor) MCS certified? Other.",
    "Which heat pump technologies was your business MCS certified to install? Select all that apply.": "26a. Which heat pump technologies was your business MCS certified to install? Select all that apply.",
    "Which heat pump technologies were you MCS certified to install? Select all that apply.": "26b. Which heat pump technologies were you MCS certified to install? Select all that apply.",
    "Which heat pump technologies was the firm you work for MCS certified to install? Select all that apply.": "26c. Which heat pump technologies was the firm you work for MCS certified to install? Select all that apply.",
    "How long was your business MCS certified for heat pump installations?": "27a. How long was your business MCS certified for heat pump installations?",
    "How long were you MCS certified for heat pump installations?": "27b. How long were you MCS certified for heat pump installations?",
    "Do you intend to reinstate your MCS certification with a new Nominated Technical Person?": "28. Do you intend to reinstate your MCS certification with a new Nominated Technical Person?",
    "Why do you prefer to remain without MCS certification? Select all that apply.": "29. Why do you prefer to remain without MCS certification? Select all that apply.",
    "Why do you prefer to remain without MCS certification? Other.": "29o. Why do you prefer to remain without MCS certification? Other.",
    "Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.": "30a. Has your business done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.",
    "Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.": "30b. Have you done any retrofit or new build heat pump installations over the last 12 months? Select all that apply.",
    "Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Select all that apply.": "31a. Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Select all that apply.",
    "Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Other.": "31ao. Over the past 12 months, has your business done retrofit heat pump installations in any of the following properties? Other.",
    "Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Select all that apply.": "31b. Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Select all that apply.",
    "Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Other.": "31bo. Over the past 12 months, have you done retrofit heat pump installations in any of the following properties? Other.",
    "Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Select all that apply.": "32a. Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Select all that apply.",
    "Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Other.": "32ao. Over the past 12 months, has your business done any new build heat pump installations in any of the following properties? Other.",
    "Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Select all that apply.": "32b. Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Select all that apply.",
    "Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Other.": "32bo. Over the past 12 months, have you done any new build heat pump installations in any of the following properties? Other.",
    "Over the past 12 months, where has the majority of the heat pump installations your business has done been?": "33a. Over the past 12 months, where has the majority of the heat pump installations your business has done been?",
    "Over the past 12 months, where has the majority of your heat pump installation work been?": "33b. Over the past 12 months, where has the majority of your heat pump installation work been?",
    "Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done?": "34a. Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done?",
    "Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done? Other.": "34ao. Over the past 12 months, which of the following accounts for the majority of the retrofit heat pump installations your business has done? Other.",
    "Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations?": "34b. Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations?",
    "Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations? Other.": "34bo. Over the past 12 months, which of the following accounts for the majority of your retrofit heat pump installations? Other.",
    "Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done?": "35a. Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done?",
    "Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done? Other.": "35ao. Over the past 12 months, which of the following accounts for the majority of the new build heat pump installations your business has done? Other.",
    "Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations?": "35b. Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations?",
    "Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations? Other.": "35bo. Over the past 12 months, which of the following accounts for the majority of your new build heat pump installations? Other.",
    "In your business's retrofit work, does your business install heat pumps through: Select all that apply.": "36a. In your business's retrofit work, does your business install heat pumps through: Select all that apply.",
    "In your business's retrofit work, does your business install heat pumps through: Other.": "36ao. In your business's retrofit work, does your business install heat pumps through: Other.",
    "In your (Sole trader) retrofit work, do you install heat pumps through: Select all that apply.": "36b. In your retrofit work, do you install heat pumps through: Select all that apply.",
    "In your (Sole trader) retrofit work, do you install heat pumps through: Other.": "36bo. In your retrofit work, do you install heat pumps through: Other.",
    "In your (Employee) retrofit work, do you install heat pumps through: Select all that apply.": "36c. In your retrofit work, do you install heat pumps through: Select all that apply.",
    "In your (Employee) retrofit work, do you install heat pumps through: Other.": "36co. In your retrofit work, do you install heat pumps through: Other.",
    "In your (Contractor) retrofit work, do you install heat pumps through: Select all that apply.": "36d. In your retrofit work, do you install heat pumps through: Select all that apply.",
    "In your (Contractor) retrofit work, do you install heat pumps through: Other.": "36do. In your retrofit work, do you install heat pumps through: Other.",
    "Approximately how many heat pumps did your business install in the past twelve months?": "37a. Approximately how many heat pumps did your business install in the past twelve months?",
    "Approximately how many heat pumps did you install in the past twelve months?": "37b. Approximately how many heat pumps did you install in the past twelve months?",
    "Would you like your business to install more heat pumps each year?I'd like to install:": "38a. Would you like your business to install more heat pumps each year? I'd like to install:",
    "Would you like to install more heat pumps each year?I'd like to install:": "38b. Would you like to install more heat pumps each year? I'd like to install:",
    "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option. (Owners)": "39a. What's the biggest reason you have for wanting to reduce the number of heat pumps you install? Please select one option.",
    "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install? Other. (Owners)": "39ao. What's the biggest reason you have for wanting to reduce the number of heat pumps you install? Other.",
    "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install?Please select one option. (Employees, contractors, sole traders)": "39b. What's the biggest reason you have for wanting to reduce the number of heat pumps you install? Please select one option.",
    "What’s the biggest reason you have for wanting to reduce the number of heat pumps you install? Other. (Employees, contractors, sole traders)": "39bo. What's the biggest reason you have for wanting to reduce the number of heat pumps you install? Other.",
    "What’s the biggest barrier to you installing more heat pumps? Please select one option. (Owners)": "40a. What's the biggest barrier to you installing more heat pumps? Please select one option.",
    "What’s the biggest barrier to you installing more heat pumps? Other. (Owners)": "40ao. What's the biggest barrier to you installing more heat pumps? Other.",
    "What’s the biggest barrier to you installing more heat pumps?Please select one option. (Employees, contractors, sole traders)": "40b. What's the biggest barrier to you installing more heat pumps? Please select one option.",
    "What’s the biggest barrier to you installing more heat pumps? Other. (Employees, contractors, sole traders)": "40bo. What's the biggest barrier to you installing more heat pumps? Other.",
    "Please indicate how you feel about the amount of time your business spends on: Business management (eg. recruitment, planning future of business and strategy)": "41a. Please indicate how you feel about the amount of time your business spends on: Business management (eg. recruitment, planning future of business and strategy)",
    "Please indicate how you feel about the amount of time your business spends on: Business administration (eg. finances, paperwork, reporting)": "41a. Please indicate how you feel about the amount of time your business spends on: Business administration (eg. finances, paperwork, reporting)",
    "Please indicate how you feel about the amount of time your business spends on: Training staff or apprentices": "41a. Please indicate how you feel about the amount of time your business spends on: Training staff or apprentices",
    "Please indicate how you feel about the amount of time your business spends on: Sales, customer relations, and quotes": "41a. Please indicate how you feel about the amount of time your business spends on: Sales, customer relations, and quotes",
    "Please indicate how you feel about the amount of time your business spends on: Heat pump system survey - on site": "41a. Please indicate how you feel about the amount of time your business spends on: Heat pump system survey - on site",
    "Please indicate how you feel about the amount of time your business spends on: Heat pump system design - office based": "41a. Please indicate how you feel about the amount of time your business spends on: Heat pump system design - office based",
    "Please indicate how you feel about the amount of time your business spends on: Emitter output calculations": "41a. Please indicate how you feel about the amount of time your business spends on: Emitter output calculations",
    "Please indicate how you feel about the amount of time your business spends on: Ordering and delivery of materials and supplies, and monitoring stock levels": "41a. Please indicate how you feel about the amount of time your business spends on: Ordering and delivery of materials and supplies, and monitoring stock levels",
    "Please indicate how you feel about the amount of time your business spends on: Planning permission process": "41a. Please indicate how you feel about the amount of time your business spends on: Planning permission process",
    "Please indicate how you feel about the amount of time your business spends on: Installation of heat pump system (including heat pump unit, pipes, emitters)": "41a. Please indicate how you feel about the amount of time your business spends on: Installation of heat pump system (including heat pump unit, pipes, emitters)",
    "Please indicate how you feel about the amount of time your business spends on: Heat pump commissioning and householder handover": "41a. Please indicate how you feel about the amount of time your business spends on: Heat pump commissioning and householder handover",
    "Please indicate how you feel about the amount of time your business spends on: MCS, BUS, DNO and other post-installation paperwork": "41a. Please indicate how you feel about the amount of time your business spends on: MCS, BUS, DNO and other post-installation paperwork",
    "Please indicate how you feel about the amount of time your business spends on: Heat pump servicing and maintenance": "41a. Please indicate how you feel about the amount of time your business spends on: Heat pump servicing and maintenance",
    "Please indicate how you feel about the amount of time you spend on: Business management (eg. recruitment, planning future of business and strategy)": "41b. Please indicate how you feel about the amount of time you spend on: Business management (eg. recruitment, planning future of business and strategy)",
    "Please indicate how you feel about the amount of time you spend on: Business administration (eg. finances, paperwork, reporting)": "41b. Please indicate how you feel about the amount of time you spend on: Business administration (eg. finances, paperwork, reporting)",
    "Please indicate how you feel about the amount of time you spend on: Training staff or apprentices": "41b. Please indicate how you feel about the amount of time you spend on: Training staff or apprentices",
    "Please indicate how you feel about the amount of time you spend on: Sales, customer relations, and quotes": "41b. Please indicate how you feel about the amount of time you spend on: Sales, customer relations, and quotes",
    "Please indicate how you feel about the amount of time you spend on: Heat pump system survey - on site": "41b. Please indicate how you feel about the amount of time you spend on: Heat pump system survey - on site",
    "Please indicate how you feel about the amount of time you spend on: Heat pump system design - office based": "41b. Please indicate how you feel about the amount of time you spend on: Heat pump system design - office based",
    "Please indicate how you feel about the amount of time you spend on: Emitter output calculations": "41b. Please indicate how you feel about the amount of time you spend on: Emitter output calculations",
    "Please indicate how you feel about the amount of time you spend on: Ordering and delivery of materials and supplies, and monitoring stock levels": "41b. Please indicate how you feel about the amount of time you spend on: Ordering and delivery of materials and supplies, and monitoring stock levels",
    "Please indicate how you feel about the amount of time you spend on: Planning permission process": "41b. Please indicate how you feel about the amount of time you spend on: Planning permission process",
    "Please indicate how you feel about the amount of time you spend on: Installation of heat pump system (including heat pump unit, pipes, emitters)": "41b. Please indicate how you feel about the amount of time you spend on: Installation of heat pump system (including heat pump unit, pipes, emitters)",
    "Please indicate how you feel about the amount of time you spend on: Heat pump commissioning and householder handover": "41b. Please indicate how you feel about the amount of time you spend on: Heat pump commissioning and householder handover",
    "Please indicate how you feel about the amount of time you spend on: MCS, BUS, DNO and other post-installation paperwork": "41b. Please indicate how you feel about the amount of time you spend on: MCS, BUS, DNO and other post-installation paperwork",
    "Please indicate how you feel about the amount of time you spend on: Heat pump servicing and maintenance": "41b. Please indicate how you feel about the amount of time you spend on: Heat pump servicing and maintenance",
    "Do you offer repairs, servicing and maintenance to heat pump customers?": "42a. Do you offer repairs, servicing and maintenance to heat pump customers?",
    "Does the business you work for offer repairs, servicing and maintenance to heat pump customers?": "42b. Does the business you work for offer repairs, servicing and maintenance to heat pump customers?",
    "My business offers heat pump repairs, servicing and maintenance:": "43a. My business offers heat pump repairs, servicing and maintenance:",
    "I offer heat pump repairs, servicing and maintenance:": "43b. I offer heat pump repairs, servicing and maintenance:",
    "The business I work for offers heat pump repairs, servicing and maintenance:": "43c. The business I work for offers heat pump repairs, servicing and maintenance:",
    "Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?": "44a. Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    "Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.": "44ao. Why do you only offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
    "Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?": "44b. Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    "Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.": "44bo. Why does the firm you work for offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
    "Have you found any challenges working in heat pump repairs, servicing and maintenance?": "45. Have you found any challenges working in heat pump repairs, servicing and maintenance?",
    "Have you found any challenges working in heat pump repairs, servicing and maintenance? Other.": "45o. Have you found any challenges working in heat pump repairs, servicing and maintenance? Other.",
    "Do you expect to expand your work in heat pump repairs, servicing and maintenance?": "46. Do you expect to expand your work in heat pump repairs, servicing and maintenance?",
    "When doing repairs, servicing or maintenance to installations by other installers, how often do you identify bad installation practice that negatively affects heat pump performance?": "47. When doing repairs, servicing or maintenance to installations by other installers, how often do you identify bad installation practice that negatively affects heat pump performance?",
    "I intend to offer heat pump repairs, servicing and maintenance: (Owners)": "48a. I intend to offer heat pump repairs, servicing and maintenance:",
    "I intend to offer heat pump repairs, servicing and maintenance: (Contractor/Soletrader)": "48b. I intend to offer heat pump repairs, servicing and maintenance:",
    "The business I work for intends to offer heat pump repairs, servicing and maintenance:": "48c. The business I work for intends to offer heat pump repairs, servicing and maintenance:",
    "Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?": "49a. Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    "Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.": "49ao. Why do you intend to offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
    "Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?": "49b. Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed?",
    "Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.": "49bo. Why does the firm you work for intend to offer repairs, servicing and maintenance only for heat pump systems you have installed? Other.",
    "Why have you previously not offered repairs, servicing and maintenance?": "50. Why have you previously not offered repairs, servicing and maintenance?",
    "Why have you previously not offered repairs, servicing and maintenance? Other.": "50o. Why have you previously not offered repairs, servicing and maintenance? Other.",
    "Why do you now intend to move into heat pump repairs, servicing and maintenance?": "51. Why do you now intend to move into heat pump repairs, servicing and maintenance?",
    "Why do you now intend to move into heat pump repairs, servicing and maintenance? Other.": "51o. Why do you now intend to move into heat pump repairs, servicing and maintenance? Other.",
    "Why don’t you currently offer repairs, servicing and maintenance to customers?": "52a. Why don’t you currently offer repairs, servicing and maintenance to customers?",
    "Why don’t you currently offer repairs, servicing and maintenance to customers? Other.": "52ao. Why don’t you currently offer repairs, servicing and maintenance to customers? Other.",
    "Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?": "52b. Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers?",
    "Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers? Other.": "52bo. Why doesn’t the business you work for currently offer repairs, servicing and maintenance to customers? Other.",
    "How often is your business unable to complete work related to a heat pump installation to the standard that you would like?": "53a. How often is your business unable to complete work related to a heat pump installation to the standard that you would like?",
    "How often are you unable to complete work related to a heat pump installation to the standard that you would like?": "53b. How often are you unable to complete work related to a heat pump installation to the standard that you would like?",
    "In which areas could you (Owners) improve the standard of your heat pump installations?": "54a. In which areas could you improve the standard of your heat pump installations?",
    "In which areas could you (Owners) improve the standard of your heat pump installations? Other.": "54ao. In which areas could you improve the standard of your heat pump installations? Other.",
    "In which areas could you (Employee, Contractor, Sole trader) improve the standard of your heat pump installations?": "54b. In which areas could you improve the standard of your heat pump installations?",
    "In which areas could you (Employee, Contractor, Sole trader) improve the standard of your heat pump installations? Other.": "54bo. In which areas could you improve the standard of your heat pump installations? Other.",
    "How often do you, or others in your business, use software apps and digital tools to support the business's activity?": "55a. How often do you, or others in your business, use software apps and digital tools to support the business's activity?",
    "How often do you use software, apps and digital tools to support you with your work?": "55b. How often do you use software, apps and digital tools to support you with your work?",
    "In which areas of your business do you use software, apps or digital tools?": "56a. In which areas of your business do you use software, apps or digital tools?",
    "In which areas of your business do you use software, apps or digital tools? Other.": "56ao. In which areas of your business do you use software, apps or digital tools? Other.",
    "In which areas of your work do you use software, apps or digital tools?": "56b. In which areas of your work do you use software, apps or digital tools?",
    "In which areas of your work do you use software, apps or digital tools? Other.": "56bo. In which areas of your work do you use software, apps or digital tools? Other.",
    "How would you describe existing software, apps and digital tools in terms of: Cost": "57. How would you describe existing software, apps and digital tools in terms of: Cost",
    "How would you describe existing software, apps and digital tools in terms of: Reliability": "57. How would you describe existing software, apps and digital tools in terms of: Reliability",
    "How would you describe existing software, apps and digital tools in terms of: Ease-of-use": "57. How would you describe existing software, apps and digital tools in terms of: Ease-of-use",
    "How would you describe existing software, apps and digital tools in terms of: Choice": "57. How would you describe existing software, apps and digital tools in terms of: Choice",
    "How would you describe existing software, apps and digital tools in terms of: Functionality": "57. How would you describe existing software, apps and digital tools in terms of: Functionality",
    "In which areas of your business (owners) do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)": "58a. In which areas of your business do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)",
    "In which areas of your business (owners) do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)": "58a. In which areas of your business do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)",
    "In which areas of your business (owners) do you think extra support could be most helpful: Training staff or apprentices": "58a. In which areas of your business do you think extra support could be most helpful: Training staff or apprentices",
    "In which areas of your business (owners) do you think extra support could be most helpful: Sales, customer relations, and quotes": "58a. In which areas of your business do you think extra support could be most helpful: Sales, customer relations, and quotes",
    "In which areas of your business (owners) do you think extra support could be most helpful: Heat pump system survey - on site": "58a. In which areas of your business do you think extra support could be most helpful: Heat pump system survey - on site",
    "In which areas of your business (owners) do you think extra support could be most helpful: Heat pump system design - office based": "58a. In which areas of your business do you think extra support could be most helpful: Heat pump system design - office based",
    "In which areas of your business (owners) do you think extra support could be most helpful: Emitter output calculations": "58a. In which areas of your business do you think extra support could be most helpful: Emitter output calculations",
    "In which areas of your business (owners) do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels": "58a. In which areas of your business do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels",
    "In which areas of your business (owners) do you think extra support could be most helpful: Planning permission process": "58a. In which areas of your business do you think extra support could be most helpful: Planning permission process",
    "In which areas of your business (owners) do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)": "58a. In which areas of your business do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)",
    "In which areas of your business (owners) do you think extra support could be most helpful: Heat pump commissioning and householder handover": "58a. In which areas of your business do you think extra support could be most helpful: Heat pump commissioning and householder handover",
    "In which areas of your business (owners) do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork": "58a. In which areas of your business do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork",
    "In which areas of your business (owners) do you think extra support could be most helpful: Heat pump servicing and maintenance": "58a. In which areas of your business do you think extra support could be most helpful: Heat pump servicing and maintenance",
    "In which areas of your business (owners) do you think extra support could be most helpful: Finding contractors or new staff": "58a. In which areas of your business do you think extra support could be most helpful: Finding contractors or new staff",
    "In which areas of your business (owners) do you think extra support could be most helpful: Thermal store selection": "58a. In which areas of your business do you think extra support could be most helpful: Thermal store selection",
    "In which areas of your work (employee) do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)": "58b. In which areas of your work do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)",
    "In which areas of your work (employee) do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)": "58b. In which areas of your work do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)",
    "In which areas of your work (employee) do you think extra support could be most helpful: Training staff or apprentices": "58b. In which areas of your work do you think extra support could be most helpful: Training staff or apprentices",
    "In which areas of your work (employee) do you think extra support could be most helpful: Sales, customer relations, and quotes": "58b. In which areas of your work do you think extra support could be most helpful: Sales, customer relations, and quotes",
    "In which areas of your work (employee) do you think extra support could be most helpful: Heat pump system survey - on site": "58b. In which areas of your work do you think extra support could be most helpful: Heat pump system survey - on site",
    "In which areas of your work (employee) do you think extra support could be most helpful: Heat pump system design - office based": "58b. In which areas of your work do you think extra support could be most helpful: Heat pump system design - office based",
    "In which areas of your work (employee) do you think extra support could be most helpful: Emitter output calculations": "58b. In which areas of your work do you think extra support could be most helpful: Emitter output calculations",
    "In which areas of your work (employee) do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels": "58b. In which areas of your work do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels",
    "In which areas of your work (employee) do you think extra support could be most helpful: Planning permission process": "58b. In which areas of your work do you think extra support could be most helpful: Planning permission process",
    "In which areas of your work (employee) do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)": "58b. In which areas of your work do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)",
    "In which areas of your work (employee) do you think extra support could be most helpful: Heat pump commissioning and householder handover": "58b. In which areas of your work do you think extra support could be most helpful: Heat pump commissioning and householder handover",
    "In which areas of your work (employee) do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork": "58b. In which areas of your work do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork",
    "In which areas of your work (employee) do you think extra support could be most helpful: Heat pump servicing and maintenance": "58b. In which areas of your work do you think extra support could be most helpful: Heat pump servicing and maintenance",
    "In which areas of your work (employee) do you think extra support could be most helpful: Thermal store selection": "58b. In which areas of your work do you think extra support could be most helpful: Thermal store selection",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)": "58c. In which areas of your work do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)": "58c. In which areas of your work do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Training staff or apprentices": "58c. In which areas of your work do you think extra support could be most helpful: Training staff or apprentices",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Sales, customer relations, and quotes": "58c. In which areas of your work do you think extra support could be most helpful: Sales, customer relations, and quotes",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Heat pump system survey - on site": "58c. In which areas of your work do you think extra support could be most helpful: Heat pump system survey - on site",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Heat pump system design - office based": "58c. In which areas of your work do you think extra support could be most helpful: Heat pump system design - office based",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Emitter output calculations": "58c. In which areas of your work do you think extra support could be most helpful: Emitter output calculations",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels": "58c. In which areas of your work do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Planning permission process": "58c. In which areas of your work do you think extra support could be most helpful: Planning permission process",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)": "58c. In which areas of your work do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Heat pump commissioning and householder handover": "58c. In which areas of your work do you think extra support could be most helpful: Heat pump commissioning and householder handover",
    "In which areas of your work (contractor) do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork": "58c. In which areas of your work do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Heat pump servicing and maintenance": "58c. In which areas of your work do you think extra support could be most helpful: Heat pump servicing and maintenance",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Finding contractor job opportunities": "58c. In which areas of your work do you think extra support could be most helpful: Finding contractor job opportunities",
    "In which areas of your work (contractor) do you think extra support could be most helpful: Thermal store selection": "58c. In which areas of your work do you think extra support could be most helpful: Thermal store selection",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)": "58d. In which areas of your business do you think extra support could be most helpful: Business management (eg. recruitment, planning future of business and strategy)",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)": "58d. In which areas of your business do you think extra support could be most helpful: Business administration (eg. finances, paperwork, reporting)",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Training staff or apprentices": "58d. In which areas of your business do you think extra support could be most helpful: Training staff or apprentices",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Sales, customer relations, and quotes": "58d. In which areas of your business do you think extra support could be most helpful: Sales, customer relations, and quotes",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Heat pump system survey - on site": "58d. In which areas of your business do you think extra support could be most helpful: Heat pump system survey - on site",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Heat pump system design - office based": "58d. In which areas of your business do you think extra support could be most helpful: Heat pump system design - office based",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Emitter output calculations": "58d. In which areas of your business do you think extra support could be most helpful: Emitter output calculations",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels": "58d. In which areas of your business do you think extra support could be most helpful: Ordering and delivery of materials and supplies, and monitoring stock levels",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Planning permission process": "58d. In which areas of your business do you think extra support could be most helpful: Planning permission process",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)": "58d. In which areas of your business do you think extra support could be most helpful: Installation of heat pump system (including heat pump unit, pipes, emitters)",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Heat pump commissioning and householder handover": "58d. In which areas of your business do you think extra support could be most helpful: Heat pump commissioning and householder handover",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork": "58d. In which areas of your business do you think extra support could be most helpful: MCS, BUS DNO and other post-installation paperwork",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Heat pump servicing and maintenance": "58d. In which areas of your business do you think extra support could be most helpful: Heat pump servicing and maintenance",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Finding contractors or new staff": "58d. In which areas of your business do you think extra support could be most helpful: Finding contractors or new staff",
    "In which areas of your business (sole traders) do you think extra support could be most helpful: Thermal store selection": "58d. In which areas of your business do you think extra support could be most helpful: Thermal store selection",
    "What do you find most challenging about the final stages of the installation and the customer handover? You can select up to 3 responses.": "59. What do you find most challenging about the final stages of the installation and the customer handover? You can select up to 3 responses.",
    "How do you (owners and employees) manage the design for the majority of your heat pump installations?": "60a. How do you manage the design for the majority of your heat pump installations?",
    "How do you (owners and employees) manage the design for the majority of your heat pump installations? Other": "60ao. How do you manage the design for the majority of your heat pump installations? Other",
    "How do you (contractors) manage the design for the majority of your heat pump installations?": "60b. How do you manage the design for the majority of your heat pump installations?",
    "How do you (contractors) manage the design for the majority of your heat pump installations? Other": "60bo. How do you manage the design for the majority of your heat pump installations? Other",
    "Which design software or platform do you use? Select all that apply.": "70. Which design software or platform do you use? Select all that apply.",
    "Which design software or platform do you use? Other.": "70o. Which design software or platform do you use? Other.",
    "How do you source the following skills? Business administration": "71. How do you source the following skills? Business administration",
    "How do you source the following skills? System design": "71. How do you source the following skills? System design",
    "How do you source the following skills? Installation of the heat pump system \(including heat pump unit, pipes, emitters\)": "71. How do you source the following skills? Installation of the heat pump system (including heat pump unit, pipes, emitters)",
    "How do you source the following skills? Commissioning": "71. How do you source the following skills? Commissioning",
    "How do you source the following skills? MCS and post install documentation": "71. How do you source the following skills? MCS and post install documentation",
    "How do you source the following skills? Service and maintenance on site": "71. How do you source the following skills? Service and maintenance on site",
    "How do you source the following skills? Customer support off site": "71. How do you source the following skills? Customer support off site",
    "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this?Please select one option.": "72. If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this? Please select one option.",
    "If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this? Other.": "72o. If you were to increase the number of heat pumps you install, what single skill could you add to your business to help you do this? Other.",
    "For the role you selected above, what experience level would you most like to recruit?": "73. For the role you selected above, what experience level would you most like to recruit?",
    "How likely are you to directly employ new staff in the next 12 months?": "74. How likely are you to directly employ new staff in the next 12 months?",
    "How likely are you to subcontract new staff in the next 12 months?": "75. How likely are you to subcontract new staff in the next 12 months?",
    "How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?": "76. How likely are you to increase the workload of family members already working with you or encourage new family members to join the business in the next 12 months?",
    "If you were looking for new staff, which of the following would you prefer?Please select one option.": "77. If you were looking for new staff, which of the following would you prefer? Please select one option.",
    "If you were looking for new staff, which of the following would you prefer? Other.": "77o. If you were looking for new staff, which of the following would you prefer? Other.",
    "If you were looking for new staff, what are the biggest barriers to taking on new directly employed staff?": "78. If you were looking for new staff, what are the biggest barriers to taking on new directly employed staff?",
    "If you were looking for new staff, what are the biggest barriers to subcontracting staff?": "79. If you were looking for new staff, what are the biggest barriers to subcontracting staff?",
    "Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?": "80. Do you currently employ an apprentice who works on heat pump installations, or have you done so in the last 12 months?",
    "What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations?": "81. What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations?",
    "What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations? Other.": "81o. What challenges, if any, have you faced as part of taking on an apprentice to work with you on heat pump installations? Other.",
    "What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations?": "82. What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations?",
    "What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations? Other.": "82o. What are the challenges you foresee with taking on an apprentice to work with you on heat pump installations? Other.",
    "How confident are you that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work for you?": "83. How confident are you that a recent graduate from an apprenticeship scheme would be trained to an appropriate level to work for you?",
    "If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations?": "84. If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations?",
    "If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations? Other.": "84o. If you were recruiting, what skills would you prioritise in a recent graduate from an apprenticeship scheme to work with you on heat pump installations? Other.",
    "What do you think could be most improved from the training that plumbing and heating apprentices receive?Please select one option.": "85. What do you think could be most improved from the training that plumbing and heating apprentices receive? Please select one option.",
    "What do you think could be most improved from the training that plumbing and heating apprentices receive? Other.": "85o. What do you think could be most improved from the training that plumbing and heating apprentices receive? Other.",
    "If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?": "86. If you were recruiting, how likely would you be to take on candidates with paper qualifications but no practical or vocational experience in the field?",
    "Why might you choose to take on someone with vocational experience over paper qualifications?Please select one option.": "87. Why might you choose to take on someone with vocational experience over paper qualifications? Please select one option.",
    "Why might you choose to take on someone with vocational experience over paper qualifications? Other.": "87o. Why might you choose to take on someone with vocational experience over paper qualifications? Other.",
    "Why might you choose to take on someone with only paper qualifications?Please select one option.": "88. Why might you choose to take on someone with only paper qualifications? Please select one option.",
    "Why might you choose to take on someone with only paper qualifications? Other.": "88o. Why might you choose to take on someone with only paper qualifications? Other.",
    "What might further encourage you most to take on someone with only paper qualifications?Please select one option.": "89a. What might further encourage you most to take on someone with only paper qualifications? Please select one option.",
    "What might further encourage you most to take on someone with only paper qualifications? Other.": "89ao. What might further encourage you most to take on someone with only paper qualifications? Other.",
    "What might encourage you most to take on someone with only paper qualifications?Please select one option.": "89b. What might encourage you most to take on someone with only paper qualifications? Please select one option.",
    "What might encourage you most to take on someone with only paper qualifications? Other.": "89bo. What might encourage you most to take on someone with only paper qualifications? Other.",
    "What proportion of heat pump enquiries result in generating a comprehensive quote for works?": "90. What proportion of heat pump enquiries result in generating a comprehensive quote for works?",
    "What proportion of comprehensive quotes for works result in installations?": "91. What proportion of comprehensive quotes for works result in installations?",
    "What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote?Please select one option.": "92. What do you think the main reason is that customers don't go ahead with a heat pump installation after you provide a quote? Please select one option.",
    "What do you think the main reason is that customers don’t go ahead with a heat pump installation after you provide a quote? Other.": "92o. What do you think the main reason is that customers don't go ahead with a heat pump installation after you provide a quote? Other.",
    "How frequently do you have to decline viable heat pump installation work because you don’t have the capacity to do it?": "93. How frequently do you have to decline viable heat pump installation work because you don't have the capacity to do it?",
    "Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it?": "94. Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it?",
    "Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it? Other.": "94o. Have you ever declined work for any of the following reasons, even when the customer is keen and you're able to do it? Other.",
    "Do you ever feel your customer service is of a lower quality than you would like?": "95. Do you ever feel your customer service is of a lower quality than you would like?",
    "In which areas could you improve your standards to help you provide a better service to your customers?": "96. In which areas could you improve your standards to help you provide a better service to your customers?",
    "In which areas could you improve your standards to help you provide a better service to your customers? Other.": "96o. In which areas could you improve your standards to help you provide a better service to your customers? Other.",
    "What training or certification do you have? Select all that apply.": "97. What training or certification do you have? Select all that apply.",
    "What training or certification do you have? Other.": "97o. What training or certification do you have? Other.",
    "With the skills you’ve gained from the formal training you’ve done so far, how prepared do you feel for your current heat pump installation work?": "98. With the skills you've gained from the formal training you've done so far, how prepared do you feel for your current heat pump installation work?",
    "If there are areas in which your formal training has not been sufficient, how have you addressed these gaps? Select all that apply.": "99. If there are areas in which your formal training has not been sufficient, how have you addressed these gaps? Select all that apply.",
    "If there are areas in which your formal training has not been sufficient, how have you addressed these gaps? Other.": "99o. If there are areas in which your formal training has not been sufficient, how have you addressed these gaps? Other.",
    "In which of these areas would you most like to improve your skills?Please select one option.": "100. In which of these areas would you most like to improve your skills? Please select one option.",
    "In which of these areas would you most like to improve your skills? Other.": "100o. In which of these areas would you most like to improve your skills? Other.",
    "Are you interested in completing training on new technologies (e.g. heat batteries)?": "101. Are you interested in completing training on new technologies (e.g. heat batteries)?",
    "What is your preferred way of doing training?": "102. What is your preferred way of doing training?",
    "What is your preferred way of doing training? Other.": "102o. What is your preferred way of doing training? Other.",
    "How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation? Select all that apply.": "103. How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation? Select all that apply.",
    "How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation? Other.": "103o. How do you learn about updates to policy that affects your work, for instance changes to MCS standards or updates to relevant regulations or legislation? Other.",
    "Where do you think training should be most improved in order to best support the next generation?Please select one option.": "104. Where do you think training should be most improved in order to best support the next generation? Please select one option.",
    "Where do you think training should be most improved in order to best support the next generation? Other.": "104o. Where do you think training should be most improved in order to best support the next generation? Other.",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? MCS": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? MCS",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Manufacturers": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Manufacturers",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? UK government": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? UK government",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Energy companies": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Energy companies",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Certification bodies": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Certification bodies",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Training providers": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Training providers",
    "Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Trade associations such as HPF, GSHPA, HPA": "105. Do you feel able to communicate your ideas, concerns and feedback with the bodies that influence your work? Trade associations such as HPF, GSHPA, HPA",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? MCS": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? MCS",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Manufacturers": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Manufacturers",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? UK government": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? UK government",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Energy companies": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Energy companies",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Certification bodies": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Certification bodies",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Training providers": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Training providers",
    "To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Trade associations such as HPF, GSHPA, HPA": "106. To what extent could the following organisations act on your opinions on how your job and the industry could be improved? Trade associations such as HPF, GSHPA, HPA",
    "Which bodies are you a member of?Select all that apply.": "107. Which bodies are you a member of? Select all that apply.",
    "Which bodies are you a member of? Other.": "107. Which bodies are you a member of? Other.",
    "To what extent does your membership(s) meet your needs for formal industry representation?": "108. To what extent does your membership(s) meet your needs for formal industry representation?",
    "To what extent does your membership(s) meet your needs for the sharing of technical knowledge, industry information, and experiences from your work?": "109. To what extent does your membership(s) meet your needs for the sharing of technical knowledge, industry information, and experiences from your work?",
    "Which certification bodies for MCS do you use? Select all that apply.": "109z. Which certification bodies for MCS do you use? Select all that apply.",
    "To what extent do you want to feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?": "110. To what extent do you want to feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?",
    "To what extent do you currently feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?": "111. To what extent do you currently feel part of an informal network of heat pump professionals, with whom you share technical knowledge, industry information, and experiences from your work?",
    "How do you share knowledge and experiences with other heat pump installers? Select all that apply.": "112. How do you share knowledge and experiences with other heat pump installers? Select all that apply.",
    "How do you share knowledge and experiences with other heat pump installers? Other.": "112o. How do you share knowledge and experiences with other heat pump installers? Other.",
    "How do you think manufacturers can better support heat pump installers? You can select up to three options.": "113. How do you think manufacturers can better support heat pump installers? You can select up to three options.",
    "How do you think manufacturers can better support heat pump installers? Other.": "113o. How do you think manufacturers can better support heat pump installers? Other.",
    "Have you experienced and/or have you been diagnosed with a mental health condition?": "114. Have you experienced and/or have you been diagnosed with a mental health condition?",
    'To what extent do you agree with this statement? "My work in the heat pump sector negatively affects my mental health."': '115. To what extent do you agree with this statement? "My work in the heat pump sector negatively affects my mental health."',
}


# %%
# Rename columns
data = data.rename(columns=column_dict)

# %%
# Reorder columns
data = data.loc[:, column_dict.values()]

# %% [markdown]
# # Save Cleaned Data as Parquet File

# %%
clean_data_path = f"""/mnt/g/Shared drives/A Sustainable Future/1. Reducing household emissions/\
2. Projects Research Work/36. Installer survey/05 survey data/{datetime.now().strftime("%Y%m%d")}_Installer_survey_clean_data_anonymised.parquet"""

# %%
data.to_parquet(clean_data_path)
