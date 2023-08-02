import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from q import time_function


def remove_duplicates(df, column_name):
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)
    return df


def remove_null_values(df, column_name):
    df.dropna(subset=[column_name], inplace=True)
    return df


def rename_column(df, old_name, new_name):
    df = df.rename(columns={old_name: new_name})
    return df


def reset_dataframe_index(df):
    df.reset_index(drop=True, inplace=True)
    return df


def count_languages(df, languages_column, new_column):
    df[new_column] = df[languages_column].str.count(',') + 1
    df[new_column] = df[new_column].fillna(0)
    df[new_column] = df[new_column].astype(int)
    return df


def preprocess_data(df):
    df_t = df[['followers', 'number_of_repos', 'achievements']]
    scaler = MinMaxScaler()
    normalized_df = pd.DataFrame(scaler.fit_transform(df_t), columns=df_t.columns)
    return normalized_df


def cluster_data(normalized_df, n_clusters=17, random_state=0):
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state).fit(normalized_df)
    df_cluster = normalized_df.copy()
    df_cluster['cluster_number'] = kmeans.labels_
    return df_cluster


def visualize_clusters(normalized_df):
    tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, random_state=42)
    tsne_result = tsne.fit_transform(normalized_df)
    return tsne_result


def assign_cluster_labels(df, df_cluster):
    df['cluster_number'] = df_cluster['cluster_number']
    df['Position'] = df['cluster_number'].apply(lambda x: 'Developer' if x == 4
    else ('Senior Developer' if x in [16, 0, 9, 14, 8]
          else 'Solution Architect'))
    return df


def write_to_database(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='replace', index=False)


@time_function
def Data_CleanSort():
    conn = sqlite3.connect('GitHub.db')
    df = pd.read_sql_query("SELECT * FROM GitHub", conn)
    df = remove_duplicates(df, 'username')
    df = remove_null_values(df, 'email')
    df = rename_column(df, 'number of repos', 'number_of_repos')
    df = reset_dataframe_index(df)
    df = count_languages(df, 'languages', 'count')
    normalized_df = preprocess_data(df)
    df_cluster = cluster_data(normalized_df)
    tsne_result = visualize_clusters(normalized_df)
    df_labeled = assign_cluster_labels(df, df_cluster)
    write_to_database(df_labeled, 'GithubCleanData', conn)

    conn.commit()

    conn.close()


if __name__ == '__main__':
    Data_CleanSort()
