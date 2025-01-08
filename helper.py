from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import numpy as np

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    stats = {
        'num_messages': df.shape[0],
        'words': sum(len(message.split()) for message in df['message']),
        'media_messages': df[df['message'].str.contains('<Media omitted>')].shape[0],
        'links': sum(len(extractor.find_urls(message)) for message in df['message']),
        'avg_length': round(np.mean([len(message.split()) for message in df['message']]), 2)
    }
    
    return stats

def fetch_most_busy_user(df):
    user_stats = df[df['user'] != 'group_notification']['user'].value_counts()
    return pd.DataFrame({'user': user_stats.index, 'count': user_stats.values})

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out media messages and group notifications
    df = df[~df['message'].str.contains('<Media omitted>')]
    df = df[df['user'] != 'group_notification']
    
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    
    words = ' '.join([word.lower() 
                     for message in df['message'] 
                     for word in message.split() 
                     if word.lower() not in stop_words])
    
    wc = WordCloud(width=800, height=400, 
                  background_color='white',
                  min_font_size=10,
                  colormap='viridis')
    
    return wc.generate(words)

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter messages
    df = df[~df['message'].str.contains('<Media omitted>')]
    df = df[df['user'] != 'group_notification']
    
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    
    words = [word.lower()
             for message in df['message']
             for word in message.split()
             if word.lower() not in stop_words]
    
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = [c for message in df['message']
              for c in message
              if c in emoji.EMOJI_DATA]
    
    return pd.DataFrame(Counter(emojis).most_common())

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()
    timeline['time'] = timeline.apply(lambda x: f"{x['month']}-{x['year']}", axis=1)
    
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df.groupby('only_date')['message'].count().reset_index()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df.pivot_table(index='day_name',
                         columns='hour',
                         values='message',
                         aggfunc='count').fillna(0)