from django.shortcuts import render, redirect
import plotly.express as px
import pandas as pd
from dashboard.Codechef import CodechefTools
from dashboard.decorators import isfacultygraph

def graph_student(request, codechef_id):
    if not codechef_id:
        return redirect('/')
    codechef_scrapper = CodechefTools(codechef_id)
    if codechef_scrapper.account_exists():
        all_details = codechef_scrapper.pd_fetch()
    else:
        return redirect("/")
        
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
            text=f"Rating graph".upper(),
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
        line=dict(color="lightgreen"),  # Line color
        mode='lines+markers',  # Add markers at every point
        marker=dict(color='green', size=5),  # Marker color
        hoverinfo='text+name',  # Hover information
        hovertemplate='<b>%{text}</b><br><br>Contest: %{x}<br>Rating: %{y}<extra></extra>',
        text=[f"Contest: {contest}<br>Rating: {rating}" for contest, rating in zip(all_details['Contest'], all_details['Rating'])]  # Custom hover text
    )

    line_chart_graph.add_annotation(
        x=1.12,
        y=mean_rating,
        xref="paper",
        yref="y",
        text=str(round(mean_rating, 2)),
        showarrow=False,
        font=dict(
            color="red",
            size=12
        ),
        bgcolor="white",
        opacity=0.8
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

    bar_chart_graph.add_annotation(
        x=1.12,
        y=mean_rank,
        xref="paper",
        yref="y",
        text= str(round(mean_rank, 2)),
        showarrow=False,
        font=dict(
            color="red",
            size=12
        ),
        bgcolor="white",
        opacity=0.8
    )
    
    # Update layout to make background transparent, responsive, and decrease grid opacity
    bar_chart_graph.update_layout(
        title=dict(
            text=f"Ranking graph".upper(),
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
    
    # Calculate the count of stars for each rating
    all_ratings = list(all_details['Rating'])
    all_stars = codechef_scrapper.all_contest_stars(all_ratings)
    star_counts = pd.Series(all_stars).value_counts().sort_index()
    
    # Create a pie chart for the count of stars
    pie_chart_graph = px.pie(
        names=star_counts.index,
        values=star_counts.values,
        title="Distribution of Stars",
        labels={'label': 'Stars', 'value': 'Count'},
        width=400,
        height=350,
    )
    
    # Update layout to make background transparent, responsive, and decrease grid opacity
    pie_chart_graph.update_layout(
        title=dict(
            text="Distribution of Stars",
            font=dict(color="cyan", weight="bold")  # Title color
        ),
        legend=dict(
            font=dict(color="white")  # Legend text color
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        autosize=True,
    )
    
    # Update trace to set hover information
    pie_chart_graph.update_traces(
        hoverinfo='label+percent+name',  # Hover information
        textinfo='label+percent',  # Text information
        textfont=dict(color="white"),  # Text color
        marker=dict(
            line=dict(color='rgba(255, 255, 255, 0.2)', width=2)  # Marker border color and width
        )
    )
    
    # Ensure the mode bar is visible
    pie_chart = pie_chart_graph.to_html(full_html=True, config={
        'responsive': True,
        'scrollZoom': True,
        'displaylogo': False  # Optionally remove the Plotly logo
    })

    all_contest_problems = codechef_scrapper.fetch_contest_problems()

    # Extract keys and values for the histogram
    contest_keys = [" ".join(contest.split(" ")[0:2]) for contest in all_contest_problems.keys()]
    contest_values = [len(problems) for problems in all_contest_problems.values()]
    
    # Create histogram for keys and values
    histogram_graph = px.bar(
        x=contest_keys,
        y=contest_values,
        title="Histogram of Contest Problems",
        labels={'x': 'Contest', 'y': 'Number of Problems Solved'},
        width=700,
        height=350,
    )

    histogram_graph.update_layout(
        title=dict(
            text="Histogram of Contest Problems Solved",
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
                text="Number of Problems Solved",
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
    
    histogram = histogram_graph.to_html(full_html=True, config={
        'responsive': True,
        'scrollZoom': True,
        'displaylogo': False  # Optionally remove the Plotly logo
    })
    
    # Add the distribution chart to the graphs dictionary
    graphs = {
        "line_chart": line_chart,
        "bar_chart": bar_chart,
        "pie_chart": pie_chart,
        "histogram": histogram,
        "codechef_id": codechef_id
    }

    return render(request, 'graph_base.html', graphs)

@isfacultygraph
def graph_home(request):
    return render(request, "graph_faculty.html")