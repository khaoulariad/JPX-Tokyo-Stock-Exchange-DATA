from dataExtract.dataExtract import downloadData
from dbEngine.dbEngine import DbEngine
import pandas as pd
import os



# ------------------------------------------------
# Reads all CSV files from the specified directory 
# and stores them into a MySQL database.
# ------------------------------------------------
def storeCsvFromDir(dbEngine, csvDirectory):

    scriptDir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the csvDirectory
    csvDirectoryPath = os.path.join(scriptDir, csvDirectory)

    # Check if the directory exists
    if not os.path.exists(csvDirectoryPath):
        raise FileNotFoundError(f"The directory {csvDirectoryPath} does not exist.")
    
    print(f'Saving files in {csvDirectory} as tables in the database')
    for filename in os.listdir(csvDirectoryPath):
        if filename.endswith('.csv'):
            # Generate table name from the CSV file name
            tableName = os.path.splitext(filename)[0]  # Remove the .csv extension

            # Read the CSV file into a DataFrame
            csvPath = os.path.join(csvDirectory, filename)
            df = pd.read_csv(csvPath, low_memory=False)
            if tableName == 'stock_list':
                df['EffectiveDate'] = pd.to_datetime(df['EffectiveDate'].astype(str))
            elif tableName == 'stock_prices':
                df['Date'] = pd.to_datetime(df['Date'])
            if tableName == 'financials':
                longColName = 'NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock'
                df.rename(columns={longColName: 'issuedShares'}, inplace=True)

            # Write the DataFrame to the database
            dbEngine.writeTableInDb(tableName, df)
            print(f"Successfully wrote {filename} to table {tableName}")


if __name__ == '__main__':
    
    # Extract
    downloadData()

    # Transform and Store
    dbEngine = DbEngine()
    dbEngine.createDatabase()
    storeCsvFromDir(dbEngine, 'datasets/train_files')
    storeCsvFromDir(dbEngine, 'datasets')
