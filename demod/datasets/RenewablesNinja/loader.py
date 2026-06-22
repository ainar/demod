"""Ninja Renewable  https://www.renewables.ninja/.

Thanks to Open-Power-System-Data for their code, which is used here.
https://github.com/Open-Power-System-Data/weather_data/blob/master/download.ipynb
"""

from datetime import timedelta
import os
from typing import Any, Dict
import urllib.request
from io import StringIO

import numpy as np
import pandas as pd
from ..base_loader import ClimateLoader
from ...utils.countries import country_name_to_code, is_country_code


class NinjaRenewablesClimate(ClimateLoader):
    """Loader of the climate.

    Data comes from
    `Ninja Renewable <https://www.renewables.ninja/>`_
    The raw datasets are downloaded on demand by this dataloader.
    It corresponds to MERRA-2(global).

    Available data:

    - 'datetime' in UTC
    - 'precipitation'
    - 'snowfall'
    - 'snow_mass'
    - 'clearness'
    - 'air_density'
    - 'outside_temperature'
    - 'irradiance'

    Attributes:
        weighted_type: The method used to weight the climate.
            This was performed by Renewables.ninja. Can be
            'population' or 'land_area'.

    Loaders:
        :py:meth:`~demod.datasets.base_loader.ClimateLoader.load_historical_climate_data`

    """

    DATASET_NAME = 'RenewablesNinja'
    # Default step size from ninja
    step_size = timedelta(hours=1)

    def __init__(
        self, country_name,
        update_raw_data: bool = False,
        weighted_type: str = 'pop',
        **kwargs
    ) -> Any:
        """Initialize the climate loader for the country.

        If update_raw_data, the raw data will be acutualized and parsed
        again, only for the selected country.
        """
        super().__init__(**kwargs)
        # Creates the path for the requested country
        self.parsed_path_climate = os.path.join(
            self.parsed_path_climate, country_name)
        # creates the parsed path
        if not os.path.exists(self.parsed_path_climate):
            os.mkdir(self.parsed_path_climate)
        # Creates the raw path
        if not os.path.exists(self.raw_path):
            os.mkdir(self.raw_path)

        self.country = country_name

        self._check_download_raw_file(update_raw_data, weighted_type)

    def _check_download_raw_file(self, update_raw_data, weighted_type):
        country_code = (
            country_name_to_code(self.country)
            if not is_country_code(self.country) else self.country
        )
        self.raw_file_path = os.path.join(
            self.raw_path, country_code + '_' + weighted_type + '.csv'
        )
        # Check if the raw file already exists and should not be updated
        if os.path.isfile(self.raw_file_path) and not update_raw_data:
            return
        # Else download it
        base_url = 'https://www.renewables.ninja/country_downloads/'
        list_data = [
            'precipitation',
            'temperature',
            'irradiance_surface',
            'irradiance_toa',
            'snowfall',
            'snow_mass',
            'cloud_cover',
            'air_density',
        ]
        merged_df = None
        for i in list_data:
            country_url_template = (
                '{country}/ninja-weather-country-{country}-'
                + i + '_{weighted_type}_wtd-merra2.csv'
            )
            country_url = base_url + country_url_template.format(
                country=country_code,
                weighted_type=weighted_type
            )
            print('Downloading {} raw data from {}.'.format(
                self.DATASET_NAME, country_url
            ))
            print('This can take some time.')
            # Creates the request
            user_agent = (
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) '
                'Gecko/2009021910 Firefox/3.0.7'
            )
            headers = {'User-Agent': user_agent}
            request = urllib.request.Request(country_url, None, headers)

            # Reads the url and  download the data
            with urllib.request.urlopen(request) as response:
                csv_data = response.read().decode('utf-8')
                df = pd.read_csv(StringIO(csv_data), skiprows=3, index_col=0)
                df = df[['DE']]  # keep only national average values
                df = df.rename(columns={'DE': i})
                if merged_df is None:
                    merged_df = df
                else:
                    # Add only new data column(s)
                    value_cols = [c for c in df.columns if c not in merged_df.columns]
                    merged_df = merged_df.merge(df[value_cols], on='time', how='outer')
            print('download finished')

        # Write final merged dataframe once
        merged_df.to_csv(self.raw_file_path, index=True)

        # Now the file is downloaded, we can remove old parsed data
        for f in os.listdir(self.parsed_path_climate):
            os.remove(os.path.join(self.parsed_path_climate, f))





    def _parse_historical_climate_data(self) -> Dict[str, np.ndarray]:
        """Parse the historical climate data.

        Returns:
            climate_dict: climate_dict with keys:
                - 'datetime' in UTC
                - 'precipitation'
                - 'snowfall'
                - 'snow_mass'
                - 'clearness'
                - 'air_density'
                - 'outside_temperature'
                - 'irradiance'
        """
        df = pd.read_csv(self.raw_file_path, index_col=0)

        out_dict = {}

        out_dict['datetime'] = np.array(
            df.index,
            dtype='datetime64'
        )

        out_dict['precipitation'] = np.array(df['precipitation'])
        out_dict['snowfall'] = np.array(df['snowfall'])
        out_dict['snow_mass'] = np.array(df['snow_mass'])

        out_dict['clearness'] = np.array(df['cloud_cover'])

        out_dict['air_density'] = np.array(df['air_density'])

        out_dict['outside_temperature'] = np.array(df['temperature'])

        radiation_direct = np.array(df['irradiance_surface'])
        radiation_diffuse = np.array(df['irradiance_toa'])
        # https://meteonorm.meteotest.ch/en/faq/definition-of-direct-and-diffuse-radiation
        out_dict['irradiance'] = radiation_diffuse + radiation_direct

        return out_dict
