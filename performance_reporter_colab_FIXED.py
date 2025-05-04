# %%
import os


# %%
import pandas as pd


# %%
import matplotlib.pyplot as plt



# %%
def generate_performance_report(csv_path, report_name='performance_report', save_dir='reports/', export_html=False, export_pdf=False):
    """
    Erstellt Performance-Report aus Trade-Log-Datei (CSV) mit KPIs und speichert optional HTML/PDF.
    """
    try:
        if not os.path.exists(csv_path):
            print(f"⚠️ Datei nicht gefunden: {csv_path}")
            return None

        df = pd.read_csv(csv_path, parse_dates=['timestamp'])

        buys = df[df['action'] == 'BUY'].reset_index(drop=True)
        sells = df[df['action'] == 'SELL'].reset_index(drop=True)

        if buys.empty or sells.empty:
            print("⚠️ Nicht genügend Trades für Auswertung.")
            return None

        profits = sells['price'].values - buys['price'].values
        reasons = buys['reason'][:len(profits)].tolist()
        timestamps = sells['timestamp'][:len(profits)].tolist()

        report_df = pd.DataFrame({
            'timestamp': timestamps,
            'entry_price': buys['price'][:len(profits)].values,
            'exit_price': sells['price'][:len(profits)].values,
            'profit': profits,
            'reason': reasons,
            'duration_min': (sells['timestamp'].values[:len(profits)] - buys['timestamp'].values[:len(profits)]) / pd.Timedelta(minutes=1)
        })

        # KPIs
        total_profit = report_df['profit'].sum()
        win_trades = report_df[report_df['profit'] > 0].shape[0]
        loss_trades = report_df[report_df['profit'] <= 0].shape[0]
        total_trades = len(report_df)

        print("\n📈 Performance Report")
        print(f"Trades: {total_trades}")
        print(f"Gewinn-Trades: {win_trades}")
        print(f"Verlust-Trades: {loss_trades}")
        print(f"Gesamter Profit: {total_profit:.2f}")

        # Report speichern
        os.makedirs(save_dir, exist_ok=True)
        report_df.to_csv(os.path.join(save_dir, f"{report_name}_table.csv"), index=False)

        # Optional Export als Notebook → HTML/PDF
        if export_html or export_pdf:


# %%
            from IPython.display import Javascript
            print("💾 Notebook wird gespeichert...")
            display(Javascript('IPython.notebook.save_checkpoint();'))

            notebook_path = f"/content/drive/MyDrive/CryptoTradingAI/reports/{report_name}.ipynb"
            if export_html:
                os.system(f'jupyter nbconvert "{notebook_path}" --to html --output "{report_name}.html" --output-dir="{save_dir}"')
                print(f"📄 HTML gespeichert: {save_dir}{report_name}.html")
            if export_pdf:
                os.system(f'jupyter nbconvert "{notebook_path}" --to pdf --output "{report_name}.pdf" --output-dir="{save_dir}"')
                print(f"📄 PDF gespeichert: {save_dir}{report_name}.pdf")

        return report_df
    except Exception as e:
        print("❌ Fehler beim Report:", e)
        return None