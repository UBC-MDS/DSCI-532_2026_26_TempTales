import plotly.graph_objects as go

def build_base_map(all_countries):
    empty_z = [None] * len(all_countries)

    fig = go.FigureWidget(data=go.Choropleth(
        locations=all_countries,
        locationmode='country names',
        z=empty_z,
        colorscale='RdBu_r',
        zmin=-3, zmax=3,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar=dict(
            title="Change (°C)",
            orientation="h",
            len=0.7,
            lenmode="fraction",
            thickness=12,
            x=0.5,
            xanchor="center",
            y=-0.08,
            yanchor="top",
        )
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="darkgray",
            showland=True,
            landcolor="#eaeaea",
            showocean=True,
            oceancolor="#dde5ed",
            showlakes=False,
            bgcolor="rgba(0,0,0,0)",
            projection=dict(type="natural earth"),
            fitbounds="locations",
        ),
        margin=dict(l=0, r=0, t=0, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        height=None,
        width=None,
    )

    return fig

def apply_country_highlight(fig, all_countries, selected_country):
    line_widths = []
    line_colors = []
    opacities = []

    for c in all_countries:
        if c == selected_country:
            line_widths.append(1.5)
            line_colors.append("white")
            opacities.append(1.0)
        else:
            line_widths.append(0.5)
            line_colors.append("gray")
            opacities.append(0.6)

    fig.data[0].marker.line.width = line_widths
    fig.data[0].marker.line.color = line_colors
    fig.data[0].marker.opacity = opacities
