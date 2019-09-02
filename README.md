# Dopplershift

Pythonic SQL for mere mortals.

# Install

```
pip install -U dopplershift
```


# Usage


```python
from dopplershift import Connection

host   = 'rayleigh.3onystnrm1rn.us-east-1.redshift.amazonaws.com'
dbname = 'testing'
port   = '1234'
user   = 'alvations'
pwd    = 'JjMKkdW8vJABswyT'

con = Connection(dbname, host, port, user, pwd)
con.show_column_names('testing.data')
```

[out]:

```
view_schema name | view_name name | col_name name       | col_type varchar            | col_num int
---------------------------------------------------------------------------------------------------
testing          |      data      | id                  | integer                     | 1          
testing          |      data      | text                | character varying(1024)     | 2          
testing          |      data      | language            | character varying(3)        | 4          
testing          |      data      | timestamp           | timestamp without time zone | 5          
```

###

```
# Get column names.
>>> con.get_column_names('testing.data')
('id', 'text', 'language', 'timestamp')

# Get top N rows from table.
>>> con.topn_rows('testing.data', n=3, column_names="id, text, language")
[(1, "hello world", "en"), (2, "hallo welt", "de"), (3, "你好，世界。", "zh")]

# Execute queries and fetch results.
>>> con.execute_fetchall("SELECT TOP 2 * FROM testing.data")
[ (1, "hello world", "en", datetime.datetime(2019, 9, 2, 14, 5, 58)),
  (2, "hallo welt", "de", datetime.datetime(2019, 9, 2, 14, 6, 15)) ]

# Show all tables in DB.
>>> con.show_all_tables()
table_schema  | table_name                                          
--------------+----------------
testing       | data
stagging      | results
production    | results
```
