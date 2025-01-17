import requests
from bs4 import BeautifulSoup
import pandas as pd

class VitibrasilScraper:
    BASE_URL = 'http://vitibrasil.cnpuv.embrapa.br/index.php'

    def __init__(self, year: int = 2023):
        if not isinstance(year, int):
            raise TypeError(f"Expected an integer, but got {type(year).__name__}")
        if not (1970 <= year <= 2023):
            raise ValueError("The year must be between 1970 and 2023")
        self.year = year

    def _fetch_data(self, opcao: str, subopcao: str = None) -> BeautifulSoup:
        try:
            params = {
                'ano': self.year,
                'opcao': opcao
            }
            if subopcao:
                params['subopcao'] = subopcao

            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")
            return None

    def get_production(self) -> pd.DataFrame:
        soup = self._fetch_data('opt_02')
        if soup is None:
            return None

        return self._parse_table(soup, ['category', 'product', 'quantity_l'])

    def get_processing(self) -> pd.DataFrame:
        grape_types = {
            1: 'Viníferas',
            2: 'Americanas e híbridas',
            3: 'Uvas de mesa',
            4: 'Sem classificação'
        }
        rows = []
        for key, grape_type in grape_types.items():
            soup = self._fetch_data('opt_03', f'subopt_0{key}')
            if soup is None:
                continue
            rows.extend(self._parse_processing_data(soup, grape_type))

        return pd.DataFrame(rows, index=range(1, len(rows) + 1))

    def get_commercialization(self) -> pd.DataFrame:
        soup = self._fetch_data('opt_04')
        if soup is None:
            return None

        return self._parse_table(soup, ['product', 'type', 'quantity_l'])

    def get_importation(self) -> pd.DataFrame:
        table_wine = {
            1: 'Vinhos de Mesa',
            2: 'Espumantes',
            3: 'Uvas frescas',
            4: 'Uvas passas',
            5: 'Suco de uva'
        }
        rows = []
        for key, wine_type in table_wine.items():
            soup = self._fetch_data('opt_05', f'subopt_0{key}')
            if soup is None:
                continue
            rows.extend(self._parse_import_export_data(soup, wine_type))

        return pd.DataFrame(rows, index=range(1, len(rows) + 1))

    def get_exportation(self) -> pd.DataFrame:
        table_wine = {
            1: 'Vinhos de Mesa',
            2: 'Espumantes',
            3: 'Uvas frescas',
            4: 'Suco de uva'
        }
        rows = []
        for key, wine_type in table_wine.items():
            soup = self._fetch_data('opt_06', f'subopt_0{key}')
            if soup is None:
                continue
            rows.extend(self._parse_import_export_data(soup, wine_type))

        return pd.DataFrame(rows, index=range(1, len(rows) + 1))

    def _parse_table(self, soup: BeautifulSoup, columns: list) -> pd.DataFrame:
        table = soup.find('table', {'class', 'tb_base tb_dados'})
        tbody = table.find('tbody')

        data = []
        current_item = None

        for row in tbody.find_all('tr'):
            row_classes = [td.get('class', []) for td in row.find_all('td')]

            if any('tb_item' in classes for classes in row_classes):
                current_item = [col.text.strip() for col in row.find_all('td')]
                data.append({'item': current_item, 'subitems': []})
            elif any('tb_subitem' in classes for classes in row_classes):
                subitem = [col.text.strip() for col in row.find_all('td')]
                if current_item:
                    data[-1]['subitems'].append(subitem)

        rows = []
        for entry in data:
            item_name, _ = entry['item']
            for subitem_name, subitem_value in entry['subitems']:
                rows.append({columns[0]: item_name, columns[1]: subitem_name, columns[2]: subitem_value})

        return pd.DataFrame(rows, index=range(1, len(rows) + 1))

    def _parse_processing_data(self, soup: BeautifulSoup, grape_type: str) -> list:
        table = soup.find('table', {'class', 'tb_base tb_dados'})
        tbody = table.find('tbody')
        data = []
        current_item = None

        for row in tbody.find_all('tr'):
            row_classes = [td.get('class', []) for td in row.find_all('td')]

            if any('tb_item' in classes for classes in row_classes):
                current_item = [col.text.strip() for col in row.find_all('td')]
                data.append({'item': current_item, 'subitems': []})
            elif any('tb_subitem' in classes for classes in row_classes):
                subitem = [col.text.strip() for col in row.find_all('td')]
                if current_item:
                    data[-1]['subitems'].append(subitem)

        rows = []
        for entry in data:
            item_name, item_value = entry['item']
            if 'subitems' in entry and entry['subitems']:
                for subitem_name, subitem_value in entry['subitems']:
                    rows.append({
                        'grape_type': grape_type,
                        'category': item_name,
                        'sub_category': subitem_name,
                        'quantity_kg': subitem_value
                    })
            else:
                rows.append({
                    'grape_type': grape_type,
                    'category': item_name,
                    'sub_category': '-',
                    'quantity_kg': item_value
                })
        return rows

    def _parse_import_export_data(self, soup: BeautifulSoup, wine_type: str) -> list:
        table = soup.find('table', {'class', 'tb_base tb_dados'})
        tbody = table.find('tbody')
        data = []

        for row in tbody.find_all('tr'):
            current_item = [col.text.strip() for col in row.find_all('td')]
            data.append({'item': current_item})

        rows = []
        for entry in data:
            country, qty, amt = entry['item']
            rows.append({
                'table_wine': wine_type,
                'country': country,
                'quantity_kg': qty,
                'ammount_usd': amt
            })
        return rows

# Example Usage
# scraper = VitibrasilScraper(year=2023)
# production_df = scraper.get_production()
# print(production_df)