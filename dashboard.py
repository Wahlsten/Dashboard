import streamlit as st
import altair as alt
import GetDataUtil as util_func
import PlotDashboard as plot_func

options = ['Budget', 'Assets and loans']

plot_func.SetPageConfiguration(st, alt)

budget_df = util_func.LoadBudgetData()
asset_df  = util_func.LoadAssetData()

selected_option = plot_func.GetOption(st, options)

category_list   = util_func.GetCategories(selected_option)

selected_year   = plot_func.GetYear(st, category_list['year'])

if selected_option == 'Budget':
    if selected_year != 'All':
        filtered_df      = util_func.FilterDataframe(budget_df, selected_year)
        month_df         = util_func.CreateMonthData(filtered_df)
        total_month_dict = util_func.CreateTotalMonthData(filtered_df)

        plot_func.PlotPieChart(st, total_month_dict)
        plot_func.PlotMonthlyBudget(st, month_df)
    else:
        category        = plot_func.GetCategory(st, category_list)
        total_month_df  = util_func.CreateMonthDataframe(budget_df, category_list['year'], category['time_resolution'])

        if category['category'] != []:
            if category['line'] == 'Line':
                plot_func.PlotLine(st, total_month_df, category['category'])
            else:
                plot_func.PlotHistogram(st, total_month_df, category['category'])

elif selected_option == 'Assets and loans':
    if selected_year != 'All':
        df_year  = util_func.FilterDataframe(asset_df, selected_year)
        df_assets, df_loans = util_func.CreateAssetLoanDataFrame(df_year)
        df_asset_loan_total = util_func.CreateAssetLoanTotalDataFrame(df_assets, df_loans)

        plot_func.PlotAssetsAndLoans(st, df_assets, df_loans)
    else:
        df_assets        = util_func.CreateYearAssetLoanDataframe(asset_df, category_list['year'])
        df_loan          = util_func.CreateYearLoanDataframe(asset_df, category_list['year'])
        category         = plot_func.GetCategory(st, category_list['category_list'])
        plot_category    = plot_func.GetLineOption(st, category_list['line_list'])
        asset_df         = asset_df.set_index("year")
        asset_df         = asset_df.sort_index()

        if category != []:
            if plot_category == 'Line':
                plot_func.PlotLine(st, asset_df, category)
            else:
                plot_func.PlotHistogram(st, asset_df, category)
