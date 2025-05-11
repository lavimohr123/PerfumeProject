# shop_finder_api.py to add feature to the main code (in perfume finder)

import requests        # Import the 'requests' library to handle HTTP requests to external APIs

def find_shops(perfume_name, location="Zurich"):
    """
    Searches for nearby shops selling a specific perfume using the Google Places API.

    Args:
        perfume_name (str): The name of the perfume to search for.
        location (str): The location to search around. Default is 'Zurich'.

    Returns:
        list: A list of dictionaries with 'name' and 'address' of found shops.
    """
    api_key = "AIzaSyBL6VBzyzqNyBnMuoB-aay5SGUQXNUsE2I"      # Google Places API key
    search_query = f"{perfume_name} perfume store near {location}"        # Construct a text-based search query combining perfume name and location
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&key={api_key}"        # Build the full request URL for the Google Places Text Search API

    try:
        response = requests.get(url)        # Send a GET request to the API endpoint using the constructed URL
        data = response.json()        # Convert the JSON response into a Python dictionary
        results = data.get('results', [])        # Get the list of places (shops) from the API response; default to empty list if key is missing

        shops = []        # Initialize an empty list to store extracted shop data
        for place in results[:5]:  # Iterate over the first 5 results from the API response
            shops.append({        # Extract the name and address of each place and add it to the shops list
                'name': place.get('name', 'Unknown Shop'),        # Use 'Unknown Shop' if name is missing
                'address': place.get('formatted_address', 'No address available')           # Fallback address if missing
            })
        return shops        # Return the list of found shops as dictionaries with name and address

    except Exception as e:        # If any error occurs during the request or data handling, catch it and print the error message
        print(f"Error fetching shop data: {e}")
        return []        # Return an empty list to indicate that no shops were found or an error occurred
