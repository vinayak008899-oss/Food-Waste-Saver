import streamlit as st
import urllib.parse
from PIL import Image
from datetime import datetime
from supabase import create_client, Client

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍔", layout="centered")

# --- 2. DATABASE CONNECTION ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error("⚠️ Vault disconnected.")
        return None

supabase = init_connection()

# --- 3. PAGE ROUTING SYSTEM ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'admin_unlocked' not in st.session_state:
    st.session_state['admin_unlocked'] = False

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

# --- 5. THE MENU (Sidebar) ---
with st.sidebar:
    st.write("### Menu")
    st.caption("Jaipur, Rajasthan")
    st.markdown("---")
    
    if st.session_state['current_page'] == 'home':
        st.button("👤 My Profile")
        st.button("📞 Help & Support")
        st.markdown("---")
        
        if st.button("🔒 Admin Access"):
            st.session_state['current_page'] = 'admin'
            st.rerun() 
            
    elif st.session_state['current_page'] == 'admin':
        if st.button("⬅️ Back to Home"):
            st.session_state['current_page'] = 'home'
            st.session_state['admin_unlocked'] = False
            st.rerun()

# ==========================================
# PAGE 1: THE PUBLIC MARKETPLACE
# ==========================================
if st.session_state['current_page'] == 'home':
    st.title("🍔 Jaipur Food Saver")
    st.markdown("**Save Money. Save Food. Save Earth.**")
    st.write("")

    tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 Post Deal"])

    # --- TAB 1: BUYER ---
    with tab_buyer:
        search_loc = st.text_input("📍 Search your area (e.g., WTP, Raja Park)", "")
        st.markdown("---")
        
        if supabase:
            try:
                # NEW LOGIC: Only fetch deals where quantity is greater than 0
                response = supabase.table("deals").select("*").gt("quantity", 0).order("id", desc=True).execute()
                deals = response.data
                
                found = False
                for deal in deals:
                    if search_loc == "" or search_loc.lower() in deal['loc'].lower():
                        found = True
                        
                        with st.container(border=True):
                            c1, c2 = st.columns([1, 2])
                            with c1:
                                st.image(deal['image_url'], use_container_width=True)
                                    
                            with c2:
                                st.subheader(deal['item'])
                                st.write(f"🏠 **{deal['shop']}** ({deal['loc']})")
                                discount = int(((deal['old_price'] - deal['new_price']) / deal['old_price']) * 100)
                                st.markdown(f"### ₹{deal['new_price']}  <span style='color:red; font-size:14px'><s>₹{deal['old_price']}</s> ({discount}% OFF)</span>", unsafe_allow_html=True)
                                
                                # BUTTON SHOWS EXACT QUANTITY LEFT
                                if st.button(f"👉 Reserve Now ({deal['quantity']} left)", key=f"res_{deal['id']}"):
                                    
                                    # 1. LIVE DEDUCTION: Subtract 1 from the database
                                    new_qty = deal['quantity'] - 1
                                    supabase.table("deals").update({"quantity": new_qty}).eq("id", deal['id']).execute()
                                    
                                    # 2. LOG THE LEAD
                                    current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
                                    supabase.table("leads").insert({
                                        "click_time": current_time,
                                        "shop_name": deal['shop'],
                                        "food_item": deal['item'],
                                        "revenue": "₹5"
                                    }).execute()
                                    
                                    st.balloons()
                                    st.success("✅ Reserved! Contact the shop:")
                                    wa_msg = f"Hello {deal['shop']}! I reserved the {deal['item']} on Food Saver. I am coming!"
                                    wa_link = f"https://wa.me/{deal['phone']}?text={urllib.parse.quote(wa_msg)}"
                                    map_query = f"{deal['shop']} {deal['loc']} Jaipur"
                                    map_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(map_query)}"
                                    
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        st.link_button("📲 Notify Shop", wa_link)
                                    with col_b:
                                        st.link_button("🗺️ Directions", map_link)
                                        
                if not found:
                    st.info(f"😕 No deals found in '{search_loc}'.")
            except Exception as e:
                st.error("Connecting to server...")

    # --- TAB 2: SELLER ---
    with tab_seller:
        st.write("### 🚀 Post a Flash Deal")
        with st.form("shop_form", border=True):
            shop = st.text_input("Shop Name", "My Bakery")
            phone = st.text_input("WhatsApp Number", "91")
            loc = st.text_input("Exact Address", "e.g., Shop No 5, WTP Mall")
            item = st.text_input("Item Name", "Cream Roll")
            
            col_price, col_qty = st.columns(2)
            with col_price:
                price = int(st.number_input("Discounted Price (₹)", min_value=1, value=50))
            with col_qty:
                # NEW LOGIC: Ask shopkeeper how many items they have
                stock = int(st.number_input("Quantity Available", min_value=1, value=1))
                
            uploaded_photo = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("Post Deal")
            
            if submitted and supabase:
                if uploaded_photo is None:
                    st.error("⚠️ Please take a photo!")
                elif loc == "":
                    st.error("⚠️ Please enter your location!")
                else:
                    with st.spinner("Uploading to Server..."):
                        try:
                            file_bytes = uploaded_photo.getvalue()
                            clean_name = uploaded_photo.name.replace(" ", "_").replace("-", "_")
                            file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{clean_name}"
                            
                            supabase.storage.from_("food_images").upload(
                                file_name, 
                                file_bytes,
                                {"content-type": uploaded_photo.type}
                            )
                            img_url = supabase.storage.from_("food_images").get_public_url(file_name)
                            
                            supabase.table("deals").insert({
                                "item": item, 
                                "shop": shop, 
                                "loc": loc, 
                                "old_price": price * 2, 
                                "new_price": price, 
                                "image_url": img_url, 
                                "phone": phone,
                                "quantity": stock # SAVES INVENTORY TO CLOUD
                            }).execute()
                            
                            st.success("✅ Deal is Live Permanently!")
                        except Exception as e:
                            st.error(f"Upload Error: Make sure your bucket is public!")

# ==========================================
# PAGE 2: THE CEO GATEWAY
# ==========================================
elif st.session_state['current_page'] == 'admin':
    st.title("🔒 Corporate Mainframe")
    st.markdown("---")
    
    if not st.session_state['admin_unlocked']:
        st.write("### Authentication Required")
        with st.form("admin_login"):
            admin_id = st.text_input("Admin ID (Phone Number)")
            pwd = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")
            
            if submit:
                if admin_id != "" and pwd == "Vinayak#0000":
                    st.session_state['admin_unlocked'] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid ID or Password.")
                    
    else:
        st.success("✅ Identity Verified. Welcome, CEO.")
        
        if supabase:
            try:
                leads_data = supabase.table("leads").select("*").execute()
                all_leads = leads_data.data
                
                total_leads = len(all_leads)
                total_revenue = total_leads * 5
                
                st.write("### Live Revenue Dashboard")
                c1, c2 = st.columns(2)
                c1.metric("Leads Generated", total_leads)
                c2.metric("Owed Revenue (₹5/Lead)", f"₹{total_revenue}")
                
                st.write("---")
                st.write("**Permanent Click Ledger:**")
                if total_leads > 0:
                    st.dataframe(all_leads, use_container_width=True)
                else:
                    st.info("No clicks recorded in the database yet.")
            except Exception as e:
                st.error("Could not fetch ledger data.")
