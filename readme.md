# Set up
1. Create python virtual environment
    - `python3.11 -m venv venv`
2. Active virtual environment
    - `source venv/bin/activate`
3. Install requirements
    - `pip install -r requirements.txt`
4. Add google api key
    - `export GOOGLE_API_KEY='your_api_key_here'`
# Generating ChromaDB for Style
1. Run cells in "Data Processing.ipynb" under the Lex Podcast Dataset Processing
# Running Server
1. Run server
    - `fastapi run main.py`
2. Access server at localhost:8000 or test endpoints at localhost:8000/docs