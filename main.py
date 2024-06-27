import requests
import os
import streamlit as st

X_API_KEY = os.getenv("X_API_KEY")

st.set_page_config(layout="wide")
st.title("Relevant Sources Demo V0.3")

if st.button("Get Sources"):
    if not st.session_state.get('document'):
        st.write('Please input your document first.')
    else:
        with st.spinner("Processing, this may take up to a minute..."):
            url = "https://api.gptzero.me/v2/relevant_sources/text"
            headers = {'Content-Type': 'application/json',
                       'x-api-key': X_API_KEY}
            data = {
                "text": st.session_state['document']
            }
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status() 
                st.session_state['results'] = response.json().get('results', [])
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred: {http_err}")
            except Exception as err:
                st.error(f"An error occurred: {err}")

doc_col, analysis_col = st.columns(2)

with doc_col:
    st.session_state['document'] = st.text_area("Place your document here", height=1000, max_chars=2000)

with analysis_col:
    if 'results' in st.session_state:
        st.subheader(f"{len(st.session_state['results'])} claim(s) found")
        for i, result in enumerate(st.session_state['results']):
            for source in result['sources']:
                del source["content"]
                del source["justification"]
                del source["relevance_score"]
                del source["reliability_score"]
                del source["stance"]
                del source["date"]
                source["source summary"] = source.pop("summary")
            with st.expander(f"Claim {i + 1} - {result['claim']['text']}"):
                st.write('Below is a nested list of relevant sources for the identified claim:')
                st.write(result['sources'])
    else:
        st.write('Results will appear here.')
