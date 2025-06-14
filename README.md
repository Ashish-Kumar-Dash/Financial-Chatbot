
# Financial Chatbot Project

## Overview
This Flask-based web chatbot answers predefined financial queries for Microsoft, Tesla, and Apple based on financial_data.xlsx.

## Setup
1. Ensure Python 3.x is installed.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place your own `financial_data.xlsx` in the project root, with columns:
   - Company, Fiscal Year, Total Revenue (B USD), Net Income (B USD), Total Assets (B USD), Total Liabilities (B USD), Operating Cash Flow (B USD)

## Running the App
```bash
python app.py
```
Access `http://127.0.0.1:5000/` in your browser. Select company or All, enter query, and submit.

## Supported Queries
- What is the total revenue for [Company] in [Year]?
- How has net income changed from [Year1] to [Year2] for [Company]?
- What is the operating cash flow for [Company] in [Year]?
- Which company had the highest revenue in [Year]?
- Which company saw the biggest drop in net income from [Year1] to [Year2]?

## Limitations
- Only handles predefined patterns via keyword and regex matching.
- Depends on data in `financial_data.xlsx`. Update file for new years or companies.
- Simple UI; can be extended with better styling or additional endpoints.

## Testing
- Manually test queries via web UI or API endpoint `/api/query` with JSON:
  ```json
  { "company": "Microsoft", "query": "What is the total revenue for Microsoft in 2024?" }
  ```
- Example using curl:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"company":"Tesla","query":"Which company had the highest revenue in 2023?"}' http://127.0.0.1:5000/api/query
  ```
