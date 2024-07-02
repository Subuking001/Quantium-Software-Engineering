# download the app.py run in the terminal with python app.py
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

data = pd.read_csv('final_original_data.csv')
df = pd.DataFrame(data)


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Sales Analysis Dashboard", style={'text-align': 'center'}),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format='YYYY-MM-DD'
    ),

    html.Div([
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in df['product'].unique()],
            value=df['product'].unique()[0]
        ),
        html.Div(id='total-sales-display', style={'text-align': 'center', 'fontSize': 24, 'margin': '20px 0'})
    ]),

    dcc.Graph(id='individual-product-sales-bar-chart'),
    dcc.Graph(id='total-sales-bar-chart'),
    dcc.Graph(id='sales-over-time-line-chart')
])


@app.callback(
    [Output('individual-product-sales-bar-chart', 'figure'),
     Output('total-sales-display', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('product-dropdown', 'value')]
)
def update_individual_product_sales_bar_chart(start_date, end_date, selected_product):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date) & (df['product'] == selected_product)
    filtered_df = df[mask]

    total_sales_before = filtered_df[filtered_df['date'] < '2021-01-15']['sales'].sum()
    total_sales_after = filtered_df[filtered_df['date'] >= '2021-01-15']['sales'].sum()

    bar_data = pd.DataFrame({
        'Period': ['Before Jan 15, 2021', 'After Jan 15, 2021'],
        'Total Sales': [total_sales_before, total_sales_after]
    })

    fig = px.bar(bar_data, x='Period', y='Total Sales', title=f'Total Sales Before and After Price Increase for {selected_product}')
    fig.update_layout(xaxis_title='', yaxis_title='Total Sales')

    total_sales_text = f'Total Sales for {selected_product}: {total_sales_before + total_sales_after:.2f}'
    return fig, total_sales_text

# Callback to update total sales bar chart for all products
@app.callback(
    Output('total-sales-bar-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_total_sales_bar_chart(start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df[mask]

    total_sales_before = filtered_df[filtered_df['date'] < '2021-01-15'].groupby('product')['sales'].sum().reset_index()
    total_sales_after = filtered_df[filtered_df['date'] >= '2021-01-15'].groupby('product')['sales'].sum().reset_index()

    total_sales_before['Period'] = 'Before Jan 15, 2021'
    total_sales_after['Period'] = 'After Jan 15, 2021'

    total_sales = pd.concat([total_sales_before, total_sales_after])

    fig = px.bar(total_sales, x='product', y='sales', color='Period', barmode='group', title='Total Sales for All Products Before and After Price Increase')
    fig.update_layout(xaxis_title='Product', yaxis_title='Total Sales')
    return fig


@app.callback(
    Output('sales-over-time-line-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_line_chart(start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df[mask]

    fig = px.line(filtered_df, x='date', y='sales', color='product', title='Sales Over Time')
    fig.add_vline(x='2021-01-15', line_width=3, line_dash="dash", line_color="red")
    fig.update_layout(xaxis_title='Date', yaxis_title='Sales')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
