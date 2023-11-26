import plotly.graph_objects as go


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
                                    color=['#0397AB' if i == max_dmg_index else '#C89B3C' for i in names]),
                                hoverinfo='none', name=''))

    # Update the layout for better visualization
    fig.update_layout(title='Average Damage on Champions',
                      autosize=True,
                      hoverlabel=dict(bgcolor='#010A13', font_color='#fff'),
                      height=500)

    fig.update_yaxes(showgrid=False, title=None)
    fig.update_xaxes(title=None)

    # Show the plot
    return fig


def graph_vision(data: dict):
    # Extract names and damages from the dictionary
    names = list(data.keys())
    vision = list(data.values())
    max_vis_index = max(data, key=data.get)

    # Create a bar chart
    fig = go.Figure(data=go.Bar(x=names, y=vision,
                                text=vision, textposition='outside', texttemplate='%{text:.2s}',
                                marker=dict(
                                    color=['#0397AB' if i == max_vis_index else '#C89B3C' for i in names]),
                                hoverinfo='none', name=''))

    # Update the layout for better visualization
    fig.update_layout(title='Average Vision Score',
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
            color='rgb(120, 90, 40)'
        ),
        hovertemplate='%{x}'
    ))
    fig.add_trace(go.Bar(
        y=names,
        x=physicals,
        name='Physical Damage',
        orientation='h',
        marker=dict(
            color='rgb(200, 155, 60)'
        ),
        hovertemplate='%{x}'
    ))
    fig.add_trace(go.Bar(
        y=names,
        x=magics,
        name='Magic Damage',
        orientation='h',
        marker=dict(
            color='rgb(200, 170, 110)'
        ),
        hovertemplate='%{x}'
    ))

    fig.update_layout(title='Damage Proportion', barmode='stack', height=500,
                      hoverlabel=dict(bgcolor='#000', font_color='#fff'))
    return fig
