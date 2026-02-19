import streamlit as st
import random

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- DATABASE (With WORKING Image Links) ---
if 'deals' not in st.session_state:
    st.session_state['deals'] = [
        {
            "Item": "Chocolate Truffle", 
            "Shop": "Sharma Bakery", 
            "Loc": "Vaishali Nagar", 
            "Old": 500, "New": 250, 
            "Img": "https://loremflickr.com/400/300/cake,chocolate" # <--- NEW WORKING LINK
        },
        {
            "Item": "Paneer Patties", 
            "Shop": "Rawat Mishthan", 
            "Loc": "Sindhi Camp", 
            "Old": 40, "New": 20, 
            "Img": "https://loremflickr.com/400/300/food,indian"
        },
        {
            "Item": "Veg Supreme Pizza", 
            "Shop": "Dominos Leftover", 
            "Loc": "Malviya Nagar", 
            "Old": 600, "New": 199, 
            "Img": "https://loremflickr.com/400/300/pizza"
        },
    ]

# 2. HEADER
st.title("🍔 Jaipur Food Saver")
st.caption("Save Money. Save Food. Save Earth.")

# 3. TABS
tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 I Am a Shopkeeper"])

# --- TAB 1: BUYER ---
with tab_buyer:
    # LOCATION FILTER
    locations = ["All Jaipur", "Vaishali Nagar", "Sindhi Camp", "Malviya Nagar", "Raja Park"]
    selected_loc = st.selectbox("📍 Where are you right now?", locations)
    
    st.markdown("---")
    
    # DISPLAY CARDS
    found = False
    for deal in st.session_state['deals']:
        if selected_loc == "All Jaipur" or deal['Loc'] == selected_loc:
            found = True
            
            # THE "CARD" UI
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    # NEW: Robust Image Display
                    try:
                        st.image(deal['Img'], use_container_width=True)
                    except:
                        st.error("Img Error")
                        
                with c2:
                    st.subheader(deal['Item'])
                    st.write(f"🏠 **{deal['Shop']}** ({deal['Loc']})")
                    discount = int(((deal['Old'] - deal['New']) / deal['Old']) * 100)
                    st.markdown(f"### ₹{deal['New']}  <span style='color:red; font-size:14px'><s>₹{deal['Old']}</s> ({discount}% OFF)</span>", unsafe_allow_html=True)
                    
                    # NEW FEATURE: View Photo Option
                    with st.expander("🔍 View Full Photo"):
                        st.image(deal['Img'], caption=f"Real photo of {deal['Item']}")
                    
                    if st.button(f"👉 Reserve", key=random.random()):
                        st.balloons()
                        st.success(f"Reserved! Go to {deal['Shop']} in next 30 mins.")
            st.markdown("---")
            
    if not found:
        st.info(f"😕 No deals in {selected_loc} right now. Check Raja Park?")

# --- TAB 2: SELLER ---
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    
    with st.form("shop_form"):
        shop = st.text_input("Shop Name", "My Bakery")
        loc = st.selectbox("Location", locations[1:])
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", 50)
        category = st.selectbox("Category", ["Cake", "Pizza", "Indian", "Burger", "Fruits"])
        
        submitted = st.form_submit_button("Post Deal")
        
        if submitted:
            # Map Category to NEW Image Tool
            img_map = {
                "Cake": "cake", 
                "Pizza": "pizza", 
                "Indian": "samosa", 
                "Burger": "burger", 
                "Fruits": "fruit"
            }
            
            new_deal = {
                "Item": item, "Shop": shop, "Loc": loc, "Old": price*2, "New": price, 
                "Img": f"https://loremflickr.com/400/300/{img_map[category]}" # <--- FIXED HERE TOO
            }
            st.session_state['deals'].append(new_deal)
            
            # WhatsApp Link
            wa_text = f"🔥 FLASH SALE at {shop}! {item} for just ₹{price}. Come to {loc} before it is gone!"
            wa_link = f"https://wa.me/?text={wa_text.replace(' ', '%20')}"
            
            st.success("✅ Deal is Live on the App!")
            st.link_button("📲 Send WhatsApp Blast", wa_link)
