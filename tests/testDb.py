import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataExtract.dataExtract import downloadData
from dbEngine.dbEngine import DbEngine
import pytest
from sqlalchemy import create_engine, text

TABLE_NAMES = ['stock_prices', 'stock_list', 'secondary_stock_prices', 'financials', 'trades'] 

@pytest.fixture(scope="module")
def engine():

    #Setup and teardown for the database engine.
    dbEngine = DbEngine()
    engine = dbEngine.createDbengine()
    yield engine
    engine.dispose()

@pytest.mark.parametrize("table_name", TABLE_NAMES)
def test_select_all_from_table(engine, table_name):
    
    """
    Test selecting all rows from a specified table.

    This test runs a SELECT query to retrieve all rows from the given table and 
    checks if the result is not empty. It is parameterized to run for each table 
    listed in TABLE_NAMES.
    """
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT * FROM {table_name}"))
        rows = result.fetchall()
        
        # Example assertion: Check if the result is not empty
        assert len(rows) > 0
