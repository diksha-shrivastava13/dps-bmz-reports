import streamlit as st
import requests
import json
import re
import pandas as pd

st.set_page_config(
    page_title="Prompt Bot",
    page_icon=":hourglass_flowing_sand:",
    layout="centered"
)
st.markdown("<h1 style='text-align: center;'>⏳ Portfolio Navigator: Yearly Program Reports </h1>",
            unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is None:
    st.info("Please upload a PDF file.")
else:
    try:
        # Prepare the file for sending
        files = {'file': ('file.pdf', uploaded_file.getvalue(), 'application/pdf')}

        # Make the POST request
        response = requests.post(
            "https://dps-ai-prod.bluemoss-c00786e0.germanywestcentral.azurecontainerapps.io/api/program/report/",
            files=files
        )

        # Check if the request was successful
        if response.status_code == 200:
            st.success("Request successful!")

            # Process and display the results
            result = json.loads(response.text)
            string = result['fixed_data']
            json_content = re.search(r'```json\n{(.*)}\n```', string, re.DOTALL).group(1)
            key_value_pairs = re.findall(r'"([^"]+)":\s*"([^"]*)"', json_content)
            metadata = dict(key_value_pairs)

            df = pd.DataFrame(list(metadata.items()), columns=['Key', 'Value'])
            markdown_table = df.to_markdown(index=False)

            st.markdown(markdown_table, unsafe_allow_html=True)
            st.markdown(result['recommendation'])

        else:
            st.error(f"Error: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
