import pandas as pd
import glob
import os
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# 🔹 Load and clean data
folder_path = './data'
all_files = glob.glob(os.path.join(folder_path, 'daily_sales_data_*.csv'))
df_list = [pd.read_csv(file) for file in all_files]
data = pd.concat(df_list, ignore_index=True)

# Filter for Pink Morsels
pink_data = data[data['product'] == 'pink morsel'].copy()
pink_data['date'] = pd.to_datetime(pink_data['date'])
pink_data['price'] = pink_data['price'].replace('[\$,]', '', regex=True).astype(float)
pink_data['sales'] = pink_data['price'] * pink_data['quantity']

# Build Dash app
app = Dash(__name__)
app.title = 'Pink Morsel Sales Visualizer'

# Layout with radio items for region filter and graph
app.layout = html.Div([
    html.H1('Pink Morsel Sales Visualizer'),
    
    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'North', 'value': 'north'},
            {'label': 'East', 'value': 'east'},
            {'label': 'South', 'value': 'south'},
            {'label': 'West', 'value': 'west'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all',
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        inputStyle={"margin-right": "5px"}
    ),
    
    dcc.Graph(id='sales-line-chart')
])

# Callback to update the line chart based on selected region
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('region-filter', 'value')]
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = pink_data
    else:
        filtered_df = pink_data[pink_data['region'] == selected_region]
    
    # Group by date to sum sales
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    
    fig = px.line(daily_sales, x='date', y='sales', title=f'Daily Sales of Pink Morsels - {selected_region.capitalize()} Region')
    fig.update_layout(xaxis_title='Date', yaxis_title='Sales ($)')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
