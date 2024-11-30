import altair as alt
import pandas as pd
import plotly.express as px

def GetYear(st, year_list):

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_year = st.selectbox('Select a year', ['All'] + year_list)

    st.write('')

    return selected_year

def GetCategory(st, category_list):

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_year = st.selectbox('Select a Category', category_list, index=0)

    st.write('')

    return selected_year


def GetOption(st):

    option_list = ['Budget', 'Assets and loans']

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_year = st.selectbox('Select a year', option_list, index=0)

    return selected_year

def SetPageConfiguration(st, alt):

    st.set_page_config(
        page_title="Budget",
        layout="wide",
        initial_sidebar_state="expanded")

    alt.themes.enable("dark")

    col = st.columns((1, 1, 1), gap='medium')

    with col[1]:
        st.title("Budget")

def PlotMonthlyBudget(st, df):

    col = st.columns((0.1, 1), gap='medium')

    with col[1]:
        #st.markdown('#### Monthly')1
        st.dataframe(df)

def PlotPieChart(st, budget_data):

    col = st.columns((0.15, 1.0, 0.35), gap='medium')

    with col[1]:
        data_pie = px.pie(
            names  = budget_data.keys(),
            values = budget_data.values(),
            height= 750,
            title  = 'Budget'
        )
        
        data_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(data_pie)

def PlotHistogram(st, df, category):

    col = st.columns((0.15, 1.0, 0.35), gap='medium')

    with col[1]:
        fig = px.bar(df, y=category, title=category)
        fig.update_layout(
            yaxis_title="SEK",
            title=dict(text=category, x=0.5),
            height = 750,
            bargap = 0.5
            )
        st.plotly_chart(fig)

def PlotAssetsAndLoans(st, df_assets, df_loans):

    col = st.columns((15.5, 2.5), gap='medium')

    with col[0]:
        st.markdown('#### Asset')
        st.dataframe(df_assets)

    with col[0]:
        st.markdown('#### Loan')
        st.dataframe(df_loans)