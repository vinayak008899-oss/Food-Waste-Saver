import streamlit as st
import urllib.parse
from PIL import Image
from datetime import datetime

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- 2. DATABASE & SYSTEM MEMORY ---
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

if 'leads' not in st.session_state:
    st.session_state['leads'] = []

# NEW: The "Multi-Page" Routing System
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

if 'admin_unlocked' not in st.session_state:
    st.session_state['admin_unlocked'] = False

# --- 3. DESIGN ENGINE (CSS) ---
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

# --- 4. THE MENU (Sidebar) ---
with st.sidebar:
    st.write("### Menu")
    st.caption("Jaipur, Rajasthan")
    st.markdown("---")
    
    # Switch the buttons based on which page we are on
    if st.session_state['current_page'] == 'home':
        st.button("👤 My Profile")
        st.button("📞 Help & Support")
        st.markdown("---")
        
        # This button instantly swaps the screen to the Admin Page
        if st.button("🔒 Admin Access"):
            st.session_state['current_page'] = 'admin'
            st.rerun() 
            
    elif st.session_state['current_page'] == 'admin':
        # If we are on the admin page, show a "Go Back" button
        if st.button("⬅️ Back to Home"):
            st.session_state['current_page'] = 'home'
            st.session_state['admin_unlocked'] = False # Auto-logs you out when you leave
            st.rerun()

# ==========================================
# PAGE ROUTING (The Brain of the App)
# ==========================================

if st.session_state['current_page'] == 'home':
    # ----------------------------------------
    # THE PUBLIC APP (Visible to everyone)
    # ----------------------------------------
    st.title("🍔 Jaipur Food Saver")
    st.markdown("**Save Money. Save Food. Save Earth.**")
    st.write("")

    tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 Post Deal"])

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
                            current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
                            st.session_state['leads'].append({
                                "Date & Time": current_time,
                                "Shop Name": deal['Shop'],
                                "Food Item": deal['Item'],
                                "Revenue": "₹5"
                            })
                            
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

    with tab_seller:
        st.write("### 🚀 Post a Flash Deal")
        with st.form("shop_form", border=True):
            shop = st.text_input("Shop Name", "My Bakery")
            phone = st.text_input("WhatsApp Number", "91")
            loc = st.text_input("Exact Address", "e.g., Shop No 5, WTP Mall")
            item = st.text_input("Item Name", "Cream Roll")
            price = st.number_input("Discounted Price (₹)", min_value=1, value=50)
            uploaded_photo = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("Post Deal")
            
            if submitted:
                if uploaded_photo is None:
                    st.error("⚠️ Please take a photo!")
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

elif st.session_state['current_page'] == 'admin':
    # ----------------------------------------
    # THE CEO GATEWAY (Full Screen Takeover)
    # ----------------------------------------
    st.title("🔒 Corporate Mainframe")
    st.markdown("---")
    
    # If the CEO hasn't logged in yet, show the lock
    if not st.session_state['admin_unlocked']:
        st.write("### Authentication Required")
        with st.form("admin_login"):
            admin_id = st.text_input("Admin ID (Phone Number)")
            pwd = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")
            
            if submit:
                # IMPORTANT: I put a basic check here. You can change it to check your specific phone number.
                if admin_id != "" and pwd == "Vinayak#0000":
                    st.session_state['admin_unlocked'] = True
                    st.rerun() # Reloads instantly to show the dashboard
                else:
                    st.error("❌ Invalid ID or Password.")
                    
    # If the CEO is logged in, show the data
    else:
        st.success("✅ Identity Verified. Welcome, CEO.")
        
        total_leads = len(st.session_state['leads'])
        total_revenue = total_leads * 5
        
        st.write("### Live Revenue Dashboard")
        c1, c2 = st.columns(2)
        c1.metric("Leads Generated", total_leads)
        c2.metric("Owed Revenue (₹5/Lead)", f"₹{total_revenue}")
        
        st.write("---")
        st.write("**Click Ledger:**")
        if total_leads > 0:
            st.dataframe(st.session_state['leads'], use_container_width=True)
        else:
            st.info("No clicks recorded yet. Go back to Home and click Reserve to test.")
