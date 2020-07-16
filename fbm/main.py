import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
import joblib
from fbm_predict import FBM

header_info = ['league', 'home_score', 'away_score']
companies = ['bet365', 'hg', 'bet10', 'ac',
             'ysb', 'wd',  'bet12', 'bet18', 'ybb', 'pb']
company_odd = ['win', 'draw', 'loss', 'let_up', 'let',
               'let_down', 'size_up', 'size', 'size_down']


def inverse_odd(x):
    if x == 0:
        return 0
    return x


def inverse_let(x):
    if isinstance(x, str):
        vals = x.split('/')
        if(len(vals) == 2):
            return (float(vals[0]) + float(vals[1])) / 2.0
        else:
            float(vals[0])
    return x


def inverse_size(x):
    if isinstance(x, str):
        vals = x.split('/')
        if(len(vals) == 2):
            return (float(vals[0]) + float(vals[1])) / 2.0
        else:
            float(vals[0])
    return x


def wash_data():
    header_companies = []
    header_all_let = []
    header_all_size = []
    for comp in companies:
        header_all_let.append("%s_let" % comp)
        header_all_size.append("%s_size" % comp)
        for odd in company_odd:
            header_companies.append("%s_%s" % (comp, odd))
    df = pd.read_csv('leisu/merge.csv')

    header = header_info + header_companies

    info = df[header].dropna(subset=header_companies, how="all")
    le = LabelEncoder()
    le.fit(info['league'])
    info['league'] = le.fit_transform(info['league'])
    all_let = info[header_all_let]
    info['let_min'] = all_let.min(axis=1)
    info['let_avg'] = all_let.mean(axis=1)
    info['let_max'] = all_let.max(axis=1)
    all_size = info[header_all_size]
    info['size_min'] = all_size.min(axis=1)

    info['y0'] = info.apply(
        lambda x: 1 if x['home_score'] > x['away_score'] else 0, axis=1)
    info['y1'] = info.apply(
        lambda x: 1 if x['home_score'] == x['away_score'] else 0, axis=1)
    info['y2'] = info.apply(
        lambda x: 1 if x['home_score'] < x['away_score'] else 0, axis=1)
    info['y3'] = info.apply(
        lambda x: 1 if x['home_score'] >= x['away_score'] else 0, axis=1)
    info['y4'] = info.apply(
        lambda x: 1 if x['home_score'] + x['let_min'] >= x['away_score'] else 0, axis=1)
    info['y5'] = info.apply(
        lambda x: 1 if x['home_score'] + x['let_avg'] >= x['away_score'] else 0, axis=1)
    info['y6'] = info.apply(
        lambda x: 1 if x['home_score'] + x['let_max'] >= x['away_score'] else 0, axis=1)
    info['y7'] = info.apply(
        lambda x: 1 if x['home_score'] + x['away_score'] > x['size_min'] else 0, axis=1)

    for comp in companies:
        for col in ['win', 'draw', 'loss', 'let_up', 'let_down', 'size_up',  'size_down']:
            col_ = "%s_%s" % (comp, col)
            info[col_] = info[col_].map(inverse_odd)
        let = "%s_let" % comp
        info[let] = info[let].map(inverse_let)
        size = "%s_size" % comp
        info[size] = info[size].map(inverse_size)

    info.fillna(0, inplace=True)

    info.to_csv('data.csv', index=0)
    joblib.dump(le, "label_encoder.pkl")
    print(info.tail())


# 采样相同数量的数据
def sample(df, label):
    df_one = df[(df[label] > 0.5)]
    df_zero = df[(df[label] < 0.5)]
    one_count = len(df_one)
    zero_count = len(df_zero)
    if one_count > zero_count:
        df_one = shuffle(df_one).head(zero_count)
    else:
        df_zero = shuffle(df_zero).head(zero_count)
    
    return shuffle(pd.concat([df_one, df_zero], ignore_index=True))

def train_win():
    header_companies = []
    for comp in companies:
        for odd in ['win', 'draw', 'loss', 'let_up', 'let', 'let_down']:
            header_companies.append("%s_%s" % (comp, odd))
    df = pd.read_csv('data.csv')
    df = sample(df, 'y3')
    x = df[header_companies]
    y = df[['y3']]
    fbm = FBM(len(header_companies), 'win.best.hdf5')
    fbm.train(x, y)


def train_draw():
    header_companies = []
    for comp in companies:
        for odd in ['win', 'draw', 'loss', 'let_up', 'let', 'let_down']:
            header_companies.append("%s_%s" % (comp, odd))
    df = pd.read_csv('data.csv')
    df = sample(df, 'y1')
    x = df[header_companies]
    y = df[['y1']]
    fbm = FBM(len(header_companies), 'draw.best.hdf5')
    fbm.train(x, y)


def train_let(y_label):
    '''
    y_label:
        y4 use min
        y5 use avg
        y6 user max
    '''
    header_companies = []
    for comp in companies:
        for odd in ['win', 'draw', 'loss', 'let_up', 'let', 'let_down']:
            header_companies.append("%s_%s" % (comp, odd))
    df = pd.read_csv('data.csv')
    df = sample(df, y_label)
    x = df[header_companies]
    y = df[[y_label]]
    fbm = FBM(len(header_companies), 'let.best.hdf5')
    fbm.train(x, y)


def train_size():
    header_companies = []
    for comp in companies:
        for odd in ['let_up', 'let', 'let_down', 'size_up', 'size', 'size_down']:
            header_companies.append("%s_%s" % (comp, odd))
    df = pd.read_csv('data.csv')
    df = sample(df, 'y7')
    x = df[header_companies]
    y = df[['y7']]
    fbm = FBM(len(header_companies), 'size.best.hdf5')
    fbm.train(x, y)


def main():
    # wash_data()
    # train_win()
    # train_let('y5')
    train_size()
    # train_draw()


if __name__ == '__main__':
    main()

