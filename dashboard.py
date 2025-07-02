import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(layout="wide", page_title="Copilot Monitor Dashboard")

# Sidebar
with st.sidebar:
    st.header("Filters & Options")
    # Placeholder for future filters
    st.write("Filters will be added here (e.g., date range, language).")

# Title
st.title("Copilot Monitor Dashboard")
st.write("Analytics and trends from your Copilot usage.")


# Supabase Connection
@st.cache_resource
def init_supabase_client():
    """Initializes and returns the Supabase client."""
    try:
        url = os.environ.get("SUPABASE_CME_URL")
        key = os.environ.get("SUPABASE_CME_KEY")
        if not url or not key:
            st.error("Supabase URL or Key not found. Please set SUPABASE_CME_URL and SUPABASE_CME_KEY environment variables.")
            return None
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error initializing Supabase client: {e}")
        return None

supabase_client = init_supabase_client()

@st.cache_data(ttl=600) # Cache data for 10 minutes
def fetch_prompt_logs(_client: Client):
    """Fetches all data from the prompt_log table."""
    if not _client:
        return pd.DataFrame() # Return empty DataFrame if client is None
    try:
        response = _client.table("prompt_log").select("*").order("created_at", desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            # Convert created_at to datetime objects
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

            # Ensure correct data types
            if 'score' in df.columns:
                df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0).astype(int)
            if 'accepted' in df.columns:
                df['accepted'] = df['accepted'].astype(bool)

            # Add derived columns
            if 'created_at' in df.columns and not df['created_at'].isnull().all():
                df['date'] = df['created_at'].dt.date
                df['hour'] = df['created_at'].dt.hour

            return df
        else:
            st.write("No data found in prompt_log table.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data from Supabase: {e}")
        return pd.DataFrame()

if supabase_client:
    df_logs = fetch_prompt_logs(supabase_client)

    if df_logs.empty:
        st.info("No data available to display. Start using the Copilot Monitor extension to see analytics.")
    else:
        # Optional Raw Data Display
        with st.expander("View Raw Prompt Logs"):
            st.dataframe(df_logs, use_container_width=True)

        # Metrics Section
        st.divider()
        st.header("📊 Metrics Overview")

        # Metric 1: Average score per file/language
    st.subheader("Average Score per File/Language")
    if 'file_path' in df_logs.columns and 'lang' in df_logs.columns and 'score' in df_logs.columns:
        avg_scores = df_logs.groupby(['file_path', 'lang'])['score'].mean().reset_index()
        avg_scores = avg_scores.sort_values(by='score', ascending=False)
        avg_scores.rename(columns={'score': 'average_score'}, inplace=True)
        st.dataframe(avg_scores, use_container_width=True)
    else:
        st.write("Required columns (file_path, lang, score) not found for this metric.")

    st.divider()
    # Metric 2: Copilot usage timeline
    st.subheader("Copilot Usage Timeline (Suggestions per Day)")
    if 'date' in df_logs.columns:
        usage_timeline = df_logs.groupby('date').size().reset_index(name='suggestions_count')
        usage_timeline = usage_timeline.set_index('date') # Set date as index for st.line_chart
        if not usage_timeline.empty:
            st.line_chart(usage_timeline)
        else:
            st.write("Not enough data to display usage timeline.")
    else:
        st.write("Required 'date' column not found for this metric.")

    st.divider()
    # Metric 3: Prompt/Suggestion Analysis
    st.subheader("Prompt & Suggestion Analysis")
    if 'prompt' in df_logs.columns and 'suggestion' in df_logs.columns and 'accepted' in df_logs.columns:
        avg_prompt_length = df_logs['prompt'].str.len().mean()
        avg_suggestion_length = df_logs['suggestion'].str.len().mean()

        st.metric(label="Average Prompt Length (chars)", value=f"{avg_prompt_length:.2f}")
        st.metric(label="Average Suggestion Length (chars)", value=f"{avg_suggestion_length:.2f}")

        accepted_counts = df_logs['accepted'].value_counts()
        st.bar_chart(accepted_counts)
        # More detailed display for accepted counts
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Accepted Suggestions", value=accepted_counts.get(True, 0))
        with col2:
            st.metric(label="Not Accepted Suggestions", value=accepted_counts.get(False, 0))

    else:
        st.write("Required columns (prompt, suggestion, accepted) not found for this metric.")

    # TODO: Add more metric display logic (actual ratio graphs if clarified)
elif not supabase_client: # This case is for when supabase_client itself is None
    st.warning("Supabase client could not be initialized. Please check environment variables and connection.")


if __name__ == "__main__":
    # This part is mostly for local development if needed,
    # Streamlit apps are typically run with `streamlit run dashboard.py`
    pass
