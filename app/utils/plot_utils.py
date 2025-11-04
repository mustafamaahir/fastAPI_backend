# app/utils/plot_utils.py
# Utilities to render matplotlib plots to PNG bytes.

import io
import matplotlib.pyplot as plt
from typing import List


def plot_dates_values_png_bytes(dates: List[str], values: List[float], title: str = "Forecast"):
    """
    Create a line plot for given ISO date strings and numeric values.
    Return PNG bytes (not base64) ready for StreamingResponse.
    """
    plt.figure(figsize=(10, 4.5))
    plt.plot(dates, values, marker="o", linestyle="-")
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Rainfall")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()
    buf.seek(0)
    return buf.getvalue()
