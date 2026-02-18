import streamlit as st
import random

# 1. PAGE SETUP (Mobile Friendly Layout)
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- MOCK DATABASE (With Locations & Images) ---
if 'deals_db' not in st.session_state:
    st.session_state['deals_db'] = [
        {
            "Item": "Chocolate Truffle", 
            "Shop": "Sharma Bakery", 
            "Location": "Vaishali Nagar", 
            "Original": 500, 
            "Price": 250, 
            "Image": "https://share.google/xNX4MB5XRTq5sr4n6"
        },
        {
            "Item": "Farmhouse Pizza", 
            "Shop": "Dominos Surplus", 
            "Location": "Raja Park", 
            "Original": 400, 
            "Price": 150, 
            "Image": "https://source.unsplash.com/400x300/?pizza"
        },
        {
            "Item": "Paneer Patties (Bulk)", 
            "Shop": "Rawat Mishthan", 
            "Location": "Sindhi Camp", 
            "Original": 200, 
            "Price": 50, 
            "Image": "https://source.unsplash.com/400x300/?indianfood"
        }
    ]

# 2. APP TITLE
st.title("🍔 Jaipur Food Saver")
st.write("Don't let good food go to waste. Eat cheap, save the planet.")

# 3. TABS (Customer vs Shopkeeper)
tab1, tab2 = st.tabs(["🛍️ I WANT FOOD", "🏪 I HAVE FOOD"])

# --- TAB 1: THE CUSTOMER EXPERIENCE (Visual & Local) ---
with tab1:
    # THE "NEAR ME" FILTER
    locations = ["All Jaipur", "Vaishali Nagar", "Raja Park", "Sindhi Camp", "Malviya Nagar"]
    selected_location = st.selectbox("📍 Where are you?", locations)
    
    st.markdown("---") # A divider line
    
    # FILTER THE DEALS
    count = 0
    for deal in st.session_state['deals_db']:
        # Show deal IF "All Jaipur" is selected OR locations match
        if selected_location == "All Jaipur" or deal["Location"] == selected_location:
            count += 1
            
            # --- THE "CARD" UI (Beautiful Look) ---
            with st.container():
                # Create 2 columns: Image on Left, Details on Right
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    # Show the tasty food image
                    try:
                        st.image(deal["Image"], use_container_width=True)
                    except:
                        st.write("🖼️ Image Loading...")
                
                with c2:
                    st.subheader(deal["Item"])
                    st.write(f"🏠 **{deal['Shop']}** ({deal['Location']})")
                    
                    # Price Math
                    discount_val = int(((deal['Original'] - deal['Price']) / deal['Original']) * 100)
                    
                    # The Price Tag
                    st.markdown(f"### ₹{deal['Price']}  <span style='color:red; font-size:15px'><s>₹{deal['Original']}</s> ({discount_val}% OFF)</span>", unsafe_allow_html=True)
                    
                    if st.button(f"👉 Claim this Deal", key=random.random()):
                        st.success(f"🎉 Reserved! Go to {deal['Shop']} and show this screen.")
            
            st.markdown("---") # Divider between cards

    if count == 0:
        st.warning(f"No deals found in {selected_location} right now. Check back later!")


# --- TAB 2: THE SHOPKEEPER EXPERIENCE (Easy Posting) ---
with tab2:
    st.header("📝 Post a Flash Sale")
    
    with st.form("shop_form"):
        shop_name = st.text_input("Shop Name", "My Store")
        location = st.selectbox("Shop Location", locations[1:]) # Skip "All Jaipur"
        item_name = st.text_input("What are you selling?", "Veg Burger")
        category = st.selectbox("Category (Auto-Image)", ["Pizza", "Burger", "Cake", "Indian Food", "Fruits"])
        
        c1, c2 = st.columns(2)
        with c1:
            original_price = st.number_input("Original Price", 100)
        with c2:
            days_left = st.slider("Days to Expiry", 0, 5, 1)
            
        submitted = st.form_submit_button("🚀 Post Deal")
        
        if submitted:
            # AI Pricing Logic
            discount = 0.50 if days_left <= 2 else 0.20
            ai_price = int(original_price * (1 - discount))
            
            # Auto-Select Image based on Category
            img_map = {
                "Pizza": "https://source.unsplash.com/400x300/?pizza",
                "Burger": "https://source.unsplash.com/400x300/?burger",
                "Cake": "https://source.unsplash.com/400x300/?cake",
                "Indian Food": "https://source.unsplash.com/400x300/?samosa",
                "Fruits": "https://source.unsplash.com/400x300/?fruit"
            }
            
            new_deal = {
                "Item": item_name,
                "Shop": shop_name,
                "Location": location,
                "Original": original_price,
                "Price": ai_price,
                "Image": img_map[category]
            }
            
            st.session_state['deals_db'].append(new_deal)
            st.success(f"✅ Live! Your {item_name} is listed in {location} for ₹{ai_price}")
