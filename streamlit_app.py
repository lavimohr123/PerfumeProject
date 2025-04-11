import streamlit as st
import requests
import pandas as pd
import altair as alt
#import openpyxl

# UI
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
            color: black;
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
            color: black;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #e60000;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# load the excel file
df = pd.read_csv("Perfumes.csv", sep = ",", index_col=0, usecols = ["brand", "gender"])

#  UI rendering 
def render_sidebar_filters(data):
    st.sidebar.title("Perfume Finder")
    st.sidebar.markdown("### Find Your Perfect Fragrance")

    return {
        'brand': st.sidebar.selectbox("Brand", ["All"] + df["brand"].unique()),
        'gender': st.sidebar.selectbox("Gender", ["All"] + exctract_unique_options(excel, 'gender')),
        'scent': st.sidebar.selectbox("Scent Direction", ["All"] + extract_unique_options(data, 'scent_direction', 'Unknown')),
        'season': st.sidebar.selectbox("Season", ["All"] + extract_unique_options(data, 'season', 'All Year')),
        'occasion': st.sidebar.selectbox("Personality", ["All"] + extract_unique_options(data, 'occasion', 'Everyday')),
        'personality': st.sidebar.selectbox("Occasion", ["All"] + extract_unique_options(data, 'personality', 'Classic')),
        'price': st.sidebar.selectbox("Price", ["All"] + extract_unique_options(data, 'price', 'Unknown'))
    }

# filters
def filter_perfumes(data, filters):
    return [
        perfume for perfume in data
        if (filters['gender'] == 'All' or perfume.get('gender') == filters['gender']) and
           (filters['scent'] == 'All' or perfume.get('scent_direction') == filters['scent']) and
           (filters['season'] == 'All' or perfume.get('season') == filters['season']) and
           (filters['occasion'] == 'All' or perfume.get('occasion') == filters['occasion']) and
           (filters['personality'] == 'All' or perfume.get('personality') == filters['personality']) and
           (filters['price'] == 'All' or perfume.get('price') == filters['price'])
    ]

# results
def display_results(filtered_data):
    st.markdown("### Matching Perfumes")
    st.write(f"Found {len(filtered_data)} perfumes matching criteria:")

    for perfume in filtered_data:
        st.markdown(f"**{perfume.get('name', 'Unknown')}** by {perfume.get('brand', 'Unknown')}")
        st.markdown(f"*Gender:* {perfume.get('gender', 'Unknown')} | *Scent:* {perfume.get('scent_direction', 'Unknown')} | *Season:* {perfume.get('season', 'Unknown')}")
        st.markdown(f"*Occasion:* {perfume.get('occasion', 'Unknown')} | *Personality:* {perfume.get('personality', 'Unknown')} | *Price:* {perfume.get('price', 'Unknown')}\n")
        st.markdown("---")

#charts
def display_price_chart(data):
    df = pd.DataFrame(data)
    if not df.empty and 'name' in df.columns and 'price' in df.columns:
        df = df[['name', 'price']].sort_values(by='price', ascending=False)
        df.columns = ['Perfume', 'Price']
        bar_chart = alt.Chart(df).mark_bar(cornerRadius=10).encode(
            x='Price',
            y=alt.Y('Perfume', sort='-x'),
            color=alt.value('#ff4b4b'),
            tooltip=['Perfume', 'Price']
        ).properties(title='Perfume Price Comparison')
        st.altair_chart(bar_chart, use_container_width=True)


def main():
    set_background()
    data = fetch_data()
    filters = render_sidebar_filters(data)

    if st.sidebar.button('Show Results'):
        filtered = filter_perfumes(data, filters)
        if filtered:
            display_results(filtered)
            display_price_chart(filtered)
        else:
            st.warning("No perfumes match your criteria.")
    else:
        st.write("Select your preferences and click 'Show Results' to explore perfumes.")



if __name__ == "__main__":
    main()
