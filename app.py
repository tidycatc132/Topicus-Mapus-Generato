import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
from pyvis.network import Network
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Topicus Mapus Generato",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions ---

def generate_mind_map_html(data):
    """Generates an interactive mind map using Pyvis and returns it as an HTML string."""
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True, directed=True)

    pillar_topic = data.get('pillar_topic', 'Pillar')
    net.add_node(pillar_topic, label=pillar_topic, color='#FF4B4B', size=30, shape='box')

    for cluster in data.get('clusters', []):
        cluster_title = cluster.get('cluster_title', 'Cluster')
        net.add_node(cluster_title, label=cluster_title, color='#00C49A', size=20, shape='box')
        net.add_edge(pillar_topic, cluster_title)

        for page in cluster.get('pages', []):
            page_title = page.get('page_title', 'Page')
            # Create a detailed label with keywords and word count for hover
            hover_title = (
                f"Keywords: {', '.join(page.get('keywords', []))}\n"
                f"Word Count: {page.get('word_count', 'N/A')}"
            )
            net.add_node(page_title, label=page_title, color='#1E90FF', size=15, title=hover_title, shape='box')
            net.add_edge(cluster_title, page_title)

    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "font": {
          "size": 16
        }
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": {
          "type": "cubicBezier"
        }
      },
      "interaction": {
        "navigationButtons": true,
        "keyboard": true
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -30000,
          "springConstant": 0.04,
          "springLength": 150
        },
        "minVelocity": 0.75
      }
    }
    """)
    
    # Save network to a temporary file and read it
    try:
        net.save_graph("mind_map.html")
        with open("mind_map.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except Exception as e:
        st.error(f"Error generating mind map: {e}")
        return None

def prepare_csv_data(data):
    """Flattens the topical map data for CSV export."""
    records = []
    pillar_topic = data.get('pillar_topic', '')
    for cluster in data.get('clusters', []):
        cluster_title = cluster.get('cluster_title', '')
        for page in cluster.get('pages', []):
            records.append({
                "Pillar Topic": pillar_topic,
                "Cluster Title": cluster_title,
                "Page Title": page.get('page_title', ''),
                "Keywords": ", ".join(page.get('keywords', [])),
                "Suggested Word Count": page.get('word_count', '')
            })
    df = pd.DataFrame(records)
    return df.to_csv(index=False).encode('utf-8')


# --- Streamlit App UI ---

# --- Sidebar for API Key ---
with st.sidebar:
    st.header("🔑 API Configuration")
    st.markdown("Enter your Google Gemini API key to get started.")
    google_api_key = st.text_input("Gemini API Key", type="password", key="google_api_key_input")
    st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")
    "[View Source Code](https://github.com/your-repo/topical-map-streamlit)" # Replace with your repo link

# --- Main App Interface ---
st.title("🗺️ AI Topical Map Generator")
st.markdown("Enter a main topic to generate a comprehensive topical map, including content pillars, clusters, page topics, and keyword suggestions.")

# Initialize session state
if 'topical_map_data' not in st.session_state:
    st.session_state.topical_map_data = None
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = ""

topic_input = st.text_input("Enter your main topic or search term:", placeholder="e.g., 'Digital Marketing Strategies'")

if st.button("Generate Topical Map", type="primary"):
    if not google_api_key:
        st.error("Please enter your Google Gemini API key in the sidebar.")
    elif not topic_input:
        st.warning("Please enter a topic to generate the map.")
    else:
        st.session_state.last_topic = topic_input
        with st.spinner("🧠 The AI is thinking... This may take a moment."):
            try:
                genai.configure(api_key=google_api_key)
                
                # Model Configuration - Use a model that supports JSON output
                model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                     generation_config={"response_mime_type": "application/json"}
                )
                
                prompt = f"""
                Act as an expert SEO content strategist. Your task is to create a detailed topical map for the main topic: "{topic_input}".

                Structure your response as a valid JSON object with the following schema:
                {{
                  "pillar_topic": "The main, overarching topic provided.",
                  "clusters": [
                    {{
                      "cluster_title": "A logical sub-topic or category related to the pillar.",
                      "pages": [
                        {{
                          "page_title": "A specific, long-tail article title or question that falls under the cluster.",
                          "keywords": ["a list", "of 5-7 relevant", "long-tail keywords"],
                          "word_count": "A suggested word count for the article, e.g., 1200"
                        }}
                      ]
                    }}
                  ]
                }}

                Generate at least 4-6 relevant clusters. For each cluster, generate at least 4-6 specific page topics. Ensure the keywords are highly relevant and practical for SEO. The page titles should be engaging and answer specific user intents.
                """

                response = model.generate_content(prompt)
                
                # Store the successful response in session state
                st.session_state.topical_map_data = json.loads(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.topical_map_data = None


# --- Display Results ---
if st.session_state.topical_map_data:
    st.success(f"Topical Map generated for: **{st.session_state.last_topic}**")

    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Visual Mind Map", "📄 Detailed View & Export"])

    with tab1:
        st.subheader("Interactive Topical Map Visualization")
        st.markdown("Click and drag nodes to explore the map. Hover over page nodes (blue) for more details.")
        html_content = generate_mind_map_html(st.session_state.topical_map_data)
        if html_content:
            components.html(html_content, height=800, scrolling=False)

    with tab2:
        st.subheader("Detailed Content Plan")

        # Add a download button for the CSV
        csv_data = prepare_csv_data(st.session_state.topical_map_data)
        st.download_button(
           label="📥 Export as CSV",
           data=csv_data,
           file_name=f"topical_map_{st.session_state.last_topic.replace(' ', '_')}.csv",
           mime="text/csv",
        )
        
        # Display the data in expanders
        pillar = st.session_state.topical_map_data.get('pillar_topic', 'N/A')
        st.info(f"#### Pillar Topic: {pillar}")

        for i, cluster in enumerate(st.session_state.topical_map_data.get('clusters', [])):
            with st.expander(f"**Cluster {i+1}: {cluster.get('cluster_title', 'N/A')}**", expanded=True):
                pages_data = []
                for page in cluster.get('pages', []):
                    pages_data.append({
                        "Page Topic / Article Title": page.get('page_title', ''),
                        "Keywords": ", ".join(page.get('keywords', [])),
                        "Suggested Word Count": page.get('word_count', '')
                    })
                
                if pages_data:
                    df = pd.DataFrame(pages_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
