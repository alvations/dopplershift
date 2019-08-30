# Dopplershift

Pythonic SQL for mere mortals.


# Usage:

```
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
