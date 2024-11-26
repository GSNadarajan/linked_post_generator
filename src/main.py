import streamlit as st
from few_shot import FewShotPosts
from post_generate import generate_post

length_options = ["Short", "Medium", "Long"]
langugage_options = ["English","Hinglish"]
def main():
    
    st.subheader("LinkedIn Post Generator")
    
    ## Create three columns for the dropdown
    col1, col2, col3  = st.columns(3)
    
    fs = FewShotPosts()
    tags = fs.get_tags()
    
    with col1:
        selected_tag = st.selectbox("Title", options=tags)
        
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
        
    with col3:
        selected_language = st.selectbox("Language", options=langugage_options)
    
    
    ## Generate button
    if st.button("Generate"):
        post = generate_post(selected_tag, selected_length, selected_language)
        st.write(post)
    
    
# Run the app
if __name__ == "__main__":
    main()