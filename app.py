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

# =========================================================
# Plot 2: Top 10 Products by Number of Reviews
# =========================================================

st.subheader("Top 10 Products by Number of Reviews")

# Group by product title and count reviews
product_review_counts = df['product/title'].value_counts().reset_index()

product_review_counts.columns = [
    'product/title',
    'review_count'
]

# Get top 10
top_10_products = product_review_counts.head(10)

# Create figure
fig2, ax2 = plt.subplots(figsize=(12, 8))

sns.barplot(
    x='review_count',
    y='product/title',
    data=top_10_products,
    palette='viridis',
    ax=ax2
)

ax2.set_title('Top 10 Products by Number of Reviews')
ax2.set_xlabel('Number of Reviews')
ax2.set_ylabel('Product Title')

# Add labels
for index, row in top_10_products.iterrows():
    ax2.text(
        row['review_count'],
        index,
        f"{row['review_count']}",
        color='black',
        va='center'
    )

# Show in Streamlit
st.pyplot(fig2)


# =========================================================
# Plot 3: Average Review Score for Top 10 Products
# =========================================================

st.subheader("Average Review Score for Top 10 Products")

# Get titles
top_10_product_titles = top_10_products['product/title'].tolist()

# Filter dataframe
df_top_10_reviews = df[
    df['product/title'].isin(top_10_product_titles)
].copy()

# Convert scores to numeric
df_top_10_reviews['review/score'] = pd.to_numeric(
    df_top_10_reviews['review/score'],
    errors='coerce'
)

# Remove NaN values
df_top_10_reviews.dropna(
    subset=['review/score'],
    inplace=True
)

# Average score
average_scores = (
    df_top_10_reviews
    .groupby('product/title')['review/score']
    .mean()
    .reset_index()
)

# Sort
average_scores = average_scores.sort_values(
    by='review/score',
    ascending=False
)

# Create figure
fig3, ax3 = plt.subplots(figsize=(12, 8))

sns.barplot(
    x='review/score',
    y='product/title',
    data=average_scores,
    palette='magma',
    ax=ax3
)

ax3.set_title('Average Review Score for Top 10 Products')
ax3.set_xlabel('Average Review Score')
ax3.set_ylabel('Product Title')

ax3.set_xlim(0, 5)

# Add labels
for index, row in average_scores.iterrows():
    ax3.text(
        row['review/score'],
        index,
        f"{row['review/score']:.2f}",
        color='black',
        va='center'
    )

# Show in Streamlit
st.pyplot(fig3)
