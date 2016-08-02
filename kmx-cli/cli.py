#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlparse
from sqlparse.tokens import DML, Keyword, Whitespace, Wildcard, Comparison
from sqlparse.sql import IdentifierList, Identifier, Where
from sqlparse.sql import Comparison as sqlcomp

import requests
import json
import argparse

from colorama import init, Fore, Back
init(autoreset=True)

class cli:

    def __init__(self):
        print 'KMX CLI is running ...'
        # self.url = 'http://192.168.130.2/cloud/qa3/kmx/v2'

    def isDML(self, sql):
        tokens = sql.tokens
        firstToken = tokens[0]
        if firstToken.ttype is not DML:
            print 'The SQL is not a select statement ...'
            return False
        else:
            return True

    def getColumnAndTables(self, sql):
        ids = []
        # print sql.tokens
        for token in sql.tokens:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    ids.append(identifier.get_name())
            elif isinstance(token, Identifier):
                ids.append(token.value)
            elif token.ttype is Keyword and token.value.upper() == 'FROM':
                ids.append(token.value)
            elif token.ttype is Wildcard:
                ids.append(token.value)
        return ids

    def getColumns(self, sql):
        if self.isDML(sql) == False:
            return None
        ids = self.getColumnAndTables(sql)
        columns = []
        for id in ids:
            if id.upper() == 'FROM':
                break
            columns.append(id)
        return columns

    def getTables(self, sql):
        if self.isDML(sql) == False:
            return None
        ids = self.getColumnAndTables(sql)
        columns = self.getColumns(sql)
        tables = []
        for id in ids:
            if id.upper() <> 'FROM' and id not in columns:
                tables.append(id)
        return tables

    def getWhere(self, sql):
        if self.isDML(sql) == False:
            return None
        tokens = sql.tokens
        for token in tokens:
            if isinstance(token, Where):
                # print token.value
                pointQueryValue = {}
                pointQuery = {"sampleTime": pointQueryValue}

                rangeQueryStart = {}
                rangeQueryEnd = {}
                rangeQuery = {"timeRange": {"start": rangeQueryStart, "end": rangeQueryEnd}}

                whereToekns = token.tokens
                # print whereToekns
                # If there is comparison token in where token
                hasComparisonToken = False
                for token in whereToekns:
                    if isinstance(token, sqlcomp):
                        hasComparisonToken = True
                        # print token.value
                        comparisonTokens = token.tokens
                        # id = None
                        # comp = None
                        # value = None
                        for ctoken in comparisonTokens:
                            # print ctoken.ttype
                            if isinstance(ctoken, Identifier):
                                # print ctoken.value
                                id = ctoken.value
                            elif ctoken.ttype is Comparison:
                                # print ctoken.value
                                comp = ctoken.value
                            elif ctoken.ttype is not Whitespace:
                                # print ctoken.value
                                value = ctoken.value
                        # tell if comparion is "=", if yes, the query is a point query
                        # print '===='
                        # print comp
                        value = str(value).replace("'", "")
                        # print value
                        if comp == '=':
                            pointQueryValue.update({id: value})
                        elif comp == '>':
                            rangeQueryStart.update({id: value})
                        elif comp == '<':
                            rangeQueryEnd.update({id: value})

                if hasComparisonToken == False:
                    id = None
                    comp = None
                    value = None
                    for token in whereToekns:
                        if token.ttype is Keyword and (token.value.upper() == 'WHERE' or token.value.upper() == 'AND' or token.value.upper() == 'OR'):
                            continue
                        # if token.ttype is Keyword and token.value.upper() == 'AND':
                        #     continue
                        if token.ttype is Whitespace:
                            continue

                        if token.ttype is Keyword:
                            id = token.value
                        elif token.ttype is Comparison:
                            comp = token.value
                        elif token.ttype is not Whitespace:
                            value = token.value

                        if id <> None and value <> None:
                            if comp == '=':
                                pointQueryValue.update({id: value})
                            elif comp == '>':
                                rangeQueryStart.update({id: value})
                            elif comp == '<':
                                rangeQueryEnd.update({id: value})


                    # print pointQueryValue
                    # print rangeQueryStart
                    # print rangeQueryEnd
                if pointQueryValue:
                    # return json.dumps(pointQuery)
                    return pointQuery
                if rangeQueryStart:
                    # return json.dumps(rangeQuery)
                    return rangeQuery

                # return token.value

    def transfer(self, dmls):
        for dml in dmls:
            # print '-- ' + str(dml)

            if self.isDML(dml) == False:
                continue

            devices = self.getTables(dml)
            # print devices
            if len(devices) > 1:
                print 'Multi-devices query is not supported now ...'
                continue
            sensors = self.getColumns(dml)
            predicate = self.getWhere(dml)
            if predicate == None:
                print 'The select statement does NOT contain WHERE predicates, currently is not supported ...'
                return None
            # print predicate
            query_url = 'data-points'
            if predicate.has_key('sampleTime'):
                key = 'sampleTime'
                value = predicate['sampleTime']
            elif predicate.has_key('timeRange'):
                key = 'timeRange'
                value = predicate['timeRange']
                query_url = 'data-rows'
            else:
                print 'The query is not supported now ...'

            sources = {"device": devices[0], "sensors": sensors}
            sources[key] = value
            select = {"sources": sources}

            selectstr = json.dumps(select)
            # print str(select)
            # print json.dumps(select)

            query = requests.get(self.url + '/data/' + query_url + '?select=' + selectstr)
            # print self.url + '/data/data-points?select=' + selectstr
            print Fore.RED + query.url
            # print query.text
            response = json.loads(query.text)
            print json.dumps(response, sort_keys=True, indent=4)

    def execQuery(self):
        var = 1
        while var == 1:
            sql = raw_input("> ")
            if sql.upper() == 'EXIT' or sql.upper() == 'BYE':
                print 'Exit KMX CLI ...'
                return
            parsed = sqlparse.parse(sql)
            # print len(parsed)
            self.transfer(parsed)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help = 'Input HTTP REST URL of your KMX query engine.')
    args = parser.parse_args()
    url = args.url
    if url == None:
        print 'You must provide an HTTP REST URL for KMX query ...'
        print 'Use -u or --url to init URL'
        print 'Use -h to get help ...'
    else:
        print 'URL input is: ' + Back.GREEN + str(url)

        CLI = cli()
        CLI.url = url
        CLI.execQuery()