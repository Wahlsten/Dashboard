import pandas as pd
from openpyxl import load_workbook
import TransformerModel as tf_model

def PreprocessData(df):

    df_cleaned = df.map(lambda x: x.translate(str.maketrans('åäöÅÄÖ ()-*%&_:.,', 'aaoAAO          .')) if isinstance(x, str) else x)
    df_cleaned = df_cleaned.map(lambda x: x.replace(' ', '') if isinstance(x, str) else x)

    df_cleaned.index = pd.to_datetime(df_cleaned.index)
    max_index = max(df_cleaned.index)

    # Remove Saving data
    df_cleaned = df_cleaned[~df_cleaned['Specifikation'].isin(['AVANZABANK', 'TrustlyGroupAB'])]

    # Remove early loan + amortization data
    df_cleaned = df_cleaned[(df_cleaned['Specifikation'] != 'Lan12780647914')           | (df_cleaned.index.day > 5)]
    df_cleaned = df_cleaned[(df_cleaned['Specifikation'] != 'SwishtillELISABETHARVEMO')]
    
    #Split loan and amortization data
    loan = float(df_cleaned[df_cleaned['Specifikation'] == 'Lan12780647914']['Belopp'].iloc[0])
    amortization = 3500
    interest = loan - amortization

    df_cleaned = df_cleaned[df_cleaned['Specifikation'] != 'Lan12780647914']

    mortgage_row = pd.DataFrame({'Specifikation': ['Amortering lgh', 'Ranta lgh'], 'Belopp': [amortization, interest]}, index=[max_index, max_index])

    loan_row = pd.DataFrame({'Specifikation': ['Amortering lgh mamma', 'Ranta lgh mamma'], 'Belopp': [1000, 150]}, index=[max_index, max_index])

    # Append the new row using pd.concat()
    df_cleaned = pd.concat([df_cleaned, mortgage_row, loan_row])
    df_cleaned['Belopp'] = df_cleaned['Belopp'].astype(float)
    df_cleaned = df_cleaned.map(lambda x: x.translate(str.maketrans('0123456789', '          ')) if isinstance(x, str) else x)
    df_cleaned = df_cleaned.map(lambda x: x.replace(' ', '') if isinstance(x, str) else x)

    return df_cleaned

def ClassifyData(sequence):

    tokenized_seq  = tf_model.Tokenize(sequence)
    model          = tf_model.LoadTransformer()
    classified_seq = tf_model.PredictCategory(model, tokenized_seq)

    return classified_seq

input_file_name = r'C:\Users\Quake\OneDrive\Dokument\Coding\Python\Other\Dashboard\DanskeKonto-12780647906-20250301.csv'
ouput_file_name = r'C:\Users\Quake\OneDrive\Dokument\Coding\Python\OTher\Dashboard\BudgetCSVBackup.csv'

# Read the CSV file
df = pd.read_csv(input_file_name, encoding='cp1252', sep=';')
df = df.set_index("Bokföringsdag")
df = df.sort_index()
df = df[['Specifikation', 'Belopp']]

preprocess_df = PreprocessData(df)
preprocess_df['Kategori'] = ClassifyData(preprocess_df['Specifikation'].to_numpy())

preprocess_df['Belopp'] = preprocess_df.apply(
    lambda row: -row['Belopp'] if row['Kategori'] != 'Inkomst' else row['Belopp'], axis=1
)

preprocess_df.to_csv(ouput_file_name, mode='a', index=True, header=False)