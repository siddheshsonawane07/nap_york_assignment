import streamlit as st
import github_analytics
# import repository_analytics

def main():
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>GitHub Projects Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D3D3D3;'>Explore trends and insights from popular repositories</p>", unsafe_allow_html=True)
    
    page = st.sidebar.selectbox("Choose a page", ["Home", "GitHub Dataset Analysis", "Repository Dataset Analysis"])

    if page == "Home":
        st.markdown("Select a page from the sidebar to begin exploring!")
    elif page == "GitHub Dataset Analysis":
        github_analytics.run()
    # elif page == "Repository Dataset Analysis":
    #     repository_analytics.run()

    st.markdown("<hr style='border-top: 2px solid #FFA500;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4D3D3;'>Built with ❤ by Siddhesh</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()