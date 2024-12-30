import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
from datetime import date
import GetDataUtil as util_func
import PlotDashboard as plot_func

plot_func.SetPageConfiguration(st, alt)

budget_df = util_func.LoadBudgetData()

year_options, category_list = util_func.GetYearAndCategoryOptions(budget_df)

selected_option = plot_func.GetOption(st)
selected_year   = plot_func.GetYear(st, year_options)

if selected_option == 'Budget':
    if selected_year != 'All':
        filtered_df      = util_func.FilterDataframe(budget_df, selected_year)
        month_df         = util_func.CreateMonthData(filtered_df)
        total_month_dict = util_func.CreateTotalMonthData(filtered_df)

        plot_func.PlotMonthlyBudget(st, month_df)
        plot_func.PlotPieChart(st, total_month_dict)
    else:
        total_month_df = util_func.CreateYearDataframe(budget_df, year_options)
        plot_func.PlotMonthlyBudget(st, total_month_df)

        category = plot_func.GetCategory(st, category_list)
        plot_func.PlotHistogram(st, total_month_df, category)

elif selected_option == 'Assets and loans':
    asset_df            = util_func.LoadAssetData()
    df_year             = util_func.FilterDataframe(asset_df, selected_year)
    df_assets, df_loans = util_func.CreateAssetLoanDataFrame(df_year)
    df_asset_loan_total = util_func.CreateAssetLoanTotalDataFrame(df_assets, df_loans)

    plot_func.PlotAssetsAndLoans(st, df_assets, df_loans)