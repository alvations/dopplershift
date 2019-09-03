# -*- coding: utf-8 -*-

import sys

import psycopg2
import numpy as np

__version__ = "0.0.5"

class Connection:
    def __init__(self, dbname, host, port, user, pwd, **kwargs):
        self.con = psycopg2.connect(dbname=dbname, host=host, port= port,
                                    user=user, password=pwd, **kwargs)
        self.cursor = self.con.cursor()

    def pretty_print(self, column_names, inputs, output=sys.stdout):
        column_headers = column_names.split(', ')
        columns_max_len = np.matrix([[len(str(mx)) for mx in row]
                            for row in inputs + [column_headers]]).max(0).tolist()[0]
        header_line = ' | '.join([ch.ljust(mx) for ch, mx in
                                  zip(column_headers, columns_max_len)])
        # Pretty separator line.
        separator_line = list('-' * len(header_line))
        for idx, ch in enumerate(header_line):
            if ch == '|':
                separator_line[idx] = "+"
        separator_line = ''.join(separator_line)
        # Actual printing of header and separator line.
        print(header_line, file=output)
        print(separator_line, file=output)
        # Actual printing of columns and details.
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

    def rollback(self):
        self.con.rollback()

    @auto_rollback
    def execute_fetchall(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    @auto_rollback
    def topn_rows(self, table_name, n=10, column_names="*", output=sys.stdout):
        if column_names == "*":
            column_names = ', '.join(self.get_column_names(table_name))
        self.cursor.execute(f"SELECT TOP {n} {column_names} from {table_name};")
        ##self.pretty_print(column_names, self.cursor.fetchall(), output)
        return self.cursor.fetchall()

    @auto_rollback
    def get_column_names(self, table_name):
        self.cursor.execute("""select * from pg_get_cols('{}')
        cols(view_schema name, view_name name, col_name name, col_type varchar, col_num int);""".format(table_name))
        results = self.cursor.fetchall()
        return list(zip(*results))[2]

    @auto_rollback
    def show_column_names(self, table_name, output=sys.stdout):
        self.cursor.execute("""select * from pg_get_cols('{}')
        cols(view_schema name, view_name name, col_name name, col_type varchar, col_num int);""".format(table_name))
        column_names = 'view_schema name, view_name name, col_name name, col_type varchar, col_num int'
        self.pretty_print(column_names, self.cursor.fetchall(), output)

    @auto_rollback
    def show_all_tables(self, output=sys.stdout):
        query = str("select table_schema, table_name "
                    "from information_schema.tables "
                    "where table_schema "
                    "not in ('information_schema', 'pg_catalog') "
                    "and table_type = 'BASE TABLE' "
                    "order by table_schema, table_name;")
        self.cursor.execute(query)
        self.pretty_print("table_schema, table_name", self.cursor.fetchall(), output)
