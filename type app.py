import streamlit as st
import random

# 1. APP CONFIG (Make it look like a Mobile App)
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- DATABASE (Simulated) ---
if 'deals' not in st.session_state:
    st.session_state['deals'] = [
        {"Item": "Chocolate Truffle", "Shop": "Sharma Bakery", "Loc": "Vaishali Nagar", "Old": 500, "New": 250, "Img": "https://source.unsplash.com/400x300/?cake"},
        {"Item": "Paneer Patties", "Shop": "Rawat Mishthan", "Loc": "Sindhi Camp", "Old": 40, "New": 20, "Img": "https://source.unsplash.com/400x300/?samosa"},
        {"Item": "Veg Supreme Pizza", "Shop": "Dominos Leftover", "Loc": "Malviya Nagar", "Old": 600, "New": 199, "Img": "https://source.unsplash.com/400x300/?pizza"},
    ]

# 2. HEADER
st.title("🍔 Jaipur Food Saver")
st.caption("Save Money. Save Food. Save Earth.")

# 3. TABS
tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 I Am a Shopkeeper"])

# --- TAB 1: BUYER (The Visual "Zomato" Style) ---
with tab_buyer:
    # A. LOCATION FILTER (Crucial for "Near Me")
    locations = ["All Jaipur", "Vaishali Nagar", "Sindhi Camp", "Malviya Nagar", "Raja Park"]
    selected_loc = st.selectbox("📍 Where are you right now?", locations)
    
    st.markdown("---")
    
    # B. DISPLAY CARDS
    found = False
    for deal in st.session_state['deals']:
        if selected_loc == "All Jaipur" or deal['Loc'] == selected_loc:
            found = True
            
            # THE "CARD" UI
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(deal['Img'], use_container_width=True)
                with c2:
                    st.subheader(deal['Item'])
                    st.write(f"🏠 **{deal['Shop']}** ({deal['Loc']})")
                    discount = int(((deal['Old'] - deal['New']) / deal['Old']) * 100)
                    st.markdown(f"### ₹{deal['New']}  <span style='color:red; font-size:14px'><s>₹{deal['Old']}</s> ({discount}% OFF)</span>", unsafe_allow_html=True)
                    
                    # The "Book Now" Logic
                    if st.button(f"👉 Reserve", key=random.random()):
                        st.balloons()
                        st.success(f"Reserved! Go to {deal['Shop']} in next 30 mins.")
            st.markdown("---")
            
    if not found:
        st.info(f"😕 No deals in {selected_loc} right now. Check Raja Park?")

# --- TAB 2: SELLER (The Notification Engine) ---
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    
    with st.form("shop_form"):
        shop = st.text_input("Shop Name", "My Bakery")
        loc = st.selectbox("Location", locations[1:])
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", 50)
        
        # Auto-Image Logic
        category = st.selectbox("Category", ["Cake", "Pizza", "Indian", "Burger"])
        
        submitted = st.form_submit_button("Post Deal")
        
        if submitted:
            # 1. Add to Database
            img_map = {"Cake": "cake", "Pizza": "pizza", "Indian": "curry", "Burger": "burger"}
            new_deal = {
                "Item": item, "Shop": shop, "Loc": loc, "Old": price*2, "New": price, 
                "Img": f"https://source.unsplash.com/400x300/?{img_map[category]}"
            }
            st.session_state['deals'].append(new_deal)
            
            # 2. THE NOTIFICATION SYSTEM (WhatsApp)
            # This generates a pre-written message they can blast to customers
            wa_text = f"🔥 FLASH SALE at {shop}! {item} for just ₹{price}. Come to {loc} before it is gone!"
            wa_link = f"https://wa.me/?text={wa_text.replace(' ', '%20')}"
            
            st.success("✅ Deal is Live on the App!")
            st.markdown(f"### 📢 Notify Your Customers:")
            st.link_button("📲 Send WhatsApp Blast", wa_link)
