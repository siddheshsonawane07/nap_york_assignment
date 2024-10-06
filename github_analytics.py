import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    """Load and preprocess GitHub dataset."""
    df = pd.read_csv("./csv/github_dataset.csv")
    
    df = df.replace('NULL', None)
    
    repo_names = []
    for repo in df['repositories']:
        # splitting the repo data using "/" and accesing last element
        repo_name = repo.split('/')[-1]
        repo_names.append(repo_name)
    
    df['repo_name'] = repo_names
    return df

def display_bar_chart(
    df, x, y, title, xlabel, ylabel, fig_size=(10, 6), palette="coolwarm"
):
    fig, ax = plt.subplots(figsize=fig_size)
    sns.barplot(data=df, x=x, y=y, ax=ax, palette=palette)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def display_scatter_plot(df, x, y, title, xlabel, ylabel, fig_size):
    fig, ax = plt.subplots(figsize=fig_size)
    sns.scatterplot(data=df, x=x, y=y, ax=ax, hue="language", palette="viridis", s=100)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    st.pyplot(fig)


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
        ["Popular Repositories", "Stars vs Forks ", "Issues vs Pull Requests"]
    )

    # Popular Repositories
    with tab1:

        # Top Repositories by Stars
        st.subheader("Top 10 Repositories by Stars")
        top_repos_by_stars = df_filtered.nlargest(10, "stars_count")
        display_bar_chart(
            top_repos_by_stars,
            "stars_count",
            "repo_name",
            "Top 10 Repositories by Stars",
            "Stars",
            "Repository",
            fig_size=(12, 6),
            palette="Blues_d",
        )

        st.markdown("---")

        # Top Repositories by Forks
        st.subheader("Top 10 Repositories by Forks")
        top_repos_by_forks = df_filtered.nlargest(10, "forks_count")
        display_bar_chart(
            top_repos_by_forks,
            "forks_count",
            "repo_name",
            "Top 10 Repositories by Forks",
            "Forks",
            "Repository",
            fig_size=(12, 6),
            palette="Greens_d",
        )

        st.markdown("---")

        # Top Repositories by Contributions
        st.subheader("Top 10 Repositories by Contributions")
        top_repos_by_contributors = df_filtered.nlargest(10, "contributors")
        display_bar_chart(
            top_repos_by_contributors,
            "contributors",
            "repo_name",
            "Top 10 Repositories by Contributions",
            "Contributors",
            "Repository",
            fig_size=(12, 6),
            palette="Oranges_d",
        )

        st.markdown("---")

        # Top Repositories by Issues
        st.subheader("Top 10 Repositories by number of Issues")
        top_repos_by_issues = df_filtered.nlargest(10, "issues_count")
        display_bar_chart(
            top_repos_by_issues,
            "issues_count",
            "repo_name",
            "Top 10 Repositories by number of Issues",
            "Issues",
            "Repository",
            fig_size=(12, 6),
            palette="Reds_d",
        )

    # Stars and Fork Analysis
    with tab2:
        if selected_language != "All":
            st.subheader("Stars vs. Forks")
            display_scatter_plot(
                df_filtered,
                "stars_count",
                "forks_count",
                "Stars vs. Forks",
                "Stars",
                "Forks",
                (15,10)
            )
        else:
            st.warning(
                    "Please select a specific language to see the Stars vs Forks analysis."
            )
    
    # Issues vs Pull Requests Scatter Plot
    with tab3:
        if selected_language != "All":
            st.subheader("Issues vs. Pull Requests")
            display_scatter_plot(
                df_filtered,
                "issues_count",
                "pull_requests",
                "Issues vs. Pull Requests",
                "Issues",
                "Pull Requests",
                (15,10)

            )
        else:
            st.warning(
                    "Please select a specific language to see the Issues vs Pull Requests analysis."
            )

if __name__ == "__main__":
    run()