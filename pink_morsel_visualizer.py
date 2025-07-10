import pandas as pd
import glob
import os
from dash import Dash, html, dcc
import plotly.express as px

# 🔹 Load and clean data
folder_path = './data'
all_files = glob.glob(os.path.join(folder_path, 'daily_sales_data_*.csv'))
df_list = [pd.read_csv(file) for file in all_files]
data = pd.concat(df_list, ignore_index=True)
pink_data = data[data['product'] == 'pink morsel'].copy()
pink_data['date'] = pd.to_datetime(pink_data['date'])
pink_data['price'] = pink_data['price'].replace('[\$,]', '', regex=True).astype(float)
pink_data['sales'] = pink_data['price'] * pink_data['quantity']
daily_sales = pink_data.groupby('date')['sales'].sum().reset_index()

# 🔹 Build Dash app
app = Dash(__name__)
app.title = 'Pink Morsel Sales Visualizer'
fig = px.line(daily_sales, x='date', y='sales', title='Daily Sales of Pink Morsels')
fig.update_layout(xaxis_title='Date', yaxis_title='Sales ($)')
app.layout = html.Div([
    html.H1('Pink Morsel Sales Visualizer'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
