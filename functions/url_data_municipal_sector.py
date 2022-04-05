# Libraries
# ==============================================================================
from attr import attr
import pandas as pd
import requests
import urllib
from bs4 import BeautifulSoup


def url_data_sm_cgr(year_start, year_end, report = 'all'):

    """
    
    """

    # Validation args year_start and year_end
    if type(year_start) != int or type(year_end) != int:

        raise TypeError('year_start and year_end must be of type int')

    # Validation arg report
    if type(report) != str:

        raise TypeError('report argument must be format string')

    elif report not in ('all', 'budget', 'equity'):

        raise ValueError('Report only allows the following parameters: all, budget or equity')

    # URL
    url = 'https://www.contraloria.cl/web/cgr/base-de-datos-municipales'

    # GET-Request
    try:
        print(f'Generating connection to: {url}')
        response = requests.get(url)
    
    except urllib.error.HTTPError as http:
        print('\nHTTP error: ' + http)

    except urllib.error.URLError as ue:
        print('\nThe server is not operational, please try again later')
    
    else:
        print(f'\nSuccessful connection')

    # Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Results with all the href of the url
    result = soup.find_all('a', href = True)

    # Url lists for reports budget and equity
    url_budget = []
    url_equity = []

    # url cgr
    url_cgr = 'https://www.contraloria.cl'

    # extract url budget and equity
    for u in result:
        href = u.get('href')

        if 'Presupuestaria' in href:
            url_budget.append(f'{url_cgr}{href}')

        elif 'Patrimonial' in href:
            url_equity.append(f'{url_cgr}{href}')

    if response == 'budget':
        return url_budget

    elif response == 'equity':
        return url_equity

    else:
        return (url_budget, url_equity)


url_data_sm_cgr(
    year_end = 2021,
    year_start = 2021,
    report = "budget"
)