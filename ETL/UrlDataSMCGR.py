# Libraries
# ==============================================================================
import numpy as np
import requests
import urllib
from bs4 import BeautifulSoup

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class UrlDataSMCGR():

    def __init__(self, year_start, year_end, report = 'all'):
        self.year_start = year_start
        self.year_end = year_end
        self.report = report

        selected_years = self.selected_years()
        years_reports = self.years_reports()

        # Validation args year_start and year_end
        if type(year_start) != int or type(year_end) != int:

            raise TypeError(
                'year_start and year_end must be of type int'
                )

        # Validation args year_end greater than or equal year_start
        if year_end < year_start:
            
            raise ValueError(
                'Argument year_end must be greater than or equal to year_start'
                )

        # Validation args range year selected
        for sy in selected_years:
            if sy not in years_reports:

                raise ValueError(
                    f"""
                    Years selected {sy} outside the allowed range, the financial reports 
                    to be downloaded comprise the following years {min(years_reports)} and {max(years_reports)}
                    """
                )
                
        # Validation arg report
        if type(report) != str:

            raise TypeError(
                'report argument must be format string'
                )

        elif report not in ('all', 'budget', 'equity'):

            raise ValueError(
                'Report only allows the following parameters: all, budget or equity'
                )

    @property
    def url_bd_sm(self):

        # Url CGR financial report municipal sector
        url = 'https://www.contraloria.cl/web/cgr/base-de-datos-municipales'

        return url

    @property
    def url_cgr(self):

        url = 'https://www.contraloria.cl'

        return url

    def response_url(self, url):

        # GET-Request
        try:
            print(f'Generating connection to: {url}')
            response = requests.get(url)
        
        except urllib.error.HTTPError as http:
            print('\nHTTP error: ' + http)

        except urllib.error.URLError as ue:
            print('\nThe server is not operational, please try again later')
        
        else:
            print(f'\nSuccessful connection\n')

        return response

    def soup(self):

        # Soup
        soup = BeautifulSoup(
            self.response_url(self.url_bd_sm).text, 
            'html.parser'
        )

        return soup

    def years_reports(self):

        results = self.soup()
        results = results.find_all(
            'a', 
            class_ = 'tablinks'
        )
        
        years = []

        for result in results:

            years.append(result.get_text())

        years = sorted(list(map(int, years)))

        return years

    def selected_years(self):

        select = np.arange(
            self.year_start, 
            self.year_end + 1
        ).tolist()

        return select

    def url_data(self):
        
        results = self.soup()
        results = results.find_all(
            'div', 
            class_ = 'tabcontent', 
            id = self.selected_years()
        )

        # Url lists for reports budget and equity
        url_budget = []
        url_equity = []

        # Url cgr
        url_cgr = self.url_cgr    

        # Extract url budget and equity
        for result in results:
            href = result.find_all('a', href = True)

            for hr in href:
                url = hr.get('href')

                if 'Presupuestaria' in url:
                    url_budget.append(f'{url_cgr}{url}')

                elif 'Patrimonial' in url:
                    url_equity.append(f'{url_cgr}{url}')

        # Return url
        if self.report == 'budget':
            return {
                'budget': url_budget
                }

        elif self.report == 'equity':
            return {
                'equity' : url_equity
                }

        else:
            return {
                'budget' : url_budget, 
                'equity' : url_equity
                }