# This code creates a webpage that acts as a perfume finder – matching the perfect perfume to a person based on user-chosen features. 

# Import different services to build web app, work with tables and data, and create graphs.
import streamlit as st
import pandas as pd
import altair as alt
from shop_finder_api import find_shops 
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors

# Load perfume dataset (in CSV format) using pandas
df = pd.read_csv("Perfumes.csv", sep=";", encoding="utf-8")
# Stored in df; uses semicolons as separators due to CSV formatting; utf-8 encoding ensures special characters are read properly

# Configure session state variables for app memory
if "started" not in st.session_state:
    st.session_state.started = False     #Indicates if the user has clicked "Start Now"

if "show_results" not in st.session_state:
    st.session_state.show_results = False     #Indicates if user has clicked "Show results"
# These initialize both to False when app is opened to have a clean intro screen

# Set page layout depending on whether app has been started
if not st.session_state.started:
    st.set_page_config(
        page_title="Your Perfect Fragrance",    # Sets title in browser tab
        layout="wide",                          # Uses wide page layout
        initial_sidebar_state="collapsed"       # Sidebar is hidden initially
    )
# Page configuration in initial state with clean intro screen

else:
    st.set_page_config(
        page_title="Your Perfect Fragrance",    # Same title
        layout="wide",                          # Same layout
        initial_sidebar_state="expanded"        # Sidebar is visible after start
    )
# Once the user clicks "Start Now", the app remembers that with session_state and opens up the full layout with sidebar filters

# Train ML model for perfume similarity
features = ['brand', 'gender', 'scent_direction', 'season', 'personality', 'occasion', 'price']
df_filtered = df.dropna(subset=features + ['name'])  # Drop incomplete rows
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(df_filtered[features])  # Convert categorical to binary features
model_knn = NearestNeighbors(n_neighbors=4, metric='cosine')  # Initialize KNN
model_knn.fit(X_encoded)  # Train model

# Define function to recommend similar perfumes using ML
def ml_recommend_similar(perfume):
    """
    Recommends similar perfumes using KNN based on scent, season, occasion, personality, and price.
    """
    if perfume.get('name') not in df_filtered['name'].values:
        return []
    idx = df_filtered[df_filtered['name'] == perfume['name']].index[0]
    distances, indices = model_knn.kneighbors(X_encoded[idx])
    similar_indices = indices[0][1:]  # Skip the perfume itself
    return df_filtered.iloc[similar_indices][['name', 'brand', 'scent_direction']].to_dict(orient='records')

# Define custom function "set_background", which will apply a series of CSS styles to the app
def set_background():
    """
    Renders sidebar dropdown filters based on the perfume dataset.

    Args:
        df (DataFrame): The DataFrame containing perfume data.

    Returns:
        dict: A dictionary of selected filter values.
    """
    # "st.markdown" introduces HTML and CSS into the app 
    # <style> is a container from CSS that gives the app a specific design and layout by telling the browser how to draw each element on the screen
    # styling html and body sets the default font and layout for the entire web page; [class*="st-"] targets every class name with st- to ensure that all streamlit componenets use the style as well
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
    """, unsafe_allow_html=True) #allows raw HTML/CSS to be interpreted (normally restricted for security)
# Changes font everywhere, sets app background and text colour, styles the sidebar, styles the header, and styles the buttons.


# Define title page with title, intro text, 3 pics, and start now button
def show_intro(): # Defined a function called show_intro that when called renders the app's welcome screen
    # Styles title and intro text displaying a big title and two paragraphs of intro text; injected custom HTML (st.markdown) to gain full control over visual styling and layout
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
    # Wrap all content inside a div (HTML container) and center all text horizontally
    # h1 for the main header; p for the paragraphs below; "text-align:center" to position text horizontally in the center

    # Create three columns to divide the screen into three equal vertical sections to have a structure for the images
    col1, col2, col3 = st.columns(3)
    # st.columns(3) creates a horizontal layout with 3 equally sized columns: col1 (left), col2 (center), col3 (right)

    with col1:        # Creates a context block inside the first column (col1) in which all components will be rendered
        st.image("missdior.jpg", use_container_width=True)     # use_container_width=True so that the image will stretch to fit the column
    
    with col2:        # Creates a context block inside the second column (col2) in which all components will be rendered
        st.image("Gentleman.jpg", use_container_width=True)    # use_container_width=True so that the image will stretch to fit the column
        col2.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)    
        # Starts a <div> to center-align everything inside it and adds top margin to create spacing above the button
        if st.button("Start Now", key="start"): # Creates a button labeled "Start Now" which when clicked allows following actions to run:
            st.session_state.started = True # Sets session state variable "started" to True, allowing the app to show the next screen
            st.rerun() # Reruns the app to reflect the updated state immediately
        col2.markdown("</div>", unsafe_allow_html=True) # Closes the centered <div> container after the button)

    with col3:        # Creates a context block inside the third column (col3) in which all compoenets will be rendered
        st.image("Si.jpg", use_container_width=True)           # use_container_width=True so that the image will stretch to fit the column

# Sidebar filters
def render_sidebar_filters(df):    
# Defines a function that takes the perfume DataFrame df as input to set up interactive filters in the sidebar and returns selected values as dictionary
    """
    Renders sidebar dropdown filters based on the perfume dataset.

    Args:
        df (DataFrame): The DataFrame containing perfume data.

    Returns:
        dict: A dictionary of selected filter values.
    """
    st.sidebar.title("Your Signature Scent")    # Adds title at the top of the sidebar
    st.sidebar.markdown("### Matched to yourself")    # Adds a smaller title below the other to guide the user
    # Returns a dictionary with user-selected filter values from the sidebar
    return {
        # Dropdown for selecting brand; includes "All" plus unique, non-null brands from the dataset
        'brand': st.sidebar.selectbox("Brand", ["All"] + sorted(df["brand"].dropna().unique())),
        # Dropdown for selecting gender (e.g. Male, Female, Unisex)
        'gender': st.sidebar.selectbox("Gender", ["All"] + sorted(df["gender"].dropna().unique())),
        # Dropdown for selecting scent direction (e.g. Floral, Woody, etc.)
        'scent': st.sidebar.selectbox("Scent", ["All"] + sorted(df["scent_direction"].dropna().unique())),
        # Dropdown for selecting suitable season (e.g. Spring, Winter)
        'season': st.sidebar.selectbox("Season", ["All"] + sorted(df["season"].dropna().unique())),
        # Dropdown for selecting personality match (e.g. Confident, Romantic)
        'personality': st.sidebar.selectbox("Personality", ["All"] + sorted(df["personality"].dropna().unique())),
        # Dropdown for selecting usage occasion (e.g. Everyday, Formal)
        'occasion': st.sidebar.selectbox("Occasion", ["All"] + sorted(df["occasion"].dropna().unique())),
        # Dropdown for selecting price level (e.g. Low, High)
        'price': st.sidebar.selectbox("Price", ["All"] + sorted(df["price"].dropna().unique())),
    }
    # '...' is the name of the box of the dropdown; Selectbox triggers the dropdown for user to select from; 
    # dropna() removes any rows where the value is missing; unique() assures that value is named only once and not repeated

# Filter perfumes based on sidebar input
def filter_perfumes(df, filters):
# Define a function that filters the perfume dataset based on the selected sidebar filters
# Takes in two parameters: df (the full DataFrame containing all perfume entries) and filters (a dictionary with user-selected filter values)
    """
    Filters the perfume DataFrame based on selected criteria.

    Args:
        df (DataFrame): The full perfume dataset.
        filters (dict): Dictionary of user-selected filters.

    Returns:
        list: A list of filtered perfume rows.
    """
    filtered = []        # Create empty list to store perfumes that match all selected filters
    for _, p in df.iterrows():    # Loop for each row (perfume) in the DataFrame
        if filters["brand"] != "All" and p["brand"] != filters ["brand"]: 
            continue
        # If a a specific brand is selected and the perfume doesn't match, skip it
        if filters["gender"] != "All" and p["gender"] != filters ["gender"]:
            continue
        # If a specific gender is selected and this perfume doesn't match, skip it
        if filters["scent"] != "All" and p["scent"] != filters ["scent"]:
            continue
        # If a specific scent is selected and this perfume doesn't match, skip it
        if filters["season"] != "All" and p["season"] != filters ["season"]:
            continue
        # If a specific season is selected and this perfume doesn't match, skip it
        if filters["occasion"] != "All" and p["occasion"] != filters ["occasion"]:
            continue
        # If a specific occasion is selected and this perfume doesn't match, skip it
        if filters["personality"] != "All" and p["personality"] != filters ["personality"]:
            continue
        # If a specific personality is selected and this perfume doesn't match, skip it
        if filters["price"] != "All" and p["price"] != filters ["price"]:
            continue
        # If a specific price is selected and this perfume doesn't match, skip it
        filtered.append(p)    # If none of the filters ruled it out, the perfume is a match and added to the result list
    return filtered    # Return the list of perfumes that matched all active filters

# Define a function that displays a list of perfume matches along with an interactive option (shop finder)
def display_results(results):    # Takes in 'results', which is a list of perfume dictionaries matching the user's filters
    st.markdown("### Matching Fragrances")    # Print a section title above the results using markdown formattin
    st.write(f"{len(results)} matches found:")    # Show the total number of perfumes found based on the applied filters
    # f"{len(results)} is an f-string used to insert a value inside a string dynamically

    # Loop through each perfume in the results list
    for idx, p in enumerate(results):    # 'idx' is the index used so that each perfume's buttons, interactions, and saved state are kept separate and uniquely identified in your loop
        with st.container():    # Group the perfume display content in a Streamlit container for layout separation and visual clarity
            st.markdown(f"**{p.get('name')}** by {p.get('brand')}")    # Display the perfume's name in bold and the brand next to it
            # Display perfume attributes in a structured, inline markdown format including gender, scent direction, season, occasion, personality, and price:
            st.markdown(
                f"*Gender:* {p.get('gender')} | *Scent:* {p.get('scent_direction')} | *Season:* {p.get('season')}  \n"
                f"*Occasion:* {p.get('occasion')} | *Personality:* {p.get('personality')} | *Price:* {p.get('price')}"
            )

            # Find shops feature connected with API
            button_key = f"find_shops_{idx}"    # Define a unique key for this perfume's shop-finding button so that each perfume is treated as a separate UI element (for tracking)
            if st.button(f"Find Shops for {p.get('name')}"):    # A button that, when clicked, triggers a shop-finding function for the perfume
                st.session_state[f'shops_{idx}'] = find_shops(p.get('name'))    # Call a function that searches for shops selling the perfume and store the result in session state
                # Session state is used so the result persists across app reruns

            if f'shops_{idx}' in st.session_state:   # Check if shop results for this specific perfume (indexed by idx) are stored in session state
            # This would be True only if the "Find Shops" button was previously clicked
                shops = st.session_state[f'shops_{idx}']    # Retrieve the shop list for this specific perfume from session state
                if shops:    # If shops were found, show a green success message
                    st.success("Shops found nearby:")
                    for shop in shops:
                        st.markdown(f"- **{shop['name']}** – {shop['address']}")
                else:    # If no shops were found, display a warning message
                    st.warning("No shops found nearby. Try a different location.") 
            # Draw a horizontal line to separate this perfume result from the next one
            # Helps maintain a clean, structured layout in the app
            st.markdown("---")

# Display price comparison chart
def display_price_chart(results):
     """
    Displays a horizontal bar chart comparing perfume prices.

    Args:
        results (list): A list of filtered perfume dictionaries.
    """
    df_chart = pd.DataFrame(results)    # Convert the list of result dictionaries into a pandas DataFrame (each perfume becomes a rom)
    if not df_chart.empty and 'name' in df_chart.columns and 'price' in df_chart.columns:    # Check if the DataFrame is not empty and contains both 'name' and 'price' columns
    # This ensures that the chart is only generated if valid data is available
        df_chart = df_chart[['name', 'price']].dropna().sort_values(by='price', ascending=False)    # Keep only the 'name' and 'price' columns for charting and sort in descending order
        df_chart.columns = ['Perfume', 'Price']    # Rename the columns to more readable labels for the chart display
        chart = alt.Chart(df_chart).mark_bar(cornerRadius=10).encode(    # Create a horizontal bar chart using Altair; encode() tells Altair how to map data columns to visual elements in the chart
            x='Price', # X-axis: price values
            y=alt.Y('Perfume', sort='-x'),    # Y-axis: perfume names (sorted by price descending using '-x')
            color=alt.value('#d27979'),    # Color: all bars use the same color
            tooltip=['Perfume', 'Price']    # Tooltip: shows perfume name and price on hover
        ).properties(title='Perfume Price Comparison')    # sets title to  tell users what the chart represents
        st.altair_chart(chart, use_container_width=True)    # Render the chart in the Streamlit app, stretching it to the full container widt

# Main application logic
def main():        # is the core function that runs your app’s logic, deciding what content to show at each stage, based on the user’s actions
    set_background()     # Apply the custom CSS background, fonts, and button styling defined earlier

    if not st.session_state.get("started"):    # Check if the app has been "started" (i.e., if the user has clicked "Start Now"); if not, show the intro screen and exit the function early
        show_intro()       # Render the intro title, description, and images
        return             # Exit the function to prevent the rest of the app from running

    filters = render_sidebar_filters(df)    # Render the sidebar filter UI and store the selected filter values

    # Initialize the session state flag to control whether results should be shown
    if "show_results" not in st.session_state:    
        st.session_state["show_results"] = False

    # Create a "Show Results" button in the sidebar
    if st.sidebar.button("Show Results"):    # When clicked, sets the session flag to True so filtered results will be displayed
        st.session_state["show_results"] = True

    # If the "Show Results" button was clicked:
    if st.session_state.show_results:
        result = filter_perfumes(data, filters)    # Apply the filter logic to the perfume dataset using the selected filters
        if result:    # If matching perfumes are found, display them and show a price comparison chart
            display_results(result)
            display_price_chart(result)
        else:        # If no perfumes match the selected filters, display a warning message
            st.warning("No perfumes match your criteria.")
    else:        # If results haven't been requested yet, show an instructional layout with an image and guidance
        col1, col2, col3 = st.columns([1, 2, 1])        # Create three columns (left = 1, center = 2, right = 1) for centered layout

        with col2:        # In the center column, display an image and usage instructions
            st.image("Gentleman.jpg", width=450)        # Show a centered image (acts as a visual welcome)
            # Display instructional text using custom HTML to center-align and format it
            st.markdown("""
                <h2 style="text-align: center; margin-top: 1rem;">Welcome to Your Perfect Fragrance</h2>
                <p style="text-align: center; font-size: 18px;">Use the filters depending on your preferences to sort perfumes by brand, season, occasion, and more.</p>
                <p style="text-align: center; font-size: 18px;">Once you're ready, click <em>Show Results</em> to explore fragrances curated to your personality and mood.</p>
                <p style="text-align: center; font-size: 18px;">Not sure what to pick? Start with your favorite brand or season!</p>
            """, unsafe_allow_html=True)    # Allow raw HTML formatting

# Ensure the main() function runs only when this script is executed directly
# Prevents the app from running automatically if the file is imported as a module elsewhere
if __name__ == "__main__":
    main()
