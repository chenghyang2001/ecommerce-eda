"""業務指標計算與視覺化模組"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class BusinessMetricsCalculator:
    """計算五大面向業務指標：營收、產品、地理、滿意度、配送"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def revenue_metrics(self) -> dict:
        """營收指標"""
        monthly = self.df.groupby('year_month')['total_amount'].sum().reset_index()
        monthly.columns = ['month', 'revenue']
        monthly['growth_rate'] = monthly['revenue'].pct_change() * 100

        return {
            'total_revenue': self.df['total_amount'].sum(),
            'total_orders': len(self.df),
            'avg_order_value': self.df['total_amount'].mean(),
            'monthly_revenue': monthly,
            'latest_growth': monthly['growth_rate'].iloc[-1] if len(monthly) > 1 else 0,
        }

    def product_metrics(self) -> pd.DataFrame:
        """產品類別指標"""
        return self.df.groupby('category').agg(
            order_count=('order_id', 'count'),
            total_revenue=('total_amount', 'sum'),
            avg_price=('unit_price', 'mean'),
            avg_satisfaction=('customer_satisfaction', 'mean'),
        ).round(2).sort_values('total_revenue', ascending=False).reset_index()

    def geo_metrics(self) -> pd.DataFrame:
        """地理指標"""
        return self.df.groupby('state').agg(
            total_revenue=('total_amount', 'sum'),
            order_count=('order_id', 'count'),
        ).round(2).sort_values('total_revenue', ascending=False).reset_index()

    def satisfaction_metrics(self) -> dict:
        """滿意度指標"""
        return {
            'mean': self.df['customer_satisfaction'].mean(),
            'median': self.df['customer_satisfaction'].median(),
            'distribution': self.df['customer_satisfaction'].value_counts().sort_index(),
        }

    def delivery_metrics(self) -> dict:
        """配送指標"""
        return {
            'avg_days': self.df['delivery_days'].mean(),
            'median_days': self.df['delivery_days'].median(),
            'over_7_days_pct': (self.df['delivery_days'] > 7).mean() * 100,
            'by_satisfaction': self.df.groupby('delivery_days')['customer_satisfaction'].mean().reset_index(),
        }


class MetricsVisualizer:
    """Plotly 互動式圖表產生器"""

    @staticmethod
    def revenue_trend(monthly_df: pd.DataFrame) -> go.Figure:
        """月營收趨勢圖"""
        fig = px.line(monthly_df, x='month', y='revenue',
                      title='Monthly Revenue Trend',
                      labels={'month': 'Month', 'revenue': 'Revenue ($)'})
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    @staticmethod
    def category_performance(product_df: pd.DataFrame) -> go.Figure:
        """類別表現圖"""
        fig = px.bar(product_df, x='category', y='total_revenue',
                     color='avg_satisfaction', title='Category Revenue & Satisfaction',
                     labels={'category': 'Category', 'total_revenue': 'Revenue ($)'},
                     color_continuous_scale='RdYlGn')
        return fig

    @staticmethod
    def state_revenue(geo_df: pd.DataFrame) -> go.Figure:
        """各州營收排名"""
        geo_sorted = geo_df.sort_values('total_revenue', ascending=True)
        fig = px.bar(geo_sorted, x='total_revenue', y='state',
                     orientation='h', title='Revenue by State',
                     labels={'total_revenue': 'Revenue ($)', 'state': 'State'})
        return fig

    @staticmethod
    def satisfaction_distribution(df: pd.DataFrame) -> go.Figure:
        """滿意度分布圖"""
        fig = px.histogram(df, x='customer_satisfaction', nbins=5,
                           title='Customer Satisfaction Distribution',
                           labels={'customer_satisfaction': 'Satisfaction Score'})
        return fig

    @staticmethod
    def delivery_vs_satisfaction(delivery_df: pd.DataFrame) -> go.Figure:
        """配送天數 vs 滿意度"""
        fig = px.scatter(delivery_df, x='delivery_days', y='customer_satisfaction',
                         title='Delivery Days vs Satisfaction',
                         labels={'delivery_days': 'Delivery Days',
                                 'customer_satisfaction': 'Avg Satisfaction'})
        return fig
