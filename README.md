## Business Process / Data Requirements
- Analytics team wants to understand **what songs** their **users** are listening to.
- Analytics team wants a **Postgres DB** with tables designed to **optimize queries** on song play analysis.

## Engineering Task
- Create a Postgres DB schema and ETL pipeline for the analysis
  - Explore & import raw data from *JSON* files given by the project
  - Define fact & dimension tables for a star schema for this particular analytic purpose
  - Write an ETL pipeline that imports and transfers data from *JSON* files to tables in Postgres DB
- Test database and ETL pipeline by running some test queires

## Tools Used
- Python 3
- SQL
- [Pandas](https://pandas.pydata.org/docs/index.html#)
- [Psycopg2](https://pypi.org/project/psycopg2/)
- [Postgres DB](https://www.postgresql.org/)
- [LucidChart](https://www.lucidchart.com/)

## Original Data Sources
**Note** that the actual data (in *JSON*) used in this project is a subset of original dataset preprocessed by the course.
1. [Million Song Dataset](http://millionsongdataset.com/)
2. [Event Simulator](https://github.com/Interana/eventsim) based on [Million Song Dataset](http://millionsongdataset.com/)


## Database Schema (Data Warehousing) Design
**User Story**: User *user_id* plays a *song* whose artist is *artist_name* at time *start_time* using *agent*.<br/>
From the above story, we can extract some necessary information/dimentions:

- **Who**: *user* dimension
- **What**: *songs* and *artists* dimension
- **When**: *time* dimension
- **How (many)**: songplay fact
- (More possible dimensions but not used in this project):
	- **Where**: *geo-locations* dimension
	- **How**: *agents* dimension

Since the core business process/metric is an user playing a song, the fact table should store the song play records with 
user/song identifier together with related information about the how and where the song is played. Based on the data and tables 
given in the project, the star schema looks like this (generated using [LucidChart](https://www.lucidchart.com/)): <br/>
![Start Schema](assets/images/ERD.png)


## ETL Process
1. Extract songs data from corresponding *JSON* files and insert them into dimension tables:
 	- *songs*
  	- *artists*
2. Extract users and time data from corresponding *JSON* files and insert them into dimension tables:
  	- *users*
  	- *time*
3. Extract song play records from corresponding *JSON* files and insert them into fact table (and make sure to conform to entity relation constraints):
  	- *songplays*
4. Test the entire ETL process and runing some queries.

## Implementation Details/Notes
* Explicitly declear **FOREIGN KEY** to enforce referential integrity and improve performance, 
check this [link](https://www.linkedin.com/pulse/importance-foreign-key-constraint-tim-miles/)
* Use Standard DataTime format: ``YYYY-MM-DD HH:MM:SS.SSSSS``
* song duration (decimal, per song): ``song_len <= 24 hours``
* latitude range (decimal): ``-90 <= lat_val <=  +90``
* longitude range (decimal): ``-180 <= long_val <= +180``
* hour (int): ``0 <= hour <= 23``
* day (int, leap year has 366 days, the last day being at 365th): ``0 <= day <= 365``
* week (int, 52 weeks in total plus one/two days, ceiling to 53 weeks): ``0 <= week <= 52``
* month (int): ``1 <= month <= 12``
* year (int, the earliest recorded songs were made after 1800s according to [wikipedia](https://en.wikipedia.org/wiki/Sound_recording_and_reproduction) and 
assuming artists and users in the database were not born before 1800s)
	* year from *songs* table ``year >= 1800`` **or** ``year == 0`` (default or not specified)
	* year from *time* table: ``year >= 1800``
* weekday (int): ``0 <= weekday <= 6``
* first/last name of users length: ``1 <= len <= 100``
* artist name length: ``1 <= len <= 200``
* foreign keys should not be ``NULL``, however it will result in producing only one record in fact table *songplays*. Therefore, relaxing the constraints to have only 
attributes ``start_time`` and ``user_id`` as ``NOT NULL`` in fact table *songplays*.

## Run project locally (Mac)

- Install Postgres Database<br/>
``brew install postgresql``
- Install packages
	- Using pip command<br/>
 	``pip install psycopg2``<br/>
 	``pip install pandas``
	- **Or** Using conda environment<br/>
 	``conda install psycopg2``<br/>
 	``conda install pandas``
- (Re) Start Postgres services<br/>
``brew services start postgresql``
- Check if Postgres is installed successfully<br/>
``postgres -V``
- Check Postgres Users/DBs
	- Log in as user **postgres**:<br/>
 	``psql postgres -U postgres``
 	- Display all users/roles:<br/>
 	``\du``
 	- Display all existing databases:<br/>
 	``\list``
 	- Log out:<br/>
 	``\q``
- Create a new user<br/>
	- username: **student**<br/>
	- number of connections (max): **8**<br/>
	- current username (with privilege of creating new users/roles): **postgres**<br/>
``createuser -c 8 -d -P -U postgres student``
- Create default database **studentdb**<br/>
``createdb studentdb -U student``
- Verify the creation of user and database<br/>
	- Log in as user **student**:<br/>
 	``psql postgres -U student``
 	- List databases:<br/>
 	``\list``

## Resources
1. Setup Postgres on Mac: [Getting Started with PostgreSQL on Mac OSX](https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)