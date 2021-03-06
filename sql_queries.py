# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

# fact table: songplays
songplay_table_create = (
"""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id bigserial  PRIMARY KEY,
    start_time  timestamp  NOT NULL REFERENCES time (start_time),
    user_id     bigint     NOT NULL REFERENCES users (user_id),
    level       varchar,
    song_id     varchar    REFERENCES songs (song_id),
    artist_id   varchar    REFERENCES artists (artist_id),
    session_id  bigint,
    location    varchar,
    user_agent  varchar
);
""")

# dim table: users
user_table_create = (
"""
CREATE TABLE IF NOT EXISTS users (
    user_id      bigint        PRIMARY KEY,
    first_name   varchar(100)  NOT NULL,
                 CONSTRAINT first_name_len_min
                 CHECK(LENGTH(first_name) >= 1),
    last_name    varchar(100)  NOT NULL,
                 CONSTRAINT last_name_len_min
                 CHECK(LENGTH(last_name) >= 1),
    gender       varchar(20),
    level        varchar(20)
);
""")

# dim table: songs
song_table_create = (
"""
CREATE TABLE IF NOT EXISTS songs (
    song_id    varchar         PRIMARY KEY,
    title      varchar         NOT NULL,
    artist_id  varchar         NOT NULL,
    year       int             NOT NULL DEFAULT 0,
               CONSTRAINT song_year
               CHECK(year >= 1800 OR year = 0),
    duration   DECIMAL(10, 5)  NOT NULL,
               CONSTRAINT duration_range
               CHECK(duration BETWEEN 0.00000 AND 86400.00000)
);
""")

# dim table: artists
artist_table_create = (
"""
CREATE TABLE IF NOT EXISTS artists (
    artist_id  varchar       PRIMARY KEY,
    name       varchar(200)  NOT NULL,
               CONSTRAINT artist_name_len_min
               CHECK(LENGTH(name) >= 1),
    location   varchar,
    latitude   DECIMAL(9, 6),
               CONSTRAINT latitude_range
               CHECK(latitude BETWEEN -90.000000 AND 90.000000),
    longitude  DECIMAL(9, 6),
               CONSTRAINT longitude_range
               CHECK(longitude BETWEEN -180.000000 AND 180.000000)
);
""")

# dim table: time
time_table_create = (
"""
CREATE TABLE IF NOT EXISTS time (
    start_time  timestamp  PRIMARY KEY,
    hour        smallint   NOT NULL,
                CONSTRAINT hour_range
                CHECK(hour BETWEEN 0 AND 23),
    day         smallint   NOT NULL,
                CONSTRAINT day_range
                CHECK(day BETWEEN 0 AND 365),
    week        smallint   NOT NULL,
                CONSTRAINT week_range
                CHECK(week BETWEEN 0 AND 52),
    month       smallint   NOT NULL,
                CONSTRAINT month_range
                CHECK(month BETWEEN 1 AND 12),
    year        smallint   NOT NULL,
                CONSTRAINT year_range
                CHECK(year >= 1800),
    weekday     smallint   NOT NULL,
                CONSTRAINT weekday_range
                CHECK(weekday BETWEEN 0 AND 6)
);
""")

# INSERT RECORDS

user_table_insert = (
"""
INSERT INTO users (user_id, first_name, last_name, gender, level) 
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (user_id)
DO UPDATE SET level = excluded.level;
""")

song_table_insert = (
"""
INSERT INTO songs (song_id, title, artist_id, year, duration) 
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING;
""")

artist_table_insert = (
"""
INSERT INTO artists (artist_id, name, location, latitude, longitude) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO NOTHING;
""")

time_table_insert = (
"""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING;
""")

songplay_table_insert = (
"""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")


# find song_id and artist_id that match (artist_name, song_name, song_len)

song_select = (
"""
SELECT songs.song_id, sub.artist_id
  FROM songs
  JOIN (SELECT artists.artist_id
        FROM artists
       WHERE artists.name = %(artist_name)s
       ) AS sub
    ON songs.artist_id = sub.artist_id
 WHERE songs.title = %(song_name)s 
   AND songs.duration = %(song_len)s;
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]