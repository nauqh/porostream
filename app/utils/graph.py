import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots


import plotly.graph_objects as go


def create_bar_chart(names, values, max_index, title, color_highlight):
    fig = go.Figure(data=go.Bar(
        x=names, y=values,
        text=values, textposition='outside', texttemplate='%{text:,.2s}',
        marker=dict(color=[color_highlight if i ==
                    max_index else '#ffc300' for i in names]),
        hovertemplate=f'{title}: %{{y:.2s}}', name=''))

    fig.update_layout(
        title=title, title_font_size=20,
        autosize=True,
        hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
        height=500)

    fig.update_yaxes(showgrid=False, title=None)
    fig.update_xaxes(title=None)

    return fig


def graph_dmg(data: dict):
    names, damages = list(data.keys()), list(data.values())
    max_dmg_index = max(data, key=data.get)
    return create_bar_chart(names, damages, max_dmg_index, 'Damage on Champions', '#1e96fc')


def graph_vision(data: dict):
    names, vision = list(data.keys()), list(data.values())
    max_vis_index = max(data, key=data.get)
    return create_bar_chart(names, vision, max_vis_index, 'Vision Score', '#fc7a57')


def graph_dmgproportion(names, trues, physicals, magics):
    fig = go.Figure()

    damage_types = ['True Damage', 'Physical Damage', 'Magic Damage']
    colors = ['#ff9500', '#ffc300', '#ffdd00']

    for damage_type, color in zip(damage_types, colors):
        fig.add_trace(go.Bar(
            y=names,
            x=trues if damage_type == 'True Damage' else (
                physicals if damage_type == 'Physical Damage' else magics),
            name=damage_type,
            orientation='h',
            marker=dict(color=color),
            hovertemplate='%{x:,.0f}'
        ))

    fig.update_layout(title='Damage Proportion', barmode='stack', title_font_size=20,
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
            hoverinfo='none'
        ))

        # Add annotation for win rate on top of each bar
        fig.add_annotation(
            x=win_rate + 3,  # Adjust this value for proper positioning
            y=f'{bar_color} side',
            text=f'{win_rate:.0f}%',
            showarrow=False,
            font=dict(color='white', size=15),
            align='left'
        )

    fig.update_layout(
        title='Winrate by side', title_font_size=18,
        margin=dict(t=30, l=0, r=0, b=30),
        showlegend=False,
        hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
        xaxis=dict(title='Winrate (%)'),
        height=200
    )

    return fig
# =======================================


def convert_timestamp_to_date(timestamp):
    date_object = datetime.utcfromtimestamp(timestamp)
    formatted_date = date_object.strftime('%b %d %H:%M')
    return formatted_date


def graph_personal(matchdf, playerdf):
    # Reverse the order of rows
    matchdf = matchdf.iloc[::-1].reset_index(drop=True)
    playerdf = playerdf.iloc[::-1].reset_index(drop=True)

    matchdf['CSperMin'] = (playerdf['totalMinionsKilled'] + playerdf['neutralMinionsKilled']) / \
        (matchdf['gameDuration'] / 60)
    matchdf['VisionperMin'] = playerdf['visionScore'] / \
        (matchdf['gameDuration'] / 60)
    matchdf['GoldperMin'] = playerdf['goldEarned'] / \
        (matchdf['gameDuration'] / 60)

    matchdf['gameCreation'] = matchdf['gameCreation'] / 1000
    matchdf['gameCreation'] = matchdf['gameCreation'].apply(
        convert_timestamp_to_date)

    # Calculate the difference between CSperMin and GoldperMin
    matchdf['CS_Gold_Difference'] = abs(
        matchdf['CSperMin'] - matchdf['GoldperMin'])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    metrics = ['VisionperMin', 'CSperMin', 'GoldperMin']

    for metric in metrics:
        trace = go.Scatter(
            x=matchdf['gameCreation'],
            y=round(matchdf[metric], 2),
            mode='lines+markers',
            name=metric,
            hovertemplate='%{y:.1f}'
        )

        # Assign the trace to the appropriate y-axis based on the metric
        if metric == 'GoldperMin':
            fig.add_trace(trace, secondary_y=True)
        else:
            fig.add_trace(trace)

    fig.update_layout(title="Laning statistics", title_font_size=25,
                      height=500,
                      legend=dict(orientation="h", yanchor="top",
                                  xanchor="center", x=0.5, y=1.1),
                      hovermode='x unified')

    fig.update_yaxes(title=None, showgrid=False)
    fig.update_yaxes(secondary_y=False,
                     range=[0, 10], showgrid=False)
    fig.update_xaxes(title=None, showticklabels=False)

    return fig


def graph_dmgpersonal(matchdf, playerdf):
    matchdf = matchdf.iloc[::-1].reset_index(drop=True)
    playerdf = playerdf.iloc[::-1].reset_index(drop=True)
    matchdf['DmgperMin'] = playerdf['totalDamageDealtToChampions'] / \
        (matchdf['gameDuration'] / 60)
    matchdf['CSperMin'] = (playerdf['totalMinionsKilled'] +
                           playerdf['neutralMinionsKilled']) / (matchdf['gameDuration'] / 60)
    matchdf['GoldperMin'] = playerdf['goldEarned'] / \
        (matchdf['gameDuration'] / 60)

    matchdf['gameCreation'] = matchdf['gameCreation'] / 1000
    matchdf['gameCreation'] = matchdf['gameCreation'].apply(
        convert_timestamp_to_date)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=matchdf['gameCreation'], y=matchdf['CSperMin'],
                             name="CSperMin", hovertemplate='%{y:.1f}'), secondary_y=True)

    fig.add_trace(go.Scatter(x=matchdf['gameCreation'], y=matchdf['DmgperMin'],
                             name="DamageperMin", hovertemplate='%{y:,.2f}<br>Champion: %{customdata}',
                             customdata=playerdf['championName']))

    fig.add_trace(go.Bar(x=matchdf['gameCreation'], y=matchdf['GoldperMin'],
                         name='GoldperMin', hovertemplate='%{y:.1f}',
                         text=matchdf['GoldperMin'], textposition='outside', texttemplate='%{text:.2s}',
                         marker=dict(color="#ffc300")))

    fig.update_layout(title="Gold by Damage and CS", title_font_size=25, height=600,
                      legend=dict(orientation="h", yanchor="top",
                                  xanchor="center", x=0.5, y=1.1),
                      hovermode='x unified')

    fig.update_yaxes(title=None, showgrid=False)
    fig.update_yaxes(secondary_y=True, range=[0, 10], showgrid=False)
    fig.update_xaxes(title=None, showticklabels=False)

    return fig


def graph_role_dist(df):
    df['role'] = df['role'].replace(
        {'NONE': 'JUNGLE', 'SOLO': 'TOP', 'CARRY': 'ADC'})
    role_counts = df['role'].value_counts()

    role = role_counts.idxmax()

    colors = ['#ffdd00', '#ffc300', '#ff9500']

    labels = role_counts.index.astype(str).str.capitalize()

    fig = go.Figure(data=[go.Pie(labels=labels, values=role_counts.values, hole=0.4, sort=False,
                                 direction='clockwise', pull=[0.1]*len(role_counts.index))])

    fig.update_traces(name='', textinfo='none',
                      hovertemplate='Role: %{label}<br>Percentage: %{percent}<extra></extra>',
                      marker=dict(colors=colors, line=dict(color='#000', width=1)))

    fig.update_layout(
        title='Roles distribution', title_font_size=18,
        margin=dict(t=40, l=0, r=0, b=0),
        legend=dict(
            x=0,
            y=1
        ), height=350)
    return fig, role.capitalize()
