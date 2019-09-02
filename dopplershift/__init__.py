# -*- coding: utf-8 -*-

import sys

import psycopg2
import numpy as np

__version__ = "0.0.3"

class Connection(psycopg2.extensions.connection):
    def __init__(self, dbname, host, port, user, pwd, **kwargs):
        self.con = psycopg2.connect(dbname=dbname, host=host, port= port,
                                    user=user, password=pwd, **kwargs)

    def show_column_names(self, table_name, output=sys.stdout):
        self.con.rollback()
        cursor = self.con.cursor()
        cursor.execute("""select * from pg_get_cols('{}')
        cols(view_schema name, view_name name, col_name name, col_type varchar, col_num int);""".format(table_name))
        x = cursor.fetchall()
        column_headers = 'view_schema name, view_name name, col_name name, col_type varchar, col_num int'.split(', ')
        columns_max_len = np.matrix([[len(str(mx)) for mx in row] for row in x + [column_headers]]).max(0).tolist()[0]

        header_line = ' | '.join([ch.ljust(mx) for ch, mx in zip(column_headers, columns_max_len)])
        print(header_line, file=output)
        print('-' * len(header_line), file=output)

        for column_name in x:
            print(' | '.join([str(_c).ljust(hl) for _c, hl in zip(column_name, columns_max_len)]), file=output)
        self.con.rollback()
