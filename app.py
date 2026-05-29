import streamlit as st
import gzip
import simplejson
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Streamlit title
# ----------------------------
st.title("Amazon Watch Reviews Analysis")

# ----------------------------
# Parse function
# ----------------------------
def parse(filename):
    f = gzip.open(filename, 'rt')

    entry = {}

    for l in f:
        l = l.strip()

        colonPos = l.find(':')

        if colonPos == -1:
            yield entry
            entry = {}
            continue

        eName = l[:colonPos]
        rest = l[colonPos + 2:]

        entry[eName] = rest

    yield entry

# ----------------------------
# Load dataset
# ----------------------------
parsed_data = list(parse("Watches.txt.gz"))

df = pd.DataFrame(parsed_data)

# ----------------------------
# Convert scores to numeric
# ----------------------------
df['review/score'] = pd.to_numeric(df['review/score'])

# ----------------------------
# Count review scores
# ----------------------------
score_counts = df['review/score'].value_counts().sort_index()

# ----------------------------
# Create plot
# ----------------------------
fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(
    x=score_counts.index,
    y=score_counts.values,
    palette='viridis',
    ax=ax
)

ax.set_title('Count of Reviews by Score')
ax.set_xlabel('Review Score')
ax.set_ylabel('Number of Reviews')

# Add labels on top of bars
for index, value in enumerate(score_counts.values):
    ax.text(
        index,
        value + 50,
        str(value),
        ha='center'
    )

# ----------------------------
# Show plot in Streamlit
# ----------------------------
st.pyplot(fig)
