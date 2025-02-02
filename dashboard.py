import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
from datetime import date
import GetDataUtil as util_func
import PlotDashboard as plot_func

plot_func.SetPageConfiguration(st, alt)

line_option_list       = ['Histogram', 'Line']
resolution_option_list = ['Month', 'Year']
year_options           = util_func.GetYearAndCategoryOptions()

selected_option = plot_func.GetOption(st)
selected_year   = plot_func.GetYear(st, year_options)
category_list   = util_func.GetCategory(selected_option)

if selected_option == 'Budget':
    budget_df = util_func.LoadBudgetData()
    if selected_year != 'All':
        filtered_df      = util_func.FilterDataframe(budget_df, selected_year)
        month_df         = util_func.CreateMonthData(filtered_df)
        total_month_dict = util_func.CreateTotalMonthData(filtered_df)

        plot_func.PlotPieChart(st, total_month_dict)
        plot_func.PlotMonthlyBudget(st, month_df)
    else:
        plot_resolution = plot_func.GetResolutionOption(st, resolution_option_list)
        total_month_df  = util_func.CreateMonthDataframe(budget_df, year_options, plot_resolution)
        category        = plot_func.GetCategory(st, category_list)

        if category != []:
            plot_category   = plot_func.GetLineOption(st, line_option_list)
            if plot_category == 'Line':
                plot_func.PlotLine(st, total_month_df, category)
            else:
                plot_func.PlotHistogram(st, total_month_df, category)

elif selected_option == 'Assets and loans':
    asset_df = util_func.LoadAssetData()
    if selected_year != 'All':
        df_year  = util_func.FilterDataframe(asset_df, selected_year)
        df_assets, df_loans = util_func.CreateAssetLoanDataFrame(df_year)
        df_asset_loan_total = util_func.CreateAssetLoanTotalDataFrame(df_assets, df_loans)

        plot_func.PlotAssetsAndLoans(st, df_assets, df_loans)
    else:
        df_assets        = util_func.CreateYearAssetLoanDataframe(asset_df, year_options)
        df_loan          = util_func.CreateYearLoanDataframe(asset_df, year_options)
        category         = plot_func.GetCategory(st, category_list)
        plot_category    = plot_func.GetLineOption(st, line_option_list)
        asset_df         = asset_df.set_index("year")
        asset_df         = asset_df.sort_index()

        if category != []:
            if plot_category == 'Line':
                plot_func.PlotLine(st, asset_df, category)
            else:
                plot_func.PlotHistogram(st, asset_df, category)
