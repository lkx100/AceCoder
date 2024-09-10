from django.shortcuts import render, redirect
import plotly.express as px
import pandas as pd
from dashboard.Codechef import CodechefTools
from dashboard.decorators import isfacultygraph

# Create your views here.
def graph_student(request, codechef_id):
    if not codechef_id:
        return redirect('/')
    codechef_scrapper = CodechefTools(codechef_id)
    if codechef_scrapper.account_exists():
        all_details = codechef_scrapper.pd_fetch()
    else:
        return redirect("/")
    
    print(all_details)
    
    # Ensure 'Rating' and 'Rank' columns are numeric
    all_details['Rating'] = pd.to_numeric(all_details['Rating'], errors='coerce')
    all_details['Rank'] = pd.to_numeric(all_details['Rank'], errors='coerce')
    
    # Drop rows with NaN values in 'Rating' and 'Rank' columns
    all_details.dropna(subset=['Rating', 'Rank'], inplace=True)
    
    # Rating graph - Line chart
    line_chart_graph = px.line(
        all_details, 
        x="Contest", 
        y="Rating", 
        title="RATINGS GRAPH",
        width=700,
        height=350, 
    )
    
    # Calculate mean rating
    mean_rating = all_details["Rating"].mean()
    
    # Add mean line to the line chart
    line_chart_graph.add_shape(
        type="line",
        x0=0,
        x1=1,
        y0=mean_rating,
        y1=mean_rating,
        xref="paper",
        yref="y",
        line=dict(color="red", width=2, dash="dash"),
    )
    
    # Update layout to make background transparent, responsive, and decrease grid opacity
    line_chart_graph.update_layout(
        title=dict(
            text=f"{codechef_id} Rating graph".upper(),
            font=dict(color="cyan", weight="bold")  # Title color
        ),
        xaxis=dict(
            title=dict(
                text="Contest",
                font=dict(color="white")  # X-axis label color
            ),
            tickfont=dict(color="white"),  # X-axis tick color
            gridcolor='rgba(255, 255, 255, 0.2)',  # X-axis grid color with decreased opacity
            gridwidth=1  # X-axis grid width
        ),
        yaxis=dict(
            title=dict(
                text="Rating",
                font=dict(color="white")  # Y-axis label color
            ),
            tickfont=dict(color="white"),  # Y-axis tick color
            gridcolor='rgba(255, 255, 255, 0.2)',  # Y-axis grid color with decreased opacity
            gridwidth=1  # Y-axis grid width
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        autosize=True,
    )
    
    # Update trace to set line color and add markers
    line_chart_graph.update_traces(
        line=dict(color="orange"),  # Line color
        mode='lines+markers',  # Add markers at every point
        marker=dict(color='red'),  # Marker color
        hoverinfo='text+name',  # Hover information
        hovertemplate='<b>%{text}</b><br><br>Contest: %{x}<br>Rating: %{y}<extra></extra>',
        text=[f"Contest: {contest}<br>Rating: {rating}" for contest, rating in zip(all_details['Contest'], all_details['Rating'])]  # Custom hover text
    )
    
    # Ensure the mode bar is visible
    line_chart = line_chart_graph.to_html(full_html=True, config={
        'responsive': True,
        'scrollZoom': True,
        'displaylogo': False  # Optionally remove the Plotly logo
    })
    
    # Ranking graph - Bar chart
    bar_chart_graph = px.bar(
        all_details, 
        x="Contest", 
        y="Rank", 
        title="RANKING GRAPH",
        width=700,
        height=350, 
    )
    
    # Calculate mean rank
    mean_rank = all_details["Rank"].mean()
    
    # Add mean line to the bar chart
    bar_chart_graph.add_shape(
        type="line",
        x0=0,
        x1=1,
        y0=mean_rank,
        y1=mean_rank,
        xref="paper",
        yref="y",
        line=dict(color="red", width=2, dash="dash"),
    )
    
    # Update layout to make background transparent, responsive, and decrease grid opacity
    bar_chart_graph.update_layout(
        title=dict(
            text=f"{codechef_id} Ranking graph".upper(),
            font=dict(color="cyan", weight="bold")  # Title color
        ),
        xaxis=dict(
            title=dict(
                text="Contest",
                font=dict(color="white")  # X-axis label color
            ),
            tickfont=dict(color="white"),  # X-axis tick color
            gridcolor='rgba(255, 255, 255, 0.2)',  # X-axis grid color with decreased opacity
            gridwidth=1  # X-axis grid width
        ),
        yaxis=dict(
            title=dict(
                text="Rank",
                font=dict(color="white")  # Y-axis label color
            ),
            tickfont=dict(color="white"),  # Y-axis tick color
            gridcolor='rgba(255, 255, 255, 0.2)',  # Y-axis grid color with decreased opacity
            gridwidth=1,  # Y-axis grid width
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        autosize=True,
    )
    
    # Update trace to set bar color and add hover information
    bar_chart_graph.update_traces(
        marker=dict(color="blue"),  # Bar color
        hoverinfo='text+name',  # Hover information
        hovertemplate='<b>%{text}</b><br><br>Contest: %{x}<br>Rank: %{y}<extra></extra>',
        text=[f"Contest: {contest}<br>Rank: {rank}" for contest, rank in zip(all_details['Contest'], all_details['Rank'])]  # Custom hover text
    )
    
    # Ensure the mode bar is visible
    bar_chart = bar_chart_graph.to_html(full_html=True, config={
        'responsive': True,
        'scrollZoom': True,
        'displaylogo': False  # Optionally remove the Plotly logo
    })
    
    graphs = {
        "line_chart": line_chart,
        "bar_chart": bar_chart
    }
    return render(request, 'graph_base.html', graphs)

@isfacultygraph
def graph_home(request):
    return render(request, "graph_faculty.html")