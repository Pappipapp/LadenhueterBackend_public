import psycopg2


class Database:
    """
    PostgreSQL Database-Wrapper
    It should always be instantiated using the keyword 'with', in order to ensure a correct initialization as well
        as a correct shut down
    """

    def __init__(self, db_name, user, password, host, port=5432):
        """
        Initializes the parameters for the database
        Remind that no connection is established on initialization, but rather on the entrance of the
            respective 'with'-block

        :param db_name: Name of the database in PostgreSQL
        :param user: Login for PostgreSQL
        :param password: Password for PostgreSQL
        :param host: Ip on which the database is hosted
        :param port: Port on which the database is listening
        """

        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        """
        Connects to the PostgreSQL database when the 'with'-block is entered
        """

        print('Starting database: {}...'.format(self.db_name))

        # Start DB and acquire cursor
        self.db_connection = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password,
                                              host=self.host, port=self.port)
        self.cursor = self.db_connection.cursor()

        # Return the instance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Shuts down the database when the 'with'-block is left
        """

        # Close the DB
        print('Closing database: {}...'.format(self.db_name))
        self.db_connection.close()

    def execute_single_query(self, query, values=None, safe_changes=False):
        """
        Executes a single query on the database and returns all acquired results
        All queries to the database should be executed using this interface or an interface building upon this one

        :param query: Query to execute
        :param values: Values that shall be inserted in the query - if no shall be inserted, pass None or a empty list
        :param safe_changes: Whether to safe (commit) changes - e.g. this should be set for a 'alter' query
        :return: Results of the query
        """

        # Execute the query
        self.cursor.execute(query, values)

        # Safe changes
        if safe_changes:
            self.db_connection.commit()

        try:
            results = self.cursor.fetchall()
        except psycopg2.ProgrammingError:
            # The executed query did not contain a 'Returning'-Statement, so a psycopg2.ProgrammingError is thrown
            # Since this should not be prohibited behaviour, we rather return am empty list of results
            results = []

        return results

    def single_select(self, table_name, columns_to_select, condition_columns=(), condition_values=()):
        """
        Performs a single select on the database

        :param table_name: Table to select from
        :param columns_to_select: Columns to select, provided as iterable - remind that the order of these columns also
            determines the order of the column-values in the result
        :param condition_columns: Columns to put conditions on, provided as iterable - if no conditions are required,
            pass an empty tuple
        :param condition_values: Values against which the columns shall be tested, provided as iterable - it must have
            the same length as condition_columns
        :return: Result of the query
        """
        # We need to select at least a single column
        if len(columns_to_select) < 1:
            raise ValueError('At least a single column has to be selected!')
        # Also, we must have a value for each given column with a condition
        elif len(condition_columns) != len(condition_values):
            raise ValueError('There must be as many column values as condition columns!')

        # Construct base query
        columns = ['{}.{}'.format(table_name, column) for column in columns_to_select]
        query = 'SELECT {} FROM {}'.format(', '.join(columns), table_name)

        # Do we have conditions and therefore need a 'WHERE'-Clause?
        if len(condition_columns) > 0:
            # Build conditions with placeholder, that later will be filled by psycopg
            conditions = ['{}.{} = %s'.format(table_name, column) for column in condition_columns]

            # Add 'WHERE'-clause and conditions
            # Join multiple conditions with 'ANDs'
            query += ' WHERE ' + ' AND '.join(conditions)

        # Execute query and return result
        return self.execute_single_query(query, condition_values, True)

    def single_insert(self, table_name, column_names, values, return_column_index=0):
        """
        Performs a single insert on the database

        :param table_name: Table to select from
        :param column_names: Columns for which values shall be set, provided as iterable - at least 1 column must be
            given
        :param values: Values to insert, provided as iterable - it must be the same length as column_names
        :param return_column_index: Index, which column shall be returned as result - by default, it is set to 0 and
            therefore the first column given in column_names is returned
        :return: Value of the column, which index has been given in return_column_index
        """

        # We must insert at least one value
        if len(column_names) < 1:
            raise ValueError('At least a value needs to be inserted!')
        # Also, we must have a value for each given column and
        elif len(column_names) != len(values):
            raise ValueError('For each column, a value must be provided!')
        # The return column index must be valid
        elif not return_column_index < len(column_names):
            raise ValueError('The return columnn index must be lower then the amount of given columns!')

        # Construct base query
        query = 'INSERT INTO {} ('.format(table_name)

        # Insert column names, separated by a comma each
        query += ', '.join(column_names) + ')'

        # Insert placeholders for values, which will be later filled by psycopg
        query += ' VALUES (' + ', '.join(['%s'] * len(values)) + ')'

        # Return a given column
        query += ' RETURNING {}.{};'.format(table_name, column_names[return_column_index])

        # Execute query and return result
        return self.execute_single_query(query, values, True)

    def remove_row(self, table_name, condition_column, condition_column_value):
        """
        Deletes the row in table_name, where condition_column = condition_column_value
        :param table_name: name of the table, where the query is executed upon
        :param condition_column: After which field the condition is set
        :param condition_column_value: specifies which row to delete: where condition_column = condition_column_value

        :return: Value of the condition_column in the deleted row
        """
        query = 'DELETE FROM {}'.format(table_name)

        query += ' WHERE {} = %s'.format(condition_column)

        query += ' RETURNING {}'.format(condition_column)

        return self.execute_single_query(query, [condition_column_value], True)
