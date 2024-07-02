# %% [markdown]
# #### Marking responses to Installer Survey Findings Quiz
#  These responses were collected at the Installer Show June 25-27 2024 via SurveyApp. This notebook is for marking responses and determining the respondent who got the highest number of correct answers.
# - Author: Elysia Lucas
# - Date: 02-07-2024

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
# Importing and cleaning data

# %%
# Read raw data (stored locally due to personal data i.e. email addresses)
responses_raw = pd.read_csv("../data/Responses-Survey-Findings-Quiz-20240625-20240627.csv")

## Cleaning
responses_clean = responses_raw.copy()

# Remove rows with 'abandoned' responses (i.e. incomplete)
responses_clean = responses_clean.drop(responses_clean[responses_clean['Abandoned'] == 1.0].index)

# Remove duplicate columns for Slide 3 and 15
responses_clean = responses_clean.drop(['3. 77% of respondents said their heat pump installation work in the last 12 months was ____.'], axis=1)
responses_clean = responses_clean.drop(['15. The most popular skills company owners want to add to their business to install more heat pumps are ___, ___ and ___.'], axis=1)
responses_clean = responses_clean.drop(['Unnamed: 42'], axis=1)

# Renaming columns
for n in range(0,len(responses_clean.columns)):
    if type(responses_clean.iloc[0,n]) == str:
        responses_clean.columns.values[n] = responses_clean.iloc[0,n]
    else:
        pass

# Remove redundant non-response first row
responses_clean = responses_clean.drop([0,0])

# Remove rows with responses from ASF team
responses_clean = responses_clean[responses_clean['1. Enter your email so we can contact you if you win'].str.contains("nesta")==False]

# Reset index
responses_clean = responses_clean.reset_index()


# %% [markdown]
# Marking each row of responses

# %%
def marking_responses(x: pd.DataFrame):
    '''Returns number of correct answers for a given row of responses'''

    score = 0

    # Q1
    if x["only/mostly retrofit"] == "1":
        score = score + 1
    else:
        pass

    # Q2
    if x["43%"] == "1":
        score = score + 1
    else:
        pass

    # Q3
    if x["87%"] == "1":
        score = score + 1
    else:
        pass

    # Q4
    if x["1%"] == "1":
        score = score + 1
    else:
        pass

    # Q5(i)-(iii)
    if x["low customer demand"] == "1":
        score = score + 1
    else:
        pass

    if x["difficulty finding additional staff"] == "1":
        score = score + 1
    else:
        pass

    if x["amount of time on 'unnecessary' tasks and admin"] == "1":
        score = score + 1
    else:
        pass

    # Q6
    if x["there is too much paperwork"] == "1":
        score = score + 1
    else:
        pass

    # Q7(i)-(iii)
    if x["sales and marketing skills"] == "1":
        score = score + 1
    else:
        pass

    if x["heat loss surveying and calculations"] == "1":
        score = score + 1
    else:
        pass

    if x["administrative skills"] == "1":
        score = score + 1
    else:
        pass

    # Q8
    if x["practical general plumbing skills"] == "1":
        score = score + 1
    else:
        pass

    # Q9
    if x["more than half"] == "1":
        score = score + 1
    else:
        pass

    # Q10
    if x["costs are too high across all quotes"] == "1":
        score = score + 1
    else:
        pass

    return score

# %%
# Score each row of responses
responses_marked = responses_clean.copy()
responses_marked["Score"] = responses_clean.apply(marking_responses, axis=1)

# Identify winner
# Maximum score is 14 correct answers
print("Highest score: "+ str(responses_marked["Score"].max()) + " out of 14")
i = responses_marked[["Score"]].idxmax()
print("Winner: " + responses_marked["1. Enter your email so we can contact you if you win"].iloc[i.values[0]])

# %% [markdown]
# Exploring most common answers

# %%
# Q1 77% of respondents said their heat pump installation work in the last 12 months was ____.
q1_answers = ["only/mostly retrofit", "only/mostly new build"]
q1_counts = [responses_clean["only/mostly retrofit"].count(),
          responses_clean["only/mostly new build"].count()]

q1_bars = plt.bar(q1_answers, q1_counts)
q1_bars[0].set_color('green')

# %%
# Q2 ___% of company owners said their company installed more than 10 heat pumps in the last 12 months.
q2_answers = ["28%", "43%", "62%", "95%"]
q2_counts = []
for x in q2_answers:
    count = responses_clean[x].count()
    q2_counts.append(count)

q2_bars = plt.bar(q2_answers, q2_counts)
q2_bars[1].set_color('green')

# %%
# Q3 ___% of respondents said they want to increase the number of heat pumps they install.
q3_answers = ["41%", "53%", "68%", "87%"]
q3_counts = []
for x in q3_answers:
    count = responses_clean[x].count()
    q3_counts.append(count)

q3_bars = plt.bar(q3_answers, q3_counts)
q3_bars[3].set_color('green')

# %%
# Q4 ___% of company owners said they don’t see any barriers to installing more heat pumps.
q4_answers = ["1%", "5%", "12%", "20%"]
q4_counts = []
for x in q4_answers:
    count = responses_clean[x].count()
    q4_counts.append(count)

q4_bars = plt.bar(q4_answers, q4_counts)
q4_bars[0].set_color('green')

# %%
# Q5 The top three barriers to installing more heat pumps reported by company owners are ___, ___ and ___.
q5_answers = ["low customer demand",
              "other work is more attractive",
              "difficulty sourcing hardware",
              "difficulty finding additional staff",
              "amount of time on 'unnecessary' tasks and admin"
              ]
q5_counts = []
for x in q5_answers:
    count = responses_clean[x].count()
    q5_counts.append(count)

q5_bars = plt.bar(q5_answers, q5_counts)
plt.xticks(rotation=90)
q5_bars[0].set_color('green')
q5_bars[3].set_color('green')
q5_bars[4].set_color('green')

# %%
# Q6 The most common reason why company owners haven’t obtained (or re-obtained) MCS certification is that ___.
q6_answers = ["it is too expensive",
              "there is too much paperwork",
              "there is too much required training",
              "they prefer to work through an MCS umbrella scheme",
              "they prefer to do retrofit outside the MCS scheme"
              ]
q6_counts = []
for x in q6_answers:
    count = responses_clean[x].count()
    q6_counts.append(count)

q6_bars = plt.bar(q6_answers, q6_counts)
plt.xticks(rotation=90)
q6_bars[1].set_color('green')

# %%
# Q7 The most popular skills company owners want to add to their business to install more heat pumps are ___, ___ and ___.
q7_answers = ["sales and marketing skills",
              "heat loss surveying and calculations",
              "heating system design",
              "administrative skills",
              "F-gas skills",
              "plumbing skills"
              ]
q7_counts = []
for x in q7_answers:
    count = responses_clean[x].count()
    q7_counts.append(count)

q7_bars = plt.bar(q7_answers, q7_counts)
plt.xticks(rotation=90)
q7_bars[0].set_color('green')
q7_bars[1].set_color('green')
q7_bars[3].set_color('green')

# %%
# Q8 55% of respondents think that ___ can be most improved in plumbing and heating apprenticeship training.
q8_answers = ["customer service and communication skills",
              "general knowledge in heating system design",
              "practical general plumbing skills",
              "practical skills for heat pump installation",
              "knowledge in low temperature heating system design"
              ]
q8_counts = []
for x in q8_answers:
    count = responses_clean[x].count()
    q8_counts.append(count)

q8_bars = plt.bar(q8_answers, q8_counts)
plt.xticks(rotation=90)
q8_bars[2].set_color('green')

# %%
# Q9 When asked what proportion of their heat pump enquiries turn into a comprehensive quote, the most popular answer was ___.
q9_answers = ["very few (10% or under)",
              "less than half",
              "more than half",
              "almost all (90-100%)"
              ]
q9_counts = []
for x in q9_answers:
    count = responses_clean[x].count()
    q9_counts.append(count)

q9_bars = plt.bar(q9_answers, q9_counts)
plt.xticks(rotation=90)
q9_bars[2].set_color('green')

# %%
# Q10 45% of respondents think the main reason for customers not proceeding with an installation after a quote is ___.
q10_answers = ["planning permission",
              "inconvenient work",
              "running cost estimates are too high",
              "cheaper quotes from another installer",
              "costs are too high across all quotes"
              ]
q10_counts = []
for x in q10_answers:
    count = responses_clean[x].count()
    q10_counts.append(count)

q10_bars = plt.bar(q10_answers, q10_counts)
plt.xticks(rotation=90)
q10_bars[4].set_color('green')


