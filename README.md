# AI Laptop Price Comparison Website

An intelligent web application that searches across the internet to find laptops and compare prices from multiple sellers. Built with Flask backend and vanilla JavaScript frontend, integrated with SerpAPI for real-time product data.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **AI-Powered Search** - Intelligent laptop search using SerpAPI
- **Price Comparison** - Compare prices from multiple online retailers
- **Direct Links** - Click through to seller websites for purchases
- **Smart Filtering** - Sort by price and filter by brand
- **Detailed Specs** - View processor, RAM, storage, and graphics info
- **Product Ratings** - See customer ratings when available
- **Modern UI** - Beautiful, responsive design that works on all devices
- **Real-time Results** - Get up-to-date pricing information instantly


## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A SerpAPI account and API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-laptop-price-comparison-website.git
cd AI-laptop-price-comparison-website
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install flask flask-cors requests beautifulsoup4 python-dotenv
```

4. **Set up your API key**

Create a `.env` file in the project root:
```bash
SERPAPI_KEY=your_serpapi_key_here
```

To get a SerpAPI key:
- Visit [https://serpapi.com/](https://serpapi.com/)
- Sign up for a free account (100 searches/month free)
- Copy your API key from the dashboard

5. **Run the Flask backend**
```bash
python app.py
```

You should see:
```
Starting Flask server...
Server running at http://localhost:5000
Test search: http://localhost:5000/api/search?q=dell
```

6. **Open the frontend**

Open `index.html` in your web browser, or use a local server:
```bash
# Using Python's built-in server (in a new terminal)
python -m http.server 8080
```

Then visit `http://localhost:8080`

## Usage

### Basic Search

1. Open the web interface
2. Type your search query (e.g., "Dell XPS 13", "gaming laptop", "MacBook Pro")
3. Click **Search** or press Enter
4. Browse results with prices, specs, and ratings
5. Click **View Deal →** to visit the seller's website

### Advanced Features

**Sort Results:**
- Relevance (default)
- Price: Low to High
- Price: High to Low

**Filter by Brand:**
- All Brands
- Dell
- HP
- Lenovo
- Apple
- ASUS
- Acer

## API Endpoints

### Search for Laptops
```
GET /api/search?q=<query>
```

**Parameters:**
- `q` (required) - Search query

**Response:**
```json
{
  "results": [
    {
      "title": "Dell XPS 13 9310...",
      "price": "$1,299.99",
      "seller": "amazon.com",
      "url": "https://amazon.com/...",
      "specs": ["Intel Core i7", "16GB RAM", "512GB SSD"],
      "rating": 4.5
    }
  ],
  "count": 15
}
```

### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Flask backend is running"
}
```

### Product Details (Optional)
```
GET /api/product?product_id=<id>
```

## Project Structure

```
AI-laptop-price-comparison-website/
├── app.py                 # Flask backend server
├── index.html            # Frontend interface
├── .env                  # Environment variables (API keys)
├── .gitignore           # Git ignore file
├── README.md            # This file
└── requirements.txt     # Python dependencies (optional)
```

## Configuration

### Change API Provider

The backend supports multiple search providers. To switch:

**Option 1: SerpAPI (Default)**
```python
# In app.py, line 23
results = search_with_serpapi(query)
```

**Option 2: Brave Search API**
```python
# Get API key from https://brave.com/search/api/
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
results = search_with_brave(query)
```

**Option 3: Demo Mode** (no API key needed)
```python
results = search_demo_mode(query)
```

### Change Backend URL

If running Flask on a different port or domain:

```javascript
// In index.html, line 366
const API_URL = 'http://localhost:5000';  // Change this
```

## Deployment

### Deploy to Heroku

1. Create a `requirements.txt`:
```bash
pip freeze > requirements.txt
```

2. Create a `Procfile`:
```
web: gunicorn app:app
```

3. Install gunicorn:
```bash
pip install gunicorn
```

4. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku config:set SERPAPI_KEY=your_key_here
```

### Deploy to Render/Railway

1. Connect your GitHub repository
2. Set environment variable: `SERPAPI_KEY`
3. Deploy automatically on push

## Troubleshooting

### Backend Connection Error
**Problem:** Frontend shows "Backend Not Running"

**Solution:**
- Make sure Flask is running: `python app.py`
- Check the URL in index.html matches your Flask server
- Verify no firewall is blocking port 5000

### No Results Found
**Problem:** Search returns empty results

**Solution:**
- Check your SerpAPI key is valid and has credits
- Verify internet connection
- Try a different search query
- Check Flask terminal for error messages

### Links Don't Work
**Problem:** Clicking "View Deal" doesn't navigate to seller

**Solution:**
- Links are generated by SerpAPI and may vary
- Some results may have redirect links
- Try searching for more specific laptop models
- Check browser console for JavaScript errors

## API Rate Limits

**SerpAPI Free Tier:**
- 250 searches per month
- Upgrade for more searches

**Best Practices:**
- Cache search results
- Implement request throttling
- Consider upgrading for production use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Add price history tracking
- [ ] Email alerts for price drops
- [ ] Save favorite laptops
- [ ] Compare multiple laptops side-by-side
- [ ] Support for more product categories
- [ ] User authentication and profiles
- [ ] Advanced filtering (RAM, processor, price range)
- [ ] Mobile app version

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SerpAPI](https://serpapi.com/) for providing the search API
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- All contributors who help improve this project

## Contact

For questions or support, please open an issue on GitHub or contact:
- Email: mwema.irungu@gmail.com
- GitHub: [@austin100-v](https://github.com/austin100-v)

---

**If you find this project helpful, please give it a star!**

Made by [Austine Irungu]