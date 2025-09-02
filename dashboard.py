import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

from data_fetcher import DataFetcher
from technical_analysis import TechnicalAnalysis

# Initialize the Dash app with dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Bitcoin Price Analysis Dashboard"

# Initialize data fetcher
fetcher = DataFetcher()

# Global variables to store data
btc_data = None
market_data = None
correlations = None
technical_analysis = None

# Custom CSS for dark theme and Bitcoin branding
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #0a0a0a !important;
                color: #ffffff !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .dashboard-container {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .metric-card {
                background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
                border: 1px solid #333;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(255, 165, 0, 0.2);
            }
            .price-positive { color: #00ff88 !important; }
            .price-negative { color: #ff4757 !important; }
            .bitcoin-orange { color: #f7931a !important; }
            .chart-container {
                background: #1e1e1e;
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
                border: 1px solid #333;
            }
            .time-selector {
                background: #2d2d2d;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 10px;
                margin: 15px 0;
            }
            .header-title {
                background: linear-gradient(45deg, #f7931a, #ffd700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 2.5rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def fetch_and_process_data():
    """Fetch and process all data"""
    global btc_data, market_data, correlations, technical_analysis
    
    print("Fetching Bitcoin data...")
    btc_data = fetcher.fetch_bitcoin_data()
    
    if btc_data is not None:
        print("Fetching traditional market data...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        market_data = fetcher.fetch_traditional_markets(start_date, end_date)
        
        if market_data is not None:
            correlations = fetcher.calculate_correlations(btc_data, market_data)
        
        # Initialize technical analysis
        technical_analysis = TechnicalAnalysis(btc_data)
        print("Data processing complete!")
    else:
        print("Failed to fetch data")

# Fetch data on startup
fetch_and_process_data()

# App layout with modern dark theme
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Bitcoin Price Analysis Dashboard", className="header-title"),
        html.P("Real-time Bitcoin market analysis with advanced technical indicators", 
               style={'textAlign': 'center', 'color': '#888', 'marginBottom': '30px'})
    ]),
    
    # Time Range Selector
    html.Div([
        html.H5("Select Time Range", style={'color': '#f7931a', 'marginBottom': '15px'}),
        dbc.ButtonGroup([
            dbc.Button("1M", id="1m-btn", color="warning", outline=True, size="sm"),
            dbc.Button("3M", id="3m-btn", color="warning", outline=True, size="sm"),
            dbc.Button("6M", id="6m-btn", color="warning", outline=True, size="sm"),
            dbc.Button("1Y", id="1y-btn", color="warning", outline=True, size="sm"),
            dbc.Button("2Y", id="2y-btn", color="warning", outline=True, size="sm", active=True),
        ], className="time-selector")
    ], className="chart-container"),
    
    # Summary Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Current Price", className="card-title", style={'color': '#f7931a'}),
                    html.H2(id="current-price", className="bitcoin-orange"),
                    html.P(id="price-change", className="card-text"),
                    html.Small(id="price-timestamp", style={'color': '#888'})
                ])
            ], className="metric-card text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Market Trend", className="card-title", style={'color': '#f7931a'}),
                    html.H2(id="market-trend", className="text-primary"),
                    html.P(id="trend-details", className="card-text"),
                    html.Small(id="trend-strength", style={'color': '#888'})
                ])
            ], className="metric-card text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Volatility", className="card-title", style={'color': '#f7931a'}),
                    html.H2(id="volatility-status", className="text-warning"),
                    html.P(id="volatility-details", className="card-text"),
                    html.Small(id="volatility-trend", style={'color': '#888'})
                ])
            ], className="metric-card text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Volume", className="card-title", style={'color': '#f7931a'}),
                    html.H2(id="volume-pattern", className="text-info"),
                    html.P(id="volume-details", className="card-text"),
                    html.Small(id="volume-trend", style={'color': '#888'})
                ])
            ], className="metric-card text-center")
        ], width=3)
    ], className="mb-4"),
    
    # Main Price Chart with Technical Indicators
    html.Div([
        html.H5("Bitcoin Price Chart with Technical Indicators", 
                style={'color': '#f7931a', 'marginBottom': '20px'}),
        dcc.Graph(id="price-chart", style={'height': '600px'})
    ], className="chart-container"),
    
    # Secondary Analysis Charts
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5("Volume Analysis", style={'color': '#f7931a', 'marginBottom': '20px'}),
                dcc.Graph(id="volume-chart", style={'height': '400px'})
            ], className="chart-container")
        ], width=6),
        dbc.Col([
            html.Div([
                html.H5("Volatility Analysis", style={'color': '#f7931a', 'marginBottom': '20px'}),
                dcc.Graph(id="volatility-chart", style={'height': '400px'})
            ], className="chart-container")
        ], width=6)
    ], className="mb-4"),
    
    # Technical Indicators and Market Correlations
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5("Technical Indicators", style={'color': '#f7931a', 'marginBottom': '20px'}),
                dcc.Graph(id="indicators-chart", style={'height': '500px'})
            ], className="chart-container")
        ], width=6),
        dbc.Col([
            html.Div([
                html.H5("Market Correlations", style={'color': '#f7931a', 'marginBottom': '20px'}),
                dcc.Graph(id="correlation-chart", style={'height': '500px'})
            ], className="chart-container")
        ], width=6)
    ], className="mb-4"),
    
    # Market Summary and Statistics
    html.Div([
        html.H5("Market Summary & Statistics", style={'color': '#f7931a', 'marginBottom': '20px'}),
        dbc.Row([
            dbc.Col([
                html.Div(id="period-stats", className="metric-card p-3")
            ], width=6),
            dbc.Col([
                html.Div(id="performance-metrics", className="metric-card p-3")
            ], width=6)
        ])
    ], className="chart-container"),
    
    # Controls and Data Management
    html.Div([
        html.H5("Data Management", style={'color': '#f7931a', 'marginBottom': '20px'}),
        dbc.Row([
            dbc.Col([
                dbc.Button("🔄 Refresh Data", id="refresh-btn", color="warning", size="lg", className="me-3"),
                dbc.Button("📊 Download Data", id="download-btn", color="success", size="lg", className="me-3"),
                dbc.Button("📈 Export Charts", id="export-btn", color="info", size="lg")
            ], className="text-center")
        ]),
        html.Div([
            html.Small(id="last-updated", style={'color': '#888'})
        ], className="text-center mt-3")
    ], className="chart-container"),
    
    # Hidden div for storing data
    html.Div(id="data-store", style={"display": "none"}),
    
    # Download component
    dcc.Download(id="download-dataframe-csv"),
    
    # Store for time range selection
    dcc.Store(id="time-range-store", data="2Y")
    
], className="dashboard-container")

# Callback to handle time range selection
@app.callback(
    Output("time-range-store", "data"),
    [Input("1m-btn", "n_clicks"),
     Input("3m-btn", "n_clicks"),
     Input("6m-btn", "n_clicks"),
     Input("1y-btn", "n_clicks"),
     Input("2y-btn", "n_clicks")]
)
def update_time_range(btn1, btn2, btn3, btn4, btn5):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "2Y"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    time_mapping = {
        "1m-btn": "1M",
        "3m-btn": "3M", 
        "6m-btn": "6M",
        "1y-btn": "1Y",
        "2y-btn": "2Y"
    }
    
    return time_mapping.get(button_id, "2Y")

# Callback to update summary cards
@app.callback(
    [Output("current-price", "children"),
     Output("price-change", "children"),
     Output("price-timestamp", "children"),
     Output("market-trend", "children"),
     Output("trend-details", "children"),
     Output("trend-strength", "children"),
     Output("volatility-status", "children"),
     Output("volatility-details", "children"),
     Output("volatility-trend", "children"),
     Output("volume-pattern", "children"),
     Output("volume-details", "children"),
     Output("volume-trend", "children")],
    [Input("refresh-btn", "n_clicks"),
     Input("time-range-store", "data")]
)
def update_summary_cards(n_clicks, time_range):
    if btc_data is None or technical_analysis is None:
        return ["N/A"] * 12
    
    try:
        # Filter data based on time range
        filtered_data = filter_data_by_time_range(btc_data, time_range)
        
        if filtered_data.empty:
            return ["N/A"] * 12
        
        # Get current price and changes
        current_price = filtered_data['price'].iloc[-1]
        price_change_1d = filtered_data['returns'].iloc[-1] * 100 if len(filtered_data) > 1 else 0
        
        # Calculate period changes
        if len(filtered_data) > 1:
            price_change_period = ((current_price / filtered_data['price'].iloc[0]) - 1) * 100
        else:
            price_change_period = 0
        
        # Format price change with color
        if price_change_1d >= 0:
            price_change_text = f"+{price_change_1d:.2f}% (1D) • +{price_change_period:.2f}% ({time_range})"
        else:
            price_change_text = f"{price_change_1d:.2f}% (1D) • {price_change_period:.2f}% ({time_range})"
        
        # Get trend analysis
        trend_analysis = technical_analysis.get_trend_analysis()
        if isinstance(trend_analysis, dict):
            trend = trend_analysis.get('trend', 'N/A')
            trend_details = f"Above 20MA: {'Yes' if trend_analysis.get('above_20') else 'No'}"
            trend_strength = f"Trend Strength: {get_trend_strength(trend_analysis)}"
        else:
            trend = 'N/A'
            trend_details = 'Insufficient data'
            trend_strength = 'Trend analysis unavailable'
        
        # Get volatility analysis
        vol_analysis = technical_analysis.get_volatility_analysis()
        if isinstance(vol_analysis, dict):
            vol_status = vol_analysis.get('status', 'N/A')
            vol_details = f"Current: {vol_analysis.get('current_volatility', 0)*100:.2f}%"
            vol_trend = f"Ratio: {vol_analysis.get('volatility_ratio', 0):.2f}x average"
        else:
            vol_status = 'N/A'
            vol_details = 'Insufficient data'
            vol_trend = 'Volatility analysis unavailable'
        
        # Get volume analysis
        vol_pattern_analysis = technical_analysis.get_volume_analysis()
        if isinstance(vol_pattern_analysis, dict):
            vol_pattern = vol_pattern_analysis.get('pattern', 'N/A')
            vol_details_text = f"Current: {vol_pattern_analysis.get('current_volume', 0):,.0f}"
            vol_trend_text = f"Ratio: {vol_pattern_analysis.get('volume_ratio', 0):.2f}x average"
        else:
            vol_pattern = 'N/A'
            vol_details_text = 'Insufficient data'
            vol_trend_text = 'Volume analysis unavailable'
        
        # Timestamp
        timestamp = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return [
            f"${current_price:,.2f}",
            price_change_text,
            timestamp,
            trend,
            trend_details,
            trend_strength,
            vol_status,
            vol_details,
            vol_trend,
            vol_pattern,
            vol_details_text,
            vol_trend_text
        ]
    except Exception as e:
        print(f"Error updating summary cards: {e}")
        return ["Error"] * 12

def filter_data_by_time_range(data, time_range):
    """Filter data based on selected time range"""
    if data is None or data.empty:
        return pd.DataFrame()
    
    end_date = data.index[-1]
    
    if time_range == "1M":
        start_date = end_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = end_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = end_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = end_date - timedelta(days=365)
    else:  # 2Y
        start_date = end_date - timedelta(days=730)
    
    return data[data.index >= start_date]

def get_trend_strength(trend_analysis):
    """Calculate trend strength based on moving average positions"""
    if not isinstance(trend_analysis, dict):
        return "Unknown"
    
    above_20 = trend_analysis.get('above_20', False)
    above_50 = trend_analysis.get('above_50', False)
    above_200 = trend_analysis.get('above_200', False)
    
    if above_20 and above_50 and above_200:
        return "Strong Bullish"
    elif above_20 and above_50:
        return "Bullish"
    elif above_20:
        return "Weak Bullish"
    elif not above_20 and not above_50 and not above_200:
        return "Strong Bearish"
    elif not above_20 and not above_50:
        return "Bearish"
    else:
        return "Mixed"

# Callback to update price chart
@app.callback(
    Output("price-chart", "figure"),
    [Input("refresh-btn", "n_clicks"),
     Input("time-range-store", "data")]
)
def update_price_chart(n_clicks, time_range):
    if btc_data is None or technical_analysis is None:
        return go.Figure()
    
    try:
        # Filter data based on time range
        filtered_data = filter_data_by_time_range(btc_data, time_range)
        
        if filtered_data.empty:
            return go.Figure()
        
        # Create subplot for price and volume
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'Bitcoin Price ({time_range})', 'Volume'),
            row_heights=[0.7, 0.3]
        )
        
        # Price line with Bitcoin orange color
        fig.add_trace(
            go.Scatter(
                x=filtered_data.index,
                y=filtered_data['price'],
                mode='lines',
                name='BTC Price',
                line=dict(color='#f7931a', width=3),
                hovertemplate='<div style="background-color: white; color: black; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">' +
                            '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                            '<b>💰 Price</b>: $%{y:,.2f}<br>' +
                            '<b>📊 Change</b>: %{customdata[0]:+.2f}%<br>' +
                            '<b>📈 Volume</b>: %{customdata[1]:,.0f}<extra></extra></div>',
                customdata=np.column_stack((
                    filtered_data['returns'] * 100,
                    filtered_data['volume']
                ))
            ),
            row=1, col=1
        )
        
        # Moving averages
        if 'SMA_20' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['SMA_20'],
                    mode='lines',
                    name='SMA 20',
                    line=dict(color='#00d4ff', width=2),
                    hovertemplate='<div style="background-color: white; color: black; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">' +
                                '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                                '<b>📊 SMA 20</b>: $%{y:,.2f}<extra></extra></div>'
                ),
                row=1, col=1
            )
        
        if 'SMA_50' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['SMA_50'],
                    mode='lines',
                    name='SMA 50',
                    line=dict(color='#ff6b35', width=2),
                    hovertemplate='<div style="background-color: white; color: black; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">' +
                                '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                                '<b>📊 SMA 50</b>: $%{y:,.2f}<extra></extra></div>'
                ),
                row=1, col=1
            )
        
        if 'SMA_200' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['SMA_200'],
                    mode='lines',
                    name='SMA 200',
                    line=dict(color='#ff4757', width=2),
                    hovertemplate='<div style="background-color: white; color: black; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">' +
                                '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                                '<b>📊 SMA 200</b>: $%{y:,.2f}<extra></extra></div>'
                ),
                row=1, col=1
            )
        
        # Bollinger Bands
        if 'BB_upper' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['BB_upper'],
                    mode='lines',
                    name='BB Upper',
                    line=dict(color='rgba(255,255,255,0.5)', width=1, dash='dash'),
                    fill=None,
                    hovertemplate='<div style="background-color: white; color: black; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">' +
                                '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                                '<b>📊 BB Upper</b>: $%{y:,.2f}<extra></extra></div>'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['BB_lower'],
                    mode='lines',
                    name='BB Lower',
                    line=dict(color='rgba(255,255,255,0.5)', width=1, dash='dash'),
                    fill='tonexty',
                    fillcolor='rgba(255,255,255,0.1)',
                    hovertemplate='<div style="background-color: white; color: black; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">' +
                                '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                                '<b>📊 BB Lower</b>: $%{y:,.2f}<extra></extra></div>'
                ),
                row=1, col=1
            )
        
        # Volume bars with color coding
        colors = ['#00ff88' if filtered_data['returns'].iloc[i] >= 0 else '#ff4757' 
                 for i in range(len(filtered_data))]
        
        fig.add_trace(
            go.Bar(
                x=filtered_data.index,
                y=filtered_data['volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7,
                hovertemplate='<div style="background-color: white; color: black; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">' +
                            '<b>📅 Date</b>: %{x|%B %d, %Y}<br>' +
                            '<b>📊 Volume</b>: %{y:,.0f}<br>' +
                            '<b>💰 Price</b>: $%{customdata:,.2f}<extra></extra></div>',
                customdata=filtered_data['price']
            ),
            row=2, col=1
        )
        
        # Update layout with dark theme
        fig.update_layout(
            title=f"Bitcoin Price Analysis - {time_range}",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=600,
            showlegend=True,
            hovermode='closest',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Update axes styling
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.3)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.3)')
        
        return fig
        
    except Exception as e:
        print(f"Error updating price chart: {e}")
        return go.Figure()

# Callback to update volume chart
@app.callback(
    Output("volume-chart", "figure"),
    [Input("refresh-btn", "n_clicks"),
     Input("time-range-store", "data")]
)
def update_volume_chart(n_clicks, time_range):
    if btc_data is None:
        return go.Figure()
    
    try:
        filtered_data = filter_data_by_time_range(btc_data, time_range)
        
        if filtered_data.empty:
            return go.Figure()

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('Volume Analysis', 'Volume Rate of Change'),
            row_heights=[0.6, 0.4]
        )
        
        # Volume with moving average
        fig.add_trace(
            go.Scatter(
                x=filtered_data.index,
                y=filtered_data['volume'],
                mode='lines',
                name='Volume',
                line=dict(color='#1f77b4', width=2)
            ),
            row=1, col=1
        )
        
        if 'volume_SMA_20' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['volume_SMA_20'],
                    mode='lines',
                    name='Volume SMA 20',
                    line=dict(color='orange', width=1)
                ),
                row=1, col=1
            )
        
        # Volume Rate of Change
        if 'volume_ROC' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['volume_ROC'] * 100,
                    mode='lines',
                    name='Volume ROC (%)',
                    line=dict(color='green', width=2)
                ),
                row=2, col=1
            )
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
        
        fig.update_layout(
            title="Volume Analysis",
            xaxis_title="Date",
            height=400,
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error updating volume chart: {e}")
        return go.Figure()

# Callback to update indicators chart
@app.callback(
    Output("indicators-chart", "figure"),
    [Input("refresh-btn", "n_clicks"),
     Input("time-range-store", "data")]
)
def update_indicators_chart(n_clicks, time_range):
    if btc_data is None:
        return go.Figure()
    
    try:
        filtered_data = filter_data_by_time_range(btc_data, time_range)
        
        if filtered_data.empty:
            return go.Figure()

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('RSI', 'MACD', 'Stochastic'),
            row_heights=[0.33, 0.33, 0.33]
        )
        
        # RSI
        if 'RSI' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=2)
                ),
                row=1, col=1
            )
            
            # Add overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=1, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=1, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="gray", row=1, col=1)
        
        # MACD
        if 'MACD' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['MACD'],
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue', width=2)
                ),
                row=2, col=1
            )
            
            if 'MACD_signal' in filtered_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=filtered_data.index,
                        y=filtered_data['MACD_signal'],
                        mode='lines',
                        name='MACD Signal',
                        line=dict(color='red', width=1)
                    ),
                    row=2, col=1
                )
            
            if 'MACD_histogram' in filtered_data.columns:
                colors = ['green' if val >= 0 else 'red' for val in filtered_data['MACD_histogram']]
                fig.add_trace(
                    go.Bar(
                        x=filtered_data.index,
                        y=filtered_data['MACD_histogram'],
                        name='MACD Histogram',
                        marker_color=colors
                    ),
                    row=2, col=1
                )
        
        # Stochastic
        if 'stoch_k' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['stoch_k'],
                    mode='lines',
                    name='%K',
                    line=dict(color='blue', width=2)
                ),
                row=3, col=1
            )
            
            if 'stoch_d' in filtered_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=filtered_data.index,
                        y=filtered_data['stoch_d'],
                        mode='lines',
                        name='%D',
                        line=dict(color='red', width=1)
                    ),
                    row=3, col=1
                )
            
            # Add overbought/oversold lines
            fig.add_hline(y=80, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=20, line_dash="dash", line_color="green", row=3, col=1)
        
        fig.update_layout(
            title="Technical Indicators",
            xaxis_title="Date",
            height=500,
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error updating indicators chart: {e}")
        return go.Figure()

# Callback to update correlation chart
@app.callback(
    Output("correlation-chart", "figure"),
    [Input("refresh-btn", "n_clicks"),
     Input("time-range-store", "data")]
)
def update_correlation_chart(n_clicks, time_range):
    if correlations is None:
        return go.Figure()
    
    try:
        # Create correlation bar chart
        markets = list(correlations.keys())
        corr_values = list(correlations.values())
        
        # Color coding based on correlation strength
        colors = []
        for corr in corr_values:
            if abs(corr) > 0.7:
                colors.append('red' if corr < 0 else 'green')
            elif abs(corr) > 0.5:
                colors.append('orange' if corr < 0 else 'lightgreen')
            else:
                colors.append('gray')
        
        fig = go.Figure(data=[
            go.Bar(
                x=markets,
                y=corr_values,
                marker_color=colors,
                text=[f'{val:.3f}' for val in corr_values],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Bitcoin Correlation with Traditional Markets",
            xaxis_title="Market",
            yaxis_title="Correlation Coefficient",
            yaxis=dict(range=[-1, 1]),
            height=500,
            showlegend=False,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="white")
        
        return fig
        
    except Exception as e:
        print(f"Error updating correlation chart: {e}")
        return go.Figure()

# Callback to update volatility chart
@app.callback(
    Output("volatility-chart", "figure"),
    [Input("refresh-btn", "n_clicks"),
     Input("time-range-store", "data")]
)
def update_volatility_chart(n_clicks, time_range):
    if btc_data is None:
        return go.Figure()
    
    try:
        filtered_data = filter_data_by_time_range(btc_data, time_range)
        
        if filtered_data.empty:
            return go.Figure()

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('Price Volatility', 'Volatility Ratio'),
            row_heights=[0.6, 0.4]
        )
        
        # Volatility
        if 'volatility' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['volatility'] * 100,
                    mode='lines',
                    name='Volatility (%)',
                    line=dict(color='red', width=2)
                ),
                row=1, col=1
            )
        
        # Volatility ratio
        if 'volatility_ratio' in filtered_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['volatility_ratio'],
                    mode='lines',
                    name='Volatility Ratio',
                    line=dict(color='purple', width=2)
                ),
                row=2, col=1
            )
            
            # Add reference lines
            fig.add_hline(y=1, line_dash="dash", line_color="gray", row=2, col=1)
            fig.add_hline(y=1.5, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=0.5, line_dash="dash", line_color="green", row=2, col=1)
        
        fig.update_layout(
            title="Volatility Analysis",
            xaxis_title="Date",
            height=400,
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error updating volatility chart: {e}")
        return go.Figure()

# Callback to refresh data
@app.callback(
    Output("last-updated", "children"),
    [Input("refresh-btn", "n_clicks")]
)
def refresh_data(n_clicks):
    if n_clicks:
        fetch_and_process_data()
        return f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Callback to download data
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("download-btn", "n_clicks")],
    prevent_initial_call=True
)
def download_csv(n_clicks):
    if btc_data is None:
        return None
    
    try:
        # Prepare data for download
        download_data = btc_data.reset_index()
        download_data['date'] = download_data['date'].dt.strftime('%Y-%m-%d')
        
        return dcc.send_data_frame(
            download_data.to_csv,
            "bitcoin_analysis_data.csv",
            index=False
        )
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

if __name__ == '__main__':
    print("🚀 Starting Enhanced Bitcoin Price Analysis Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Features: Dark theme, time range selector, real-time data, enhanced visualizations")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
