# shop_finder_api.py

import requests

def find_shops(perfume_name, location="Zurich"):
    api_key = "AIzaSyBL6VBzyzqNyBnMuoB-aay5SGUQXNUsE2I"  # <-- Replace with your actual Google Places API Key
    search_query = f"{perfume_name} perfume store near {location}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        results = data.get('results', [])

        shops = []
        for place in results[:5]:  # Limit to top 5 results
            shops.append({
                'name': place.get('name', 'Unknown Shop'),
                'address': place.get('formatted_address', 'No address available')
            })
        return shops

    except Exception as e:
        print(f"Error fetching shop data: {e}")
        return []
