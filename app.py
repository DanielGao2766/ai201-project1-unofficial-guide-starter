import streamlit as st
from embed import retrieve
from generate import generate_answer

st.set_page_config(page_title="UVA Housing — The Unofficial Guide", page_icon="🏠")
st.title("UVA Housing — The Unofficial Guide")
st.caption("Ask a plain-language question about UVA first-year housing and get a grounded, cited answer.")

query = st.text_input("Your question", placeholder="e.g. Which dorm is closest to Runk Dining Hall?")

if query:
    with st.spinner("Looking up..."):
        chunks = retrieve(query)
        answer = generate_answer(query, chunks)

    st.markdown(answer)

    st.markdown("---")
    st.markdown("**Sources:**")
    seen = set()
    for chunk in chunks:
        url = chunk["source_url"]
        label = chunk["source_label"]
        if url and url not in seen:
            st.markdown(f"- [{label}]({url})")
            seen.add(url)
