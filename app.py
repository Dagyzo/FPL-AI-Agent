import requests
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Function to fetch FPL data
def fetch_fpl_data():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return pd.DataFrame(data['elements'])

# Function to recommend captain
def recommend_captain(players_df):
    captain_candidates = players_df.sort_values('form', ascending=False).head(3)
    return captain_candidates[['first_name', 'second_name', 'form']].to_dict(orient='records')

# Function to recommend transfers
def recommend_transfers(players_df):
    top_performers = players_df[players_df['form'].astype(float) > 5]  # Players with high form
    return top_performers[['first_name', 'second_name', 'team', 'form']].to_dict(orient='records')

# Function to detect injured players
def injury_alert(players_df):
    injured_players = players_df[players_df['status'] == 'i']  # 'i' for injured players
    return injured_players[['first_name', 'second_name', 'team', 'status']].to_dict(orient='records')

# Route to display recommendations as a webpage
@app.route('/fpl/recommendations')
def get_recommendations():
    players_df = fetch_fpl_data()
    if players_df is None:
        return "Error fetching FPL data. Please try again later."
    
    captain = recommend_captain(players_df)
    transfers = recommend_transfers(players_df)
    injuries = injury_alert(players_df)

    return render_template('recommendations.html', captain=captain, transfers=transfers, injuries=injuries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

