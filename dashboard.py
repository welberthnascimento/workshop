import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Financial Transaction Analysis Dashboard")


@st.cache_data
def load_data():
    file_path = r"c:\Users\pereiwe\git_projects\workshop\data\unzipped_archive\Synthetic_Financial_datasets_log.csv"
    df = pd.read_csv(file_path)
    return df


data_load_state = st.text("Loading data...")
df = load_data()
data_load_state.text("Loading data...done!")

st.header("Dataset Overview")
st.write(df.head())
st.write(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

st.header("Transaction Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Types Distribution")
    fig_transaction_types = px.pie(df, names="type", title="Distribution of Transaction Types")
    st.plotly_chart(fig_transaction_types, use_container_width=True)

with col2:
    st.subheader("Fraudulent vs. Non-Fraudulent Transactions")
    fraud_counts = df["isFraud"].value_counts().reset_index()
    fraud_counts.columns = ["isFraud", "count"]
    fraud_counts["isFraud"] = fraud_counts["isFraud"].map({0: "Not Fraud", 1: "Fraud"})
    fig_fraud = px.bar(
        fraud_counts,
        x="isFraud",
        y="count",
        title="Number of Fraudulent vs. Non-Fraudulent Transactions",
        color="isFraud",
        color_discrete_map={"Not Fraud": "blue", "Fraud": "red"},
    )
    st.plotly_chart(fig_fraud, use_container_width=True)

st.header("Exploring Fraudulent Transactions")

fraudulent_transactions = df[df["isFraud"] == 1]

st.subheader("Transaction Types in Fraudulent Activities")
fig_fraud_types = px.pie(
    fraudulent_transactions, names="type", title="Distribution of Transaction Types in Fraudulent Activities"
)
st.plotly_chart(fig_fraud_types, use_container_width=True)

st.subheader("Details of Fraudulent Transactions")
st.write(fraudulent_transactions.head())

st.subheader("Transaction Amount Distribution for Fraudulent vs. Non-Fraudulent Transactions")
fig_amount_dist = px.histogram(
    df,
    x="amount",
    color="isFraud",
    nbins=50,
    title="Transaction Amount Distribution",
    labels={"amount": "Transaction Amount"},
    barmode="overlay",
)
st.plotly_chart(fig_amount_dist, use_container_width=True)
