# -*- coding: utf-8 -*-

import sys

import psycopg2
import numpy as np

__version__ = "0.0.4"

class Connection:
    def __init__(self, dbname, host, port, user, pwd, **kwargs):
        self.con = psycopg2.connect(dbname=dbname, host=host, port= port,
                                    user=user, password=pwd, **kwargs)
        self.cursor = self.con.cursor()

    def pretty_print(self, header_names, inputs, output=sys.stdout):
        column_headers = header_names.split(', ')
        columns_max_len = np.matrix([[len(str(mx)) for mx in row]
                            for row in inputs + [column_headers]]).max(0).tolist()[0]
        header_line = ' | '.join([ch.ljust(mx) for ch, mx in
                                  zip(column_headers, columns_max_len)])
        print(header_line, file=output)
        print('-' * len(header_line), file=output)

        for column_name in inputs:
            print(' | '.join([str(_c).ljust(hl) for _c, hl in
                              zip(column_name, columns_max_len)]), file=output)

    def auto_rollback(func):
        def rollback_wrapper(self, *args, **kwargs):
            self.con.rollback()
            ret = func(self, *args, **kwargs)
            self.con.rollback()
            return ret
        return rollback_wrapper

    @auto_rollback
    def show_column_names(self, table_name, output=sys.stdout):
        self.cursor.execute("""select * from pg_get_cols('{}')
        cols(view_schema name, view_name name, col_name name, col_type varchar, col_num int);""".format(table_name))
        header_names = 'view_schema name, view_name name, col_name name, col_type varchar, col_num int'
        self.pretty_print(header_names, self.cursor.fetchall(), output)

    @auto_rollback
    def list_all_tables(self, output=sys.stdout):
        query = str("select table_schema, table_name "
                    "from information_schema.tables "
                    "where table_schema "
                    "not in ('information_schema', 'pg_catalog') "
                    "and table_type = 'BASE TABLE' "
                    "order by table_schema, table_name;")
        self.cursor.execute(query)
        self.pretty_print("table_schema, table_name", self.cursor.fetchall(), output)
