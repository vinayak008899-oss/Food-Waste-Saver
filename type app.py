import streamlit as st
import pandas as pd

# 1. SETUP THE PAGE
st.set_page_config(page_title="Food Saver Marketplace", page_icon="🛒", layout="wide")
st.title("🛒 Jaipur Food Saver: Live Marketplace")

# --- DATABASE SIMULATION (This holds the live deals) ---
# In a real startup, this would be a Cloud Database.
# For now, we simulate "Current Deals" available in the market.
if 'deals_db' not in st.session_state:
    st.session_state['deals_db'] = [
        {"Item": "Chocolate Cake", "Shop": "Sharma Bakery", "Original": 500, "Price": 250, "Discount": "50%", "Status": "Available"},
        {"Item": "Amul Milk", "Shop": "Reliance Fresh", "Original": 60, "Price": 12, "Discount": "80%", "Status": "Fast Selling!"},
    ]

# 2. CREATE TABS (The Two Faces)
tab1, tab2 = st.tabs(["🛍️ FOR CUSTOMERS", "🏪 FOR SHOPKEEPERS"])

# --- TAB 1: THE CUSTOMER VIEW (What Students See) ---
with tab1:
    st.header("⚡ Live Flash Sales in Jaipur")
    st.write("Grab these deals before they expire!")
    
    # Show the deals in a nice table
    deals_df = pd.DataFrame(st.session_state['deals_db'])
    st.dataframe(deals_df, use_container_width=True)
    
    st.info("ℹ️ Found a deal? Go to the shop and show this screen to claim it!")

# --- TAB 2: THE SHOPKEEPER VIEW (The AI Tool) ---
with tab2:
    st.header("📝 Post a New Deal")
    st.write("Use AI to calculate the best price and post it to the marketplace.")
    
    col1, col2 = st.columns(2)
    with col1:
        shop_name = st.text_input("Shop Name", "My Store")
        item_name = st.text_input("Product Name", "Sandwich")
    with col2:
        original_price = st.number_input("Original Price (₹)", min_value=10, value=100)
        days_left = st.slider("Days to Expiry", 0, 7, 1)

    # THE AI CALCULATION
    if days_left == 0:
        st.error("Item Expired. Do not sell.")
        valid_deal = False
    else:
        valid_deal = True
        discount = 0
        if days_left <= 1: discount = 0.80
        elif days_left <= 3: discount = 0.50
        elif days_left <= 7: discount = 0.10
        
        ai_price = round(original_price * (1 - discount), 2)
        st.success(f"🤖 AI Suggested Price: ₹{ai_price} ({int(discount*100)}% Off)")

    # THE "POST TO MARKET" BUTTON
    if valid_deal:
        if st.button("🚀 Post Deal to Marketplace"):
            # Add the new deal to our "Live Database"
            new_deal = {
                "Item": item_name,
                "Shop": shop_name,
                "Original": original_price,
                "Price": ai_price,
                "Discount": f"{int(discount*100)}%",
                "Status": "Just Posted"
            }
            st.session_state['deals_db'].append(new_deal)
            st.success(f"Success! {item_name} is now LIVE for customers to see.")
            st.balloons()
