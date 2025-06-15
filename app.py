
from flask import Flask, request, jsonify, render_template
import pandas as pd
import re

app = Flask(__name__)

# Load financial data
df = pd.read_excel('b.csv')

def simple_chatbot_query(company, user_query):
    q = user_query.lower()
    # Identify year(s)
    years = re.findall(r'20\d{2}', user_query)
    years = [int(y) for y in years]
    # Helper to get value
    def get_value(comp, year, column):
        row = df[(df['Company'] == comp) & (df['Fiscal Year'] == year)]
        if not row.empty:
            return row.iloc[0][column]
        return None

    # Total revenue
    if 'total revenue' in q and company:
        if years:
            year = years[0]
        else:
            # default to latest year for company
            subset = df[df['Company'] == company]
            if subset.empty:
                return f"No data found for {company}."
            year = int(subset['Fiscal Year'].max())
        val = get_value(company, year, 'Total Revenue (B USD)')
        if val is not None:
            return f"The total revenue for {company} in {year} was {val} B USD."
        else:
            return f"Data not found for {company} in {year}."

    # Net income change
    if 'net income changed' in q or 'net income change' in q:
        if len(years) >= 2 and company:
            y1, y2 = years[0], years[1]
        elif len(years) == 1 and company:
            y2 = years[0]
            y1 = y2 - 1
        else:
            return "Please specify a company and two years or one year for net income change."
        ni1 = get_value(company, y1, 'Net Income (B USD)')
        ni2 = get_value(company, y2, 'Net Income (B USD)')
        if ni1 is None or ni2 is None:
            return "Data not found for the specified years."
        diff = ni2 - ni1
        pct = (diff / ni1 * 100) if ni1 else None
        sign = "increase" if diff > 0 else "decrease"
        if pct is not None:
            return (f"For {company}, net income {sign}d by {abs(diff):.2f} B USD "
                    f"({abs(pct):.1f}%) from {y1} to {y2}.")
        else:
            return f"Net income change from {y1} to {y2} for {company} cannot be computed due to zero baseline."

    # Operating cash flow
    if 'operating cash flow' in q and company:
        if years:
            year = years[0]
        else:
            subset = df[df['Company'] == company]
            if subset.empty:
                return f"No data found for {company}."
            year = int(subset['Fiscal Year'].max())
        val = get_value(company, year, 'Operating Cash Flow (B USD)')
        if val is not None:
            return f"The operating cash flow for {company} in {year} was {val} B USD."
        else:
            return f"Data not found for {company} in {year}."

    # Highest revenue among companies
    if 'highest revenue' in q:
        if years:
            year = years[0]
            subset = df[df['Fiscal Year'] == year]
            if subset.empty:
                return f"No data for year {year}."
            best = subset.loc[subset['Total Revenue (B USD)'].idxmax()]
            return f"{best['Company']} had the highest revenue in {year}, at {best['Total Revenue (B USD)']} B USD."
        else:
            return "Please specify a year for highest revenue query."

    # Biggest drop in net income among companies
    if 'biggest drop' in q and 'net income' in q:
        if len(years) >= 2:
            y1, y2 = years[0], years[1]
            diffs = {}
            for comp in df['Company'].unique():
                ni1 = get_value(comp, y1, 'Net Income (B USD)')
                ni2 = get_value(comp, y2, 'Net Income (B USD)')
                if ni1 is not None and ni2 is not None:
                    diffs[comp] = ni2 - ni1
            if not diffs:
                return "No sufficient data for the specified years."
            # find most negative change
            comp_drop = min(diffs, key=lambda k: diffs[k])
            diff = diffs[comp_drop]
            pct = (diff / get_value(comp_drop, y1, 'Net Income (B USD)') * 100) if get_value(comp_drop, y1, 'Net Income (B USD)') else None
            sign = "decrease" if diff < 0 else "increase"
            if pct is not None:
                return (f"{comp_drop} saw the biggest net income {sign} from {y1} to {y2}, change of {abs(diff):.2f} B USD "
                        f"({abs(pct):.1f}%).")
            else:
                return f"Net income change for {comp_drop} from {y1} to {y2} cannot be computed due to zero baseline."
        else:
            return "Please specify two years for net income drop comparison."

    return "Sorry, I can only answer predefined financial queries."

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        company = request.form.get('company')
        user_query = request.form.get('query')
        response = simple_chatbot_query(company if company != 'All' else None, user_query)
    return render_template('index.html', response=response)

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    company = data.get('company')
    user_query = data.get('query')
    if not user_query:
        return jsonify({'error': 'Missing query'}), 400
    result = simple_chatbot_query(company if company != 'All' else None, user_query)
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)
