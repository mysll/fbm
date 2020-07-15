import pandas as pd
import time
import datetime
import numpy as np


def split_file(csv_file):
    print(csv_file)
    df = pd.read_csv(csv_file)
    df = df.drop(['jc', 'lb', 'snai', 'wl', 'iw'], axis=1)
    df_info = df[['match_time', 'jc_order',
                  'league', 'home_team', 'away_team']]
    df_score = df[['score']]
    df_odds = df[['bet365', 'hg', 'bet10', 'ms', 'ac',
                  'ysb', 'wd',  'bet12', 'lj', 'yh', 'bet18', 'ybb', 'pb']]

    df_odds.fillna('nan,nan,nan,nan,nan,nan,nan,nan,nan', inplace=True)
    companies = ['bet365', 'hg', 'bet10', 'ms', 'ac',
                 'ysb', 'wd',  'bet12', 'lj', 'yh', 'bet18', 'ybb', 'pb']

    cols = ['win', 'draw', 'loss', 'let_up', 'let',
            'let_down', 'size_up', 'size', 'size_down']

    df_score = df_score['score'].str.split('-', expand=True)
    df_score.rename(columns={0: 'home_score', 1: "away_score"}, inplace=True)
    df_info = df_info.join(df_score)

    for x in companies:
        df_ = df_odds[x].str.split(',', expand=True)
        col_name = ["%s_%s" % (x, col) for col in cols]
        df_.rename(columns={i: c for (i, c) in list(
            enumerate(col_name))}, inplace=True)
        df_info = df_info.join(df_)

    df_info.to_csv("cleanout/"+csv_file, index=0)


def merge_all():
    start = datetime.datetime.strptime("201701", "%Y%m")
    end = datetime.datetime.strptime("202006", "%Y%m")
    out = None
    while start <= end:
        csv_file = "odd-%s.csv" % start.strftime("%Y%m")
        month = start.month + 1
        year = start.year
        if month == 13:
            month = 1
            year += 1
        start = datetime.datetime(month=month, year=year, day=1)
        df = pd.read_csv('cleanout/' + csv_file)
        if out is None:
            out = df
            continue
        out = pd.concat([out, df], ignore_index=True)
        
    out.to_csv("merge.csv", index=0)


def main():
    start = datetime.datetime.strptime("201701", "%Y%m")
    end = datetime.datetime.strptime("202006", "%Y%m")
    while start <= end:
        csv_file = "odd-%s.csv" % start.strftime("%Y%m")
        split_file(csv_file)
        month = start.month + 1
        year = start.year
        if month == 13:
            month = 1
            year += 1
        start = datetime.datetime(month=month, year=year, day=1)


if __name__ == '__main__':
    merge_all()
