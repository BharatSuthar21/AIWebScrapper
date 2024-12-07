import streamlit as st
from scrape import *
from parse import *
st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    # with open("scraped_result.txt", "w", encoding="utf-8") as file:
    #     file.write(result)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_decription = st.text_area("Descrive what you want to parse?")

    if st.button("Parse Content"):
        if parse_decription:
            st.write("Parsing the content")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_decription)
            st.write(result)


