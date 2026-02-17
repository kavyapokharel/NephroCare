import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Force non-GUI backend for Django servers
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import io
import os


# ============================================================
# Helper: Create figure and return bytes for API
# ============================================================
def save_fig_to_bytes(fig, filename=None):
    """
    Saves a matplotlib figure to both:
       - a local JPG file (optional)
       - an in-memory buffer for Django REST

    Returns:
        bytes: Raw image data
    """

    # Save to file if requested
    if filename:
        fig.savefig(filename, format='jpg', dpi=300, bbox_inches='tight')

    # Save to BytesIO buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format='jpg', dpi=300, bbox_inches='tight')

    buffer.seek(0)
    plt.close(fig)
    return buffer.read()


# ============================================================
# 1) BLOOD PRESSURE PLOT
# ============================================================
def generateBPPlot(size, for_type='Blood Pressure',
                   file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\Blood Pressure.xlsx'):

    output_filename = 'blood_pressure_plot.jpg'

    try:
        df = pd.read_excel(file).sort_values(by='date')
        df['date'] = pd.to_datetime(df['date'])

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))

        systolic_color = '#E53E3E'
        diastolic_color = '#38B2AC'

        ax.plot(df['date'], df['systolic'], label='Systolic Pressure',
                color=systolic_color, linewidth=3, marker='o',
                markersize=6, markeredgecolor='white', alpha=0.8,
                linestyle='--')

        ax.plot(df['date'], df['diastolic'], label='Diastolic Pressure',
                color=diastolic_color, linewidth=3, marker='s',
                markersize=6, markeredgecolor='white', alpha=0.8)

        ax.set_title(f'{for_type} Trend Over Time', fontsize=18, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Pressure (mmHg)')

        ax.set_ylim(min(df[['systolic', 'diastolic']].min()) - 10,
                    df['systolic'].max() + 10)

        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

        plt.tight_layout()

        return save_fig_to_bytes(fig, output_filename)

    except Exception as e:
        print(f"Error generating Blood Pressure plot: {e}")
        return None


# ============================================================
# 2) BODY WEIGHT PLOT
# ============================================================
def generateBodyWeightPlot(size, for_type='Body Weight',
                           file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\Body Weight.xlsx'):

    output_filename = 'body_weight_plot.jpg'

    try:
        df = pd.read_excel(file).sort_values(by='date')
        df['date'] = pd.to_datetime(df['date'])

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))

        weight_color = '#4299E1'

        ax.plot(df['date'], df['weight'], label='Body Weight',
                color=weight_color, linewidth=4, marker='D',
                markersize=7, markeredgecolor='white', alpha=0.9)

        ax.set_title(f'{for_type} Trend Over Time', fontsize=18, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Weight (lbs)')

        min_weight, max_weight = df['weight'].min(), df['weight'].max()
        ax.set_ylim(min_weight - max(5, min_weight * 0.05),
                    max_weight + max(5, max_weight * 0.05))

        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

        plt.tight_layout()

        return save_fig_to_bytes(fig, output_filename)

    except Exception as e:
        print(f"Error generating Body Weight plot: {e}")
        return None


# ============================================================
# 3) BLOOD SUGAR PLOT
# ============================================================
def generateBloodSugarPlot(size, for_type='Blood Sugar',
                           file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\Blood Sugar.xlsx'):

    output_filename = 'blood_sugar_plot.jpg'

    try:
        df = pd.read_excel(file).sort_values(by='date')
        df['date'] = pd.to_datetime(df['date'])

        bs_column = 'blood sugar (mg/dL)'

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))

        bs_color = '#F6AD55'

        ax.plot(df['date'], df[bs_column], label='Blood Sugar Reading',
                color=bs_color, linewidth=3.5, marker='^',
                markersize=7, markeredgecolor='white', alpha=0.9)

        ax.set_title(f'{for_type} Trend Over Time', fontsize=18, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel(bs_column)

        min_bs, max_bs = df[bs_column].min(), df[bs_column].max()
        ax.set_ylim(min_bs - max(10, min_bs * 0.05),
                    max_bs + max(10, max_bs * 0.05))

        ax.axhspan(70, 180, color='green', alpha=0.1, zorder=0)
        ax.axhline(180, color='red', linestyle='--', linewidth=1)

        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

        plt.tight_layout()

        return save_fig_to_bytes(fig, output_filename)

    except Exception as e:
        print(f"Error generating Blood Sugar plot: {e}")
        return None


# ============================================================
# 4) EXPENDITURE PIE CHART
# ============================================================
def expenditureChart(size=(12, 8),
                     file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\expenditure.xlsx'):

    output_filename = 'expenditure_chart.jpg'

    try:
        df = pd.read_excel(file)

        expenditure_summary = df.groupby('item')['price'].sum()
        items = expenditure_summary.index
        prices = expenditure_summary.values

        if len(prices) == 0:
            print("No data for expenditure chart.")
            return None

        plt.style.use('seaborn-v0_8-pastel')
        fig, ax = plt.subplots(figsize=size)

        colors = plt.cm.Set3.colors
        max_index = prices.argmax()
        explode = [0.05 if i == max_index else 0 for i in range(len(prices))]

        ax.pie(prices, labels=items, explode=explode, startangle=90,
               colors=colors, autopct=lambda p: f'${p/100.*prices.sum():,.2f}',
               wedgeprops={'edgecolor': 'black'})

        ax.axis('equal')
        ax.set_title("Total Expenditure by Category", fontsize=18, fontweight="bold")

        plt.tight_layout()

        return save_fig_to_bytes(fig, output_filename)

    except Exception as e:
        print(f"Error generating expenditure chart: {e}")
        return None


# ============================================================
# 5) EXPENDITURE LOG OUTPUT
# ============================================================
def expenditureLog(file=r'D:\VSCode WorkSpace\Hachathon2025\backend\carepilot\expenditure.xlsx'):
    try:
        df = pd.read_excel(file)

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        if 'price' in df.columns:
            df['price'] = df['price'].apply(lambda x: f"${x:.2f}")

        return df[['item', 'date', 'patient']].to_string(index=False)

    except Exception as e:
        return f"Error generating expenditure log: {e}"
