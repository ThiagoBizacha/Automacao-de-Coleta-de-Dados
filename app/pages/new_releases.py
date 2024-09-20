import streamlit as st
from app.components.data_loader import get_data
from app.components.filters import apply_filters
from app.components.kpi_calculator import calculate_kpis
from app.components.visualizations import render_pareto_chart
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

def show_page():

     st.title("DESENVOLVER...")

    