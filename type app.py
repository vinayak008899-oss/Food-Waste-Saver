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
        return None

supabase = init_connection()

# --- 3. PAGE ROUTING & AUTH ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'admin_unlocked' not in st.session_state:
    st.session_state['admin_unlocked'] = False

# --- 4. THE "PREMIUM ANIMATED" UI ENGINE (CSS) ---
st.markdown("""
<style>
    /* 1. IMPORT PREMIUM STARTUP FONT (POPPINS) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], h1, h2, h3, h4, h5, h6, p, span, div, button {
        font-family: 'Poppins', sans-serif !important;
    }

    /* 2. HIDE STREAMLIT WATERMARKS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 3. CLEAN BACKGROUND & SMOOTH LOAD ANIMATION */
    .stApp {
        background-color: #F8F9FA;
        animation: appFadeIn 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes appFadeIn {
        0% { opacity: 0; transform: translateY(20px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* 4. FOOD CARD ANIMATIONS (The "Hover Lift") */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
        border: 1px solid #F0F0F0 !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-6px) !important;
        box-shadow: 0 15px 30px rgba(226, 55, 68, 0.1) !important;
        border-color: rgba(226, 55, 68, 0.3) !important;
    }
    
    /* 5. PREMIUM BUTTON PHYSICS */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #E23744 0%, #D0202D 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 12px 20px;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(226, 55, 68, 0.25);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(226, 55, 68, 0.4);
    }
    div.stButton > button:active {
        transform: translateY(1px) scale(0.98);
        box-shadow: 0 2px 5px rgba(226, 55, 68, 0.2);
    }
    
    /* 6. TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 25px;
        border-bottom: 2px solid #F0F0F0;
    }
    .stTabs [aria-selected="true"] {
        color: #E23744 !important;
        border-bottom: 3px solid #E23744 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. THE SIDEBAR (CEO Only) ---
with st.sidebar:
    st.write("### 🔒 System Access")
    if st.session_state['current_page'] == 'home':
        if st.button("Admin Login"):
            st.session_state['current_page'] = 'admin'
            st.rerun() 
    elif st.session_state['current_page'] == 'admin':
        if st.button("⬅️ Exit Admin"):
            st.session_state['current_page'] = 'home'
            st.session_state['admin_unlocked'] = False
            st.rerun()

# ==========================================
# PAGE 1: THE PUBLIC MARKETPLACE
# ==========================================
if st.session_state['current_page'] == 'home':
    # Animated Title Header
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <h1 style='color: #111; font-weight: 800; font-size: 42px; margin-bottom: 0;'>🍔 Food Saver</h1>
            <p style='color: #E23744; font-weight: 600; font-size: 16px; margin-top: -5px; letter-spacing: 1px;'>SAVE MONEY. SAVE FOOD. SAVE JAIPUR.</p>
        </div>
    """, unsafe_allow_html=True)

    tab_buyer, tab_seller = st.tabs(["🤤 I Want Food", "📢 Post Deal"])

    with tab_buyer:
        if supabase:
            try:
                response = supabase.table("deals").select("*").gt("quantity", 0).order("id", desc=True).execute()
                deals = response.data
                
                # --- THE GHOST TOWN UI ---
                if len(deals) == 0:
                    st.write("")
                    st.write("")
                    st.markdown("<h1 style='text-align: center; font-size: 70px; animation: appFadeIn 1.5s;'>🍽️</h1>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: #111; font-weight: 700;'>Jaipur ate everything!</h3>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: #777; font-size: 15px;'>All deals are completely sold out right now.<br>Check back this evening for fresh midnight discounts.</p>", unsafe_allow_html=True)
                    st.write("")
                    st.write("")
                # -------------------------
                else:
                    search_loc = st.text_input("📍 Search your area (e.g., WTP, Raja Park)", "")
                    st.markdown("---")
                    
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
                                    st.markdown(f"<p style='color: #666; font-size: 14px; font-weight: 500; margin-bottom: 5px;'>🏠 {deal['shop']} ({deal['loc']})</p>", unsafe_allow_html=True)
                                    discount = int(((deal['old_price'] - deal['new_price']) / deal['old_price']) * 100)
                                    st.markdown(f"<h3 style='color: #111; margin-top: 0;'>₹{deal['new_price']} <span style='color:#E23744; font-size:14px; font-weight:600;'><s>₹{deal['old_price']}</s> ({discount}% OFF)</span></h3>", unsafe_allow_html=True)
                                    
                                    if st.button(f"👉 Reserve Now ({deal['quantity']} left)", key=f"res_{deal['id']}"):
                                        new_qty = deal['quantity'] - 1
                                        supabase.table("deals").update({"quantity": new_qty}).eq("id", deal['id']).execute()
                                        
                                        current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
                                        supabase.table("leads").insert({"click_time": current_time, "shop_name": deal['shop'], "food_item": deal['item'], "revenue": "₹5"}).execute()
                                        
                                        st.balloons()
                                        st.success("✅ Reserved!")
                                        wa_msg = f"Hello {deal['shop']}! I reserved the {deal['item']} on Food Saver."
                                        wa_link = f"https://wa.me/{deal['phone']}?text={urllib.parse.quote(wa_msg)}"
                                        st.link_button("📲 Notify Shop via WhatsApp", wa_link)
                                            
                    if not found:
                        st.info(f"😕 No deals found in '{search_loc}'.")
            except:
                st.error("Connecting to server...")

    with tab_seller:
        st.write("### 🚀 Post a Flash Deal")
        with st.form("shop_form", border=True):
            shop = st.text_input("Shop Name")
            phone = st.text_input("WhatsApp Number", "91")
            loc = st.text_input("Exact Address")
            item = st.text_input("Item Name")
            c_p, c_q = st.columns(2)
            with c_p: price = int(st.number_input("Price (₹)", min_value=1, value=50))
            with c_q: stock = int(st.number_input("Quantity", min_value=1, value=1))
            photo = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
            if st.form_submit_button("Post Deal") and supabase:
                if photo and loc:
                    with st.spinner("Posting to Server..."):
                        f_bytes = photo.getvalue()
                        f_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.name.replace(' ','_')}"
                        supabase.storage.from_("food_images").upload(f_name, f_bytes, {"content-type": photo.type})
                        img_url = supabase.storage.from_("food_images").get_public_url(f_name)
                        supabase.table("deals").insert({"item": item, "shop": shop, "loc": loc, "old_price": price*2, "new_price": price, "image_url": img_url, "phone": phone, "quantity": stock}).execute()
                        st.success("✅ Live!")

# ==========================================
# PAGE 2: CORPORATE MAINFRAME
# ==========================================
elif st.session_state['current_page'] == 'admin':
    st.markdown("<h1 style='color: #111;'>🔒 Corporate Mainframe</h1>", unsafe_allow_html=True)
    if not st.session_state['admin_unlocked']:
        with st.form("admin_login", border=True):
            admin_id = st.text_input("Admin ID")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Log In"):
                if admin_id != "" and pwd == "Vinayak#0000":
                    st.session_state['admin_unlocked'] = True
                    st.rerun()
                else: st.error("❌ Access Denied.")
    else:
        st.success("✅ Verified.")
        if supabase:
            leads_data = supabase.table("leads").select("*").execute()
            all_leads = leads_data.data
            st.metric("Total Revenue", f"₹{len(all_leads) * 5}")
            st.dataframe(all_leads, use_container_width=True)
