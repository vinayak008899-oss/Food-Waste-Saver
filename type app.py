import streamlit as st
import random
import urllib.parse

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- 2. DESIGN ENGINE (CSS) ---
st.markdown("""
<style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
    }
    /* White Card Style */
    div[data-testid="stVerticalBlock"] > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    /* Red 'Zomato-style' Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #D00000;
        transform: scale(1.02);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE (Simulated) ---
if 'deals' not in st.session_state:
    st.session_state['deals'] = [
        {
            "Item": "Chocolate Truffle", 
            "Shop": "Sharma Bakery", 
            "Loc": "Vaishali Nagar", 
            "Old": 500, "New": 250, 
            "Img": "https://loremflickr.com/400/300/cake,chocolate",
            "Phone": "919876543210"
        },
        {
            "Item": "Paneer Patties", 
            "Shop": "Rawat Mishthan", 
            "Loc": "Sindhi Camp", 
            "Old": 40, "New": 20, 
            "Img": "https://loremflickr.com/400/300/food,indian",
            "Phone": "919876543211"
        },
        {
            "Item": "Veg Supreme Pizza", 
            "Shop": "Dominos Leftover", 
            "Loc": "Malviya Nagar", 
            "Old": 600, "New": 199, 
            "Img": "https://loremflickr.com/400/300/pizza",
            "Phone": "919876543212"
        },
    ]

# --- 4. HEADER ---
st.title("🍔 Jaipur Food Saver")
st.caption("Save Money. Save Food. Save Earth.")

# --- 5. TABS ---
tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 I Am a Shopkeeper"])

locations = ["All Jaipur", "Vaishali Nagar", "Sindhi Camp", "Malviya Nagar", "Raja Park"]

# ==========================================
# TAB 1: BUYER (The Customer View)
# ==========================================
with tab_buyer:
    selected_loc = st.selectbox("📍 Where are you right now?", locations)
    
    st.markdown("---")
    
    found = False
    for i, deal in enumerate(st.session_state['deals']):
        if selected_loc == "All Jaipur" or deal['Loc'] == selected_loc:
            found = True
            
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    try:
                        st.image(deal['Img'], use_container_width=True)
                    except:
                        st.error("Img Error")
                        
                with c2:
                    st.subheader(deal['Item'])
                    st.write(f"🏠 **{deal['Shop']}** ({deal['Loc']})")
                    discount = int(((deal['Old'] - deal['New']) / deal['Old']) * 100)
                    st.markdown(f"### ₹{deal['New']}  <span style='color:red; font-size:14px'><s>₹{deal['Old']}</s> ({discount}% OFF)</span>", unsafe_allow_html=True)
                    
                    with st.expander("🔍 View Full Photo"):
                        st.image(deal['Img'])
                    
                    # RESERVE LOGIC
                    if st.button(f"👉 Reserve Now", key=f"res_{i}"):
                        st.balloons()
                        st.success("✅ Reserved! Complete these 2 steps:")
                        
                        # WhatsApp Link
                        wa_msg = f"Hello {deal['Shop']}! I just reserved the {deal['Item']} on Food Saver. I am coming to pick it up!"
                        wa_link = f"https://wa.me/{deal['Phone']}?text={urllib.parse.quote(wa_msg)}"
                        
                        # Google Maps Link
                        map_query = f"{deal['Shop']} {deal['Loc']} Jaipur"
                        map_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(map_query)}"
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.link_button("📲 Notify Shop", wa_link)
                        with col_b:
                            st.link_button("🗺️ Get Directions", map_link)
                            
            st.markdown("---")
            
    if not found:
        st.info(f"😕 No deals in {selected_loc} right now.")

# ==========================================
# TAB 2: SELLER (The Shopkeeper View)
# ==========================================
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    
    with st.form("shop_form"):
        shop = st.text_input("Shop Name", "My Bakery")
        phone = st.text_input("Your WhatsApp Number (e.g., 919876543210)", "91")
        loc = st.selectbox("Location", locations[1:])
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", 50)
        category = st.selectbox("Category", ["Cake", "Pizza", "Indian", "Burger", "Fruits"])
        
        submitted = st.form_submit_button("Post Deal")
        
        if submitted:
            img_map = {
                "Cake": "cake", 
                "Pizza": "pizza", 
                "Indian": "samosa", 
                "Burger": "burger", 
                "Fruits": "fruit"
            }
            
            new_deal = {
                "Item": item, 
                "Shop": shop, 
                "Loc": loc, 
                "Old": price * 2, 
                "New": price, 
                "Img": f"https://loremflickr.com/400/300/{img_map[category]}",
                "Phone": phone
            }
            st.session_state['deals'].append(new_deal)
            
            st.success("✅ Deal is Live on the App!")
            st.info("Customers can now click 'Reserve' to WhatsApp you directly.")
