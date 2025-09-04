import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page
st.set_page_config(layout="wide")
st.title("Book Analysis Dashboard")

# =================================================================
# 1. AUTOBIOGRAPHY SCATTER PLOT (FROM FIRST CSV)
# =================================================================
st.header("Autobiography Books: Ratings vs Popularity")

AUTO_CSV = "1000_autobio_books.csv" 
auto_df = pd.read_csv(AUTO_CSV)

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.scatterplot(
    data=auto_df,
    x="Number of Ratings",
    y="Ratings",
    hue="First Published Year",
    palette="viridis",
    alpha=0.7,
    s=100,
    ax=ax1
)
ax1.set_title("Ratings vs Number of Ratings (Autobiographies)")
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# =================================================================
# 2. FICTION BAR GRAPH (FROM SECOND CSV)
# =================================================================
st.header("Top Fiction Books by Demand")

# Load second CSV (fiction)
FICTION_CSV = "1000_fiction_books.csv"
fiction_df = pd.read_csv(FICTION_CSV)

top_books = fiction_df.sort_values("Number of People Who Want to Read", ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(
    data=top_books,
    x="Number of People Who Want to Read",
    y="Title",
    palette="rocket",
    ax=ax2
)
ax2.set_title("Top 10 Most Wanted Fiction Books")
ax2.set_xlabel("Number of People Who Want to Read")
ax2.set_ylabel("")
st.pyplot(fig2)

# =================================================================
# 3. CHILDREN'S BOOKS HISTOGRAM
# =================================================================
st.header("Children's Books Rating Distribution")

children_df = pd.read_csv("1000_children_books.csv") 

fig3, ax3 = plt.subplots(figsize=(10,5))
sns.histplot(
    data=children_df,
    x="Ratings",
    bins=20,
    kde=True,
    color="skyblue",
    ax=ax3
)
ax3.set_title("Distribution of Ratings for Children's Books")
ax3.set_xlabel("Rating Score")
ax3.set_ylabel("Number of Books")
ax3.grid(alpha=0.3)
st.pyplot(fig3)

## =================================================================
# 4. HISTORY BOOKS SIMPLE LINE GRAPH (NEW)
# =================================================================
st.header("History Books Publication Trends")
history_df = pd.read_csv("1000_history_books.csv")  


year_counts = history_df["First Published Year"].value_counts().sort_index()


fig4, ax4 = plt.subplots(figsize=(10,4))  
plt.plot(year_counts.index, year_counts.values, 
         color='#2c7bb6', linewidth=2) 


ax4.set_title("Books Published Per Year", pad=20)
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Books")

# Remove spines and grid for cleaner look
sns.despine()
st.pyplot(fig4)

# =================================================================
# RAW DATA TOGGLE
# =================================================================
if st.checkbox("📊 Show raw data"):
    st.subheader("Autobiography Data")
    st.write(auto_df)
    st.subheader("Fiction Data")
    st.write(fiction_df)
    st.subheader("Children's Books Data")
    st.write(children_df)
    st.subheader("History Books Data")
    st.write(history_df)