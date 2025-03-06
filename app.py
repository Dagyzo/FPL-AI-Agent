import requests
import pandas as pd
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Function to fetch FPL data
def fetch_fpl_data():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['elements'])
    else:
        return pd.DataFrame()

# Function to recommend captain based on form
def recommend_captain(players_df):
    if not players_df.empty:
        captain_candidates = players_df.sort_values('form', ascending=False).head(3)
        return captain_candidates[['first_name', 'second_name', 'form']].to_dict(orient='records')
    return []

# Function to recommend transfers
def recommend_transfers(players_df):
    if not players_df.empty:
        top_performers = players_df[players_df['form'].astype(float) > 5]  # Players with high form
        return top_performers[['first_name', 'second_name', 'team', 'form']].to_dict(orient='records')
    return []

# Function to detect injured players
def injury_alert(players_df):
    if not players_df.empty:
        injured_players = players_df[players_df['status'] == 'i']  # 'i' for injured players
        return injured_players[['first_name', 'second_name', 'team', 'status']].to_dict(orient='records')
    return []

@app.route('/fpl/recommendations', methods=['GET'])
def get_recommendations():
    players_df = fetch_fpl_data()
    if players_df.empty:
        return jsonify({'error': 'Failed to fetch FPL data'}), 500
    
    captain = recommend_captain(players_df)
    transfers = recommend_transfers(players_df)
    injuries = injury_alert(players_df)
    
    return jsonify({
        'captain_recommendation': captain,
        'transfer_recommendations': transfers,
        'injury_alerts': injuries
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
