import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Shopping Optimizer", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>🛒 Smart Shopping Optimizer</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Settings")
budget = st.sidebar.number_input("Enter Budget (₹)", min_value=1)

num_products = st.sidebar.slider("Number of Products", 1, 10, 3)

# Input Section
st.subheader("🧾 Enter Product Details")

products = []

col1, col2, col3 = st.columns(3)

for i in range(num_products):
    with col1:
        name = st.text_input(f"Product {i+1}", key=f"name{i}")
    with col2:
        price = st.number_input(f"Price ₹{i+1}", key=f"price{i}")
    with col3:
        value = st.number_input(f"Value {i+1}", key=f"value{i}")
    
    products.append((name, price, value))

# Knapsack Algorithm
def knapsack(products, budget):
    n = len(products)
    dp = [[0]*(int(budget)+1) for _ in range(n+1)]

    for i in range(1, n+1):
        name, price, value = products[i-1]
        for w in range(int(budget)+1):
            if price <= w:
                dp[i][w] = max(value + dp[i-1][w-int(price)], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    res = dp[n][int(budget)]

    w = int(budget)
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(products[i-1][0])
            w -= int(products[i-1][1])

    return res, selected

# Optimize Button
if st.button("🚀 Optimize Shopping"):
    max_value, selected = knapsack(products, budget)

    st.success(f"✅ Maximum Value: {max_value}")

    # DataFrame
    df = pd.DataFrame(products, columns=["Product", "Price", "Value"])

    st.subheader("📊 Product Table")
    st.dataframe(df)

    # Highlight selected
    st.subheader("🛍️ Selected Products")
    for item in selected:
        st.markdown(f"✔️ **{item}**")

    # Chart
    st.subheader("📈 Price vs Value Graph")

    fig, ax = plt.subplots()
    ax.scatter(df["Price"], df["Value"])

    for i, txt in enumerate(df["Product"]):
        ax.annotate(txt, (df["Price"][i], df["Value"][i]))

    ax.set_xlabel("Price")
    ax.set_ylabel("Value")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("💡 Developed for PBL-II | Advanced Shopping Optimization System")
