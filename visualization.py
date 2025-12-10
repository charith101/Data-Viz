import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.markdown("""
    <style>
    .st-emotion-cache-scp8yw {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)
st.logo("assets/logo.svg",size="large")
PLOTLY_TEMPLATE = "plotly_white"

def plot_histogram(df, col):
    """Plots a histogram with a marginal box plot for a numerical column."""
    if col not in df.columns: return
    fig = px.histogram(df, x=col, title=f"Distribution of {col}", marginal="box",
                       template=PLOTLY_TEMPLATE)
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, width='stretch')

def plot_box_plot(df, col, category_col=None):
    """Plots a box plot for a numerical column, optionally grouped by a category."""
    if col not in df.columns: return

    if category_col and category_col not in df.columns:
        category_col = None

    title = f"Box Plot of {col}"
    if category_col:
        title += f" grouped by {category_col}"

    fig = px.box(df, y=col, x=category_col, color=category_col,
                 title=title, template=PLOTLY_TEMPLATE)
    st.plotly_chart(fig, width='stretch')

def plot_density_heatmap(df, x, y):
    """Plots a 2D density heatmap for two numerical variables."""
    if x not in df.columns or y not in df.columns: return
    
    fig = px.density_heatmap(df, x=x, y=y, 
                             title=f"2D Density Heatmap of {y} vs {x}",
                             template=PLOTLY_TEMPLATE,
                             color_continuous_scale="Viridis")
    st.plotly_chart(fig, width='stretch')

def plot_bar_chart_categorical(df, col, limit=15):
    """Plots a bar chart for categorical data (top N values)."""
    if col not in df.columns: return
    counts = df[col].dropna().value_counts().head(limit).reset_index()
    counts.columns = [col, 'Count']
    
    fig = px.bar(counts, x=col, y='Count', title=f"Top {limit} Values in {col}",
                 template=PLOTLY_TEMPLATE)
    st.plotly_chart(fig, width='stretch')

def plot_scatter(df, x, y, color=None):
    """Plots a scatter plot for bivariate analysis."""
    if x not in df.columns or y not in df.columns: return
    plot_color = color if color in df.columns else None
    
    fig = px.scatter(df, x=x, y=y, color=plot_color, 
                     title=f"{y} vs {x} (Scatter Plot)",
                     template=PLOTLY_TEMPLATE)
    st.plotly_chart(fig, width='stretch')

def plot_correlation_heatmap(df):
    """Plots a correlation heatmap for all numerical columns."""
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) < 2:
        st.info("Not enough numerical columns (requires at least 2) for correlation heatmap.")
        return
    
    corr = df[num_cols].corr()
    
    fig = px.imshow(
        corr, 
        text_auto=".2f", 
        aspect="auto", 
        color_continuous_scale=px.colors.diverging.RdBu,
        title="Correlation Heatmap (Numerical Columns)",
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(xaxis={'side': 'bottom'}, height=600)
    st.plotly_chart(fig, width='stretch')

def plot_missing_data_heatmap(df):
    """Plots a heatmap showing the location of missing values across columns."""
    if df.isnull().sum().sum() == 0:
        st.success("No missing data to plot!")
        return
        
    missing_df = df.isnull().astype(int)
    
    fig = go.Figure(data=go.Heatmap(
        z=missing_df.T.values, 
        x=missing_df.index.tolist(),
        y=missing_df.columns.tolist(),
        colorscale=[[0, 'blue'], [1, 'red']], 
        showscale=False
    ))
    
    fig.update_layout(
        title='Missing Data Pattern (Red = Missing)',
        xaxis_title='Row Index',
        yaxis_title='Column',
        height=700,
        template=PLOTLY_TEMPLATE,
        yaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, width='stretch')

def plot_pairplot(df):
    """Plots a scatter matrix (pair plot) for up to 5 numerical columns."""
    num_cols = df.select_dtypes(include='number').columns
    
    if len(num_cols) < 2:
        st.info("Need at least 2 numerical columns for a Pair Plot.")
        return

    dimensions_to_plot = num_cols[:5].tolist()
    
    fig = px.scatter_matrix(
        df, 
        dimensions=dimensions_to_plot, 
        title="Pair Plot (First 5 Numerical Columns)", 
        height=800,
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(diagonal_visible=False, showupperhalf=False)
    fig.update_layout(title_x=0.5)
    
    st.plotly_chart(fig, width='stretch')