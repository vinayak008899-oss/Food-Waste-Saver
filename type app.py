import streamlit as st
import urllib.parse
import random
import io
from PIL import Image
from datetime import datetime
from supabase import create_client, Client

# 1. APP CONFIG
st.set_page_config(page_title="Jaipur Food Saver", page_icon="🍷", layout="centered")

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

# --- 3. PAGE ROUTING & AUTH STATE ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'HOME'
if 'admin_unlocked' not in st.session_state:
    st.session_state['admin_unlocked'] = False
if 'vendor_unlocked' not in st.session_state:
    st.session_state['vendor_unlocked'] = False
if 'vendor_phone' not in st.session_state:
    st.session_state['vendor_phone'] = ""

# --- 4. THE "MIDNIGHT LUXURY" UI ENGINE (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,700;1,600&display=swap');
    
    /* SAFE TEXT STYLING (Targeting text specifically so we don't break icons) */
    p, label, input, .stMarkdown p {
        font-family: 'Montserrat', sans-serif !important;
        color: #E0E0E0;
    }
    h1, h2, h3, h4, h5 {
        font-family: 'Playfair Display', serif !important;
        color: #FFFFFF !important;
        letter-spacing: 1px;
    }

    /* CLEANUP THE HEADER (Safely remove the right-side GitHub/Share junk) */
    header { background-color: transparent !important; }
    .stAppToolbar, [data-testid="stHeaderActionElements"] { display: none !important; }
    footer { visibility: hidden; }
    
    /* MAKE THE NATIVE MENU ICON GOLD */
    [data-testid="collapsedControl"], button[kind="header"] { 
        color: #D4AF37 !important; 
    }
    [data-testid="collapsedControl"] svg, button[kind="header"] svg { 
        fill: #D4AF37 !important; 
        color: #D4AF37 !important; 
    }
    
    /* CINEMATIC BACKGROUND */
    .stApp {
        background-color: #0A0A0A;
        animation: appFadeIn 1.5s ease-out;
    }
    @keyframes appFadeIn {
        0% { opacity: 0; filter: brightness(0); }
        100% { opacity: 1; filter: brightness(1); }
    }
    
    /* FOOD CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 4px !important;
        background: #121212 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        border: 1px solid #222222 !important;
        transition: all 0.5s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #D4AF37 !important; 
    }
    
    /* BUTTONS */
    div.stButton > button {
        width: 100%;
        background: transparent;
        color: #D4AF37 !important; 
        border-radius: 0px; 
        border: 1px solid #D4AF37;
        padding: 12px 20px;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all 0.4s ease;
    }
    div.stButton > button:hover {
        background: #D4AF37;
        color: #0A0A0A !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
    }
    
    /* INPUTS */
    .stTextInput>div>div>input {
        background-color: #1A1A1A;
        color: #FFF;
        border: 1px solid #333;
        border-radius: 0px;
    }
    .stNumberInput>div>div>input {
        background-color: #1A1A1A;
        color: #FFF;
        border: 1px solid #333;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. THE CINEMATIC SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFF; margin-bottom: 30px;'>JFS</h2>", unsafe_allow_html=True)
    
    if st.button("HOME"): st.session_state['current_page'] = 'HOME'
    if st.button("GALLERY"): st.session_state['current_page'] = 'GALLERY'
    if st.button("MENU"): st.session_state['current_page'] = 'HOME' 
    if st.button("PARTY BOOKING"): st.session_state['current_page'] = 'PARTY'
    if st.button("CONTACT"): st.session_state['current_page'] = 'CONTACT'
    if st.button("RESERVATION"): st.session_state['current_page'] = 'RESERVATION' 
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Admin Panel"): st.session_state['current_page'] = 'admin'

# ==========================================
# PAGE: HOME & MENU 
# ==========================================
if st.session_state['current_page'] == 'HOME':
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 40px 0;">
            <p style='color: #D4AF37; font-weight: 400; font-size: 14px; letter-spacing: 3px; margin-bottom: 10px;'>EXCLUSIVE ACCESS</p>
            <h1 style='font-size: 48px; margin-top: 0;'>Jaipur Food Saver</h1>
        </div>
    """, unsafe_allow_html=True)

    search_loc = st.text_input("📍 ENTER LOCATION (e.g., WTP, Raja Park)", "")
    st.write("")
    st.write("")
    
    if supabase:
        try:
            response = supabase.table("deals").select("*").gt("quantity", 0).order("id", desc=True).execute()
            deals = response.data
            
            filtered_deals = [d for d in deals if search_loc == "" or search_loc.lower() in d['loc'].lower()]
            
            if len(deals) == 0:
                st.write("")
                st.markdown("<h1 style='text-align: center; font-size: 60px; color: #333;'>🍽️</h1>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center;'>The Kitchen is Closed</h3>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #888; font-size: 14px; letter-spacing: 1px;'>All culinary offerings have been reserved.<br>Return this evening for the midnight selection.</p>", unsafe_allow_html=True)
            
            elif len(filtered_deals) == 0 and search_loc != "":
                st.info(f"No current offerings found in '{search_loc}'.")
            
            else:
                for deal in filtered_deals:
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 1.5])
                        with c1:
                            st.image(deal['image_url'], use_container_width=True)
                        with c2:
                            st.markdown(f"<h3 style='margin-bottom: 5px; font-size: 26px;'>{deal['item']}</h3>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color: #D4AF37; font-size: 12px; letter-spacing: 2px; text-transform: uppercase;'>{deal['shop']} &nbsp;|&nbsp; {deal['loc']}</p>", unsafe_allow_html=True)
                            
                            st.markdown(f"<h4 style='margin-top: 15px; font-size: 22px;'>₹{deal['new_price']} <span style='color:#666; font-size:14px; font-family:Montserrat;'><s>₹{deal['old_price']}</s></span></h4>", unsafe_allow_html=True)
                            
                            st.write("")
                            if st.button(f"RESERVE ({deal['quantity']} REMAINING)", key=f"res_{deal['id']}"):
                                new_qty = deal['quantity'] - 1
                                supabase.table("deals").update({"quantity": new_qty}).eq("id", deal['id']).execute()
                                
                                current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
                                supabase.table("leads").insert({"click_time": current_time, "shop_name": deal['shop'], "food_item": deal['item'], "revenue": "₹5"}).execute()
                                
                                st.success("Reservation Confirmed.")
                                wa_msg = f"Hello {deal['shop']}. I have reserved the {deal['item']} via JFS."
                                wa_link = f"https://wa.me/{deal['phone']}?text={urllib.parse.quote(wa_msg)}"
                                st.link_button("CONTACT MAÎTRE D'", wa_link)
                                    
        except:
            st.error("Connecting to mainframe...")

# ==========================================
# PAGE: RESERVATION (The Shop Portal)
# ==========================================
elif st.session_state['current_page'] == 'RESERVATION':
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Partner Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; letter-spacing: 1px; margin-bottom: 40px;'>AUTHORIZED VENDORS ONLY</p>", unsafe_allow_html=True)
    
    if not st.session_state['vendor_unlocked']:
        with st.form("vendor_login", border=True):
            phone_input = st.text_input("REGISTERED PHONE NUMBER")
            pin_input = st.text_input("4-DIGIT PIN", type="password")
            if st.form_submit_button("AUTHENTICATE") and supabase:
                auth_check = supabase.table("vendors").select("*").eq("phone", phone_input).eq("pin", pin_input).execute()
                if len(auth_check.data) > 0:
                    st.session_state['vendor_unlocked'] = True
                    st.session_state['vendor_phone'] = phone_input 
                    st.rerun()
                else: 
                    st.error("Authentication Failed. Invalid Number or PIN.")
    else:
        st.success(f"Identity Verified. Logged in as: {st.session_state['vendor_phone']}")
        if st.button("⬅️ Secure Logout"):
            st.session_state['vendor_unlocked'] = False
            st.session_state['vendor_phone'] = ""
            st.rerun()
            
        with st.form("shop_form", border=True):
            shop = st.text_input("ESTABLISHMENT NAME")
            loc = st.text_input("LOCATION")
            item = st.text_input("CULINARY ITEM")
            c_p, c_q = st.columns(2)
            with c_p: price = int(st.number_input("EXCLUSIVE PRICE (₹)", min_value=1, value=50))
            with c_q: stock = int(st.number_input("QUANTITY", min_value=1, value=1))
            photo = st.file_uploader("UPLOAD HIGH-RES IMAGE", type=["jpg", "jpeg", "png"])
            
            if st.form_submit_button("PUBLISH OFFERING") and supabase:
                if photo and loc:
                    with st.spinner("Processing & Uploading..."):
                        img = Image.open(photo)
                        width, height = img.size
                        target_ratio = 16 / 9
                        current_ratio = width / height
                        
                        if current_ratio > target_ratio:
                            new_width = int(height * target_ratio)
                            left = (width - new_width) / 2
                            right = (width + new_width) / 2
                            img = img.crop((left, 0, right, height))
                        elif current_ratio < target_ratio:
                            new_height = int(width / target_ratio)
                            top = (height - new_height) / 2
                            bottom = (height + new_height) / 2
                            img = img.crop((0, top, width, bottom))
                            
                        img = img.resize((800, 450), Image.Resampling.LANCZOS)
                        buf = io.BytesIO()
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                            
                        img.save(buf, format="JPEG", quality=80)
                        f_bytes = buf.getvalue()

                        f_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{shop.replace(' ','_')}.jpg"
                        supabase.storage.from_("food_images").upload(f_name, f_bytes, {"content-type": "image/jpeg"})
                        img_url = supabase.storage.from_("food_images").get_public_url(f_name)
                        
                        supabase.table("deals").insert({
                            "item": item, 
                            "shop": shop, 
                            "loc": loc, 
                            "old_price": price*2, 
                            "new_price": price, 
                            "image_url": img_url, 
                            "phone": st.session_state['vendor_phone'], 
                            "quantity": stock
                        }).execute()
                        st.success("Offering is now live.")

# ==========================================
# PAGES: PLACEHOLDERS
# ==========================================
elif st.session_state['current_page'] in ['GALLERY', 'PARTY', 'CONTACT']:
    st.write("")
    st.write("")
    st.write("")
    st.markdown(f"<h1 style='text-align: center; color: #555;'>{st.session_state['current_page']}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4AF37; letter-spacing: 3px;'>COMING SOON</p>", unsafe_allow_html=True)

# ==========================================
# PAGE: CORPORATE MAINFRAME
# ==========================================
elif st.session_state['current_page'] == 'admin':
    st.markdown("<h2>System Architecture</h2>", unsafe_allow_html=True)
    if not st.session_state['admin_unlocked']:
        with st.form("admin_login", border=True):
            admin_id = st.text_input("ADMIN ID")
            pwd = st.text_input("PASSWORD", type="password")
            if st.form_submit_button("AUTHENTICATE"):
                if admin_id != "" and pwd == "Vinayak#0000":
                    st.session_state['admin_unlocked'] = True
                    st.rerun()
                else: st.error("Access Denied.")
    else:
        st.success("Authentication Successful.")
        
        tab_rev, tab_vendors = st.tabs(["💰 Revenue Tracker", "🔐 Vendor Management"])
        
        with tab_rev:
            if supabase:
                leads_data = supabase.table("leads").select("*").execute()
                all_leads = leads_data.data
                st.metric("YIELD", f"₹{len(all_leads) * 5}")
                st.dataframe(all_leads, use_container_width=True)
                
        with tab_vendors:
            st.markdown("### Authorize New Vendor")
            with st.form("add_vendor_form", border=True):
                new_phone = st.text_input("VENDOR WHATSAPP NUMBER (e.g., 919876543210)")
                if st.form_submit_button("GENERATE ACCESS KEY") and supabase:
                    if new_phone:
                        new_pin = str(random.randint(1000, 9999)) 
                        try:
                            supabase.table("vendors").insert({"phone": new_phone, "pin": new_pin}).execute()
                            st.success(f"AUTHORIZED. The exclusive PIN for {new_phone} is: {new_pin}")
                            st.warning("Write this down. Hand it to the shopkeeper.")
                        except Exception as e:
                            st.error("Error: This number may already be in the database.")
            
            st.markdown("### 📜 Authorized Vendors Ledger")
            if supabase:
                v_data = supabase.table("vendors").select("*").execute()
                st.dataframe(v_data.data, use_container_width=True)
