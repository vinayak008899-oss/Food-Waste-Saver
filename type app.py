import streamlit as st
import urllib.parse
from PIL import Image
from datetime import datetime

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- 2. DATABASE INITIALIZATION ---
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

# The Hidden Ledger for the CEO
if 'leads' not in st.session_state:
    st.session_state['leads'] = []

# --- 3. THE MENU & SECRET DASHBOARD (Sidebar) ---
with st.sidebar:
    st.write("### Menu")
    st.caption("Jaipur, Rajasthan")
    st.markdown("---")
    
    # NORMAL USER BUTTONS (Dummy buttons for realism)
    st.button("👤 My Profile")
    st.button("📞 Help & Support")
    
    st.markdown("---")
    st.write("### 🔒 System Access")
    
    # THE CEO LOCK
    pwd = st.text_input("Enter Passkey", type="password")
    
    if pwd == "vinayak123": # Your secret password
        st.success("CEO Dashboard Unlocked.")
        
        # Calculate Total Money Made
        total_leads = len(st.session_state['leads'])
        total_revenue = total_leads * 5
        
        # Display the Stats right in the menu
        st.metric("Leads Generated", total_leads)
        st.metric("Owed Revenue (₹5/Lead)", f"₹{total_revenue}")
        
        st.write("**Live Click Ledger:**")
        if total_leads > 0:
            st.dataframe(st.session_state['leads'], use_container_width=True)
        else:
            st.caption("No leads generated yet.")
            
    elif pwd != "":
        st.error("❌ Access Denied.")

# --- 4. DESIGN ENGINE (CSS) ---
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        animation: appFadeIn 0.8s ease-out;
    }
    @keyframes appFadeIn {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
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
    }
    header {background-color: transparent !important;}
</style>
""", unsafe_allow_html=True)

# --- 5. HEADER ---
st.title("🍔 Jaipur Food Saver")
st.markdown("**Save Money. Save Food. Save Earth.**")
st.write("")

# --- 6. TABS (Only 2 Tabs left for the public) ---
tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 Post Deal"])

# ==========================================
# TAB 1: BUYER (The Front End)
# ==========================================
with tab_buyer:
    search_loc = st.text_input("📍 Search your area (e.g., WTP, Raja Park)", "")
    st.markdown("---")
    
    found = False
    for i, deal in enumerate(st.session_state['deals']):
        if search_loc == "" or search_loc.lower() in deal['Loc'].lower():
            found = True
            
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
                        
                        # 1. SECRETLY LOG THE DATA
                        current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
                        st.session_state['leads'].append({
                            "Date & Time": current_time,
                            "Shop Name": deal['Shop'],
                            "Food Item": deal['Item'],
                            "Revenue": "₹5"
                        })
                        
                        # 2. SHOW THE UI
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
                            st.link_button("🗺️ Directions", map_link)
                            
    if not found:
        st.info(f"😕 No deals found in '{search_loc}'.")

# ==========================================
# TAB 2: SELLER
# ==========================================
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    with st.form("shop_form", border=True):
        shop = st.text_input("Shop Name", "My Bakery")
        phone = st.text_input("WhatsApp Number (e.g., 919876543210)", "91")
        loc = st.text_input("Exact Address", "e.g., Shop No 5, WTP Mall")
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", min_value=1, value=50)
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
