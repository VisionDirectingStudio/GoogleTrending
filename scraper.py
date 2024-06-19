import pandas as pd
from pytrends.request import TrendReq

def get_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    countries = ['US', 'CA', 'GB', 'AU', 'KR', 'JP', 'CN', 'DE', 'FR', 'NL', 'ES', 'FI', 'DK', 'ZA', 'AR']
    trends_data = []

    for country in countries:
        pytrends.build_payload(kw_list=[''], geo=country)
        trends = pytrends.trending_searches(pn=country)
        trends_data.append({'country': country, 'trends': trends})

    df = pd.DataFrame(trends_data)
    df.to_csv('google_trends.csv', index=False)

if __name__ == '__main__':
    get_google_trends()
