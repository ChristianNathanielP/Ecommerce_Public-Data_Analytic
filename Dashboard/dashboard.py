import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load Dataset
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/ChristianNathanielP/Data_Analysis_Project-Ecommerce/main/Dashboard/cleaned_ecommerce_data.csv")
    return df

df = load_data()
st.title("E-Commerce Data Analysis Dashboard")

# Sidebar
st.sidebar.header("Filter")
categories = ["All"] + list(df["product_category_name"].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

payment_methods = ["All"] + list(df["payment_type"].dropna().unique())
selected_payment = st.sidebar.selectbox("Select Payment Method", payment_methods)


# Filter data berdasarkan Kategori
if selected_category != "All":
    df_filtered = df[df["product_category_name"] == selected_category]
else:
    df_filtered = df

if selected_payment != "All":
    df_filtered = df_filtered[df_filtered["payment_type"] == selected_payment]


# Statistik Utama
st.header("Key Statistics")

total_transactions = df_filtered["order_id"].nunique()
avg_price = df_filtered["price"].mean()
avg_rating = df_filtered["review_score"].mean()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Transactions", total_transactions)
with col2:
    st.metric("Average Product Price", f"{avg_price:.2f}")
with col3:
    st.metric("Average Rating", f"{avg_rating:.2f}")

# Visualisasi
st.header("Data Visualization")

# Top Categories by Transaction Count
st.subheader("Top Categories by Transaction Count")
top_categories = df_filtered["product_category_name"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(y=top_categories.index, x=top_categories.values, ax=ax, palette="Greens_r")
ax.set_xlabel("Transaction Count")
ax.set_ylabel("Category")
st.pyplot(fig)

# Most Used Payment Methods
st.subheader("Most Used Payment Methods")
payment_counts = df_filtered["payment_type"].value_counts()
fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(payment_counts, autopct='%1.1f%%', 
                                  startangle=140, colors=["#41644A", "#A7C957", "#BFD8AF", "#D4E7C5"],
                                  wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                                  explode=[0.02]*len(payment_counts))
for text in autotexts:
    text.set_fontsize(10)
ax.legend(payment_counts.index, title="Payment Methods", loc="center left", bbox_to_anchor=(1, 0.5))  
st.pyplot(fig)

# Top 15 Categories with Highest Average Price
st.subheader("Top 15 Categories with Highest Average Price")
top_15_avg_price = df_filtered.groupby("product_category_name")["price"].mean().sort_values(ascending=False).head(15)
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=top_15_avg_price.values, y=top_15_avg_price.index, ax=ax, palette="Greens_r")
ax.set_xlabel("Average Price")
ax.set_ylabel("Category")
st.pyplot(fig)

# Analisa
st.header("Analysis Results")

# Relationship Between Price, Freight value, and Rating
st.subheader("Relationship Between Price, Freight Value, and Rating")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price vs Rating")
    fig, ax = plt.subplots()
    heatmap_data = pd.pivot_table(
        df_filtered,
        values="price",
        index="review_score",
        aggfunc="mean"
    )
    sns.heatmap(heatmap_data, cmap="Greens", annot=True, fmt=".2f")
    st.pyplot(fig)

with col2:
    st.subheader("Freight Value vs Rating")
    fig, ax = plt.subplots()
    heatmap_data_freight = pd.pivot_table(
        df_filtered,
        values="freight_value",
        index="review_score",
        aggfunc="mean"
    )
    sns.heatmap(heatmap_data_freight, cmap="Greens", annot=True, fmt=".2f")
    st.pyplot(fig)

# Average Review Score per Product Category
st.subheader("Average Review Score per Product Category")
category_ratings = df_filtered.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False)
fig, ax = plt.subplots()
category_ratings.head(15).plot(kind='barh', color='#41644A')
plt.axvline(x=df_filtered['review_score'].mean(), color='r', linestyle='--', label='Overall Avg')
st.pyplot(fig)

# Percentage of Credit Card Transactions with Installments
st.subheader("Percentage of Credit Card Transactions with Installments")
credit_card_installments = df_filtered[(df_filtered['payment_type'] == 'credit_card') & (df_filtered['payment_installments'] > 1)]
installment_counts = credit_card_installments['product_category_name'].value_counts()
total_counts = df_filtered['product_category_name'].value_counts()

installment_ratio = (installment_counts / total_counts).fillna(0) * 100
credit_card_usage = df_filtered[df_filtered["payment_type"] == "credit_card"]["product_category_name"].value_counts(normalize=True) * 100

fig, ax = plt.subplots()
installment_ratio.sort_values(ascending=False).head(15).plot(kind='barh', color='#41644A')
st.pyplot(fig)

# Caption
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p style="font-size: 14px; color: gray;">Dashboard created by <b><a href="https://instagram.com/cnpngin._" target=_blank>Christian Nathaniel</a></b></p>
    </div>
    """,
    unsafe_allow_html=True
)

