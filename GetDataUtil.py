import altair as alt
import pandas as pd
from datetime import date

def CreateTotalMonthData(df):

    Data = dict({
    'Income':          df[df.category == 'Inkomst'].cost.sum(),
    'Rent':           -df[df.category == 'Hyra'].cost.sum(),
    'Food':           -df[df.category == 'Mat'].cost.sum(),
    'Clothes':        -df[df.category == 'KlAder'].cost.sum(),
    'Transportation': -df[df.category == 'Transport'].cost.sum(),
    'Other fixed':    -df[df.category == 'Ovrig fast'].cost.sum(),
    'Other':          -df[df.category == 'Ovrig'].cost.sum(),
    'Interest':       -df[df.category == 'RAnta'].cost.sum(),
    'Amortization':   -df[df.category == 'Amortering'].cost.sum()
    })

    Data['Savings'] =   Data['Income'] - Data['Rent'] - Data['Food'] - Data['Clothes'] - Data['Transportation'] \
                      - Data['Other fixed'] - Data['Other'] - Data['Interest'] - Data['Amortization']

    df = dict({
        'Mat':        (Data['Food']           / Data['Income']) * 100,
        'Hyra':       (Data['Rent']           / Data['Income']) * 100,
        'Kläder':     (Data['Clothes']        / Data['Income']) * 100,
        'Transport':  (Data['Transportation'] / Data['Income']) * 100, 
        'Övrig fast': (Data['Other fixed']    / Data['Income']) * 100,
        'Övrig':      (Data['Other']          / Data['Income']) * 100,
        'Ränta':      (Data['Interest']       / Data['Income']) * 100, 
        'Amortering': (Data['Amortization']   / Data['Income']) * 100,
        'Sparande':   (Data['Savings']        / Data['Income']) * 100
    })

    return df 

def FilterDataframe(dataframe, selected_year):

    df_selected_year = dataframe[dataframe['year'].dt.year == selected_year]

    return df_selected_year

def CreateYearDataframe(budget_df, year_options):

    tmp_data_list = []

    for year in year_options:
        year_df = budget_df[budget_df['year'].dt.year == year]

        if year == date.today().year:
            current_month = max(date.today().month - 1, 1)
        else:
            current_month = 12

        tmp_data = dict({
            'Inkomst' :     round(year_df[year_df.category == 'Inkomst'].cost.sum() / current_month),
            'Mat' :         -round(year_df[year_df.category == 'Mat'].cost.sum() / current_month),
            'Hyra' :        -round(year_df[year_df.category == 'Hyra'].cost.sum() / current_month),
            'Kläder' :      -round(year_df[year_df.category == 'KlAder'].cost.sum() / current_month),
            'Transport' :   -round(year_df[year_df.category == 'Transport'].cost.sum() / current_month),
            'Ovrig fast' :  -round(year_df[year_df.category == 'Ovrig fast'].cost.sum() / current_month),
            'Ovrig' :       -round(year_df[year_df.category == 'Ovrig'].cost.sum() / current_month),
            'Ränta' :       -round(year_df[year_df.category == 'RAnta'].cost.sum() / current_month),
            'Amortering' :  -round(year_df[year_df.category == 'Amortering'].cost.sum() / current_month),
            })
        tmp_data['Sparande'] =  tmp_data['Inkomst'] - tmp_data['Hyra'] - tmp_data['Mat'] - tmp_data['Kläder'] - tmp_data['Transport'] \
                              - tmp_data['Ovrig fast'] - tmp_data['Ovrig'] - tmp_data['Ränta'] - tmp_data['Amortering']

        tmp_data_list.append(tmp_data)

    df_tmp = pd.DataFrame(tmp_data_list, index=year_options)
    df_tmp.index.name = 'Year'
    df_tmp.index = df_tmp.index.astype(str)

    return df_tmp

def CreateMonthData(df_selected_year):
    
    # Define categories and months
    categories = ['Inkomst', 'Hyra', 'Mat', 'KlAder', 'Transport', 'Ovrig fast', 'Ovrig', 'RAnta', 'Amortering', 'Sparande']
    months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
    
    # Initialize an empty list to store the data
    data = []
    
    # Loop through categories and months, calculating sums
    for category in categories: # + ['Sparande']:
        tmp_dict = {}
        for month_idx in range(1, 13):
            if category == 'Sparande':  # If last row ('Sparande'), sum all categories
                df_selected_tmp = df_selected_year[df_selected_year['year'].dt.month == month_idx]
            else:
                df_selected_tmp = df_selected_year[(df_selected_year['category'] == category) & (df_selected_year['year'].dt.month == month_idx)]
            
            # Calculate the total cost for the month and round
            tmp_dict[months[month_idx - 1]] = round(df_selected_tmp['cost'].sum())
        
        # Append the dictionary for this category to the data list
        data.append(tmp_dict)
    
    # Create a DataFrame using the categories as the index
    df = pd.DataFrame(data, index=categories)
    df.index.name = 'Category'
    return df

def CreateAssetLoanDataFrame(df_selected_year):
    
    # Define categories and months
    asset_columns = ['konto', 'buffert', 'sparande', 'aktier', 'certifikat', 'ETF', 'fonder', 'indexfonder', 'apartment']
    loan_columns = ['csn', 'mamma', 'danskebank']
    asset_names = ['Konto', 'Buffert', 'Sparande', 'Aktier', 'Certifikat', 'ETF', 'Fonder', 'Indexfonder', 'Lägenhet']
    loan_names = ['CSN', 'Mamma', 'Danske bank']
    months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']

    # Helper function to extract monthly sums
    def calculate_monthly_sums(df, columns):
        data = []
        for column in columns:
            tmp_dict = {}
            for month_idx in range(1, 13):
                df_selected_tmp = df[df['year'].dt.month == month_idx]
                tmp_dict[months[month_idx - 1]] = abs(round(df_selected_tmp[column].sum()))
            data.append(tmp_dict)
        return data

    # Calculate asset and loan data
    asset_data = calculate_monthly_sums(df_selected_year, asset_columns)
    loan_data  = calculate_monthly_sums(df_selected_year, loan_columns)

    # Create DataFrames
    df_assets = pd.DataFrame(asset_data, index=asset_names)
    df_loans = pd.DataFrame(loan_data, index=loan_names)

    return df_assets, df_loans

def CreateAssetLoanTotalDataFrame(df_assets, df_loan):
    df = []

    #df['total_assets']['Januari'] = df_assets['Januari'].sum

    #df.total_assets = df_assets.Konto + df_assets.Buffert + df_assets.Sparande + df_assets.Aktier + df_assets.Certifikat + df_assets.ETF + df_assets.Fonder + df_assets.Indexfonder + df_assets.Lagenhet
    #df.total_loan   = df_loans.CSN    + df_loans.Mamma

    return df

def LoadBudgetData():

    # Load budget data 
    dataframe  = pd.read_csv('C:/Users/Quake/OneDrive/Dokument/Coding/Python/Other/Dashboard/BudgetCSV.csv')
    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y-%m-%d')

    return dataframe

def LoadAssetData():

    dataframe = pd.read_csv('C:/Users/Quake/OneDrive/Dokument/Coding/Python/Other/Dashboard/BudgetCSV2.csv')
    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y-%m-%d')

    return dataframe

def GetYearAndCategoryOptions(dataframe):

    unique_year_list = list(dataframe['year'].dt.year.unique())
    unique_year_list.sort(reverse=True)
    
    category_list   = ['Inkomst', 'Mat', 'Hyra', 'Kläder', 'Transport', 'Ovrig fast', 'Ovrig', 'Ränta', 'Amortering', 'Sparande']

    return unique_year_list, category_list