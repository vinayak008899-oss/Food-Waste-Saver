
st.markdown("""
<style>
    /* 1. The Main Background (Warm Gradient) */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); /* Subtle Grey */
        background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%); /* Orange Sunset */
    }

    /* 2. Card Styling (White Box with Shadow) */
    div[data-testid="stVerticalBlock"] > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }

    /* 3. Button Styling (Pill Shape) */
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

# ... (Rest of your code) ...
# --- TAB 2: SELLER (Now asks for Phone Number) ---
with tab_seller:
    st.write("### 🚀 Post a Flash Deal")
    
    with st.form("shop_form"):
        shop = st.text_input("Shop Name", "My Bakery")
        
        # NEW: Ask for their number so customers can reach them!
        phone = st.text_input("Your WhatsApp Number (with country code, e.g., 919876543210)", "91")
        
        loc = st.selectbox("Location", locations[1:])
        item = st.text_input("Item Name", "Cream Roll")
        price = st.number_input("Discounted Price (₹)", 50)
        category = st.selectbox("Category", ["Cake", "Pizza", "Indian", "Burger", "Fruits"])
        
        submitted = st.form_submit_button("Post Deal")
        
        if submitted:
            # Map Category to Image Tool
            img_map = {
                "Cake": "cake", 
                "Pizza": "pizza", 
                "Indian": "samosa", 
                "Burger": "burger", 
                "Fruits": "fruit"
            }
            
            # NEW: Save the Phone Number into the database
            new_deal = {
                "Item": item, 
                "Shop": shop, 
                "Loc": loc, 
                "Old": price * 2, 
                "New": price, 
                "Img": f"https://loremflickr.com/400/300/{img_map[category]}",
                "Phone": phone  # <--- WE ADDED THIS HERE
            }
            st.session_state['deals'].append(new_deal)
            
            st.success("✅ Deal is Live on the App!")
            st.info("Customers can now click 'Reserve' to WhatsApp you directly.")
