import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("<h1 style='text-align: center; color: #FFA500;'>GitHub Projects Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D3D3D3;'>Explore trends and insights from popular repositories</p>", unsafe_allow_html=True)

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
    sns.set_theme(style="darkgrid")
    # st.dataframe(df)
    # st.markdown("github analytics page")
    
    st.sidebar.header("Filters")
    languages = ["All"] + sorted(df["language"].dropna().unique().tolist())
    selected_language = st.sidebar.selectbox("Select Language", languages)

    df_filtered = (
        df if selected_language == "All" else df[df["language"] == selected_language]
    )

    if selected_language == "All":
        st.header("Language Distribution")
        lang_distribution = df["language"].value_counts().nlargest(10)
        fig, ax = plt.subplots(figsize=(8, 6))
        lang_distribution.plot(
            kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, cmap="coolwarm"
        )
        ax.set_ylabel("")
        st.pyplot(fig)

    st.header("Repository Insights")
    tab1, tab2, tab3 = st.tabs(
        ["Popular Repositories", "Stars and Forks Analysis", "Contributors and Issues"]
    )

    with tab1:
        col1, col2 = st.columns(2)

        # Top Repositories by Stars
        with col1:
            st.subheader("Top 10 Repositories by Stars")
            top_repos_by_stars = df_filtered.nlargest(10, "stars_count")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_repos_by_stars, x="stars_count", y="repositories", ax=ax, palette="Blues_d")
            ax.set_title("Top 10 Repositories by Stars", fontsize=16)
            ax.set_xlabel("Stars", fontsize=14)
            ax.set_ylabel("Repository", fontsize=14)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Top Repositories by Forks
        with col2:
            st.subheader("Top 10 Repositories by Forks")
            top_repos_by_forks = df_filtered.nlargest(10, "forks_count")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_repos_by_forks, x="forks_count", y="repositories", ax=ax, palette="Greens_d")
            ax.set_title("Top 10 Repositories by Forks", fontsize=16)
            ax.set_xlabel("Forks", fontsize=14)
            ax.set_ylabel("Repository", fontsize=14)
            plt.xticks(rotation=45)
            st.pyplot(fig)

if __name__ == "__main__":
    run()