import inspect


def orm(cursor, dto_type):
    # the following line retrieve the argument names of the constructor
    args : list[str] = list(inspect.signature(dto_type.__init__).parameters.keys())

    # the first argument of the constructor will be 'self', it does not correspond
    # to any database field, so we can ignore it.
    args : list[str] = args[1:]

    # gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        # dto_type is a class, its __name__ field contains a string representing the name of the class.
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self._table_name, column_names, qmarks)

        self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)
    
    def find_all_asc(self, sort_key):
        c = self._conn.cursor()
        
        # Ensure the results are always sorted in ascending order by the chosen key
        query = f'SELECT * FROM {self._table_name} ORDER BY {sort_key} ASC'
    
        c.execute(query)
        
        # Assuming 'orm' is a function that processes the result set
        return orm(c, self._dto_type)


    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
 
        stmt = 'SELECT * FROM {} WHERE {}' \
               .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))
 
        c = self._conn.cursor()
        c.execute(stmt, params)
        return orm(c, self._dto_type)

    def delete(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
 
        stmt = 'DELETE FROM {} WHERE {}' \
               .format(self._table_name,' AND '.join([col + '=?' for col in column_names]))
 
        self._conn.cursor().execute(stmt, params)

    #UPDATE: as seen in PS 13
    def update(self, set_values, **cond):
        set_column_names = set_values.keys()
        set_params = list(set_values.values())  # Convert dict_values to list

        cond_column_names = cond.keys()
        cond_params = list(cond.values())  # Convert dict_values to list

        params = set_params + cond_params  

        stmt = 'UPDATE {} SET {} WHERE {}'.format(
            self._table_name,
            ', '.join([col + '=?' for col in set_column_names]),
            ' AND '.join([col + '=?' for col in cond_column_names])
        )

        self._conn.execute(stmt, params)
