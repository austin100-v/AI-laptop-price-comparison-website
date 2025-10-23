from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration - Add your API key here
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', 'your_brave_api_key_here')

@app.route('/api/search', methods=['GET'])
def search_laptops():
    """
    Search for laptops using the query parameter
    Example: /api/search?q=dell+xps+13
    """
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    # Choose your search method
    # Option 1: Use SerpAPI (Google Shopping)
    results = search_with_serpapi(query)
    
    # Option 2: Use Brave Search API
    # results = search_with_brave(query)
    
    # Option 3: Demo mode (no API key needed)
    # results = search_demo_mode(query)
    
    return jsonify(results)

def search_with_serpapi(query):
    """
    Search using SerpAPI - Google Shopping Results
    Get API key from: https://serpapi.com/
    """
    try:
        # First, try Google Shopping
        url = "https://serpapi.com/search"
        params = {
            'q': f'{query} laptop',
            'api_key': SERPAPI_KEY,
            'engine': 'google_shopping',
            'num': 20,
            'gl': 'us'  # Country code
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        
        # Process shopping results
        if 'shopping_results' in data:
            for item in data['shopping_results']:
                # Extract the best available URL
                product_url = item.get('link', '#')
                
                # Some results have a 'product_link' which is more direct
                if 'product_link' in item:
                    product_url = item['product_link']
                
                # Extract product ID if available for later detailed lookup
                product_id = item.get('product_id', None)
                
                results.append({
                    'title': item.get('title', ''),
                    'price': item.get('price', 'N/A'),
                    'seller': item.get('source', 'Unknown'),
                    'url': product_url,
                    'product_id': product_id,
                    'specs': extract_specs_from_title(item.get('title', '')),
                    'rating': item.get('rating', None),
                    'thumbnail': item.get('thumbnail', None)
                })
        
        # If no shopping results, try regular Google search for buy links
        if len(results) == 0:
            params['engine'] = 'google'
            params['q'] = f'{query} laptop buy online price'
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'organic_results' in data:
                for item in data['organic_results'][:15]:  # Limit to 15 results
                    # Filter for e-commerce sites
                    link = item.get('link', '')
                    if any(site in link.lower() for site in ['amazon', 'bestbuy', 'walmart', 'newegg', 'ebay']):
                        snippet = item.get('snippet', '')
                        price = extract_price(item.get('title', '') + ' ' + snippet)
                        
                        if price:
                            results.append({
                                'title': item.get('title', ''),
                                'price': price,
                                'seller': extract_domain(link),
                                'url': link,
                                'product_id': None,
                                'specs': extract_specs_from_title(item.get('title', '')),
                                'rating': None,
                                'description': snippet
                            })
        
        return {'results': results, 'count': len(results)}
    
    except Exception as e:
        print(f"Error in search_with_serpapi: {e}")
        return {'error': str(e), 'results': []}

def search_with_brave(query):
    """
    Search using Brave Search API
    Get API key from: https://brave.com/search/api/
    """
    try:
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            'Accept': 'application/json',
            'X-Subscription-Token': BRAVE_API_KEY
        }
        params = {
            'q': f'{query} laptop price buy',
            'count': 20
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        
        results = []
        if 'web' in data and 'results' in data['web']:
            for item in data['web']['results']:
                price = extract_price(item.get('description', '') + ' ' + item.get('title', ''))
                if price:
                    results.append({
                        'title': item.get('title', ''),
                        'price': price,
                        'seller': extract_domain(item.get('url', '')),
                        'url': item.get('url', '#'),
                        'specs': extract_specs_from_title(item.get('title', '')),
                        'description': item.get('description', '')
                    })
        
        return {'results': results, 'count': len(results)}
    
    except Exception as e:
        return {'error': str(e), 'results': []}

def search_demo_mode(query):
    """
    Demo mode - returns sample data
    Use this when you don't have an API key yet
    """
    demo_laptops = [
        {
            'title': 'Dell XPS 13 9310 - 11th Gen Intel Core i7, 16GB RAM, 512GB SSD',
            'price': '$1,299.99',
            'seller': 'amazon.com',
            'url': 'https://amazon.com',
            'specs': ['Intel Core i7-1185G7', '16GB RAM', '512GB SSD', '13.4" FHD+'],
            'rating': 4.5
        },
        {
            'title': 'HP Pavilion Gaming Laptop 15 - AMD Ryzen 5, 8GB RAM, GTX 1650',
            'price': '$799.99',
            'seller': 'bestbuy.com',
            'url': 'https://bestbuy.com',
            'specs': ['AMD Ryzen 5 5600H', '8GB RAM', '256GB SSD', 'GTX 1650'],
            'rating': 4.3
        },
        {
            'title': 'Apple MacBook Pro 14" M3 Pro - 18GB RAM, 512GB SSD',
            'price': '$1,999.00',
            'seller': 'apple.com',
            'url': 'https://apple.com',
            'specs': ['Apple M3 Pro', '18GB RAM', '512GB SSD', '14.2" Retina'],
            'rating': 4.8
        },
        {
            'title': 'Lenovo ThinkPad X1 Carbon Gen 11 - Intel Core i7, 16GB RAM',
            'price': '$1,499.99',
            'seller': 'lenovo.com',
            'url': 'https://lenovo.com',
            'specs': ['Intel Core i7-1355U', '16GB RAM', '512GB SSD', '14" WUXGA'],
            'rating': 4.6
        },
        {
            'title': 'ASUS ROG Strix G15 Gaming - Ryzen 9, RTX 3070, 16GB RAM',
            'price': '$1,599.99',
            'seller': 'newegg.com',
            'url': 'https://newegg.com',
            'specs': ['AMD Ryzen 9 5900HX', '16GB RAM', '1TB SSD', 'RTX 3070'],
            'rating': 4.7
        },
        {
            'title': 'Acer Swift 3 - AMD Ryzen 7, 8GB RAM, 512GB SSD',
            'price': '$649.99',
            'seller': 'walmart.com',
            'url': 'https://walmart.com',
            'specs': ['AMD Ryzen 7 5700U', '8GB RAM', '512GB SSD', '14" FHD'],
            'rating': 4.2
        },
        {
            'title': 'Dell Inspiron 15 3000 - Intel Core i5, 12GB RAM',
            'price': '$549.99',
            'seller': 'dell.com',
            'url': 'https://dell.com',
            'specs': ['Intel Core i5-1135G7', '12GB RAM', '256GB SSD', '15.6" HD'],
            'rating': 4.0
        },
        {
            'title': 'HP Envy x360 Convertible - AMD Ryzen 5, 16GB RAM',
            'price': '$899.99',
            'seller': 'hp.com',
            'url': 'https://hp.com',
            'specs': ['AMD Ryzen 5 5625U', '16GB RAM', '512GB SSD', 'Touchscreen'],
            'rating': 4.4
        },
    ]
    
    # Filter based on query
    query_lower = query.lower()
    filtered = [laptop for laptop in demo_laptops 
                if query_lower in laptop['title'].lower() or 
                any(query_lower in spec.lower() for spec in laptop['specs'])]
    
    # If no matches, return all
    if not filtered:
        filtered = demo_laptops
    
    return {'results': filtered, 'count': len(filtered), 'mode': 'demo'}

def extract_price(text):
    """Extract price from text"""
    price_patterns = [
        r'\$[\d,]+(?:\.\d{2})?',
        r'[\d,]+(?:\.\d{2})?\s*(?:USD|dollars?)',
        r'(?:KSh|Ksh|KES)\s*[\d,]+'
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def extract_domain(url):
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '')
    except:
        return 'Unknown'

def extract_specs_from_title(title):
    """Extract key specs from laptop title"""
    specs = []
    
    # Processors
    processors = ['i3', 'i5', 'i7', 'i9', 'ryzen 3', 'ryzen 5', 'ryzen 7', 'ryzen 9', 'm1', 'm2', 'm3']
    for proc in processors:
        if proc in title.lower():
            specs.append(proc.upper())
    
    # RAM
    ram_match = re.search(r'(\d+)\s*gb\s*ram', title, re.IGNORECASE)
    if ram_match:
        specs.append(f"{ram_match.group(1)}GB RAM")
    
    # Storage
    storage_match = re.search(r'(\d+)\s*(gb|tb)\s*ssd', title, re.IGNORECASE)
    if storage_match:
        specs.append(f"{storage_match.group(1)}{storage_match.group(2).upper()} SSD")
    
    # Graphics
    graphics = ['gtx', 'rtx', 'radeon', 'iris']
    for gpu in graphics:
        if gpu in title.lower():
            gpu_match = re.search(f'{gpu}\\s*\\d+', title, re.IGNORECASE)
            if gpu_match:
                specs.append(gpu_match.group(0).upper())
    
    return specs if specs else ['See details']

@app.route('/api/product', methods=['GET'])
def get_product_details():
    """
    Get detailed product information using SerpAPI product API
    Example: /api/product?product_id=12345
    """
    product_id = request.args.get('product_id', '')
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    try:
        url = "https://serpapi.com/search"
        params = {
            'engine': 'google_shopping_product',
            'product_id': product_id,
            'api_key': SERPAPI_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # Extract the actual product link
        product_link = data.get('product_results', {}).get('link', '#')
        
        return jsonify({
            'product_link': product_link,
            'data': data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Flask backend is running'})

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Laptop Price Finder API',
        'endpoints': {
            '/api/search?q=query': 'Search for laptops',
            '/api/health': 'Health check'
        }
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Server running at http://localhost:5000")
    print("Test search: http://localhost:5000/api/search?q=dell")
    app.run(debug=True, host='0.0.0.0', port=5000)