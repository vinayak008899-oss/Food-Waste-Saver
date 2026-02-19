# --- DATABASE (Now with Phone Numbers) ---
if 'deals' not in st.session_state:
    st.session_state['deals'] = [
        {
            "Item": "Chocolate Truffle", 
            "Shop": "Sharma Bakery", 
            "Loc": "Vaishali Nagar", 
            "Old": 500, "New": 250, 
            "Img": "https://loremflickr.com/400/300/cake",
            "Phone": "919876543210" # Shopkeeper's WhatsApp Number
        },
        {
            "Item": "Paneer Patties", 
            "Shop": "Rawat Mishthan", 
            "Loc": "Sindhi Camp", 
            "Old": 40, "New": 20, 
            "Img": "https://loremflickr.com/400/300/samosa",
            "Phone": "919876543211"
        },
        {
            "Item": "Veg Supreme Pizza", 
            "Shop": "Dominos Leftover", 
            "Loc": "Malviya Nagar", 
            "Old": 600, "New": 199, 
            "Img": "https://loremflickr.com/400/300/pizza",
            "Phone": "919876543212"
        },
    ]

# ... (Keep your Header and Tabs code the same) ...

# --- TAB 1: BUYER (Upgraded with Maps & WhatsApp) ---
with tab_buyer:
    locations = ["All Jaipur", "Vaishali Nagar", "Sindhi Camp", "Malviya Nagar", "Raja Park"]
    selected_loc = st.selectbox("📍 Where are you right now?", locations)
    
    st.markdown("---")
    
    found = False
    for i, deal in enumerate(st.session_state['deals']):
        if selected_loc == "All Jaipur" or deal['Loc'] == selected_loc:
            found = True
            
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    try:
                        st.image(deal['Img'], use_container_width=True)
                    except:
                        st.error("Img Error")
                        
                with c2:
                    st.subheader(deal['Item'])
                    st.write(f"🏠 **{deal['Shop']}** ({deal['Loc']})")
                    discount = int(((deal['Old'] - deal['New']) / deal['Old']) * 100)
                    st.markdown(f"### ₹{deal['New']}  <span style='color:red; font-size:14px'><s>₹{deal['Old']}</s></span>", unsafe_allow_html=True)
                    
                    with st.expander("🔍 View Full Photo"):
                        st.image(deal['Img'])
                    
                    # --- THE NEW RESERVE LOGIC ---
                    if st.button(f"👉 Reserve Now", key=f"res_{i}"):
                        st.balloons()
                        st.success("✅ Reserved! Complete these 2 steps:")
                        
                        # 1. Create WhatsApp Link (Customer -> Shopkeeper)
                        wa_msg = f"Hello {deal['Shop']}! I just reserved the {deal['Item']} on Food Saver. I am coming to pick it up!"
                        wa_link = f"https://wa.me/{deal['Phone']}?text={wa_msg.replace(' ', '%20')}"
                        
                        # 2. Create Google Maps Link
                        map_query = f"{deal['Shop']} {deal['Loc']} Jaipur"
                        map_link = f"https://www.google.com/maps/search/?api=1&query={map_query.replace(' ', '+')}"
                        
                        # Show Action Buttons side-by-side
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.link_button("📲 Notify Shop", wa_link)
                        with col_b:
                            st.link_button("🗺️ Get Directions", map_link)
                            
            
