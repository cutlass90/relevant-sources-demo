import requests
import os
import streamlit as st
from requests.auth import HTTPBasicAuth
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

X_API_KEY = os.getenv("X_API_KEY")
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")


st.set_page_config(layout="wide")
st.title("Relevant Sources Demo V0.11")

def is_huggingface_endpoint_ready(endpoint_url: str) -> bool:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    try:
        response = requests.get(endpoint_url, headers=headers)
        st.write(response.content.decode())
        if response.status_code == 200:
            return True
        else:
            print(f"Endpoint returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False



if st.button("Get Sources"):
    if not st.session_state.get('document'):
        st.write('Please input your document first.')
    else:
        with st.spinner("Processing, this may take up to a minute..."):
            #url = "https://e125-99-209-159-2.ngrok-free.app/relevant_sources"
            #url = "https://api.gptzero.me/v2/relevant_sources/text"
            url = "http://54.81.54.37:5003/relevant_sources"
            #headers = {'Content-Type': 'application/json', 'x-api-key': X_API_KEY}
            headers = {'Content-Type': 'application/json'}
            data = {
                "text": st.session_state['document']
            }
            try:
                response = requests.post(url, headers=headers, json=data)
                st.write(status_code = response.status_code)
                if response.status_code != 200:
                    st.write(response.json())
                response.raise_for_status() 
                st.session_state['results'] = response.json().get('results', [])
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred: {http_err}")
            except Exception as err:
                st.error(f"An error occurred: {err}")

doc_col, analysis_col = st.columns(2)

with doc_col:
    st.session_state['document'] = st.text_area("Place your document here", height=500, max_chars=2000,
                                               value="Climate change refers to the long-term shift in global weather patterns caused by human activity, particularly the emission of greenhouse gases into the atmosphere. ⁤⁤The most significant greenhouse gas is carbon dioxide, which is primarily produced by burning fossil fuels such as coal, oil, and gas.")

with analysis_col:
    if 'results' in st.session_state:
        st.subheader(f"{len(st.session_state['results'])} claim(s) found")
        for i, result in enumerate(st.session_state['results']):
            for source in result['sources']:
                try:
                    del source["content"]
                    del source["justification"]
                    del source["relevance_score"]
                    del source["reliability_score"]
                    del source["stance"]
                    del source["date"]
                    source["source summary"] = source.pop("summary")
                except Exception as e:
                    print(e)
            with st.expander(f"Claim {i + 1} - {result['claim']['text']}"):
                st.write('Below is a nested list of relevant sources for the identified claim:')
                st.write(result['sources'])
    else:
        st.write('Results will appear here.')
