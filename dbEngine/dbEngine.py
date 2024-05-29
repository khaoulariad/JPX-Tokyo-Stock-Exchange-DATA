
import pandas as pd
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, Session
import os
import json

class DbEngine:

    """
    A class to manage MySQL database connections and operations.

    This class initializes a connection to a MySQL server using configuration
    details from a JSON file, provides methods to create a database, and 
    write DataFrames to tables in the database.

    Methods
    -------
    createEngine(connectionString)
        Creates a SQLAlchemy engine from a connection string.
    
    createDbengine()
        Creates a SQLAlchemy engine for the specified database.
    
    loadDatabases()
        Loads and returns the list of existing databases on the MySQL server.
    
    createDatabase()
        Creates the database if it does not already exist.
    
    writeTableInDb(tableName, df)
        Writes a DataFrame to a specified table in the database.
    """

    def __init__(self):

        configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(configPath, 'r') as file:
            configText = file.read()
        config = json.loads(configText)

        # initialize MySQL connection parameters
        username = config["DbUsername"]
        password = config["DbPassword"]
        host = config["DbHost"]
        port = config["DbPort"]

        # Database connection string
        self.connectionString = f'mysql+pymysql://{username}:{password}@{host}:{port}/'
        self.databaseName = config["DbName"]

        # Create engine to connect to Mysql server and load existant databases
        self.engine = self.loadDatabases()

    def createEngine(self, connectionString):

        # Creating enging from a given cnx String
        return create_engine(connectionString)

    def createDbengine(self):

        return self.createEngine(f'{self.connectionString}{self.databaseName}')
    
    def loadDatabases(self):
        
        # Connect to the MySQL server
        engine = self.createEngine(self.connectionString)
        connection = engine.connect()
        query = text('SHOW DATABASES;')
        result = connection.execute(query)
        self.databases = [i[0] for i in result.fetchall()]
        return engine
    
    def createDatabase(self):

        # Create Database if not existant
        if self.databaseName.lower() not in self.databases:
            print(f'Creating database {self.databaseName}')
            query = text(f"CREATE DATABASE IF NOT EXISTS {self.databaseName};")
            connection = self.engine.connect()
            connection.execute(query)

    def writeTableInDb(self, tableName, df):

        # Reconnect to the newly created database
        engine = self.createDbengine()
        df.to_sql(tableName, con=engine)
