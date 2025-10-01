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

# --- Data Loading ---
import os

@st.cache_data
def load_data():
    """Loads all CSV files into a dictionary of pandas DataFrames."""
    data = {}

    # Get the directory where the script is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

    for key, filename in files.items():
        filepath = os.path.join(BASE_DIR, filename)
        try:
            if "sex" in key:
                # Sex data has a different format
                df = pd.read_csv(filepath)
                df = df.melt(var_name='key', value_name='value')
                data[key] = df
            else:
                data[key] = pd.read_csv(filepath)
        except FileNotFoundError:
            st.error(f"Error: The file '{filename}' was not found in {BASE_DIR}")
            return None

    return data


data = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
st.sidebar.info("Select a dataset below to explore the FBI crime data visualizations.")

# Create a mapping for user-friendly names
dataset_options = {
    "Offense Linked to Another Offense": "offense_linked",
    "Type of Weapon Involved": "weapon_type",
    "Victim's Relationship to Offender": "victim_relationship",
    "Location Type": "location_type",
    "Victim Demographics": "victim_demographics",
    "Offender Demographics": "offender_demographics"
}

selection = st.sidebar.radio("Go to", list(dataset_options.keys()))
selected_key = dataset_options[selection]


# --- Main App ---
st.title("FBI Crime Data Analysis Dashboard ⚖️")
st.markdown("An interactive dashboard to explore various aspects of crime data reported to the FBI.")


if data:
    # --- Generic Plotting Function ---
    def plot_bar_chart(df, title, x='key', y='value', color='key'):
        """Creates and displays a Plotly bar chart."""
        df = df.sort_values(by=y, ascending=False).head(20)
        fig = px.bar(df, x=x, y=y, title=title,
                     labels={'key': 'Category', 'value': 'Count'},
                     color=color, template='plotly_white')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Number of Incidents",
            showlegend=False,
            xaxis={'categoryorder':'total descending'}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'), use_container_width=True)

    # --- Display selected dataset ---
    if selected_key == "offense_linked":
        st.header("Offense Linked to Another Offense")
        st.markdown("This chart shows the most common offenses that are linked to another crime.")
        plot_bar_chart(data['offense_linked'], "Top 20 Linked Offenses")

    elif selected_key == "weapon_type":
        st.header("Type of Weapon Involved by Offense")
        st.markdown("This visualization displays the types of weapons most frequently involved in offenses.")
        plot_bar_chart(data['weapon_type'], "Weapon Types in Offenses")

    elif selected_key == "victim_relationship":
        st.header("Victim's Relationship to Offender")
        st.markdown("Explore the relationship between victims and offenders in reported incidents.")
        plot_bar_chart(data['victim_relationship'], "Victim-Offender Relationships")

    elif selected_key == "location_type":
        st.header("Location Type of Offenses")
        st.markdown("This chart illustrates where crimes are most likely to occur based on location type.")
        plot_bar_chart(data['location_type'], "Top 20 Crime Locations")

    elif selected_key == "victim_demographics":
        st.header("Victim Demographics")
        st.markdown("A breakdown of victim demographics by race, ethnicity, and sex.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Victim Race")
            plot_bar_chart(data['victim_race'], "Victim Race Distribution", x='key', y='value')

        with col2:
            st.subheader("Victim Ethnicity")
            plot_bar_chart(data['victim_ethnicity'], "Victim Ethnicity Distribution", x='key', y='value')

        st.subheader("Victim Sex")
        fig_sex = px.pie(data['victim_sex'], names='key', values='value', title='Victim Sex Distribution', hole=0.3)
        fig_sex.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_sex, use_container_width=True)
        st.dataframe(data['victim_sex'], use_container_width=True)


    elif selected_key == "offender_demographics":
        st.header("Offender Demographics")
        st.markdown("A breakdown of offender demographics by race, ethnicity, and sex.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Offender Race")
            plot_bar_chart(data['offender_race'], "Offender Race Distribution", x='key', y='value')

        with col2:
            st.subheader("Offender Ethnicity")
            plot_bar_chart(data['offender_ethnicity'], "Offender Ethnicity Distribution", x='key', y='value')


        st.subheader("Offender Sex")
        fig_sex = px.pie(data['offender_sex'], names='key', values='value', title='Offender Sex Distribution', hole=0.3)
        fig_sex.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_sex, use_container_width=True)
        st.dataframe(data['offender_sex'], use_container_width=True)

else:
    st.warning("Data could not be loaded. Please ensure the CSV files are in the same directory as the script.")

st.sidebar.markdown("---")
st.sidebar.markdown("Created with [Streamlit](https://streamlit.io)")
