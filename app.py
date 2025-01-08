import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def configure_page():
    st.set_page_config(page_title="WhatsApp Analyzer", layout="wide")
    st.markdown("""
        <style>
        .main { padding: 2rem }
        .stTitle { color: #2e7d32 }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.title("WhatsApp Chat Analyzer")
        st.text("Developed By: Mohammad Ayaz Alam")
        uploaded_file = st.file_uploader("Choose a WhatsApp chat export file", type=["txt"])
        return uploaded_file

def render_stats(stats, selected_user):
    st.title(f"Chat Analysis for {selected_user}")
    
    cols = st.columns(5)
    metrics = [
        ("Total Messages", stats['num_messages'], "📝"),
        ("Total Words", stats['words'], "📚"),
        ("Media Shared", stats['media_messages'], "🖼️"),
        ("Links Shared", stats['links'], "🔗"),
        ("Average Message Length", stats['avg_length'], "📊")
    ]
    
    for col, (title, value, emoji) in zip(cols, metrics):
        with col:
            st.metric(label=f"{emoji} {title}", value=value)

def render_timeline(timeline_data, daily_data):
    tab1, tab2 = st.tabs(["Monthly Activity", "Daily Activity"])
    
    with tab1:
        fig = px.line(timeline_data, x='time', y='message', 
                      title='Monthly Message Timeline',
                      labels={'message': 'Number of Messages', 'time': 'Month'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.line(daily_data, x='only_date', y='message',
                      title='Daily Message Timeline',
                      labels={'message': 'Number of Messages', 'only_date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)

def main():
    configure_page()
    uploaded_file = render_sidebar()

    if uploaded_file:
        try:
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode("utf-8")
            df = preprocessor.preprocess(data)
            
            user_list = df['user'].unique().tolist()
            user_list = [user for user in user_list if user != 'group_notification']
            user_list.sort()
            user_list.insert(0, 'Overall')
            
            selected_user = st.sidebar.selectbox("Show Analysis for", user_list)
            
            if st.sidebar.button("Analyze"):
                stats = helper.fetch_stats(selected_user, df)
                render_stats(stats, selected_user)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Hourly Activity")
                    hourly_data = helper.activity_heatmap(selected_user, df)
                    fig = px.imshow(hourly_data, 
                                  labels=dict(x="Hour of Day", y="Day of Week", color="Messages"),
                                  aspect="auto")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if selected_user == 'Overall':
                        st.subheader("User Activity Distribution")
                        user_data = helper.fetch_most_busy_user(df)
                        fig = px.pie(user_data, values='count', names='user',
                                   title='Message Distribution by User')
                        st.plotly_chart(fig, use_container_width=True)
                
                render_timeline(helper.monthly_timeline(selected_user, df),
                              helper.daily_timeline(selected_user, df))
                
                # In app.py, replace the col3, col4 section with:

                col3, col4 = st.columns(2)
                with col3:
                    st.subheader("Word Cloud")
                    wordcloud = helper.create_wordcloud(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.imshow(wordcloud)
                    ax.axis('off')
                    st.pyplot(fig)
                
                with col4:
                    st.subheader("Most Common Words")
                    common_words = helper.most_common_words(selected_user, df)
                    fig = px.bar(common_words, x=1, y=0, orientation='h',
                               labels={'1': 'Count', '0': 'Word'})
                    st.plotly_chart(fig, use_container_width=True)

                # Emoji analysis at the bottom for better layout
                st.subheader("Emoji Usage")
                emoji_data = helper.emoji_helper(selected_user, df)
                if not emoji_data.empty:
                    fig = px.pie(emoji_data.head(10), values=1, names=0,
                               title='Top 10 Emojis Used')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No emojis found in the selected messages")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please ensure you've uploaded a valid WhatsApp chat export file")

if __name__ == "__main__":
    main()