# streamlit run SPEAKERBOMB_UI_design.py

import streamlit as st
import time

# 1. INITIALIZE SESSION STATE
if 'show_filters' not in st.session_state:
    st.session_state.show_filters = False
if 'show_products' not in st.session_state:
    st.session_state.show_products = False
if 'viewing_cart' not in st.session_state:
    st.session_state.viewing_cart = False

# 2. FULL DATASET
product_data = {
    "Portimax": {"price": 15500, "color": "Arctic White", "size": "Medium", "series": "Portable Series"},
    "Portimini": {"price": 5000, "color": "Matte Black", "size": "Compact", "series": "Portable Series"},
    "Portimid": {"price": 19900, "color": "Sonic Blue", "size": "Medium", "series": "Portable Series"},
    "Deskibase": {"price": 25000, "color": "Matte Black", "size": "Large / Studio", "series": "Desk Series"},
    "Deskimid": {"price": 30000, "color": "Arctic White", "size": "Large / Studio", "series": "Desk Series"},
    "Deskipro": {"price": 34999, "color": "Arctic White", "size": "Large / Studio", "series": "Desk Series"},
    "Studio base": {"price": 150000, "color": "Arctic White", "size": "Large / Studio", "series": "Home Theater"},
    "Studio mid": {"price": 200000, "color": "Arctic White", "size": "Large / Studio", "series": "Home Theater"},
    "Studio Pro": {"price": 250000, "color": "Arctic White", "size": "Large / Studio", "series": "Home Theater"},
    "corebase": {"price": 129999, "color": "Sonic Blue", "size": "Bigger", "series": "Concert Series"},
    "coremid": {"price": 259999, "color": "Sonic Blue", "size": "Bigger", "series": "Concert Series"},
    "corepro": {"price": 429999, "color": "Sonic Blue", "size": "Bigger", "series": "Concert Series"},
    "partybase": {"price": 12099, "color": "Sonic Blue", "size": "Big", "series": "Concert Series"},
    "partymid": {"price": 29999, "color": "Sonic Blue", "size": "Big", "series": "Concert Series"},
    "partypro": {"price": 42999, "color": "Sonic Blue", "size": "Medium", "series": "Concert Series"},
}

# 3. SIDEBAR LOGIC
with st.sidebar:
    st.title("Categories")
    st.write("---")
    
    if st.button("Contact Us", key="contact"):
        st.write("📞 **Contact Details**")
        st.write("Number: +91 1234567890")
        st.write("Email: exampleID@email.com")
    
    if st.button("Filters", key="filters_btn"):
        st.session_state.show_filters = not st.session_state.show_filters

    f_color = "All Colors"
    f_size = "All Sizes"
    f_price_max = 500000

    if st.session_state.show_filters:
        st.success("Narrow your search:")
        f_color = st.selectbox("🎨 Select Color", ["All Colors", "Matte Black", "Arctic White", "Sonic Blue"])
        f_size = st.selectbox("📏 Select Size", ["All Sizes", "Compact", "Medium", "Big", "Bigger", "Large / Studio"])
        
        price_options = {"₹5k": 5000, "₹10k": 10000, "₹25k": 25000, "₹50k": 50000, "₹1L": 100000, "₹2L+": 500000}
        p_label = st.select_slider("💰 Max Price", options=list(price_options.keys()), value="₹2L+")
        f_price_max = price_options[p_label]
        
# 4. APP HEADER
st.title("SPEAKERBOMB®")
st.write("---")
st.header("What is SPEAKERBOMB?")
st.write("SPEAKERBOMB is a leading audio brand known for its high-quality speakers and innovative sound technology. We offer a wide range of products designed to meet the needs of music lovers, audiophiles, and home theater enthusiasts.")
st.write("---")

# 5. PRODUCTS SECTION
st.header("Our Products")

if st.button("View Products") or st.session_state.show_products:
    st.session_state.show_products = True
    
    # Dropdown to select series - Defaults to Home Theater (Index 3)
    series_list = ["All Products", "Portable Series", "Desk Series", "Home Theater", "Concert Series"]
    selected_series = st.selectbox("Select a Series:", series_list, index=3)

    # 6. FILTERING ENGINE
    filtered_items = []
    for name, info in product_data.items():
        color_ok = (f_color == "All Colors" or info["color"] == f_color)
        size_ok = (f_size == "All Sizes" or info["size"] == f_size)
        price_ok = (info["price"] <= f_price_max)
        series_ok = (selected_series == "All Products" or info["series"] == selected_series)
        
        if color_ok and size_ok and price_ok and series_ok:
            filtered_items.append(name)

    if not filtered_items:
        st.warning("No products match your current filters.")
    else:
        st.write(f"### {selected_series} Models")
        for product in filtered_items:
            price = product_data[product]["price"]
            st.checkbox(f"{product} (₹{price:,})", key=f"check_{product}")

    st.write("---")
    
    # 7. CART & CHECKOUT LOGIC
    selected_items = [p for p in product_data.keys() if st.session_state.get(f"check_{p}", False)]
    
    if selected_items:
        if st.button("🛒 View Cart"):
            st.session_state.viewing_cart = True
        
        if st.session_state.get('viewing_cart'):
            st.header("Your Selection")
            total_price = sum(product_data[p]["price"] for p in selected_items)
            for item in selected_items:
                st.write(f"✅ {item}: **₹{product_data[item]['price']:,}**")
            
            st.write(f"### Total: ₹{total_price:,}")
            
            if st.button("Complete Purchase"):
                with st.status("Processing Payment...", expanded=True) as status:
                    st.write("Connecting to gateway...")
                    time.sleep(1.5)
                    st.write("Verifying transaction...")
                    time.sleep(1.5)
                    status.update(label="Transaction complete", state="complete", expanded=False)
                
                st.info(f"Pay to: `speakerbomb_shopping.com` | Total: **₹{total_price:,}**")
                st.success("Payment confirmed. Order placed successfully!")

                if st.button("Shop for More"):
                    for key in list(st.session_state.keys()):
                        st.session_state[key] = False
                    st.rerun()
    else:
        st.info("Select items above to add them to your cart.")