from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extractor = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df["message"].str.contains("<Media omitted>")].shape[0]


    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

   

    return num_messages,len(words),num_media_messages, len(links)



def fetch_most_busy_user(df):
    x = df[df['user'] != 'group_notification']['user'].value_counts().head()
    new_df = round((df[df['user'] != 'group_notification']['user'].value_counts()/df[df['user'] != 'group_notification'].shape[0])*100,2).reset_index().rename(
        columns={'count':'Percent','user':'Name'})
    return x, new_df


def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []

        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color = 'black')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n'] # this line of code is not working I added the <media omiited in stop_hinglist.txt file>

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.demojize(c) != c])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year','month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap