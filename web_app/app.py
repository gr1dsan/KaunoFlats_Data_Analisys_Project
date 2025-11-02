import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

selected_df_global = None

OPTIONS = [
    'Cheapest', 'Safest', 'Closest to the city center', 'Biggest by area',
    'Biggest number of rooms', 'Least heating price'
]

PRIORITY_COLUMNS = {
    'Cheapest': 'Rank_by_prices',
    'Safest': 'Rank_by_crimes',
    'Closest to the city center': 'Ranked_by_CC_distance',
    'Biggest by area': 'Rank_by_area',
    'Biggest number of rooms': 'Average_rooms_number_ranked',
    'Least heating price': 'Heating_prices_rank',
    '--': ''
}

PROS_CONS_MAPPING = {
    'Rank_by_prices': 'Rent price',
    'Rank_by_crimes': 'Safety',
    'Ranked_by_CC_distance': 'Distance to city center',
    'Rank_by_area': 'Flat area',
    'Average_rooms_number_ranked': 'Number of rooms',
    'Heating_prices_rank': 'Heating price'
}


def calculate_final_score(df: pd.DataFrame, first: str, second: str) -> pd.DataFrame:
    """Compute weighted final score for each row based on priorities."""
    weights = {first: 0.7, second: 0.3}
    df['Final'] = 0
    for priority, weight in weights.items():
        col = PRIORITY_COLUMNS.get(priority)
        if col:
            df['Final'] += df[col] * weight
    return df


def city_center_description(rank: float) -> str:
    """Return human-readable city center distance description."""
    if rank <= 1:
        return 'In the center'
    elif rank <= 3:
        return 'Very close to the center'
    elif rank <= 5:
        return 'Close to the center'
    elif rank <= 7:
        return 'Moderately far from the center'
    elif rank <= 9:
        return 'Far from the center'
    elif rank <= 11:
        return 'Very far from the center'
    return 'Out of range'


def generate_pros_cons(row: pd.Series) -> tuple[list[str], list[str]]:
    """Generate pros and cons based on ranking values."""
    pros, cons = [], []
    for col, description in PROS_CONS_MAPPING.items():
        value = row[col]
        if value <= 5:
            pros.append(f"{description}")
        elif value >= 7:
            cons.append(f"{description}")
    return pros, cons

@app.route('/')
def redirection():
    return render_template('title.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def main():
    global selected_df_global
    res = avg_cost = avg_crime = avg_area = avg_heating_price = cc_distance = None
    pros, cons = [], []

    if request.method == 'POST':
        first_prior = request.form.get('priority1')
        second_prior = request.form.get('priority2')

        if first_prior and second_prior:
            df = pd.read_csv('web_app/data/Data.csv')
            df = calculate_final_score(df, first_prior, second_prior)

            best_district_row = (
                df.groupby('District', as_index=False)['Final']
                .sum()
                .sort_values('Final')
                .iloc[0]
            )
            res = best_district_row['District']

            selected_df_global = df[df['District'] == res]

            avg_cost = selected_df_global['Average_price'].mean()
            avg_crime = round(selected_df_global['Average_crimes'].mean())
            avg_heating_price = selected_df_global['Average_heating_price'].mean()
            avg_area = selected_df_global['Average_area'].mean()

            cc_distance = city_center_description(
                selected_df_global['Ranked_by_CC_distance'].mean()
            )

            pros, cons = generate_pros_cons(selected_df_global.iloc[0])
        else:
            print('Priority selection missing.')

    return render_template(
        'index.html', res=res, avg_crime=avg_crime, avg_cost=avg_cost,
        options=OPTIONS, avg_heating_price=avg_heating_price, avg_area=avg_area,
        cc_distance=cc_distance, pros=pros, cons=cons
    )


@app.route('/chart_data', methods=['GET', 'POST'])
def chart_data():
    global selected_df_global
    if selected_df_global is None:
        return jsonify({'error': 'No data selected yet'}), 400

    df = selected_df_global
    return jsonify({
        'under_300': df['under_300_count'].tolist(),
        'from_300_to_600': df['from_300_to_600'].tolist(),
        'from_600_to_900': df['from_600_to_900'].tolist(),
        'above_900': df['above_900_count'].tolist(),
        'number_of_modern_builds': df['Modern'].tolist(),
        'number_of_old_builds': df['Old'].tolist()
    })


if __name__ == '__main__':
    app.run(debug=True)
