# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:05:55 2016

@author: donaldfung

Contributors: Deepak Mahtani, Blayne Chong, Donald Fung
"""

# dummy company
company_ticker = "INTC"

#=========================================
""" Wiki EOD Stock Data"""

# name
wiki_dbname = "WIKI/"

# columns used
wiki_columns = ["Volume", "Adj. Close"]

# dates
start_date = "2005-01-01"
end_date = "2016-01-01"

#=========================================
""" Core US Fundamentals Data"""

# columns
sf1_columns = ["Net Income", "Cost of Goods Sold", "Gross Profit",
               "R&D", "Operating Expenses", "Operating Income",
               "Revenue", "EPS", "DPS", "Shares Outstanding", 
               "Cash", "Current Assets", "Intangibles", 
               "Total Assets", "Current Liabilities", 
               "Long Term Debt", "Retained Earnings", 
               "Total Liabilities", "Long Term Liabilities",
               "Stockholders Equity", "Operating Cash Flow"]
               
# Endpoints
sf1_codes = [
    # net income (as reported - quarterly)
    "SF1/{}_NETINCCMN_ARQ".format(company_ticker),

    # cost of goods solds (as reported - quarterly)
    "SF1/{}_COR_ARQ".format(company_ticker),

    # gross profit (as reported - quarterly)
    "SF1/{}_GP_ARQ".format(company_ticker),

    # research and development (as reported - quarterly)
    "SF1/{}_RND_ARQ".format(company_ticker),

    # operating expenses (as reported - quarterly)
    "SF1/{}_OPEX_ARQ".format(company_ticker),

    # operating income (as reported - quarterly)
    "SF1/{}_OPINC_ARQ".format(company_ticker),

    # revenue (as reported - quarterly)
    "SF1/{}_REVENUE_ARQ".format(company_ticker),

    # basic earnings per share (as reported - quarterly)
    "SF1/{}_EPS_ARQ".format(company_ticker),

    # dividends per basic share (as reported - quarterly)
    "SF1/{}_DPS_ARQ".format(company_ticker),

    # weighted average shares outstanding (as reported - quarterly)
    "SF1/{}_SHARESWA_ARQ".format(company_ticker),

    # cash and cash equivalents (as reported - quarterly)
    "SF1/{}_CASHNEQ_ARQ".format(company_ticker),

    # current assets (as reported - quarterly)
    "SF1/{}_ASSETSC_ARQ".format(company_ticker),

    # goodwill and intangible assets (as reported - quarterly)
    "SF1/{}_INTANGIBLES_ARQ".format(company_ticker),

    # total assets (as reported - quarterly)
    "SF1/{}_ASSETS_ARQ".format(company_ticker),

    # current liabilities (as reported - quarterly)
    "SF1/{}_LIABILITIESC_ARQ".format(company_ticker),

    # long-term debt (as reported - quarterly)
    "SF1/{}_DEBTNC_ARQ".format(company_ticker),

    # retained earnings (as reported - quarterly)
    "SF1/{}_RETEARN_ARQ".format(company_ticker),

    # total liabilities (as reported - quarterly)
    "SF1/{}_LIABILITIES_ARQ".format(company_ticker),
    
    # long-term liabilities (as reported - quarterly)
    "SF1/{}_LIABILITIESNC_ARQ".format(company_ticker),

    # stockholders equity (as reported - quarterly)
    "SF1/{}_EQUITYUSD_ARQ".format(company_ticker),

    # operating cash flow (as reported - quarterly)
    "SF1/{}_NCFO_ARQ".format(company_ticker)
    ]
