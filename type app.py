import streamlit as st
import random
import urllib.parse
from PIL import Image

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- 2. DESIGN ENGINE (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
    }
    div[data-testid="stVerticalBlock"] > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
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

# --- 3. DATABASE (Now handles Real Images) ---
if 'deals' not in st.session_state:
    st.session_state['deals'] = [
        # Static dummy deals so the app isn't empty on launch
        {
            "Item": "Chocolate Truffle", 
            "Shop": "Sharma Bakery", 
            "Loc": "Vaishali Nagar", 
            "Old": 500, "New": 250, 
            "Img": "https://images.unsplash.com/photo-1578985545062-69928b1ea9f1?w=400",
            "Phone": "919876543210"
        }
    ]

# --- 4. HEADER ---
st.title("🍔 Jaipur Food Saver")
st.caption("Save Money. Save Food. Save Earth.")

# --- 5. TABS ---
tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 I Am a Shopkeeper"])

# ==========================================
# TAB 1: BUYER (Search by typing)
# ==========================================
with tab_buyer:
    # UPDATED: Search bar instead of fixed dropdown
    search_loc = st.text_input("📍 Search your area (e.g., WTP, Raja Park, Vaishali)", "")
    
    st.markdown("---")
    
    found = False
    for i, deal in enumerate(st.session_state['deals']):
        # Show deal if search is empty, OR if the typed area matches the shop's location
        if search_loc == "" or search_loc.lower() in deal['Loc'].lower():
            found = True
            
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    try:
                        st.image(deal['Img'], use_container_width=True)
                    except:
                        st.error("Image Error")
                        
                with c2:
                    st.subheader(deal['Item'])
                    st.write(f"🏠 **{deal['Shop']}** ({deal['Loc']})")
                    discount = int(((deal['Old'] - deal['New']) / deal['Old']) * 100)
                    st.markdown(f"### ₹{deal['New']}  <span style='color:red; font-size:14px'><s>₹{deal['Old']}</s> ({discount}% OFF)</span>", unsafe_allow_html=True)
                    
                    # RESERVE LOGIC
                    if st.button(f"👉 Reserve Now", key=f"res_{i}"):
                        st.balloons()
                        st.success("✅ Reserved! Complete these 2 steps:")
                        
                        wa_msg = f"Hello {deal['Shop']}! I just reserved the {deal['Item']} on Food Saver. I am coming to pick it up!"
                        wa_link = f"https://wa.me/{deal['Phone']}?text={urllib.parse.quote(wa_msg)}"
                        
                        map_query = f"{deal['Shop']} {deal['Loc']} Jaipur"
                        map_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(map_query)}"
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.link_button("📲 Notify Shop", wa_link)
                        with col_b:
                            st.link_button("🗺️ Get Directions", map_link)
                            
            st.markdown("---")
            
    if not found:
        st.info(f"😕 No deals found in '{search_loc}'. Try searching a different area.")

# ==========================================
# TAB 2: SELLER (Camera & Live Address)
# ==========================================
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    
    with st.form("shop_form"):
        shop = st.text_input("Shop Name", "My Bakery")
        phone = st.text_input("Your WhatsApp Number (e.g., 919876543210)", "91")
        
        # UPDATED: Free text for exact location
        loc = st.text_input("Exact Address / Location", "e.g., Shop No 5, WTP Mall, Malviya Nagar")
        
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", min_value=1, value=50)
        
        # UPDATED: The Mobile Camera / Image Uploader
        st.write("📸 Snap a Photo of the Food")
        uploaded_photo = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("Post Deal")
        
        if submitted:
            if uploaded_photo is None:
                st.error("⚠️ Please take a photo of the food first!")
            elif loc == "":
                st.error("⚠️ Please enter your location!")
            else:
                # Convert the uploaded photo into a format the app can display
                image = Image.open(uploaded_photo)
                
                new_deal = {
                    "Item": item, 
                    "Shop": shop, 
                    "Loc": loc, 
                    "Old": price * 2, 
                    "New": price, 
                    "Img": image,  # We save the actual photo they just took
                    "Phone": phone
                }
                st.session_state['deals'].append(new_deal)
                
                st.success("✅ Deal is Live on the App!")
                st.info("Check the 'I Want Food' tab to see your post.")

