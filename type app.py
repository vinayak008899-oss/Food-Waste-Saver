import streamlit as st

# 1. APP CONFIGURATION
st.set_page_config(page_title="Food Saver AI", page_icon="🍎")
st.title("🍎 Food Waste Rescue AI")
st.write("### Dynamic Pricing Engine for Supermarkets")

# 2. SIDEBAR (Inventory)
st.sidebar.header("📦 Live Inventory Database")
inventory = {
    "Milk":  {"price": 60, "stock": 50},
    "Bread": {"price": 40, "stock": 20},
    "Cake":  {"price": 500, "stock": 5}
}
st.sidebar.json(inventory)

# 3. MAIN INTERFACE
col1, col2 = st.columns(2)
with col1:
    item = st.selectbox("Select Product", list(inventory.keys()))
with col2:
    days_left = st.slider("Days until Expiration", 0, 15, 5)

# 4. THE AI BRAIN
if st.button("💰 Calculate AI Price"):
    original_price = inventory[item]["price"]
    
    if days_left == 0:
        st.error(f"❌ STOP! {item} is Expired. Donate to Compost.")
    else:
        # Dynamic Pricing Logic
        discount = 0
        if days_left <= 1: discount = 0.80
        elif days_left <= 3: discount = 0.50
        elif days_left <= 7: discount = 0.10
        
        final_price = original_price * (1 - discount)
        
        # Display Results
        st.success(f"✅ SELL NOW FOR: ₹{final_price}")
        st.metric(label="Discount Applied", value=f"{int(discount*100)}%", delta=f"-₹{original_price - final_price}")
        
        if discount >= 0.50:
            st.balloons()
            st.warning("⚠️ High Urgency Sale! Push notification sent to customers.")
