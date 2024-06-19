import pandas as pd
import requests
import os

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
CURRENT_TABLE = 'Current'
HISTORY_TABLE = 'History'

def upload_to_airtable(table_name, data):
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f'Successfully uploaded to {table_name}')
    else:
        print(f'Failed to upload to {table_name}: {response.text}')

def get_current_data():
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{CURRENT_TABLE}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch current data: {response.text}')
        return None

def main():
    # CSV 파일 읽기
    df = pd.read_csv('google_trends.csv')
    
    # 현재 데이터 가져오기
    current_data = get_current_data()
    
    # 데이터 변환 및 업로드
    for _, row in df.iterrows():
        recent_trend = row['trends']
        country = row['country']
        is_different = True
        
        if current_data:
            for record in current_data['records']:
                if record['fields']['country'] == country:
                    if record['fields']['trend_data'] == recent_trend:
                        is_different = False
                    break
        
        if is_different:
            history_record = {
                'fields': {
                    'country': country,
                    'trend_data': recent_trend
                }
            }
            upload_to_airtable(HISTORY_TABLE, {'records': [history_record]})
            
            current_record = {
                'fields': {
                    'country': country,
                    'trend_data': recent_trend
                }
            }
            upload_to_airtable(CURRENT_TABLE, {'records': [current_record]})

if __name__ == '__main__':
    main()
