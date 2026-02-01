import streamlit as st 

from langchain_groq import ChatGroq 
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import validators 
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate

template = """You are a helpful assistant that helps to summarize the content of the url.
        {text}
        Provide a concise summary in bullet points."""
prompt = PromptTemplate(input_variables=["text"],template=template)

st.set_page_config(page_icon="🔍",page_title="Url Summarizer",layout="centered")
st.title("Langchain Powered URL Summarizer")
st.info("Enter the youtube url or generic url to summarize")

api_key = st.sidebar.text_input(label="Paste your Api key",type="password")
generic_url = st.text_input(label="Paste your url")
if st.button("Summarize the url"):
    if not (generic_url and api_key):
        st.error("Please enter the url or Api key and try again")
    
    elif not validators.url(generic_url):
        st.error("Please enter a valid url")
    else:
        try:
            llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)
            if "youtube.com" in generic_url.strip() or "youtu.be" in generic_url.strip():
                with st.spinner("Summarizing the youtube video..."):
                    print("yes")
                    loader = YoutubeLoader.from_youtube_url(generic_url,add_video_info=False)
                    print("no")
                    data = loader.load()
                    print(data)
            else:
                with st.spinner("Summarizing the webpage..."):
                    loader = UnstructuredURLLoader(urls=[generic_url],headers={"User-Agent": "Mozilla/5.0"})
                    data = loader.load()
                    
            with st.spinner("Generating the summary..."):
                chain = load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                summary = chain.run({"input_documents": data})
            st.success(summary)
        except Exception as e:
            st.exception(f"An error occurred: {e}")
            


