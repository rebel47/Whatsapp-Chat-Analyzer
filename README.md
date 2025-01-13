# WhatsApp Chat Analyzer

A simple tool to analyze WhatsApp chat exports using Python, Streamlit, and various data visualization libraries. This app processes a WhatsApp chat file (in `.txt` format) and generates insightful statistics and visualizations, including user activity, word clouds, emoji usage, message distribution, and more.

## Features

- **Chat Analysis**: Provides statistics like total messages, words, media shared, links shared, and average message length.
- **Hourly & Daily Activity**: Visualizes message activity on an hourly and daily basis.
- **Word Cloud**: Generates a word cloud based on the chat content.
- **Most Common Words**: Displays the most frequent words in the chat.
- **Emoji Analysis**: Shows the top emojis used in the chat.
- **User Activity**: Analyzes the activity of different users and their message distribution.
- **Timeline**: Visualizes message frequency on a monthly and daily basis.

## Installation

### Requirements

Ensure you have Python 3.7+ installed. You can install the necessary dependencies using `pip`:

```bash
pip install -r requirements.txt
```

The required libraries include:
- Streamlit
- Pandas
- Plotly
- Matplotlib
- Seaborn
- WordCloud
- Emoji
- Urlextract

### Downloading Requirements
You can also create a `requirements.txt` file with the following content:

```txt
streamlit==1.17.0
pandas==1.4.2
plotly==5.8.0
matplotlib==3.5.1
seaborn==0.11.2
wordcloud==1.8.1
emoji==2.2.0
urlextract==1.1.0
```

## Usage

1. **Upload Your WhatsApp Chat**: The app allows you to upload a `.txt` WhatsApp export chat file.
2. **Select User**: After uploading, you can select a specific user to analyze or view the overall chat analysis.
3. **View Insights**: After analyzing, the app provides several insights and visualizations such as:
   - Message frequency over time (monthly and daily).
   - User message distribution.
   - Word cloud and most common words.
   - Emoji usage analysis.
4. **Interactive Plots**: Visualizations are powered by Plotly for interactivity.

### Run the App

To run the app locally, use the following command:

```bash
streamlit run app.py
```

This will start the app and open it in your web browser.

## Code Explanation

### `app.py`

- **Streamlit Interface**: Sets up the main user interface, including file upload, sidebar, and rendering of the analysis results.
- **Data Visualization**: Uses Plotly, Matplotlib, and Seaborn for generating various visualizations like timelines, word clouds, and activity heatmaps.

### `helper.py`

- **Statistics Calculation**: Functions like `fetch_stats` and `fetch_most_busy_user` calculate various statistics based on the chat data.
- **Text Analysis**: Includes functions for generating word clouds, identifying the most common words, and extracting emoji usage.
- **Activity Heatmap**: Creates an activity heatmap based on the user's messaging times.

### `preprocessor.py`

- **Chat Parsing**: Processes the raw WhatsApp chat text file, extracting relevant information such as date, time, user, and message content.
- **Data Preprocessing**: Handles time formatting, date conversion, and other data wrangling tasks to create a DataFrame for analysis.

## Example Output

After uploading a WhatsApp chat file, you will see:

- **Total Messages**, **Words**, **Media Shared**, **Links Shared**, **Average Message Length** for the selected user.
- **Hourly Activity**: A heatmap showing when the user is most active.
- **Monthly and Daily Message Timeline**: Line graphs showing the frequency of messages over time.
- **Word Cloud**: A visualization of the most frequent words.
- **Most Common Words**: A bar chart showing the top 20 most frequent words.
- **Emoji Usage**: A pie chart of the top 10 emojis used by the user.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy analyzing your WhatsApp chats with this tool!
