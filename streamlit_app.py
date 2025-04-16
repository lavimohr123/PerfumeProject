import streamlit as st
import pandas as pd
import altair as alt

# define dataframe to insert and implement excel sheet
df = pd.read_csv("Perfumes.csv", sep=";", encoding="utf-8")
data = df.to_dict(orient="records")

# Page configuration
if "started" not in st.session_state:
    st.session_state.started = False

# Set page config based on whether user clicked "Start"
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

# define background, font, stylings and colors
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

#define title page with title, intro text, 3 pics, and start now button
def show_intro():
    st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem; background-color: #fff4e6;'>
            <h1 style='font-size: 48px; color: #8b4513;'>Your Perfect Fragrance</h1>
            <p style='font-size: 20px; color: #5b3a29; max-width: 800px; margin: auto;'>
                Your presence deserves a signature. <br><br>            
            </p>
            <p style='font-size: 17px; color: #5b3a29; max-width: 800px; margin: auto;'>
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
        spacer1, button_col, spacer2 = st.columns([1, 2, 1])
        with button_col:
            if st.button("Start Now", key="start"):
                st.session_state.started = True
                st.rerun()

    with col3:
        st.image("Si.jpg", use_container_width=True)


# Sidebar filters
def render_sidebar_filters(df):
    st.sidebar.title("Your Signature Scent")
    st.sidebar.markdown("### Matched to yourself")
    return {
        'brand': st.sidebar.selectbox("Brand", ["All"] + list(df["brand"].dropna().unique())),
        'gender': st.sidebar.selectbox("Gender", ["All"] + list(df["gender"].dropna().unique())),
        'scent': st.sidebar.selectbox("Scent", ["All"] + list(df["scent_direction"].dropna().unique())),
        'season': st.sidebar.selectbox("Season", ["All"] + list(df["season"].dropna().unique())),
        'personality': st.sidebar.selectbox("Personality", ["All"] + list(df["personality"].dropna().unique())),
        'occasion': st.sidebar.selectbox("Occasion", ["All"] + list(df["occasion"].dropna().unique())),
        'price': st.sidebar.selectbox("Price", ["All"] + list(df["price"].dropna().unique())),
    }

def filter_perfumes(data, filters):
    return [
        p for p in data
        if (filters['brand'] == 'All' or p.get('brand') == filters['brand']) and
           (filters['gender'] == 'All' or p.get('gender') == filters['gender']) and
           (filters['scent'] == 'All' or p.get('scent_direction') == filters['scent']) and
           (filters['season'] == 'All' or p.get('season') == filters['season']) and
           (filters['occasion'] == 'All' or p.get('occasion') == filters['occasion']) and
           (filters['personality'] == 'All' or p.get('personality') == filters['personality']) and
           (filters['price'] == 'All' or p.get('price') == filters['price'])
    ]

def display_results(results):
    st.markdown("### Matching Fragrances")
    st.write(f"{len(results)} matches found:")
    for p in results:
        st.markdown(f"**{p.get('name')}** by {p.get('brand')}")
        st.markdown(
            f"*Gender:* {p.get('gender')} | *Scent:* {p.get('scent_direction')} | *Season:* {p.get('season')}  \n"
            f"*Occasion:* {p.get('occasion')} | *Personality:* {p.get('personality')} | *Price:* {p.get('price')}"
        )
        st.markdown("---")

def display_price_chart(results):
    df = pd.DataFrame(results)
    if not df.empty and 'name' in df.columns and 'price' in df.columns:
        df = df[['name', 'price']].dropna().sort_values(by='price', ascending=False)
        df.columns = ['Perfume', 'Price']
        chart = alt.Chart(df).mark_bar(cornerRadius=10).encode(
            x='Price',
            y=alt.Y('Perfume', sort='-x'),
            color=alt.value('#ff4b4b'),
            tooltip=['Perfume', 'Price']
        ).properties(title='Perfume Price Comparison')
        st.altair_chart(chart, use_container_width=True)

def main():
    set_background()
    
    if not st.session_state.get("started"):
        show_intro()
        return  # Stop here, don't show sidebar or filters yet

    filters = render_sidebar_filters(df)

    if st.sidebar.button('Show Results'):
        result = filter_perfumes(data, filters)
        if result:
            display_results(result)
            display_price_chart(result)
        else:
            st.warning("No perfumes match your criteria.")

if __name__ == "__main__":
    main()
