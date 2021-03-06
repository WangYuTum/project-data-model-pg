import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process and extract information about songs and artists from the given JSON file 
    and insert songs and artists data into the corresponding tables.

    Arg(s):
        cur: cursor of the database connection
        filepath: filepath of the JSON file
    """
    try:
        df = pd.DataFrame(pd.read_json(filepath, typ='series').to_dict(), index=[0])
    except Exception as e:
        print('Error reading {}: {}'.format(filepath, e))

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = song_data.values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_data.values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process and extract information about users, timestamps and songplay records from the given JSON file 
    and insert users, timestamps and songplay data into the corresponding tables.

    Arg(s):
        cur: cursor of the database connection
        filepath: filepath of the JSON file
    """
    try:
        df = pd.read_json(filepath, lines=True)
    except Exception as e:
        print('Error reading {}: {}'.format(filepath, e))

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['datetime'] = pd.to_datetime(df['ts'], unit='ms')
    df_dt = df['datetime']
    
    # insert time data records
    time_data = (df_dt, df_dt.dt.hour, df_dt.dt.day, df_dt.dt.weekofyear, \
                 df_dt.dt.month, df_dt.dt.year, df_dt.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, {'song_name': row.song, 'artist_name': row.artist, 'song_len':row.length})
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.datetime, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Process the raw data (JSON files) and insert data into database by calling func.

    Arg(s):
        cur: cursor of the database connection
        conn: connection to the database
        filepath: directory to a collection of files to be processed by func
        func: the function to be called to process the files within filepath
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()