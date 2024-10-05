import streamlit as st
import seaborn as sns

st.set_page_config(page_title="Github Projects Dashboard", layout="wide", initial_sidebar_state="expanded")
sns.set_theme(style="darkgrid")

@st.cache_data
def load_data():
    """Load and preprocess GitHub dataset."""
    df = pd.read_csv("./data/github_dataset.csv")
    
    df = df.replace('NULL', None)
    
    repo_names = []
    for repo in df['repositories']:
        # splitting the repo data using "/" and accesing last element
        repo_name = repo.split('/')[-1]
        repo_names.append(repo_name)
    
    df['repo_name'] = repo_names
    return df


def run():
    df = load_data()
    df 
    st.markdown("github analytics page")

if __name__ == "__main__":
    run()