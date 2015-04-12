#!/usr/bin/python
# -*- coding: utf-8 -*-

# Parser fuer mp_properties, retrieved from http://minorplanetcenter.net/web_service on 11.4.2014 #
# done by Katja :) #

import MySQLdb as mdb
import sys

## needed to create query ##
max_amount_of_data = 3 #max number of data set to call (protect your poor computer, current DB size ~1GB)
#include_none = 1 #include parameters with value 'none' (0/1) //not implemented yet

parameters_to_limit = ['absolute_magnitude<15','mean_daily_motion>0.2'] #use [] for none (>/</=)
#parameters_to_limit = []

#find parameters with max / min, include DESC to find highest values #use [] for none 
order_by = ['absolute_magnitude DESC']
#order_by = []


def make_query_mpc_db(max_amount_of_data, parameters_to_limit, order_by):
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
    query = 'SELECT * FROM properties'
    if (len(parameters_to_limit) > 0):
        query = (query + ' WHERE ('+str(query_condition)+')')
    if (len(order_by) > 0):
        query = (query + ' ORDER BY ' + query_order_by)
    query = (query + ' LIMIT %s' % max_amount_of_data)

    return(query)

#########################################

def  retrieve_from_mpc_db(DB_SOURCE,DB_user,DB_pw,DB_name,query):
    #retrieve data
    try:
        con = []
        con = mdb.connect(DB_SOURCE, DB_user, DB_pw, DB_name)

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)

        rows = cur.fetchall()
        desc = cur.description

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

def query_mpc_db(DB_SOURCE,DB_user,DB_pw,DB_name,max_amount_of_data=100, parameters_to_limit=[], order_by=[]):
    #TODO: make inputs optional!
    query = make_query_mpc_db(max_amount_of_data, parameters_to_limit, order_by)
    mpc_data = retrieve_from_mpc_db(DB_SOURCE,DB_user,DB_pw,DB_name,query)
    return(mpc_data)

########################################
