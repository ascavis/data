"""Minor Planet Center asteroid database handling

The database is available at http://minorplanetcenter.net/web_service in
various formats. This module works with the SQL version of the database and
retrieves specific data using SQL queries.

"""

import pymysql as mdb
import sys
import string


STANDARD_COLUMNS = string.join("""
absolute_magnitude
albedo  
albedo_2  
albedo_3  
albedo_4  
albedo_neowise  
albedo_neowise_2  
albedo_neowise_3  
albedo_neowise_4  
aphelion_distance
argument_of_perihelion 
ascending_node
b_minus_v  
binary_object  
delta_v  
diameter  
diameter_2  
diameter_3  
diameter_4  
diameter_neowise  
diameter_neowise_2  
diameter_neowise_3  
diameter_neowise_4  
eccentricity
epoch_jd
inclination
lightcurve_quality
mean_anomaly
name
number
object_type
observations
panstarrs_v_minus_gprime
panstarrs_v_minus_iprime
panstarrs_v_minus_rprime
panstarrs_v_minus_uprime
panstarrs_v_minus_wprime
panstarrs_v_minus_yprime
panstarrs_v_minus_zprime
perihelion_date_jd
period
phase_slope
rc_minus_ic
residual_rms
semimajor_axis
spin_max_amplitude
spin_min_amplitude
spin_period
taxonomy_class
u_minus_b
v_minus_gprime
v_minus_iprime
v_minus_rc
v_minus_rprime
v_minus_uprime
v_minus_wprime
v_minus_yprime
v_minus_zprime
""".split(), ",")


def mpc_db_query(max_amount_of_data=100, parameters_to_limit=[],
        order_by=[], columns=STANDARD_COLUMNS):
    """Generate an SQL query to retrieve data

    TODO: sanitize!!

    """
    # Collect all conditional parts
    query_condition = []
    for n, param in enumerate(parameters_to_limit):
        query_condition.append(param)
        if n < len(parameters_to_limit) - 1:
            query_condition.append(' AND ')
    query_condition = ''.join(query_condition)

    # Collect all order-by parts
    query_order_by = []
    for m, param in enumerate(order_by):
        query_order_by.append(param)
        if m < len(order_by) - 1:
            query_order_by.append(',')
    query_order_by = ''.join(query_order_by)

    # Collect all input to query
    query = 'SELECT {} FROM properties'.format(columns)
    if len(parameters_to_limit) > 0:
        query = (query + ' WHERE ('+str(query_condition)+')')
    if len(order_by) > 0:
        query = (query + ' ORDER BY ' + query_order_by)
    query = (query + ' LIMIT %s' % max_amount_of_data)

    return query


class MpcSqlConnection(object):
    """A connection to the MPC SQL database
    
    Use it like this:

    with MpcSqlConnection(...) as con:
        con.retrieve_data(query)

    """

    def __init__(self, address, user, password, db_name):
        self.__con = mdb.connect(address, user, password, db_name)

    def __enter__(self):
        return self

    def __exit__(self, ty, value, traceback):
        if self.__con:
            self.__con.close()

    def retrieve_data(self, query):
        """Execute an SQL query on the database and retrieve the data"""
        cur = self.__con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        return rows
