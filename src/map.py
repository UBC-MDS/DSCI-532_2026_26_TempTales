import plotly.graph_objects as go

def build_base_map(all_countries):
    empty_z = [None] * len(all_countries)

    fig = go.FigureWidget(data=go.Choropleth(
        locations=all_countries,
        locationmode='country names',
        z=empty_z,
        colorscale='RdBu_r',
        zmin=-20, zmax=30,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title="Temp (°C)"
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            #projection_type='robinson',
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="lightblue"
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True,
        height=None,
        width=None
    )

    return fig

def apply_country_highlight(fig, all_countries, selected_country):
    line_widths = []
    line_colors = []
    opacities = []

    for c in all_countries:
        if c == selected_country:
            line_widths.append(3)
            line_colors.append("black")
            opacities.append(1.0)
        else:
            line_widths.append(0.5)
            line_colors.append("gray")
            opacities.append(0.6)

    fig.data[0].marker.line.width = line_widths
    fig.data[0].marker.line.color = line_colors
    fig.data[0].marker.opacity = opacities
