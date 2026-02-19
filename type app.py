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

# --- 4. THE "PREMIUM" UI ENGINE (CSS) ---
st.markdown("""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Premium Background - Clean Crisp White/Gray */
    .stApp {
        background-color: #FAFAFA;
        animation: appFadeIn 0.8s ease-out;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    @keyframes appFadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Food Card Styling - Soft Shadows & Rounded Corners */
    div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        padding: 15px;
        border: 1px solid #F0F0F0;
        transition: transform 0.2s ease-in-out;
    }
    
    /* Professional High-Contrast Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #E23744; /* Zomato Cherry Red */
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px rgba(226, 55, 68, 0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #C12735;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(226, 55, 68, 0.3);
    }
    
    /* Custom Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #E23744 !important;
        font-weight: 700;
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
    st.markdown("<h1 style='text-align: center; color: #1C1C1C;'>🍔 Food Saver</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #777; font-weight: 500;'>Save Money. Save Food. Save Jaipur.</p>", unsafe_allow_html=True)
    st.write("")

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
                    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🍽️</h1>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: #333;'>Jaipur ate everything!</h3>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: #777; font-size: 16px;'>All deals are completely sold out right now.<br>Check back this evening for fresh midnight discounts.</p>", unsafe_allow_html=True)
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
                            with st.container():
                                c1, c2 = st.columns([1, 2])
                                with c1:
                                    st.image(deal['image_url'], use_container_width=True)
                                with c2:
                                    st.subheader(deal['item'])
                                    st.write(f"🏠 **{deal['shop']}** ({deal['loc']})")
                                    discount = int(((deal['old_price'] - deal['new_price']) / deal['old_price']) * 100)
                                    st.markdown(f"### ₹{deal['new_price']} <span style='color:red; font-size:14px'><s>₹{deal['old_price']}</s> ({discount}% OFF)</span>", unsafe_allow_html=True)
                                    
                                    if st.button(f"👉 Reserve Now ({deal['quantity']} left)", key=f"res_{deal['id']}"):
                                        # Inventory Deduction
                                        new_qty = deal['quantity'] - 1
                                        supabase.table("deals").update({"quantity": new_qty}).eq("id", deal['id']).execute()
                                        
                                        # Log Lead
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
        with st.form("shop_form", border=False):
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
                    with st.spinner("Posting..."):
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
    st.markdown("<h1 style='color: #1C1C1C;'>🔒 Corporate Mainframe</h1>", unsafe_allow_html=True)
    if not st.session_state['admin_unlocked']:
        with st.form("admin_login"):
            admin_id = st.text_input("Admin ID")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Log In"):
                if admin_id != "" and pwd == "Vinayak#0000":
                    st.session_state['admin_unlocked'] = True
                    st.rerun()
                else: st.error("❌ Denied.")
    else:
        st.success("✅ Verified.")
        if supabase:
            leads_data = supabase.table("leads").select("*").execute()
            all_leads = leads_data.data
            st.metric("Total Revenue", f"₹{len(all_leads) * 5}")
            st.dataframe(all_leads, use_container_width=True)
