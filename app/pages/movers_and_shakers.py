import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import time
from wordcloud import WordCloud
from app.components.data_loader import get_data
from app.components.filters import apply_filters
from app.components.kpi_calculator import calculate_kpis
from app.components.visualizations import render_pareto_chart

def show_page():

    st.title("DESENVOLVER...")