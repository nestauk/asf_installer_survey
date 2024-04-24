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
from matplotlib import pyplot
import statsmodels.formula.api as smf
from scipy.stats import chi2_contingency

from asf_installer_survey.utils.lookups import QuestionNumbers as col

# %% [markdown]
# ## Aim
#
# The aim here to to explore the extent to which partially completed survey responses should be included/excluded from the installer survey analytical sample.
#
# At first glance, partials outnumber completions 401 - 367 (52% - 48%).
#
# If we apply the initial exclusion factor, based on `4. How long have you been working with heat pumps?` we exclude responents who don't work with heat pumps, don't know if they work with heat pumps or are only planning on working with heat pumps in the future or who had missing data.
#
# After removing ineligible responses, we see partials marginally outnumber completions 346 - 343 (50% - 50%).

# %%
# Load data
data_path = """/mnt/g/Shared drives/A Sustainable Future/1. Reducing household emissions/\
2. Projects Research Work/36. Installer survey/05 survey data/20240117_Installer_survey_clean_data_anonymised.parquet"""

data = pandas.read_parquet(data_path)

# %%
# Raw status
(
    data[col.q0d]
    .value_counts()
    .to_frame()
    .assign(proportion=lambda df: (df["count"] / df["count"].sum() * 100).round(1))
)

# %%
# Apply basic exclusion
exclusion_values = [
    "I don’t work with heat pumps and have no plans to do so",
    "I don’t work with heat pumps, but plan to do so in the twelve months",
    "Don't know",
    None,
]

data = data.loc[lambda df: ~df[col.q4].isin(exclusion_values), :]

# %%
# Status after basic exclusions
(
    data[col.q0d]
    .value_counts()
    .to_frame()
    .assign(proportion=lambda df: (df["count"] / df["count"].sum() * 100).round(1))
)

# %% [markdown]
# # How partial are partials?
#
# Or, how complete/close to finishing are the partial responses?

# %%
# Get a dataset just of partials (n=346)
partials = data.loc[lambda df: df[col.q0d] == "Partial", :]

# %% [markdown]
# ### Demographics
#
# Let's start by saying that demographics must be complete.

# %%
# A lambda function to test demographics completeness
demographics_filter = lambda df: (
    df[col.q1].isna()
    | df[col.q2].isna()
    | df[col.q3].isna()
    | df[col.q4].isna()
    | df[col.q5].isna()  # Any missing here has already been removed.
    | (df.loc[lambda x: x[col.q5] == "The owner or co-owner of a firm", col.q6a].isna())
    | (  # Q only applies to owners
        df.loc[lambda x: x[col.q5] == "An employee of a firm", col.q6b].isna()
    )
    | (  # Q only applies to employees
        df.loc[
            lambda x: x[col.q6a].isin(
                ["I own a company with 5 or fewer employees", "I’m a sole trader"]
            ),
            col.q7,
        ].apply(lambda y: len(y) == 0)
    )
    | df[col.q8].apply(  # Q only applies to small firms and sole traders.
        lambda x: len(x) == 0
    )
    | (
        df.loc[
            lambda x: x[col.q8].apply(lambda y: True if "England" in y else False),
            col.q9a,
        ].apply(lambda z: len(z) == 0)
    )
    | (  # Q only applies to companies in England
        df.loc[
            lambda x: x[col.q8].apply(lambda y: True if "Scotland" in y else False),
            col.q9b,
        ].apply(lambda z: len(z) == 0)
    )
    | (  # Q only applies to companies in Scotland
        df.loc[
            lambda x: x[col.q8].apply(lambda y: True if "Wales" in y else False),
            col.q9c,
        ].apply(lambda z: len(z) == 0)
    )
    | (  # Q only applies to companies in Wales
        df.loc[
            lambda x: x[col.q8].apply(
                lambda y: True if "Northern Ireland" in y else False
            ),
            col.q9d,
        ].apply(lambda z: len(z) == 0)
    )
    | df[col.q10].isna()  # Q only applies to companies in Northern Ireland
    | (
        df.loc[
            lambda x: x[col.q5] == "The owner or co-owner of a firm", col.q11a
        ].apply(lambda y: len(y) == 0)
    )
    | (  # Q only applies to owners
        df.loc[lambda x: x[col.q5] == "A contractor or freelancer", col.q11b].apply(
            lambda y: len(y) == 0
        )
    )
    | (  # Q only applies to contractors
        df.loc[lambda x: x[col.q5] == "An employee of a firm", col.q11c].apply(
            lambda y: len(y) == 0
        )
    )  # Q only applies to employees
)

# %%
# 37 people didn't complete the demographics section fully, we'll remove these.
demographics_filter(partials).sum()

# %%
# Now we have 309 partials.
partials = partials.loc[~demographics_filter(partials), :]

# %% [markdown]
# ## Subpopulation Completeness
#
# Owing to the complicated nature of the rest of the survey we'll focus on completeness in 4 key subpopulations:
# - Employees
# - Contractors
# - Sole traders
# - Owners (excluding soletraders)
#
# ### Employee completeness

# %%
employee_questions = [
    col.q1,
    col.q2,
    col.q3,
    col.q4,
    col.q5,
    col.q6b,
    col.q8,
    col.q10,
    col.q11c,  # page 1
    col.q12b,
    col.q13b,
    col.q14b,
    col.q15b,
    col.q16b[0],
    col.q17b[0],
    col.q18,
    col.q20[0],  # page 2
    col.q21c,
    col.q22c,
    col.q26c,  # page 3
    col.q30b,
    col.q31b[0],
    col.q32b[0],
    col.q33b,
    col.q34b[0],
    col.q35b[0],
    col.q36c[0],  # page 4
    col.q37b,
    col.q38b,
    *col.q41b,  # page 5
    col.q42b,
    col.q43c,
    col.q44b[0],
    col.q48c,
    col.q49b[0],
    col.q52b[0],  # page 6
    col.q53b,
    col.q54b[0],
    col.q55b,
    col.q56b[0],
    *col.q57,
    *col.q58b,
    col.q59,
    col.q60a[0],
    col.q70[0],  # page 7
    col.q90,
    col.q91,
    col.q92[0],
    col.q93,
    col.q94[0],
    col.q95,
    col.q96[0],  # page 10
    col.q97[0],
    col.q98,
    col.q99[0],
    col.q100[0],
    col.q101,
    col.q102[0],
    col.q103[0],
    col.q104[0],  # page 11
    *col.q105,
    *col.q106,
    col.q107[0],
    col.q108,
    col.q109,
    col.q110,
    col.q111,
    col.q112[0],
    col.q113[0],  # page 12
    col.q114,
    col.q115,  # page 13
]

# %%
employees = partials.loc[lambda df: df[col.q5] == "An employee of a firm", :]

# %%
completeness = []
for column in employee_questions:
    if employees[column].dtype == "category":
        completeness.append(1 - (employees[column].isna().sum() / len(employees)))
    elif employees[column].dtype == "object":
        completeness.append(
            1
            - (
                employees[column].apply(lambda x: True if len(x) == 0 else False).sum()
                / len(employees)
            )
        )
    else:
        pass

# %%
f, ax = pyplot.subplots(figsize=(11, 6))

pages = [8.5, 16.5, 19.5, 26.5, 41.5, 47.5, 73.5, 80.5, 88.5, 109.5, 111]
labels = [
    "Page 1",
    "Page 2",
    "Page 3",
    "Page 4",
    "Page 5",
    "Page 6",
    "Page 7",
    "Page 10",
    "Page 11",
    "Page 12",
    "Page 13",
]

ax.plot(completeness)
for page, label in zip(pages, labels):
    ax.axvline(x=page, linestyle="dashed", alpha=0.5)
    ax.text(
        x=page, y=0.02 if page < 27 else 0.8, s=label, ha="right", rotation="vertical"
    )

ax.set_yticks([x / 100 for x in range(0, 110, 10)])
ax.set_ylabel("Proportion Complete")
ax.grid(axis="y")
ax.set_xticks([])
ax.set_xticklabels([])

ax.set_title("Partial Responses for Employees (n=96)")

pyplot.savefig(
    "../../outputs/figures/completeness_employees.png", dpi=300, bbox_inches="tight"
)

# %% [markdown]
# ### Contractors

# %%
contractor_questions = [
    col.q1,
    col.q2,
    col.q3,
    col.q4,
    col.q5,
    col.q8,
    col.q10,
    col.q11b,  # page 1
    col.q12b,
    col.q13b,
    col.q14b,
    col.q15b,
    col.q16b[0],
    col.q17b[0],
    col.q18,
    col.q20[0],  # page 2
    col.q21b,
    col.q22b,
    col.q23b,
    col.q24b,
    col.q25c[0],
    col.q26b,
    col.q27b,
    col.q29[0],  # page 3
    col.q30b,
    col.q31b[0],
    col.q32b[0],
    col.q33b,
    col.q34b[0],
    col.q35b[0],
    col.q36d[0],  # page 4
    col.q37b,
    col.q38b,
    *col.q41b,  # page 5
    col.q42a,
    col.q43b,
    col.q44a[0],
    col.q45[0],
    col.q46,
    col.q47,
    col.q48b,
    col.q49a[0],
    col.q50[0],
    col.q51[0],
    col.q52a[0],  # p 6
    col.q53b,
    col.q54b[0],
    col.q55b,
    col.q56b[0],
    *col.q57,
    *col.q58c,
    col.q59,
    col.q60b[0],
    col.q70[0],  # page 7
    col.q90,
    col.q91,
    col.q92[0],
    col.q93,
    col.q94[0],
    col.q95,
    col.q96[0],  # page 10
    col.q97[0],
    col.q98,
    col.q99[0],
    col.q100[0],
    col.q101,
    col.q102[0],
    col.q103[0],
    col.q104[0],  # page 11
    *col.q105,
    *col.q106,
    col.q107[0],
    col.q108,
    col.q109,
    col.q110,
    col.q111,
    col.q112[0],
    col.q113[0],  # page 12
    col.q114,
    col.q115,  # page 13
]

# %%
contractors = partials.loc[lambda df: df[col.q5] == "A contractor or freelancer", :]

# %%
completeness = []
for column in contractor_questions:
    if contractors[column].dtype == "category":
        completeness.append(1 - (contractors[column].isna().sum() / len(contractors)))
    elif contractors[column].dtype == "object":
        completeness.append(
            1
            - (
                contractors[column]
                .apply(lambda x: True if len(x) == 0 else False)
                .sum()
                / len(contractors)
            )
        )
    else:
        pass

# %%
f, ax = pyplot.subplots(figsize=(11, 6))

pages = [7.5, 15.5, 23.5, 30.5, 45.5, 56.5, 83.5, 90.5, 98.5, 119.5, 121]
labels = [
    "Page 1",
    "Page 2",
    "Page 3",
    "Page 4",
    "Page 5",
    "Page 6",
    "Page 7",
    "Page 10",
    "Page 11",
    "Page 12",
    "Page 13",
]

ax.plot(completeness)
for page, label in zip(pages, labels):
    ax.axvline(x=page, linestyle="dashed", alpha=0.5)
    ax.text(
        x=page, y=0.02 if page < 60 else 0.8, s=label, ha="right", rotation="vertical"
    )

ax.set_yticks([x / 100 for x in range(0, 110, 10)])
ax.set_ylabel("Proportion Complete")
ax.grid(axis="y")
ax.set_xticks([])
ax.set_xticklabels([])

ax.set_title("Partial Responses for Contractors (n=32)")

pyplot.savefig(
    "../../outputs/figures/completeness_contractors.png", dpi=300, bbox_inches="tight"
)

# %% [markdown]
# ### Soletraders

# %%
soletrader_questions = [
    col.q1,
    col.q2,
    col.q3,
    col.q4,
    col.q5,
    col.q6a,
    col.q7,
    col.q8,
    col.q10,
    col.q11a,  # page 1
    col.q12b,
    col.q13b,
    col.q14b,
    col.q15b,
    col.q16b[0],
    col.q17b[0],
    col.q18,
    col.q20[0],  # page 2
    col.q21b,
    col.q22b,
    col.q23b,
    col.q24b,
    col.q25b[0],
    col.q25c[0],
    col.q26b,
    col.q27b,
    col.q29[0],  # page 3
    col.q30b,
    col.q31b[0],
    col.q32b[0],
    col.q33b,
    col.q34b[0],
    col.q35b[0],
    col.q36b[0],  # page 4
    col.q37b,
    col.q38b,
    col.q40b[0],
    col.q39b[0],
    *col.q41b,  # page 5
    col.q42a,
    col.q43b,
    col.q44a[0],
    col.q45[0],
    col.q46,
    col.q47,
    col.q48b,
    col.q49a[0],
    col.q50[0],
    col.q51[0],
    col.q52a[0],  # p 6
    col.q53b,
    col.q54b[0],
    col.q55b,
    col.q56b[0],
    *col.q57,
    *col.q58d,
    col.q59,
    col.q60a[0],
    col.q70[0],  # page 7
    *col.q71,
    col.q72[0],
    col.q73,
    col.q74,
    col.q75,
    col.q76,
    col.q77[0],
    col.q78,
    col.q79,  # page 8
    col.q80,
    col.q81[0],
    col.q82[0],
    col.q83,
    col.q84[0],
    col.q85[0],
    col.q86,
    col.q87[0],
    col.q88[0],
    col.q89a[0],
    col.q89b[0],  # p9
    col.q90,
    col.q91,
    col.q92[0],
    col.q93,
    col.q94[0],
    col.q95,
    col.q96[0],  # page 10
    col.q97[0],
    col.q98,
    col.q99[0],
    col.q100[0],
    col.q101,
    col.q102[0],
    col.q103[0],
    col.q104[0],  # page 11
    *col.q105,
    *col.q106,
    col.q107[0],
    col.q108,
    col.q109,
    col.q110,
    col.q111,
    col.q112[0],
    col.q113[0],  # page 12
    col.q114,
    col.q115,  # page 13
]

# %%
soletraders = partials.loc[lambda x: x[col.q6a] == "I’m a sole trader"]

# %%
completeness = []
for column in soletrader_questions:
    if soletraders[column].dtype == "category":
        completeness.append(1 - (soletraders[column].isna().sum() / len(soletraders)))
    elif soletraders[column].dtype == "object":
        completeness.append(
            1
            - (
                soletraders[column]
                .apply(lambda x: True if len(x) == 0 else False)
                .sum()
                / len(soletraders)
            )
        )
    else:
        pass

# %%
f, ax = pyplot.subplots(figsize=(11, 6))

pages = [
    9.5,
    17.5,
    26.5,
    33.5,
    50.5,
    61.5,
    88.5,
    103.5,
    114.5,
    121.5,
    129.5,
    150.5,
    152,
]
labels = [
    "Page 1",
    "Page 2",
    "Page 3",
    "Page 4",
    "Page 5",
    "Page 6",
    "Page 7",
    "Page 8",
    "Page 9",
    "Page 10",
    "Page 11",
    "Page 12",
    "Page 13",
]

ax.plot(completeness)
for page, label in zip(pages, labels):
    ax.axvline(x=page, linestyle="dashed", alpha=0.5)
    ax.text(
        x=page, y=0.02 if page < 62 else 0.8, s=label, ha="right", rotation="vertical"
    )

ax.set_yticks([x / 100 for x in range(0, 110, 10)])
ax.set_ylabel("Proportion Complete")
ax.grid(axis="y")
ax.set_xticks([])
ax.set_xticklabels([])

ax.set_title("Partial Responses for Sole traders (n=36)")

pyplot.savefig(
    "../../outputs/figures/completeness_soletraders.png", dpi=300, bbox_inches="tight"
)

# %% [markdown]
# ### Owners (Excluding Sole traders)

# %%
owner_questions = [
    col.q1,
    col.q2,
    col.q3,
    col.q4,
    col.q5,
    col.q6a,
    col.q7,
    col.q8,
    col.q10,
    col.q11a,  # page 1
    col.q12a,
    col.q13a,
    col.q14a,
    col.q15a,
    col.q16a[0],
    col.q17a[0],
    col.q18,
    col.q19[0],
    col.q20[0],  # page 2
    col.q21a,
    col.q22a,
    col.q23a,
    col.q24a,
    col.q25a[0],
    col.q26a,
    col.q27a,
    col.q28,
    col.q29[0],  # page 3
    col.q30a,
    col.q31a[0],
    col.q32a[0],
    col.q33a,
    col.q34a[0],
    col.q35a[0],
    col.q36a[0],  # page 4
    col.q37a,
    col.q38a,
    col.q39a[0],
    col.q40a[0],
    *col.q41a,  # page 5
    col.q42a,
    col.q43a,
    col.q44a[0],
    col.q45[0],
    col.q46,
    col.q47,
    col.q48a,
    col.q49a[0],
    col.q50[0],
    col.q51[0],
    col.q52a[0],  # p 6
    col.q53a,
    col.q54a[0],
    col.q55a,
    col.q56a[0],
    *col.q57,
    *col.q58a,
    col.q59,
    col.q60a[0],
    col.q70[0],  # page 7
    *col.q71,
    col.q72[0],
    col.q73,
    col.q74,
    col.q75,
    col.q76,
    col.q77[0],
    col.q78,
    col.q79,  # page 8
    col.q80,
    col.q81[0],
    col.q82[0],
    col.q83,
    col.q84[0],
    col.q85[0],
    col.q86,
    col.q87[0],
    col.q88[0],
    col.q89a[0],
    col.q89b[0],  # p9
    col.q90,
    col.q91,
    col.q92[0],
    col.q93,
    col.q94[0],
    col.q95,
    col.q96[0],  # page 10
    col.q97[0],
    col.q98,
    col.q99[0],
    col.q100[0],
    col.q101,
    col.q102[0],
    col.q103[0],
    col.q104[0],  # page 11
    *col.q105,
    *col.q106,
    col.q107[0],
    col.q108,
    col.q109,
    col.q110,
    col.q111,
    col.q112[0],
    col.q113[0],  # page 12
    col.q114,
    col.q115,  # page 13
]

# %%
owners = partials.loc[
    lambda x: (x[col.q5] == "The owner or co-owner of a firm")
    & (x[col.q6a] != "I’m a sole trader")
]

# %%
completeness = []
for column in owner_questions:
    if owners[column].dtype == "category":
        completeness.append(1 - (owners[column].isna().sum() / len(owners)))
    elif owners[column].dtype == "object":
        completeness.append(
            1
            - (
                owners[column].apply(lambda x: True if len(x) == 0 else False).sum()
                / len(owners)
            )
        )
    else:
        pass

# %%
f, ax = pyplot.subplots(figsize=(11, 6))

pages = [
    9.5,
    18.5,
    27.5,
    34.5,
    51.5,
    62.5,
    89.5,
    104.5,
    115.5,
    122.5,
    130.5,
    151.5,
    153,
]
labels = [
    "Page 1",
    "Page 2",
    "Page 3",
    "Page 4",
    "Page 5",
    "Page 6",
    "Page 7",
    "Page 8",
    "Page 9",
    "Page 10",
    "Page 11",
    "Page 12",
    "Page 13",
]

ax.plot(completeness)
for page, label in zip(pages, labels):
    ax.axvline(x=page, linestyle="dashed", alpha=0.5)
    ax.text(
        x=page, y=0.02 if page < 63 else 0.8, s=label, ha="right", rotation="vertical"
    )

ax.set_yticks([x / 100 for x in range(0, 110, 10)])
ax.set_ylabel("Proportion Complete")
ax.grid(axis="y")
ax.set_xticks([])
ax.set_xticklabels([])

ax.set_title("Partial Responses for Owners (excluding Sole traders) (n=145)")

pyplot.savefig(
    "../../outputs/figures/completeness_owners.png", dpi=300, bbox_inches="tight"
)


# %% [markdown]
# # Predictors of Completion
#
# ## Bivariate
#
# ### Subpopulation


# %%
# Add a subpopulation variable
def identify_subpopulation(row):
    if row[col.q5] == "An employee of a firm":
        return "An employee of a firm"
    elif row[col.q5] == "A contractor or freelancer":
        return "A contractor or freelancer"
    elif row[col.q5] == "The owner or co-owner of a firm":
        if row[col.q6a] == "I’m a sole trader":
            return "A sole trader"
        else:
            return "The owner or co-owner of a firm"
    else:
        return "Error"


data = data.loc[~demographics_filter(data), :].assign(
    subpopulation=lambda df: df.apply(identify_subpopulation, axis=1),
    complete=lambda df: df[col.q0d].map({"Complete": 1, "Partial": 0}).astype("uint8"),
)

# %%
pandas.crosstab(data[col.q0d], data["subpopulation"], margins="All")

# %%
pandas.crosstab(data[col.q0d], data["subpopulation"], normalize="columns", margins=True)

# %%
chi2_contingency(pandas.crosstab(data[col.q0d], data["subpopulation"]).values)

# %% [markdown]
# ### Age

# %%
pandas.crosstab(data[col.q0d], data[col.q1], margins="All")

# %%
pandas.crosstab(data[col.q0d], data[col.q1], normalize="columns", margins=True)

# %%
chi2_contingency(pandas.crosstab(data[col.q0d], data[col.q1]).values, correction=True)

# %% [markdown]
# ### How long have you worked in the plumbing and heating sector?

# %%
pandas.crosstab(data[col.q0d], data[col.q3], margins="All")

# %%
pandas.crosstab(data[col.q0d], data[col.q3], normalize="columns", margins=True)

# %%
chi2_contingency(pandas.crosstab(data[col.q0d], data[col.q3]).values)

# %%
model = smf.logit(
    "complete ~ var - 1", data=data.assign(var=lambda df: df[col.q3].astype(str))
).fit()

# %%
model.summary()

# %% [markdown]
# ### How long have you been working with heat pumps?

# %%
pandas.crosstab(data[col.q0d], data[col.q4], margins="All")

# %%
pandas.crosstab(data[col.q0d], data[col.q4], normalize="columns", margins=True)

# %%
chi2_contingency(pandas.crosstab(data[col.q0d], data[col.q4]).values)

# %%
model = smf.logit(
    "complete ~ var - 1", data=data.assign(var=lambda df: df[col.q4].astype(str))
).fit()

# %%
model.summary()

# %% [markdown]
# ### Region

# %%
data["England"] = data[col.q8].apply(lambda x: int("England" in x))
data["UK-wide business"] = data[col.q8].apply(lambda x: int("UK-wide business" in x))
data["Scotland"] = data[col.q8].apply(lambda x: int("Scotland" in x))
data["Wales"] = data[col.q8].apply(lambda x: int("Wales" in x))
data["Northern Ireland"] = data[col.q8].apply(lambda x: int("Northern Ireland" in x))
data["I don't work in the UK"] = data[col.q8].apply(
    lambda x: int("I don't work in the UK" in x)
)
data["Don't know"] = data[col.q8].apply(lambda x: int("Don't know" in x))

# %%
region_count = data.groupby(col.q0d).agg(
    {
        "England": "sum",
        "Scotland": "sum",
        "Wales": "sum",
        "Northern Ireland": "sum",
        "UK-wide business": "sum",
        "I don't work in the UK": "sum",
        "Don't know": "sum",
    }
)

region_count.assign(all=region_count.sum(axis=1))

# %%
region_count.assign(all=region_count.sum(axis=1)).sum()

# %%
region_count / region_count.sum(axis=0)

# %%
chi2_contingency(region_count.values, correction=True)

# %%
model = smf.logit(
    'complete ~ England + Scotland + Wales + Q("Northern Ireland") + Q("UK-wide business") + Q("I don\'t work in the UK") + Q("Don\'t know") - 1',
    data=data,
).fit()

# %%
model.summary()

# %% [markdown]
# ### Multivariate Analysis

# %%
model = smf.logit(
    'complete ~ var + England + Scotland + Wales + Q("Northern Ireland") + Q("UK-wide business") + Q("I don\'t work in the UK") + Q("Don\'t know") ',
    data=data.assign(var=lambda df: df[col.q4].astype(str)),
).fit()

# %%
model.summary()

# %%
col.q111


# %%
def define_analytical_sample(row):
    if row["0d. Status"] == "Complete":
        return True
    elif (row["0d. Status"] == "Partial") & (len(row[col.q113[0]]) > 0):
        return True
    else:
        return False


data.apply(lambda row: define_analytical_sample(row), axis=1).sum()
