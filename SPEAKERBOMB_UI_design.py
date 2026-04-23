# streamlit run SPEAKERBOMB_UI_design.py

import streamlit as st
import time

# 1. INITIALIZE SESSION STATE
if 'show_filters' not in st.session_state:
    st.session_state.show_filters = False
if 'show_products' not in st.session_state:
    st.session_state.show_products = False

# 2. SIDEBAR LOGIC
with st.sidebar:
    st.title("Categories")
    st.write("---")
    
    # Contact Us Section
    if st.button("Contact Us", key="contact"):
        st.write("📞 **Contact Details**")
        st.write("Number: +91 1234567890")
        st.write("Email: exampleID@email.com")
    
    # Filter Toggle Logic
    if st.button("Filters", key="filters_btn"):
        st.session_state.show_filters = not st.session_state.show_filters

    if st.session_state.show_filters:
        st.success("Narrow your search:")
        
        # DROPDOWN FILTERS
        st.selectbox("🎨 Select Color", ["All Colors", "Matte Black", "Arctic White", "Sonic Blue"])
        st.selectbox("📏 Select Size", ["All Sizes", "Compact", "Medium", "Large / Studio"])
        st.select_slider("💰 Price Range", options=["₹0", "₹10k", "₹50k", "₹1L", "₹2L+"])
        
        # Sort By Dropdown
        st.selectbox("🔃 Sort By", ["Newest", "Price: Low to High", "Price: High to Low", "Top Rated"])
        
        st.write("---")
        st.button("Reset Filters")

# 3. DATA DEFINITION
prices = {
    "Portimax": 15500, "Portimid": 19900, "Portimini": 5000,
    "Deskipro": 34999, "Deskimid": 26000, "Deskibase": 12000,
    "Studio Pro": 250000, "Studio Mid": 96000, "Studio Base": 90000
}

catalog = {
    "Portable Series": ["Portimax", "Portimid", "Portimini"],
    "Desk Series": ["Deskipro", "Deskimid", "Deskibase"],
    "Home Theater": ["Studio Pro", "Studio Mid", "Studio Base"]
}

# 4. APP HEADER & ABOUT US
st.title("SPEAKERBOMB")
st.write("---")
st.header("What is SPEAKERBOMB?")
st.write("""
SPEAKERBOMB is a leading audio brand known for its high-quality speakers and innovative sound technology. 
We offer a wide range of products designed to meet the needs of music lovers, audiophiles, and home theater enthusiasts.
""")
st.write("---")

# 5. PRODUCTS SECTION
st.header("Our Products")

if st.button("View Products"):
    st.session_state.show_products = True

if st.session_state.show_products:
    series_choice = st.selectbox("Select a Series:", list(catalog.keys()))
    
    st.write(f"### {series_choice} Models")
    for product in catalog[series_choice]:
        p_price = prices[product]
        st.checkbox(f"{product} (₹{p_price:,})", key=f"check_{product}")

    st.write("---")
    
    # 6. CART & CHECKOUT LOGIC
    st.write("---")
    
    # Check if any items are selected first
    selected_items = [p for p in prices.keys() if st.session_state.get(f"check_{p}")]
    
    if selected_items:
        if st.button("🛒 View Cart"):
            st.session_state.viewing_cart = True
        
        # Only show the cart details if the button was clicked
        if st.session_state.get('viewing_cart'):
            st.header("Your Selection")
            for item in selected_items:
                st.write(f"✅ {item}: **₹{prices[item]:,}**")
            
            total_price = sum(prices[p] for p in selected_items)
            st.write(f"### Total: ₹{total_price:,}")
            
            if st.button("Complete Purchase"):
                st.info("Waiting for payment...")
                
                with st.status("Processing Payment...", expanded=True) as status:
                    st.write("Connecting to gateway...")
                    time.sleep(1.5)
                    st.write("Verifying transaction...")
                    time.sleep(1.5)
                    status.update(label="Transaction details", state="complete", expanded=False)
                
                st.subheader("Payment Details")
                st.info(f"Pay to: `speakerbomb_shopping.com`  \nTotal: **₹{total_price:,}**")
                
                time.sleep(3) # Shortened for testing
                st.warning("Processing Order...")
                time.sleep(2)
                st.success("Payment confirmed. Order placed successfully!")
                st.toast("You can track your order in the 'My Orders' section.")

                # SHOP FOR MORE
                st.write("---")
                if st.button("Shop for More"):
                    # Reset all states to start fresh
                    for key in list(st.session_state.keys()):
                        st.session_state[key] = False
                    st.rerun()
    else:
        st.info("Select items above to add them to your cart.")