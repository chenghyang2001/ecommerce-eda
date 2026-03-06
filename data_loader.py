"""資料載入與整理模組"""
import pandas as pd


class EcommerceDataLoader:
    """電商資料載入器，負責讀取、清洗、特徵工程"""

    def __init__(self, data_path: str = 'ecommerce_data/orders.csv'):
        self.data_path = data_path
        self.df = None

    def load(self) -> pd.DataFrame:
        """載入並處理資料"""
        self.df = pd.read_csv(self.data_path)
        self._process_dates()
        return self.df

    def _process_dates(self):
        """日期特徵工程"""
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self.df['year'] = self.df['order_date'].dt.year
        self.df['month'] = self.df['order_date'].dt.month
        self.df['year_month'] = self.df['order_date'].dt.to_period('M').astype(str)

    def filter_by_year(self, year: int) -> pd.DataFrame:
        """篩選特定年份的資料"""
        if self.df is None:
            self.load()
        return self.df[self.df['year'] == year].copy()

    def get_date_range(self) -> tuple:
        """取得資料日期範圍"""
        if self.df is None:
            self.load()
        return self.df['order_date'].min(), self.df['order_date'].max()


def load_and_process_data(data_path: str = 'ecommerce_data/orders.csv') -> pd.DataFrame:
    """簡易介面：一行載入並處理資料"""
    loader = EcommerceDataLoader(data_path)
    return loader.load()
