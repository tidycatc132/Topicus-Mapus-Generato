AI Topical Map Generator with Streamlit and Gemini
This is a Streamlit web application that helps content strategists and SEOs generate comprehensive topical maps for any given subject. It uses the Google Gemini API to construct a content hierarchy, including a main pillar topic, related cluster topics, and specific page/article ideas.

Features
User-Friendly Interface: Simply enter a topic to get started.

Topical Map Construction: Generates a structure of Pillar -> Clusters -> Pages.

Keyword Research: Provides relevant long-tail keywords for each page topic.

Content Guidance: Suggests a target word count for each article.

Interactive Visualization: Displays the topical map as a dynamic, explorable mind map.

Data Export: Allows you to download the entire content plan as a CSV file.

Setup and Installation
1. Prerequisites
Python 3.8 or higher

A Google Gemini API Key. You can get one from Google AI Studio.

2. Clone the Repository
Clone this repository to your local machine:

git clone <your-repo-url>
cd <your-repo-directory>

3. Install Dependencies
Install the required Python libraries using the requirements.txt file:

pip install -r requirements.txt

How to Run the App
Set your API Key: The application requires your Google Gemini API key to function. You will be prompted to enter it in the sidebar of the app when you run it.

Run the Streamlit server: Open your terminal, navigate to the project directory, and run the following command:

streamlit run app.py

Use the App:

Your web browser should open a new tab with the application running.

Enter your Gemini API key in the sidebar.

Type your main topic into the input field.

Click "Generate Topical Map" and wait for the AI to process your request.

Explore the results in the visual mind map or the detailed table view.

Export the data to CSV for use in your content planning tools.
