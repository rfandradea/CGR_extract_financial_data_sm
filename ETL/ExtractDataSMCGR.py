# Libraries
# ==============================================================================
import pandas as pd
import numpy as np
import UrlDataSMCGR as UrlCGR

Url_CGR = UrlCGR.UrlDataSMCGR(
    year_start = 2021,
    year_end = 2021
)

url_data = Url_CGR.url_data()

class ExtractDataSMCGR():

    def __init__(self, url_data):
        self.url_data = url_data

    def data_budget(self):

        url = self.url_data
        url = url['budget']

        data = pd.DataFrame()

        for u in url:
            data_temp = pd.read_excel(u)

            data = pd.concat(
                [data, data_temp],
                axis = 1
            )

        return data

extract = ExtractDataSMCGR(
    url_data = url_data
)

data = extract.data_budget()