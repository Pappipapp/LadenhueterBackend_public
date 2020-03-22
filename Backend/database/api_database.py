from database import config
from database.database import Database

"""
Configuration for the app-database
"""
api_db_config = config['api-database']


class APIDatabase(Database):
    """
    Database-Wrapper for API purposes
    It should always be instantiated using the keyword 'with', in order to ensure a correct initialization as well
        as a correct shut down
    """

    def __init__(self):
        """
        Initializes the parameters for the database which are provided in the configuration
        Remember that no connection is established on initialization, but rather on the entrance of the
            respective 'with'-block
        """

        super().__init__(api_db_config['db_name'], api_db_config['user'], api_db_config['password'],
                         api_db_config['host'], api_db_config['port'])

    def get_reservations_for_market(self, market_id):
        """
        Retrieves all reservations at market ID

        :param market_id: ID of a market
        :return: timestamps of starting time of the market @id
        """
        return self.single_select('reservations', ['start_time'], ['market_id'], [market_id])

    def make_reservation(self, user_id, market_id, reservation_id, start_time):
        """
        Safes a reservation in the reservations table in the db

        :param user_id: anonymized ID of a user, that makes the reservation
        :param market_id: the ID of the market, where reservation occurs
        :param reservation_id: ID of this specific reservation
        :param start_time: the timeslot, that is taken
        :return:
        """

        return self.single_insert('reservations',
                                  ['reservation_id', 'market_id', 'user_id', 'start_time'],
                                  [reservation_id, market_id, user_id, start_time],
                                  return_column_index=0)

    def safe_market(self, market_id, address, name, latitude, longitude):
        """
        Safes a market to the db

        :param market_id: specifies market
        :param address: specifies market
        :param name: specifies market
        :param latitude: specifies market
        :param longitude: specifies market
        :return:
        """

        # Is the market already in the db?
        market_in_db = self.single_select('markets', ['market_id'], ['market_id'], [market_id])

        # If not, safe it
        if len(market_in_db) == 0:
            return self.single_insert('markets',
                                      ['market_id', 'name', 'latitude', 'longitude', 'address'],
                                      [market_id, name, latitude, longitude, address],
                                      return_column_index=0)
        # Else return "Error Code"
        else:
            return 1

    def revoke_reservation(self, reservation_id):
        """

        :param reservation_id:
        :return:
        """

        return self.remove_row('reservations', 'reservation_id', reservation_id)


