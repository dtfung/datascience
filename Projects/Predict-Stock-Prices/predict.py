# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:05:10 2016

@author: donaldfung

Contributors: Deepak Mahtani, Blayne Chong, Donald Fung
"""

import assemble
import settings
import pandas as pd

if __name__ == "__main__":
    
    # initialize company class
    company = assemble.CompanyData(settings.company_ticker)
    
    # preprocess data
    df = (pd.DataFrame()
            .pipe(company.get_wiki_data()))