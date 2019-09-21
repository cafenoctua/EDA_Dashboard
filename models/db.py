import os
import psycopg2

class Model():
    
    def __init__(self):
        db_env = os.environ.get('DATABASE_URL')
        with psycopg2.connect(db_env) as self.conn:
            self.cur = self.conn.cursor()
    
    def create_table(self, name, **kwargs):
        self.drop_exists_table(name)
        sql_cursur = f"CREATE TABLE {name} ("
        for col in kwargs:
            sql_cursur = sql_cursur + f" {col} {kwargs[col]},"
        sql_cursur = sql_cursur[:len(sql_cursur)-1] +');'
        
        # return sql_cursur
        self.cur.execute(sql_cursur)
        self.conn.commit()

    def drop_exists_table(self, name):
        sql_cursur = f"DROP TABLE IF EXISTS {name};"
        self.cur.execute(sql_cursur)
        self.conn.commit()
    
    def get_columns(self, name):
        sql_cursur = f"SELECT * FROM {name};"
        self.cur.execute(sql_cursur)
        col_name = [col.name for col in self.cur.description]
        return col_name

    def insert(self, name, **kwargs):
        sql_cursur =  f"INSERT INTO {name} "
        col_name = self.get_columns(name)

        # Definition columns values
        column_cursur = '('
        value_cursur = 'VALUES ('
        for col in kwargs:
            if col in col_name:
                column_cursur = column_cursur + f" {col},"
                value_cursur = value_cursur + f" {kwargs[col]},"
            else:
                return f"{col} is not included in {name}"
        column_cursur = column_cursur[:len(column_cursur)-1] +')'
        value_cursur = value_cursur[:len(value_cursur)-1] +')'

        sql_cursur = sql_cursur + column_cursur + ' ' + value_cursur + ';'

        self.cur.execute(sql_cursur)
        self.conn.commit()

    def fetch_table(self, name, **kwargs):
        sql_cursur =  f"SELECT "
        col_name = self.get_columns(name)

        # Definition columns
        column_cursur = '('
        value_cursur = 'VALUES ('
        for col in kwargs:
            if col in col_name:
                column_cursur = column_cursur + f" {col},"
            else:
                return f"{col} is not included in {name}"
        column_cursur = column_cursur[:len(column_cursur)-1] +')'

        sql_cursur = sql_cursur + column_cursur + f" FROM {name}" + ';'

        self.cur.execute(sql_cursur)

        # rows = self.cur.fetchall()
        # print(rows)
        # for row in self.cur:
        #     print(row)

        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
    
if __name__ == '__main__':
    model = Model()
    db_name = 'test'

    table_col = dict(
        test1='INTEGER',
        test2='INTEGER'
    )

    model.create_table(db_name, **table_col)

    print(model.get_columns('test'))

    value = dict()
    for key in table_col:
        value[key] = 0

    model.insert(db_name, **value)

    value = dict()
    for key in table_col:
        value[key] = 1

    model.insert(db_name, **value)

    rows = model.fetch_table(db_name, test1='test1')
    print(f"Row: {rows}")