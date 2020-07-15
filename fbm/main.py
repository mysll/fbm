import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

header_info = ['league', 'home_score', 'away_score']
companies = ['bet365', 'hg', 'bet10', 'ac',
             'ysb', 'wd',  'bet12', 'bet18', 'ybb', 'pb']
company_odd = ['win', 'draw', 'loss', 'let_up', 'let',
               'let_down', 'size_up', 'size', 'size_down']


def wash_data():
    header_companies = []
    for comp in companies:
        for odd in company_odd:
            header_companies.append("%s_%s" % (comp, odd))
    df = pd.read_csv('leisu/merge.csv')

    header = header_info + header_companies

    info = df[header].dropna(subset=header_companies, how="all")
    le = LabelEncoder()
    le.fit(info['league'])
    info['league'] = le.fit_transform(info['league'])
    info.to_csv('data.csv')
    joblib.dump(le, "label_encoder.pkl")


def load_data():
    header_companies = []
    for comp in companies:
        for odd in company_odd:
            header_companies.append("%s_%s" % (comp, odd))
    header = header_info + header_companies
    df = pd.read_csv('data.csv')
    df.fillna(0, inplace=True)
    print(df.head())


def main():
    load_data()


if __name__ == '__main__':
    main()
