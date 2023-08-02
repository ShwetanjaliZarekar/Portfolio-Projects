import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from q import time_function


def preprocess_data(df):
    df_t = df[['followers', 'number_of_repos', 'achievements', 'count']]
    scaler = MinMaxScaler()
    normalized_df = pd.DataFrame(scaler.fit_transform(df_t), columns=df_t.columns)
    return normalized_df


def score_assign(normalized_df, df):
    df['score'] = ''
    df['score'] = (normalized_df['followers'] * 0.25 + normalized_df['number_of_repos'] * 0.25 +
                   normalized_df['achievements'] * 0.25 + normalized_df['count'] * 0.25)
    return df


def take_user_input(df):
    while True:
        profile = input("Please enter the Job Profile: ")
        if profile in ['Solution Architect', 'Senior Developer', 'Developer']:
            df_filtered = df.loc[df['Position'] == profile].copy()
            df_filtered = df_filtered.sort_values('score', ascending=False)
            df_filtered.reset_index(drop=True, inplace=True)
            df_filtered = df_filtered.iloc[:10]
            # mails_list = df_filtered['email'].tolist()
            # pd.set_option('display.max_columns', 12)
            return df_filtered,  # mails_list
        else:
            print('Please enter a valid profile.')


@time_function
def SelectionOfProfile(mails_list=None):
    conn = sqlite3.connect('GitHub.db')
    df = pd.read_sql_query("SELECT * FROM GithubCleanData", conn)
    normalized_df = preprocess_data(df)
    df = score_assign(normalized_df, df)
    df_fil = take_user_input(df)
    print(df_fil)
    # print(mails_list)


if __name__ == '__main__':
    SelectionOfProfile()
