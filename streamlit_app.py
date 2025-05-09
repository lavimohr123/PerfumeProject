import streamlit as st
import pandas as pd
import altair as alt
from shop_finder_api import find_shops  # Import shop finder API helper

# Load perfume data
df = pd.read_csv("Perfumes.csv", sep=";", encoding="utf-8")

# Page configuration
if "started" not in st.session_state:
    st.session_state.started = False

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if not st.session_state.started:
    st.set_page_config(
        page_title="Your Perfect Fragrance",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
else:
    st.set_page_config(
        page_title="Your Perfect Fragrance",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Define background, font, stylings and colors
def set_background():
    st.markdown("""
        <style>
        html, body, [class*="st-"] {
            font-family: 'Georgia', serif !important;
        }
        .stApp {
            background-color: #fffaf0;
            color: #5b3a29;
        }
        section[data-testid="stSidebar"] {
            background-color: #f5eeee;
            color: #5b3a29;
        }
        header[data-testid="stHeader"] {
            background-color: #fffaf0;
            color: #5b3a29;
            border-bottom: 1px solid #d3c5b3;
        }
        .stButton>button {
            background-color: #d27979;
            color: white;
            border-radius: 10px;
            font-size: 18px;
            padding: 0.6rem 1.2rem;
            letter-spacing: 0.5px;
        }
        .stButton>button:hover {
            background-color: #8b4513;
        }
        </style>
    """, unsafe_allow_html=True)

# Define title page with title, intro text, 3 pics, and start now button
def show_intro():
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 48px; color: #8b4513;'>Your Perfect Fragrance</h1>
            <p style='font-size: 20px; color: #5b3a29;'>Your presence deserves a signature. <br><br>            
            </p>
            <p style='font-size: 17px; color: #5b3a29;'>
                The right scent doesn't just complete a look – it tells a story. <br>
                Discover fragrances that express who you are, before you even speak. <br>
                Curated by its notes, season, and occasion – matched to your personality.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("missdior.jpg", use_container_width=True)
    
    with col2:
        st.image("Gentleman.jpg", use_container_width=True)
        col2.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        if st.button("Start Now", key="start"):
            st.session_state.started = True
            st.rerun()
        col2.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.image("Si.jpg", use_container_width=True)

# Sidebar filters
def render_sidebar_filters(df):
    st.sidebar.title("Your Signature Scent")
    st.sidebar.markdown("### Matched to yourself")
    return {
        'brand': st.sidebar.selectbox("Brand", ["All"] + sorted(df["brand"].dropna().unique())),
        'gender': st.sidebar.selectbox("Gender", ["All"] + sorted(df["gender"].dropna().unique())),
        'scent': st.sidebar.selectbox("Scent", ["All"] + sorted(df["scent_direction"].dropna().unique())),
        'season': st.sidebar.selectbox("Season", ["All"] + sorted(df["season"].dropna().unique())),
        'personality': st.sidebar.selectbox("Personality", ["All"] + sorted(df["personality"].dropna().unique())),
        'occasion': st.sidebar.selectbox("Occasion", ["All"] + sorted(df["occasion"].dropna().unique())),
        'price': st.sidebar.selectbox("Price", ["All"] + sorted(df["price"].dropna().unique())),
    }

# Filter perfumes based on sidebar input
def filter_perfumes(df, filters):
    filtered = []
    for _, p in df.iterrows():
        if filters["brand"] != "All" and p["brand"] != filters ["brand"]:
            continue
        if filters["gender"] != "All" and p["gender"] != filters ["gender"]:
            continue
        if filters["scent"] != "All" and p["scent"] != filters ["scent"]:
            continue
        if filters["season"] != "All" and p["season"] != filters ["season"]:
            continue
        if filters["occasion"] != "All" and p["occasion"] != filters ["occasion"]:
            continue
        if filters["personality"] != "All" and p["personality"] != filters ["personality"]:
            continue
        if filters["price"] != "All" and p["price"] != filters ["price"]:
            continue
        filtered.append(p)
    return filtered

def get_similar_perfumes_tagmatch(p, max_results=3):
    signature = {
        'scent_direction': p.get('scent_direction'), 
        'season': p.get('season'), 
        'occation': p.get('gender'), 
        'personality': p.get('personality')
    }
    scored = []
    for other in data: 
        if other['name'] == p['name']:
            continue
        score = sum(1 for key in signature if other.get(key) == signature[key])
        scored.append((other, score))
    top = sorted(scored, key=lambda x: x[1], reverse = True)[:max_results]
    return [x[0] for x in top]

def display_results(results):
    st.markdown("### Matching Fragrances")
    st.write(f"{len(results)} matches found:")
    
    for idx, p in enumerate(results):
        with st.container():
            st.markdown(f"**{p.get('name')}** by {p.get('brand')}")
            st.markdown(
                f"*Gender:* {p.get('gender')} | *Scent:* {p.get('scent_direction')} | *Season:* {p.get('season')}  \n"
                f"*Occasion:* {p.get('occasion')} | *Personality:* {p.get('personality')} | *Price:* {p.get('price')}"
            )

            button_key = f"find_shops_{idx}"
            if st.button(f"Find Shops for {p.get('name')}"):
                st.session_state[f'shops_{idx}'] = find_shops(p.get('name'))

            if f'shops_{idx}' in st.session_state:
                shops = st.session_state[f'shops_{idx}']
                if shops:
                    st.success("Shops found nearby:")
                    for shop in shops:
                        st.markdown(f"- **{shop['name']}** – {shop['address']}")
                else:
                    st.warning("No shops found nearby. Try a different location.")
            st.markdown("---")
            
        similar_key = f"similar_{idx}"
        if st.button(f"Show Similar Scents to {p.get('name')}", key=similar_key):
            similar_perfumes = get_similar_perfumes_tagmatch(p)
            if similar_perfumes:
                st.markdown("**You may also like:**")
                for sim in similar_perfumes:
                    st.markdown(f"- * {sim['name']}* by {sim['brand']} ({sim['scent_direction']})")
            else: 
                st.info("No similar perfumes found.")


# Display price comparison chart
def display_price_chart(results):
    df_chart = pd.DataFrame(results)
    if not df_chart.empty and 'name' in df_chart.columns and 'price' in df_chart.columns:
        df_chart = df_chart[['name', 'price']].dropna().sort_values(by='price', ascending=False)
        df_chart.columns = ['Perfume', 'Price']
        chart = alt.Chart(df_chart).mark_bar(cornerRadius=10).encode(
            x='Price',
            y=alt.Y('Perfume', sort='-x'),
            color=alt.value('#ff4b4b'),
            tooltip=['Perfume', 'Price']
        ).properties(title='Perfume Price Comparison')
        st.altair_chart(chart, use_container_width=True)

# Main application logic
def main():
    set_background()

    if not st.session_state.get("started"):
        show_intro()
        return

    filters = render_sidebar_filters(df)

    if "show_results" not in st.session_state:
        st.session_state["show_results"] = False
    
    if st.sidebar.button("Show Results"):
        st.session_state["show_results"] = True
    
    if st.session_state.show_results:
        result = filter_perfumes(data, filters)
        if result:
            display_results(result)
            display_price_chart(result)
        else:
            st.warning("No perfumes match your criteria.")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image("Gentleman.jpg", width=450)
            st.markdown("""
                <h2 style="text-align: center; margin-top: 1rem;">Welcome to Your Perfect Fragrance</h2>
                <p style="text-align: center; font-size: 18px;">Use the filters depending on your preferences to sort perfumes by brand, season, occasion, and more.</p>
                <p style="text-align: center; font-size: 18px;">Once you're ready, click <em>Show Results</em> to explore fragrances curated to your personality and mood.</p>
                <p style="text-align: center; font-size: 18px;">Not sure what to pick? Start with your favorite brand or season!</p>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    
