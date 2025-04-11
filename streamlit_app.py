import streamlit as st
import pandas as pd
import altair as alt

# UI styling
def set_background():
    st.markdown(
        """
        <style>

        /* Global: Georgia überall */
        html, body, [class*="st-"] {
            font-family: 'Georgia', serif !important;
        }

        /* Schriftgrößen */
        h1 { font-size: 32px !important; }
        h2 { font-size: 26px !important; }
        h3 { font-size: 22px !important; }
        p, label, div { font-size: 18px !important; }

        /* App-Hintergrund */
        .stApp {
            background-color: #fffaf0;
            color: #5b3a29;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #f5eeee;
            color: #5b3a29;
            padding-top: 1rem;
        }

        /* Sidebar Titel */
        section[data-testid="stSidebar"] h1 {
            font-family: 'Georgia', serif !important;
            font-size: 30px !important;
            color: #5b3a29 !important;
            letter-spacing: 1px;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        /* Sidebar Untertitel */
        section[data-testid="stSidebar"] h3 {
            font-family: 'Georgia', serif !important;
            font-size: 20px !important;
            color: #5b3a29 !important;
            letter-spacing: 0.5px;
            font-weight: 500;
            margin-top: 0;
            margin-bottom: 1.5rem;
        }

        /* Button */
        .stButton>button {
            background-color: #d27979;
            color: white;
            border-radius: 10px;
            font-size: 18px;
            padding: 0.6rem 1.2rem;
            letter-spacing: 0.5px;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #8b4513;
        }

        /* Header oben (weißer Balken) */
        header[data-testid="stHeader"] {
            background-color: #fffaf0;
            color: #5b3a29;
            border-bottom: 1px solid #d3c5b3;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# Load the CSV once at the top
df = pd.read_csv("Perfumes.csv", sep=";", encoding="utf-8")
data = df.to_dict(orient="records")  # Convert to list of dictionaries for filtering

# Sidebar filters
def render_sidebar_filters(df):
    st.sidebar.title("Perfume Finder")
    st.sidebar.markdown("### Find Your Perfect Fragrance")

    return {
        'brand': st.sidebar.selectbox("Brand", ["All"] + list(df["brand"].dropna().unique())),
        'gender': st.sidebar.selectbox("Gender", ["All"] + list(df["gender"].dropna().unique())),
        'scent': st.sidebar.selectbox("Scent", ["All"] + list(df["scent_direction"].dropna().unique())),
        'season': st.sidebar.selectbox("Season", ["All"] + list(df["season"].dropna().unique())),
        'personality': st.sidebar.selectbox("Personality", ["All"] + list(df["personality"].dropna().unique())),
        'occasion': st.sidebar.selectbox("Occasion", ["All"] + list(df["occasion"].dropna().unique())),
        'price': st.sidebar.selectbox("Price", ["All"] + list(df["price"].dropna().unique())),
    }

# Filtering logic
def filter_perfumes(data, filters):
    return [
        perfume for perfume in data
        if (filters['brand'] == 'All' or perfume.get('brand') == filters['brand']) and
           (filters['gender'] == 'All' or perfume.get('gender') == filters['gender']) and
           (filters['scent'] == 'All' or perfume.get('scent') == filters['scent']) and
           (filters['season'] == 'All' or perfume.get('season') == filters['season']) and
           (filters['occasion'] == 'All' or perfume.get('occasion') == filters['occasion']) and
           (filters['personality'] == 'All' or perfume.get('personality') == filters['personality']) and
           (filters['price'] == 'All' or perfume.get('price') == filters['price'])
    ]

# Results section
def display_results(filtered_data):
    st.markdown("### Matching Perfumes")
    st.write(f"Found {len(filtered_data)} perfumes matching criteria:")

    for perfume in filtered_data:
        st.markdown(f"**{perfume.get('name', 'Unknown')}** by {perfume.get('brand', 'Unknown')}")
        st.markdown(
            f"*Gender:* {perfume.get('gender', 'Unknown')} | "
            f"*Scent:* {perfume.get('scent', 'Unknown')} | "
            f"*Season:* {perfume.get('season', 'Unknown')}  \n"
            f"*Occasion:* {perfume.get('occasion', 'Unknown')} | "
            f"*Personality:* {perfume.get('personality', 'Unknown')} | "
            f"*Price:* {perfume.get('price', 'Unknown')}"
        )
        st.markdown("---")

# Price chart
def display_price_chart(filtered_data):
    chart_df = pd.DataFrame(filtered_data)
    if not chart_df.empty and 'name' in chart_df.columns and 'price' in chart_df.columns:
        chart_df = chart_df[['name', 'price']].dropna().sort_values(by='price', ascending=False)
        chart_df.columns = ['Perfume', 'Price']
        chart = alt.Chart(chart_df).mark_bar(cornerRadius=10).encode(
            x='Price',
            y=alt.Y('Perfume', sort='-x'),
            color=alt.value('#ff4b4b'),
            tooltip=['Perfume', 'Price']
        ).properties(title='Perfume Price Comparison')
        st.altair_chart(chart, use_container_width=True)

# Main app
def main():
    set_background()
    filters = render_sidebar_filters(df)

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
