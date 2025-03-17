import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Get the directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get all CSV file paths in the same directory
csv_files = glob.glob(os.path.join(current_dir, "*.csv"))

# Correct way to store CSVs in a dictionary (key = filename, value = DataFrame)
dataframes_dict = {os.path.basename(file): pd.read_csv(file) for file in csv_files}

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the full image path
image_path = os.path.join(current_dir, "logo.png")

# Function to filter invalid datetime entries
def filter_invalid_dates(df, column):
    invalid_entries = df[~pd.to_datetime(df[column], errors='coerce').notna()]
    print("Invalid entries detected:\n", invalid_entries)
    return df[pd.to_datetime(df[column], errors='coerce').notna()]
# Sidebar
# Custom CSS to reduce sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 260px;  /* Adjust sidebar width */
        max-width: 260px;  /* Keep it fixed */
    }
    .sidebar-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .sidebar-subtitle {
        font-size: 14px;
        margin-bottom: 10px;
        color: #c4c4c4;
    }
    .stRadio > label {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Load the cleaned dataset
df_order_approved = dataframes_dict["cleaned_df_customer.csv"]

# Filter out invalid datetime entries
df_order_approved = filter_invalid_dates(df_order_approved, "order_approved_at")

# Safely convert the 'order_approved_at' column to datetime
df_order_approved["order_approved_at"] = pd.to_datetime(df_order_approved["order_approved_at"], errors='coerce')

# Handle NaT values if necessary
df_order_approved["order_approved_at"].fillna(pd.Timestamp('today'), inplace=True)

# Define the min and max dates based on the 'order_approved_at' column
min_date = df_order_approved["order_approved_at"].min()
max_date = df_order_approved["order_approved_at"].max()

with st.sidebar:
    st.image(image_path, width=220)
    st.markdown("<h4 style='text-align: center;'>DINS TECH</h4>", unsafe_allow_html=True)
    st.write("Smart Solutions for a Digital World")
    st.write("---")  # Horizontal line for separation
    # Date Range input
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    st.write("---")  # Horizontal line for separation

    st.write("📊 **Dashboard Navigation**")
    page = st.radio(
        "Select a page:",
        ["Overview", "Insightful Graph"],
        index=0
    )

# Create a placeholder
message_placeholder = st.empty()

# Display the selected page message temporarily
message_placeholder.write(f"### You selected: {page}")

# Wait for 2 seconds, then clear the message
time.sleep(1)

message_placeholder.empty() #Display selected page
# Main
if page == "Overview":
    st.title('E-Commerce Public Data Analysis')
    st.markdown("<h4>This is a dashboard for analyzing and got insight from E-Commerce public data.</h4>", unsafe_allow_html=True)
    st.link_button('dataset','https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download')
    st.write(' ')
    st.write(' ')

    st.subheader("Contact Information")
    st.write("**Name:** Labiba Adinda Zahwana")
    st.write("**Email:** labibaadinda11@gmail.com")
    st.write("**LinkedIn:** [Profil LinkedIn](https://id.linkedin.com/in/labibaadinda/)")
    st.write("**GitHub:** [Profil GitHub](https://github.com/labibaadinda)")


elif page == "Insightful Graph":
    st.title('Graph E-Commerce Public Data Analysis')
    st.markdown("<h6>This dashboard provides powerful insights by analyzing and visualizing E-Commerce public data through various graphs, helping you gain meaningful patterns and trends.</h6>", unsafe_allow_html=True)
    st.write(' ')

    # Load DataFrame from Dictionary
    df_customer = dataframes_dict["cleaned_df_customer.csv"]

    # Ensure 'order_purchase_timestamp' is in datetime format
    df_customer['order_purchase_timestamp'] = pd.to_datetime(df_customer['order_purchase_timestamp'])

    # Filter orders per year
    order_in_2016 = df_customer[df_customer['order_purchase_timestamp'].dt.year == 2016]
    order_in_2017 = df_customer[df_customer['order_purchase_timestamp'].dt.year == 2017]
    order_in_2018 = df_customer[df_customer['order_purchase_timestamp'].dt.year == 2018]

    # Count orders per month
    order_2016_counts = order_in_2016['order_purchase_timestamp'].dt.month.value_counts().sort_index()
    order_2017_counts = order_in_2017['order_purchase_timestamp'].dt.month.value_counts().sort_index()
    order_2018_counts = order_in_2018['order_purchase_timestamp'].dt.month.value_counts().sort_index()

    # Ensure all months (1-12) are included, fill missing months with 0
    order_2016_counts = order_2016_counts.reindex(range(1, 13), fill_value=0)
    order_2017_counts = order_2017_counts.reindex(range(1, 13), fill_value=0)
    order_2018_counts = order_2018_counts.reindex(range(1, 13), fill_value=0)

    st.write(' ')

    # Streamlit App Title
    st.subheader("📊 Total Orders Per Month (2016-2018)")

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data for each year
    ax.plot(order_2016_counts.index, order_2016_counts.values, marker='o', linestyle='-', label='2016')
    ax.plot(order_2017_counts.index, order_2017_counts.values, marker='s', linestyle='-', label='2017')
    ax.plot(order_2018_counts.index, order_2018_counts.values, marker='^', linestyle='-', label='2018')

    # Labels and title
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Orders")
    ax.set_title("Total Orders Per Month by Year (2016-2018)")
    ax.set_xticks(range(1, 13))  # Ensure months 1-12 appear
    ax.legend()
    ax.grid(True)

    # Display the plot in Streamlit
    st.pyplot(fig)

    st.write(' ')



    # Load dataset from dictionary
    df_order_customer = dataframes_dict["cleaned_df_customer.csv"]

    # Fix column names (strip spaces)
    df_order_customer.columns = df_order_customer.columns.str.strip()

    # Load dataset from dictionary
    df_order_customer = dataframes_dict["cleaned_df_customer.csv"]

    # Ensure dates are in datetime format
    df_order_customer['order_delivered_customer_date'] = pd.to_datetime(df_order_customer['order_delivered_customer_date'])
    df_order_customer['order_estimated_delivery_date'] = pd.to_datetime(df_order_customer['order_estimated_delivery_date'])

    # Create a new column: 'ontime_or_late'
    df_order_customer['ontime_or_late'] = np.where(df_order_customer['order_delivered_customer_date'] <= df_order_customer['order_estimated_delivery_date'], 'On-Time', 'Late')

    # Calculate percentage of "On-Time" vs "Late" order_customer
    info_late_ontime = df_order_customer.groupby('ontime_or_late').size()
    info_late_ontime = (info_late_ontime / info_late_ontime.sum()) * 100  # Convert to percentage
    
    st.write(' ')
    # Streamlit Title
    st.subheader("📦 Order Delivery Performance")
    st.write(' ')

    ## Convert the grouped Series into a DataFrame and reset index
    df_info = info_late_ontime.reset_index()

    # Rename the columns properly
    df_info.columns = ["Order Status", "Percentage (%)"]

    # Format percentage values correctly
    df_info["Percentage (%)"] = df_info["Percentage (%)"].map(lambda x: f"{x:.2f} %")

    st.dataframe(df_info, hide_index=True)  # Hide default index


    # Create Bar Chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(info_late_ontime.index, info_late_ontime.values, color=["red", "green"])
    ax.set_xlabel("Order Status")
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Order Status Distribution (On-Time vs Late)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.write(' ')
    # Load dataset from dictionary
    df_customer = dataframes_dict["cleaned_df_customer.csv"]

    # Get top 5 cities with the most customers
    top_cities = df_customer['customer_city'].value_counts().nlargest(5)

    # Streamlit Title
    st.subheader("📍 Top 5 Customer Cities")

    # Display the table in Streamlit
    df_top_cities = top_cities.reset_index()
    df_top_cities.columns = ["City", "Total Customers"]  # Rename columns
    st.dataframe(df_top_cities, hide_index=True)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(top_cities.index, top_cities.values, color="blue")
    ax.set_xlabel("City")
    ax.set_ylabel("Total Customers")
    ax.set_title("Top 5 Cities with Most Customers")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Display the chart in Streamlit
    st.pyplot(fig)
    
    st.write(' ')
    st.write(' ')


    # Load dataset from dictionary
    df_payments = dataframes_dict["cleaned_order_payments_dataset.csv"]

    # Get the most used payment types
    payment_counts = df_payments['payment_type'].value_counts()

    # Streamlit Title
    st.subheader("💳 Most Used Payment Types by Customers")

    # Display the table in Streamlit
    df_payment_types = payment_counts.reset_index()
    df_payment_types.columns = ["Payment Type", "Total Transactions"]
    st.dataframe(df_payment_types, hide_index=True)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(payment_counts.index, payment_counts.values, color="purple")
    ax.set_xlabel("Payment Type")
    ax.set_ylabel("Total Transactions")
    ax.set_title("Most Used Payment Types by Customers")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Display the chart in Streamlit
    st.pyplot(fig)
    
    st.write(' ')
    st.write(' ')
    
    # Load dataset from dictionary
    df_category = dataframes_dict["cleaned_df_category.csv"]

    # Get the top 10 most purchased product categories
    top_products = df_category['product_category_name'].value_counts().nlargest(10)

    # Streamlit Title
    st.subheader("🛒 Top 10 Most Purchased Products")

    # Display the table in Streamlit
    df_top_products = top_products.reset_index()
    df_top_products.columns = ["Product Category", "Total Purchases"]
    st.dataframe(df_top_products, hide_index=True)

    # Create a line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(top_products.index, top_products.values, marker='o', linestyle='-', color="blue")

    # Labeling
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Purchases")
    ax.set_title("Top 10 Most Purchased Products")
    ax.set_xticklabels(top_products.index, rotation=25)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Display the chart in Streamlit
    st.pyplot(fig)
    

    