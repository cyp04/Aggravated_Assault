# -*- coding: utf-8 -*-
"""FBI Crime Data Analysis Dashboard"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="FBI Crime Data Dashboard",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown(
    """
    <style>
        h1, h2, h3, h4 {
            color: #1f4e79;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Data Loader ---
@st.cache_data
def load_data():
    """Loads all CSV files into a dictionary of pandas DataFrames."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = {
        "offense_linked": "Offense Linked to Another Offense_09-30-2025.csv",
        "weapon_type": "Type of Weapon Involved by Offense_09-30-2025.csv",
        "victim_relationship": "Victim's Relationship to Offender_09-30-2025.csv",
        "location_type": "Location Type_09-30-2025.csv",
        "victim_ethnicity": "Victim ethnicity_09-30-2025.csv",
        "offender_ethnicity": "Offender ethnicity_09-30-2025.csv",
        "victim_race": "Victim race_09-30-2025.csv",
        "offender_race": "Offender race_09-30-2025.csv",
        "victim_sex": "Victim sex_09-30-2025.csv",
        "offender_sex": "Offender sex_09-30-2025.csv"
    }

    data = {}
    for key, filename in files.items():
        filepath = os.path.join(base_dir, filename)
        try:
            df = pd.read_csv(filepath)
            if "sex" in key:
                df = df.melt(var_name="Category", value_name="Count")
            data[key] = df
        except FileNotFoundError:
            st.error(f"❌ File not found: {filename}")
            return None
    return data


data = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("📊 Navigation")
st.sidebar.info("Choose a dataset to explore FBI crime data.")

dataset_options = {
    "Offense Linked to Another Offense": "offense_linked",
    "Type of Weapon Involved": "weapon_type",
    "Victim's Relationship to Offender": "victim_relationship",
    "Location Type": "location_type",
    "Victim Demographics": "victim_demographics",
    "Offender Demographics": "offender_demographics"
}

selection = st.sidebar.radio("Go to:", list(dataset_options.keys()))
selected_key = dataset_options[selection]

# --- Chart Helpers ---
def plot_bar_chart(df, title, x="key", y="value", color="key"):
    """Creates a consistent bar chart layout."""
    df = df.sort_values(by=y, ascending=False).head(20)
    fig = px.bar(
        df, x=x, y=y, color=color, title=title,
        labels={x: "Category", y: "Number of Incidents"},
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        xaxis=dict(categoryorder="total descending")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.style.highlight_max(axis=0, color="lightgreen"), use_container_width=True)

def plot_pie_chart(df, title):
    """Creates a consistent donut chart layout."""
    fig = px.pie(df, names="Category", values="Count", title=title, hole=0.3)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

# --- Main Dashboard ---
st.title("⚖️ FBI Crime Data Analysis Dashboard")
st.markdown("Explore various aspects of FBI-reported crime data with interactive charts and tables.")
st.divider()

if data:
    if selected_key == "offense_linked":
        st.header("🔗 Offense Linked to Another Offense")
        st.caption("Shows the most common offenses linked to another crime.")
        plot_bar_chart(data["offense_linked"], "Top 20 Linked Offenses")

    elif selected_key == "weapon_type":
        st.header("🔫 Type of Weapon Involved by Offense")
        st.caption("Types of weapons most frequently involved in offenses.")
        plot_bar_chart(data["weapon_type"], "Weapon Types in Offenses")

    elif selected_key == "victim_relationship":
        st.header("👥 Victim's Relationship to Offender")
        st.caption("Relationship patterns between victims and offenders.")
        plot_bar_chart(data["victim_relationship"], "Victim-Offender Relationships")

    elif selected_key == "location_type":
        st.header("📍 Location Type of Offenses")
        st.caption("Where crimes are most likely to occur by location type.")
        plot_bar_chart(data["location_type"], "Top 20 Crime Locations")

    elif selected_key == "victim_demographics":
        st.header("🧍 Victim Demographics")
        st.caption("Breakdown of victim demographics by race, ethnicity, and sex.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Victim Race")
            plot_bar_chart(data["victim_race"], "Victim Race Distribution")

        with col2:
            st.subheader("Victim Ethnicity")
            plot_bar_chart(data["victim_ethnicity"], "Victim Ethnicity Distribution")

        st.subheader("Victim Sex")
        plot_pie_chart(data["victim_sex"], "Victim Sex Distribution")

    elif selected_key == "offender_demographics":
        st.header("🧑‍⚖️ Offender Demographics")
        st.caption("Breakdown of offender demographics by race, ethnicity, and sex.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Offender Race")
            plot_bar_chart(data["offender_race"], "Offender Race Distribution")

        with col2:
            st.subheader("Offender Ethnicity")
            plot_bar_chart(data["offender_ethnicity"], "Offender Ethnicity Distribution")

        st.subheader("Offender Sex")
        plot_pie_chart(data["offender_sex"], "Offender Sex Distribution")

else:
    st.warning("⚠️ Data could not be loaded. Please ensure all CSV files are in the same directory.")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using [Streamlit](https://streamlit.io)")


st.sidebar.markdown("---")
st.sidebar.markdown("Created with [Streamlit](https://streamlit.io)")
