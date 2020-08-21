## Business Process / Data Requirements
- Analytics team wants to understand **what songs** their **users** are listening to.
- Analytics team wants a **Postgres DB** with tables designed to **optimize queries** on song play analysis.

## Engineering Task
- Create a Postgres DB schema and ETL pipeline for the analysis
  - Explore & import raw data from *JSON* files
  - Define fact & dimension tables for a star schema for this particular analytic purpose
  - Write an ETL pipeline that imports and transforms data from *JSON* files to tables in Postgres DB
- Test database and ETL pipeline by running pre-defined queires

## Tools Used
- Python 3
- SQL
- Pandas
- Psycopg2
- Postgres DB 

## Data Sources
1. [Million Song Dataset](http://millionsongdataset.com/)
2. [Event Simulator](https://github.com/Interana/eventsim) based on [Million Song Dataset](http://millionsongdataset.com/)


## Data Warehouse Design and ETL Process
* Explicitly declear FOREIGN KEY to "enforce referential integrity and improve performance"
   link: https://www.linkedin.com/pulse/importance-foreign-key-constraint-tim-miles/
* Use DataTime format: YYYY-MM-DD HH:MM:SS.SSSSS
* Song duration (decimal) assumption: <= 24 hours / song
* latitude range (decimal) between: -90,  +90
* longitude range (decimal) between: -180, +180
* hour (int) bewteen: 0, 23
* day (int) between (leap year has 366 days with the last day being at 365th): 0, 365
* week (int) between (52 weeks in total plus one/two days, therefore ceiling 53 weeks): 0, 52
* month (int): 0 ~ 11
* year (int, the earliest recorded songs were made after 1800s according to wikipedia and assuming artists/users were not born before 1800s): >= 1800
  link: https://en.wikipedia.org/wiki/Sound_recording_and_reproduction
* weekday (int): 0 ~ 6
* first/last name of users length: 1 ~ 100
* artist name length: 1 ~ 200

* foreign keys as not null ???

### Run project locally (Mac)

- Install Postgres Database
brew install postgresql
- Install packages
 - Using pip command
 pip install psycopg2
 pip install pandas
 - Using conda environment
 conda install psycopg2
 conda install pandas
- (Re)Start Postgres services
brew services start postgresql
- Check if Postgres is installed successfully
postgres -V
- Check Postgres Users/DBs
 - Log in as user: postgres
 psql postgres -U postgres
 - Display users
 \du
 - Display Databases:
 \list
 - Log out
 \q
- Create a new user
username: student
number of connections (max): -c 8
current username: postgres
create username with password: -P
createuser -c 8 -d -P -U postgres student
- Create default database studentdb
createdb studentdb -U student
- Verify the creation of user and database
 - Log in as user: student
 psql postgres -U student
 - List databases
 \list


