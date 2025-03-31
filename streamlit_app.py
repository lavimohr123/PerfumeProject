import streamlit as st
import requests
import pandas as pd
import altair as alt

# Set sleek background and styling
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://images.pexels.com/photos/1666335/pexels-photo-1666335.jpeg');
            background-size: cover;
            background-attachment: fixed;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
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
            color: #FFD700;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize background settings
set_background()

# Function to fetch perfume dupes data from FragranceFinderAPI
def fetch_data():
    url = "https://fragrancefinder-api.p.rapidapi.com/dupes/66c70dee71fb63515fcfa1bf"
    headers = {
        "X-RapidAPI-Key": "99f01dd00dmshf9ecd3187bff8cep1ccd6djsneb0d58196aab", 
        "X-RapidAPI-Host": "fragrancefinder-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('dupes', [])
    else:
        st.error(f"Failed to retrieve data. Status Code: {response.status_code}")
        return []

# Fetch all perfume dupes data
all_data = fetch_data()

# Extract unique attributes for filtering
# genders = sorted(set(perfume.get('gender', 'Unisex') for perfume in all_data))
genders = set({"Male" , "Female", "Diverse"})
scent_directions = sorted(set(perfume.get('scent_direction', 'Unknown') for perfume in all_data))
seasons = sorted(set(perfume.get('season', 'All Year') for perfume in all_data))
occasions = sorted(set(perfume.get('occasion', 'Everyday') for perfume in all_data))
personalities = sorted(set(perfume.get('personality', 'Classic') for perfume in all_data))
prices = sorted(set(perfume.get('price', 'Unknown') for perfume in all_data))

# Sidebar filters with modern UI
st.sidebar.title("Perfume Finder")
st.sidebar.markdown("### Find Your Perfect Fragrance")
selected_gender = st.sidebar.selectbox("Gender", ["All"] + genders)
selected_scent_direction = st.sidebar.selectbox("Scent Direction", ["All"] + scent_directions)
selected_season = st.sidebar.selectbox("Season", ["All"] + seasons)
selected_occasion = st.sidebar.selectbox("Occasion", ["All"] + occasions)
selected_personality = st.sidebar.selectbox("Personality", ["All"] + personalities)
selected_price = st.sidebar.selectbox("Price Range", ["All"] + prices)

if st.sidebar.button('Show Results'):
    st.markdown("""
        <style>
        .overlay {
            opacity: 0.7;
            background-color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    # Filter perfumes based on user selection
    filtered_data = [
        perfume for perfume in all_data
        if (selected_gender == 'All' or perfume.get('gender') == selected_gender) and
           (selected_scent_direction == 'All' or perfume.get('scent_direction') == selected_scent_direction) and
           (selected_season == 'All' or perfume.get('season') == selected_season) and
           (selected_occasion == 'All' or perfume.get('occasion') == selected_occasion) and
           (selected_personality == 'All' or perfume.get('personality') == selected_personality) and
           (selected_price == 'All' or perfume.get('price') == selected_price)
    ]

    if filtered_data:
        st.markdown("### Matching Perfumes")
        st.write(f"Found {len(filtered_data)} perfumes matching criteria:")
        
        for perfume in filtered_data:
            st.markdown(f"**{perfume.get('name', 'Unknown')}** by {perfume.get('brand', 'Unknown')}\n")
            st.markdown(f"*Gender:* {perfume.get('gender', 'Unknown')} | *Scent:* {perfume.get('scent_direction', 'Unknown')} | *Season:* {perfume.get('season', 'Unknown')}")
            st.markdown(f"*Occasion:* {perfume.get('occasion', 'Unknown')} | *Personality:* {perfume.get('personality', 'Unknown')} | *Price:* {perfume.get('price', 'Unknown')}\n")
            st.markdown("---")
        
        df = pd.DataFrame(filtered_data)
        if not df.empty:
            df = df[['name', 'price']].sort_values(by='price', ascending=False)
            df.columns = ['Perfume', 'Price']
            bar_chart = alt.Chart(df).mark_bar(cornerRadius=10).encode(
                x='Price',
                y=alt.Y('Perfume', sort='-x'),
                color=alt.value('#ff4b4b'),
                tooltip=['Perfume', 'Price']
            ).properties(
                title='Perfume Price Comparison'
            )
            st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.warning("No perfumes match your criteria.")
else:
    st.write("Select your preferences and click 'Show Results' to explore perfumes.")
