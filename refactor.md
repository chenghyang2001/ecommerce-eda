# EDA Notebook 重構需求

## 目標
將 EDA.ipynb 重構為模組化、可維護的程式碼結構。

## 四大重構目標

1. **資料讀取邏輯獨立**：建立 `data_loader.py`，提供 `load_and_process_data()` 簡易介面和 `EcommerceDataLoader` 完整類別
2. **建立業務指標模組**：建立 `business_metrics.py`，用 `BusinessMetricsCalculator` 計算營收、產品、地理、滿意度、配送五大面向指標
3. **改善視覺化**：建立 `MetricsVisualizer` 產生 Plotly 互動式圖表（營收趨勢、類別表現、州營收、滿意度分布）
4. **增加設定檔管理參數**：第一個 cell 提供可調整參數（ANALYSIS_YEAR、COMPARISON_YEAR、DATA_PATH 等）

## 預期產出
- `data_loader.py` — 資料讀取與整理
- `business_metrics.py` — 業務指標計算 + 視覺化
- `EDA_Refactored.ipynb` — 重構後的 Notebook
- `requirements.txt` — 相依套件
- `README.md` — 說明文件
