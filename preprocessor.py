import re
import pandas as pd
from datetime import datetime

def convert_to_24hr(time_str):
    try:
        # Try parsing 24-hour format first
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        try:
            # Try 12-hour format
            return datetime.strptime(time_str, '%I:%M %p').time()
        except ValueError:
            # Try other possible formats
            for fmt in ['%I:%M%p', '%I.%M %p', '%I.%M%p', '%I:%M']:
                try:
                    return datetime.strptime(time_str, fmt).time()
                except ValueError:
                    continue
    raise ValueError(f"Could not parse time: {time_str}")

def preprocess(data):
    pattern = r'\[?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),?\s+(\d{1,2}[:\.]\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?)\]?\s*-\s*'
    
    messages = re.split(pattern, data)[3::3]
    dates = []
    times = []
    
    matches = re.finditer(pattern, data)
    for match in matches:
        dates.append(match.group(1))
        times.append(match.group(2))
    
    df = pd.DataFrame({
        'user_message': messages,
        'date': dates,
        'time': times
    })
    
    # Convert dates
    for date_format in ['%d/%m/%y', '%d/%m/%Y', '%m/%d/%y', '%m/%d/%Y', 
                       '%d-%m-%y', '%d-%m-%Y', '%m-%d-%y', '%m-%d-%Y']:
        try:
            df['date'] = pd.to_datetime(df['date'], format=date_format)
            break
        except ValueError:
            continue
    
    # Convert times to 24-hour format
    df['time'] = df['time'].apply(convert_to_24hr)
    
    # Extract user and message
    df['user'] = df['user_message'].apply(lambda x: 
        re.split('([^:]+):', x)[1].strip() if len(re.split('([^:]+):', x)) > 1 
        else 'group_notification')
    
    df['message'] = df['user_message'].apply(lambda x: 
        re.split('([^:]+):', x)[-1].strip() if len(re.split('([^:]+):', x)) > 1 
        else x)
    
    df.drop('user_message', axis=1, inplace=True)
    
    # Extract components with proper time handling
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['time'].apply(lambda x: x.hour)
    df['minute'] = df['time'].apply(lambda x: x.minute)
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    
    df['period'] = df['hour'].apply(lambda x: 
        f"{x:02d}-{(x+1):02d}" if x != 23 else "23-00")
    
    return df
