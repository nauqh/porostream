import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots


def graph_dmg(data: dict):
    # Extract names and damages from the dictionary
    names = list(data.keys())
    damages = list(data.values())
    # Find the index of the maximum damage
    max_dmg_index = max(data, key=data.get)

    # Create a bar chart
    fig = go.Figure(data=go.Bar(x=names, y=damages,
                                text=damages, textposition='outside', texttemplate='%{text:,.0f}',
                                marker=dict(
                                    color=['#1e96fc' if i == max_dmg_index else '#ffc300' for i in names]),
                                hoverinfo='none', name=''))

    # Update the layout for better visualization
    fig.update_layout(title='Avg Damage on Champions',
                      autosize=True,
                      hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
                      height=500)

    fig.update_yaxes(showgrid=False, title=None)
    fig.update_xaxes(title=None)

    # Show the plot
    return fig


def graph_vision(data: dict):
    # Extract names and vision from the dictionary
    names = list(data.keys())
    vision = list(data.values())
    max_vis_index = max(data, key=data.get)

    # Create a bar chart
    fig = go.Figure(data=go.Bar(x=names, y=vision,
                                text=vision, textposition='outside', texttemplate='%{text:.2s}',
                                marker=dict(
                                    color=['#fc7a57' if i == max_vis_index else '#ffc300' for i in names]),
                                hovertemplate='Vision score: %{y}', name=''))

    # Update the layout for better visualization
    fig.update_layout(title='Avg Vision Score',
                      autosize=True,
                      yaxis=dict(title='Vision score'),
                      hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
                      height=500)

    fig.update_yaxes(showgrid=False, title=None)
    fig.update_xaxes(title=None)
    # Show the plot
    return fig


def graph_dmgproportion(names, trues, physicals, magics):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=names,
        x=trues,
        name='True Damage',
        orientation='h',
        marker=dict(
            color='#ff9500'
        ),
        hovertemplate='%{x}'
    ))
    fig.add_trace(go.Bar(
        y=names,
        x=physicals,
        name='Physical Damage',
        orientation='h',
        marker=dict(
            color='#ffc300'
        ),
        hovertemplate='%{x}'
    ))
    fig.add_trace(go.Bar(
        y=names,
        x=magics,
        name='Magic Damage',
        orientation='h',
        marker=dict(
            color='#ffdd00'
        ),
        hovertemplate='%{x}'
    ))

    fig.update_layout(title='Damage Proportion', barmode='stack',
                      height=500,
                      hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
                      legend=dict(orientation="h", yanchor="top", xanchor="center", x=0.5, y=1.1))
    return fig


def graph_winrate(df):
    data = df['teamId'].value_counts().to_dict()
    total_matches = len(df)

    fig = go.Figure()

    for team_id, count in data.items():
        win_rate = (count / total_matches) * 100

        # Encode color based on teamId
        bar_color = 'Red' if team_id == 100 else 'Blue'

        fig.add_trace(go.Bar(
            name='',
            y=[f'{bar_color} side'],
            x=[win_rate],
            orientation='h',
            hovertemplate='Win Rate: %{x}%'
        ))

    fig.update_layout(
        title='Blue / Red Winrate',
        showlegend=False,
        hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
        xaxis=dict(title='Win Rate (%)'),
        height=300
    )

    return fig

# =======================================


def convert_timestamp_to_date(timestamp):
    date_object = datetime.utcfromtimestamp(timestamp)
    formatted_date = date_object.strftime('%b %d %H:%M')
    return formatted_date


def graph_personal(matchdf, playerdf):
    matchdf['CSperMin'] = playerdf['totalMinionsKilled'] / \
        (matchdf['gameDuration'] / 60)
    matchdf['VisionperMin'] = playerdf['visionScore'] / \
        (matchdf['gameDuration'] / 60)
    matchdf['GoldperMin'] = playerdf['goldEarned'] / \
        (matchdf['gameDuration'] / 60)

    matchdf['gameCreation'] = matchdf['gameCreation'] / 1000
    matchdf['gameCreation'] = matchdf['gameCreation'].apply(
        convert_timestamp_to_date)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    metrics = ['VisionperMin', 'CSperMin', 'GoldperMin']

    for metric in metrics:
        trace = go.Scatter(
            x=matchdf['gameCreation'],
            y=round(matchdf[metric], 2),
            mode='lines+markers',
            name=metric,
            hovertemplate='%{y}'
        )

        # Assign the trace to the appropriate y-axis based on the metric
        if metric == 'GoldperMin':
            fig.add_trace(trace, secondary_y=True)
        else:
            fig.add_trace(trace)

    fig.update_layout(title='',
                      yaxis_title='VisionperMin and CSperMin',
                      yaxis2_title='GoldperMin',
                      xaxis_title='Game Creation Time',
                      legend=dict(orientation="h", yanchor="top", xanchor="center", x=0.5, y=1.1))

    fig.update_yaxes(title=None, secondary_y=False)
    fig.update_yaxes(title=None, secondary_y=True)

    fig.update_xaxes(title=None)

    return fig
