import streamlit as st
import urllib.parse
from PIL import Image

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- 2. THE MENU (Sidebar / Top Left Menu) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80) # Dummy User Icon
    st.write("### Hello, Vinayak!")
    st.caption("Jaipur, Rajasthan")
    st.markdown("---")
    st.button("👤 My Profile")
    st.button("🛒 Active Orders")
    st.button("⚙️ Settings")
    st.button("📞 Help & Support")
    st.markdown("---")
    st.button("🚪 Logout")

# --- 3. DESIGN ENGINE (Animation & Clean CSS) ---
st.markdown("""
<style>
    /* Gradient Background & Slide-In Animation */
    .stApp {
        background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        animation: appFadeIn 0.8s ease-out;
    }
    
    /* The Animation Logic */
    @keyframes appFadeIn {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Red 'Zomato-style' Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #D00000;
        transform: scale(1.03);
        color: white;
    }
    
    /* Hide the default grey Streamlit top bar for a cleaner look */
    header {background-color: transparent !important;}
</style>
""", unsafe_allow_html=True)

# --- 4. DATABASE ---
if 'deals' not in st.session_state:
    st.session_state['deals'] = [
        {
            "Item": "Chocolate Truffle", 
            "Shop": "Sharma Bakery", 
            "Loc": "Vaishali Nagar", 
            "Old": 500, "New": 250, 
            "Img": "https://images.unsplash.com/photo-1578985545062-69928b1ea9f1?w=400",
            "Phone": "919876543210"
        }
    ]

# --- 5. HEADER (Fixed formatting) ---
st.title("🍔 Jaipur Food Saver")
st.markdown("**Save Money. Save Food. Save Earth.**")
st.write("") # Spacing

# --- 6. TABS ---
tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 I Am a Shopkeeper"])

# ==========================================
# TAB 1: BUYER
# ==========================================
with tab_buyer:
    search_loc = st.text_input("📍 Search your area (e.g., WTP, Raja Park)", "")
    st.markdown("---")
    
    found = False
    for i, deal in enumerate(st.session_state['deals']):
        if search_loc == "" or search_loc.lower() in deal['Loc'].lower():
            found = True
            
            # FIXED: Using standard Streamlit containers with borders instead of aggressive CSS
            with st.container(border=True):
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
                    
                    if st.button(f"👉 Reserve Now", key=f"res_{i}"):
                        st.balloons()
                        st.success("✅ Reserved! Contact the shop:")
                        
                        wa_msg = f"Hello {deal['Shop']}! I reserved the {deal['Item']} on Food Saver. I am coming!"
                        wa_link = f"https://wa.me/{deal['Phone']}?text={urllib.parse.quote(wa_msg)}"
                        map_query = f"{deal['Shop']} {deal['Loc']} Jaipur"
                        map_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(map_query)}"
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.link_button("📲 Notify Shop", wa_link)
                        with col_b:
                            st.link_button("🗺️ Get Directions", map_link)
                            
    if not found:
        st.info(f"😕 No deals found in '{search_loc}'. Try searching a different area.")

# ==========================================
# TAB 2: SELLER
# ==========================================
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    
    with st.form("shop_form", border=True):
        shop = st.text_input("Shop Name", "My Bakery")
        phone = st.text_input("WhatsApp Number (e.g., 919876543210)", "91")
        loc = st.text_input("Exact Address / Location", "e.g., Shop No 5, WTP Mall")
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", min_value=1, value=50)
        
        st.write("📸 Snap a Photo")
        uploaded_photo = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("Post Deal")
        
        if submitted:
            if uploaded_photo is None:
                st.error("⚠️ Please take a photo of the food first!")
            elif loc == "":
                st.error("⚠️ Please enter your location!")
            else:
                image = Image.open(uploaded_photo)
                new_deal = {
                    "Item": item, "Shop": shop, "Loc": loc, "Old": price * 2, "New": price, 
                    "Img": image, "Phone": phone
                }
                st.session_state['deals'].append(new_deal)
                st.success("✅ Deal is Live!")

