import pymysql
import pandas as pd
import os

# Read local csv file
worldcup_df = pd.read_csv('./world_cup.csv', sep=';')

# Configure DB connection
host = 'my-first-db.czvdsqxwglyt.us-east-1.rds.amazonaws.com'
port = 3306
dbname = 'tutorial'
user = os.environ.get('rds_user')
password = os.environ.get('rds_password')

# Connect to the DB
connection = pymysql.connect(host,
                             user=user,
                             port=port,
                             passwd=password,
                             db=dbname)


# Create table if it does not exist
create_table = f"""CREATE TABLE IF NOT EXISTS {dbname}.WORLD_CUP(
                                    YEAR INT,
                                    WINNER VARCHAR(63),
                                    COUNTRY VARCHAR(63),
                                    RUNNERS_UP VARCHAR(63),
                                    THIRD VARCHAR(63),
                                    FOURTH VARCHAR(63),
                                    GOALS_SCORED INT,
                                    QUALIFIED_TEAMS INT,
                                    MATCHES_PLAYED INT,
                                    ATTENDANCE FLOAT
    );"""

try:
    with connection.cursor() as cursor:
        cursor.execute(create_table)
except Exception as e:
    print("EXCEPTION: ", e)


# Insert data frame into table
try:
    with connection.cursor() as cursor:
        for index, row in worldcup_df.iterrows():
            insert_df = f"""INSERT INTO {dbname}.WORLD_CUP VALUES(
                                                                    {row["Year"]},
                                                                    '{row["Winner"]}',
                                                                    '{row["Country"]}', 
                                                                    '{row["Runners-Up"]}',
                                                                    '{row["Third"]}',
                                                                    '{row["Fourth"]}',
                                                                    {row["GoalsScored"]},
                                                                    {row["QualifiedTeams"]},
                                                                    {row["MatchesPlayed"]},
                                                                    {row["Attendance"]}
                                                                );"""
            connection.commit()
            cursor.execute(insert_df)

except Exception as e:
    print("EXCEPTION:", e)

print("Data was inserted successfully")

