import sqlite3
import pandas as pd

gsheetid = "1-rf8nDiJhsZ40EZzKTeRLmsKzJnJvqLWsaONiOdfCwo"

df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv")

data = df.iloc[:, :4]


def write_to_database( df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='replace', index=False)


def EvaluationScore():
    conn = sqlite3.connect('GitHub.db')
    pd.read_sql_query("SELECT * FROM GitHub", conn)
    write_to_database(data, 'Screening', conn)

    conn.commit()

    conn.close()


def get_passed_and_failed_profiles():
    # Connect to the database
    conn = sqlite3.connect('GitHub.db')
    c = conn.cursor()

    # Select the email addresses for passed and failed candidates
    c.execute("SELECT Email_address FROM Screening WHERE PASS_FAIL = 1")
    passed_results = c.fetchall()
    passed_emails = [r[0] for r in passed_results]

    c.execute("SELECT Email_address FROM Screening WHERE PASS_FAIL = 0")
    failed_results = c.fetchall()
    failed_emails = [r[0] for r in failed_results]

    # Close the database connection
    conn.close()

    # Return the tuple of passed and failed email addresses
    return passed_emails, failed_emails

# passed_emails, failed_emails = get_passed_and_failed_profiles()

# # Print the results
# print("Passed emails:")
# print(passed_emails)
#
# print("Failed emails:")
# print(failed_emails)


if __name__ == '__main__':
    EvaluationScore()

# print(data)
