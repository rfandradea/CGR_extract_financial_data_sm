# Libraries
# ==============================================================================
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import UrlDataSMCGR as UrlCGR

Url_CGR = UrlCGR.UrlDataSMCGR(
    year_start = 2020,
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

    @property
    def order_columns_budget(self):

        columns = [
            'EJERCICIO', 'MES_EJERCICIO', 'FECHA_EJERCICIO', 'MONEDA',
            'REGION', 'COD_MUNICIPIO', 'NOMBRE_MUNICIPIO', 'COD_SERVICIO',
            'NOMBRE_SERVICIO', 'COD_AREA', 'NOMBRE_AREA', 'COD_CUENTA',
            'COD_TIPO_CUENTA', 'NOMBRE_TIPO_CUENTA', 'COD_SUBTITULO',
            'NOMBRE_SUBTITULO', 'COD_ITEM', 'NOMBRE_ITEM', 'COD_ASIGNACION',
            'NOMBRE_ASIGNACION', 'COD_SUBASIGNACION', 'NOMBRE_SUBASIGNACION',
            'PPTO_INICIAL', 'MODIF_PPTO', 'DEVENGADO', 'PERCIBIDO_PAG'
        ]

        return columns

    def data_raw_budget(self):

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
                axis = 0
            )

        return data

    def data_budget(self):

        data = self.data_raw_budget()

        data.columns = ['_'.join(c.upper().split(' ')) for c in data.columns]

        data = pd.melt(
            data,
            id_vars = data.loc[:, 'EJERCICIO':'NOMBRE_SUBASIGNACION'].columns.to_list(),
            var_name = 'CONCEPTO',
            value_name = 'MONTO'
        )

        data = data[data['MONTO'] != '0']

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
            self.months,
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

        data = pd.pivot_table(
            data,
            index = [c for c in data.columns if c not in ['CONCEPTO', 'MONTO']],
            values = 'MONTO',
            columns = 'CONCEPTO'
        ).reset_index()

        cod_columns = [
            'COD_TIPO_CUENTA', 'COD_SUBTITULO', 'COD_SUBASIGNACION'
        ]

        data['COD_TIPO_CUENTA'].replace(
            {
                '1' : '115',
                '2' : '215'
            },
            inplace = True
        )

        data['COD_CUENTA'] = data.loc[:, cod_columns].apply(
            lambda x: ''.join(x), 
            axis = 1
        )

        data = data.reindex(
            columns = self.order_columns_budget
        )

        int_columns = [
            'PPTO_INICIAL', 'MODIF_PPTO', 'DEVENGADO', 'PERCIBIDO_PAG'
        ]

        data.loc[:, int_columns] = data.loc[:, int_columns].astype('Int64')

        return data

extract = ExtractDataSMCGR(
    url_data = url_data
)

data = extract.data_budget()

# data.to_csv('../data/data_budget/data_budget.csv')