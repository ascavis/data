#!/usr/bin/python
# -*- coding: utf-8 -*-

# Parser fuer mp_properties, retrieved from http://minorplanetcenter.net/web_service on 11.4.2014 #
# done by Katja :) #

import MySQLdb as mdb
import sys

## needed to create query ##
#max_amount_of_data = 1 #max number of data set to call (protect your poor computer, current DB size ~1GB)
#include_none = 1 #include parameters with value 'none' (0/1) //not implemented yet

parameters_to_limit = ['absolute_magnitude<15','mean_daily_motion>0.2'] #use [] for none (>/</=)
#parameters_to_limit = []

#find parameters with max / min, include DESC to find highest values #use [] for none 
order_by = ['absolute_magnitude ASC']
#order_by = []


def make_query_mpc_db(max_amount_of_data, parameters_to_limit, order_by, columns="*"):
    #(TODO: sanitize!!!)

    #collect all conditional parts
    query_condition = []
    for n, (param) in enumerate(parameters_to_limit): #zip
        query_condition.append(param)
        if (n < len(parameters_to_limit)-1):
            query_condition.append(' AND ')
    query_condition = ''.join(query_condition)

    #collect all order-by parts
    query_order_by = []
    for m, (param) in enumerate(order_by):
        query_order_by.append(param)
        if (m<len(order_by)-1):
            query_order_by.append(',')
    query_order_by = ''.join(query_order_by)

    #collect all input to query
    query = 'SELECT {} FROM properties'.format(columns)
    if (len(parameters_to_limit) > 0):
        query = (query + ' WHERE ('+str(query_condition)+')')
    if (len(order_by) > 0):
        query = (query + ' ORDER BY ' + query_order_by)
    query = (query + ' LIMIT %s' % max_amount_of_data)

    return(query)

#########################################

def retrieve_from_mpc_db(DB_SOURCE,DB_user,DB_pw,DB_name,query):
    #retrieve data
    try:
        con = []
        con = mdb.connect(DB_SOURCE, DB_user, DB_pw, DB_name)

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)

        rows = cur.fetchall()
        desc = cur.description
        return rows

        mpc_data = []
        for row in rows:
            #print(row['inclination_uncertainty'])
            tmp = {}
            mpc_data.append(row)

        return(mpc_data)
        
        
    except mdb.Error, e:
      
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
            
        if con:    
            con.close()

########################################

DB_SOURCE = "192.168.100.1"
DB_user = "root"
DB_pw = "space"
DB_name = "mp_properties"

#def query_mpc_db(DB_SOURCE,DB_user,DB_pw,DB_name,max_amount_of_data=100, parameters_to_limit=[], order_by=[]):
    #TODO: make inputs optional!
import string
columns = string.join("""
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
print columns

import simplejson as json
for i in range(7):
    query = make_query_mpc_db("{} OFFSET {}".format(100000, 100000 * i), [], [], columns)
    mpc_data = retrieve_from_mpc_db(DB_SOURCE,DB_user,DB_pw,DB_name,query)
    #print mpc_data
    with open("data_dump_{}.json".format(i), "w") as json_file:
        json.dump(mpc_data, json_file)
