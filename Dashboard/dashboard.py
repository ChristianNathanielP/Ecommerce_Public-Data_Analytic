import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load Dataset
def load_data():
    df = pd.read_csv("..\Data\cleaned_ecommerce_data.csv")  
    # df = pd.read_csv("https://raw.githubusercontent.com/Data_Analysis_Project-Ecommerce/main/Dashboard/cleaned_ecommerce_data.csv")  
    return df

df = load_data()
st.title("E-Commerce Data Analysis Dashboard")

# Sidebar
st.sidebar.header("Filter")
categories = ["All"] + list(df["product_category_name"].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)


# Filter data berdasarkan Kategori
if selected_category != "All":
    df_filtered = df[df["product_category_name"] == selected_category]
else:
    df_filtered = df

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
st.header("Data Visualitation")

st.subheader("Top Categories by Transaction Count")
top_categories = df["product_category_name"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(y=top_categories.index, x=top_categories.values, ax=ax, palette=sns.color_palette("Greens_r", len(top_categories)))
ax.set_xlabel("Transaction Count")
ax.set_ylabel("Category")
st.pyplot(fig)

st.subheader("Most Used Payment Methods")
payment_counts = df["payment_type"].value_counts()
fig, ax = plt.subplots(figsize=(7, 5))  
wedges, texts, autotexts = ax.pie(payment_counts, autopct='%1.1f%%', 
                                  startangle=140, colors=["#41644A", "#A7C957", "#BFD8AF", "#D4E7C5"],
                                  wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                                  explode=[0.02]*len(payment_counts))
for text in autotexts:
    text.set_fontsize(10)
ax.legend(payment_counts.index, title="Payment Methods", loc="center left", bbox_to_anchor=(1, 0.5))  
st.pyplot(fig)

st.subheader("Top 15 Categories with Highest Average Price")
top_15_avg_price = df.groupby("product_category_name")["price"].mean().sort_values(ascending=False).head(15)
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=top_15_avg_price.values, y=top_15_avg_price.index, ax=ax, palette=sns.color_palette("Greens_r", len(top_15_avg_price)))
ax.set_xlabel("Average Price")
ax.set_ylabel("Category")
st.pyplot(fig)


# Analisa
st.header("Analysis Results")

## Q1
st.subheader("Relationship Between Price, Freight value, and Rating")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price vs Rating")
    fig, ax = plt.subplots()
    heatmap_data = pd.pivot_table(
        df,
        values="price",
        index="review_score",
        columns="price_category",
        aggfunc="count",
        observed=False)
    sns.heatmap(heatmap_data, cmap="Greens", annot=True, fmt="d")
    st.pyplot(fig)

with col2:
    st.subheader("Freight Value vs Rating")
    heatmap_data_freight = pd.pivot_table(
    df,
    values="freight_value",
    index="review_score",
    columns="freight_value_category",
    aggfunc="count",
    observed=False)
    sns.heatmap(heatmap_data_freight, cmap="Greens", annot=True, fmt="d")
    st.pyplot(fig)

# Q2
st.subheader("Average Review Score per Product Category")
category_ratings = df.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False)
print(category_ratings)

fig, ax = plt.subplots()
category_ratings.head(15).plot(kind='barh', color='#41644A')
plt.axvline(x=df['review_score'].mean(), color='r', linestyle='--', label='Overall Avg')
st.pyplot(fig)

#Q3
st.subheader("Percentage of Credit Card Transactions with Installments")
credit_card_installments = df[(df['payment_type'] == 'credit_card') & (df['payment_installments'] > 1)]
installment_counts = credit_card_installments['product_category_name'].value_counts()
total_counts = df['product_category_name'].value_counts()

installment_ratio = (installment_counts / total_counts).fillna(0) * 100
credit_card_usage = df[df["payment_type"] == "credit_card"]["product_category_name"].value_counts(normalize=True) * 100

fig, ax = plt.subplots()
installment_ratio.sort_values(ascending=False).head(15).plot(kind='barh', color='#41644A')
st.pyplot(fig)



#Caption
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p style="font-size: 14px; color: gray;">Dashboard created by <b><a href="https://instagram.com/cnpngin._" target=_blank>Christian Nathaniel</a></b></p>
    </div>
    """,
    unsafe_allow_html=True
)