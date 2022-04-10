# Libraries
# ==============================================================================
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import UrlDataSMCGR as UrlCGR

Url_CGR = UrlCGR.UrlDataSMCGR(
    year_start = 2021,
    year_end = 2021
)

url_data = Url_CGR.url_data()

class ExtractDataSMCGR():

    def __init__(self, url_data):
        self.url_data = url_data

    @property
    def months(self):
        
        months = {
            'INICIAL' : '01', 
            'ENERO' : '01', 
            'FEBRERO' : '02', 
            'MARZO' : '03', 
            'ABRIL' : '04', 
            'MAYO' : '05', 
            'JUNIO' : '06',
            'JULIO' : '07', 
            'AGOSTO' : '08', 
            'SEPTIEMBRE' : '09', 
            'OCTUBRE' : '10', 
            'NOVIEMBRE' : '11',
            'DICIEMBRE' : '12'
        }

        return months

    def data_budget(self):

        url = self.url_data
        url = url['budget']

        data = pd.DataFrame()

        for u in url:
            data_temp = pd.read_excel(
                u, 
                dtype = str
            )

            data = pd.concat(
                [data, data_temp],
                axis = 1
            )

        return data

extract = ExtractDataSMCGR(
    url_data = url_data
)

dt = extract.data_budget()
data = dt.copy()

data.columns = ['_'.join(c.upper().split(' ')) for c in data.columns]

data = pd.melt(
    data,
    id_vars = data.loc[:, 'EJERCICIO':'NOMBRE_SUBASIGNACION'].columns.to_list(),
    var_name = 'CONCEPTO',
    value_name = 'MONTO'
)

columns = data['CONCEPTO'].str.rsplit(
    '_',
    1,
    expand = True
)

columns[0].replace(
    {
        'PPTO' : 'PPTO_INICIAL',
        'PERCIBIDOPAG' : 'PERCIBIDO_PAG'
    },
    inplace = True
)

columns[1].replace(
    months,
    inplace = True
)

columns.columns = ['CONCEPTO', 'MES_EJERCICIO']

data.drop(
    columns = ['CONCEPTO'],
    inplace = True
)

data = pd.concat(
    [data, columns],
    axis = 1
)

data = data[
    (data['CONCEPTO'] != 'PORPERCIBIR') &
    (~data['MES_EJERCICIO'].isin(['ACTUALIZADO', 'ACUM']))
]

data['FECHA_EJERCICIO'] = (
    data['EJERCICIO'] + '-' + data['MES_EJERCICIO'] + '-01'
).apply(
    lambda x: datetime.strptime(x, '%Y-%m-%d') + relativedelta(day = 31)
)

