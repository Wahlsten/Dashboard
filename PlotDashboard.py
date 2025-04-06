import altair as alt
import pandas as pd
import plotly.express as px

def GetYear(st, year_list):

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_year = st.sidebar.selectbox('Select a year', ['All'] + year_list)

    st.write('')

    return selected_year

def GetCategory(st, category_list):

    selected_option = {}

    col = st.columns((0.2, 0.2, 0.2, 0.2), gap='medium')

    with col[1]:
        selected_option['line'] = st.selectbox('Select a line option', category_list['line_list'], index=0)

    with col[2]:
        selected_option['time_resolution'] = st.selectbox('Select resolution 2', category_list['time_resolution'], index=0)

    col2 = st.columns((0.1, 0.1, 0.1, 0.1, 0.1, 0.1), gap='medium')
    selected_option_cat = []
    with col2[0]:
        selected_option_cat.append(st.multiselect('Select a category 1', options = category_list['category_list']))

    if selected_option_cat[-1] != []:
        with col2[1]:
            selected_option_cat.append(st.multiselect('Select a category 2', options = category_list['category_list']))

    if selected_option_cat[-1] != []:
        with col2[2]:
            selected_option_cat.append(st.multiselect('Select a category 3', options = category_list['category_list']))

    if selected_option_cat[-1] != []:
        with col2[3]:
            selected_option_cat.append(st.multiselect('Select a category 4', options = category_list['category_list']))
    
    selected_option['category'] = selected_option_cat

    st.write('')

    return selected_option

def GetLineOption(st, category_list):

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_option = st.sidebar.selectbox('Select a line option 2', category_list, index=0)

    st.write('')

    return selected_option 

def GetResolutionOption(st, resolution_list):

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_option = st.sidebar.selectbox('Select resolution', resolution_list, index=0)

    st.write('')

    return selected_option


def GetOption(st, option_list):

    col = st.columns((0.6, 0.3, 1), gap='medium')

    with col[1]:
        selected_year = st.sidebar.selectbox('Select an option', option_list, index=0)

    return selected_year

def SetPageConfiguration(st, alt):

    st.set_page_config(
        page_title="Economy",
        layout="wide",
        initial_sidebar_state="expanded")

    alt.themes.enable("dark")

    col = st.columns((1, 1, 1), gap='medium')

    with col[1]:
        st.title("Economy")

def PlotMonthlyBudget(st, df):

    col = st.columns((0.15, 1.0, 0.35), gap='medium')

    with col[1]:
        st.markdown('#### Budget')
        st.dataframe(df, width=1200)

def PlotPieChart(st, budget_data):

    col = st.columns((0.15, 1.0, 0.35), gap='medium')

    with col[1]:
        data_pie = px.pie(
            names  = budget_data.keys(),
            values = budget_data.values(),
            height = 600
        )
        
        data_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(data_pie)

def PlotHistogram(st, df, categories):

    col = st.columns((0.15, 1.0, 0.35), gap='medium')

    with col[1]:
        fig = px.bar(df, y=categories, barmode='group')
        fig.update_layout(
            yaxis_title="SEK",
            bargap = 0.5,
            height = 600,
            width  = 1200
            )
        st.plotly_chart(fig)

def PlotLine(st, df, categories):

    col = st.columns((0.15, 1.0, 0.35), gap='medium')
    print(categories)
    with col[1]:
        fig = px.line(df, y=categories)
        fig.update_layout(
            yaxis_title="SEK",
            #title=dict(text=category[0], x=0.5),
            height = 600,
            width = 1200
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