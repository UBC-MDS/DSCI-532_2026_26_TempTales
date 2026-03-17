"""
Table styling utilities.
Provides diverging color-coded styles for data tables.
"""
import pandas as pd


def diverging_styles(cells: list, alpha: float = 0.65) -> list:
    """
    Generate DataGrid styles for a diverging color scale.
    0 = neutral gray, negative = blue, positive = red.

    Args:
        cells: list of (row_idx, col_idx, value) tuples
        alpha: background opacity (0.0 to 1.0)

    Returns:
        List of style dicts compatible with Shiny's render.DataGrid styles param.
    """
    if not cells:
        return []

    vals = [v for _, _, v in cells]
    low = min(min(vals), 0)
    high = max(max(vals), 0)
    eps = 1e-9
    if high - low < eps:
        high = low + eps

    WHITE = (255, 255, 255)
    BLUE  = (41, 128, 185)
    RED   = (231, 76, 60)

    def _interp(t: float, c0: tuple, c1: tuple) -> str:
        r = int(c0[0] + t * (c1[0] - c0[0]))
        g = int(c0[1] + t * (c1[1] - c0[1]))
        b = int(c0[2] + t * (c1[2] - c0[2]))
        return f"rgba({r},{g},{b},{alpha})"

    styles = []
    for row_idx, col_idx, val_num in cells:
        if val_num < 0:
            t = val_num / low if low < -eps else 0
            t = max(0.0, min(1.0, t))
            bg = _interp(t, WHITE, BLUE)
        elif val_num > 0:
            t = val_num / high if high > eps else 0
            t = max(0.0, min(1.0, t))
            bg = _interp(t, WHITE, RED)
        else:
            bg = "rgba(248,249,250,0.5)"

        styles.append({
            "rows": [row_idx],
            "cols": [col_idx],
            "style": {"color": "#333", "backgroundColor": bg}
        })
    return styles


def table_styles_wide(df: pd.DataFrame) -> list:
    """
    Generate diverging color styles for the Change row (row index 2)
    in the wide-format monthly comparison table.

    Positive values (warming) trend red, negative (cooling) trend blue,
    zero is neutral. Intensity scales with magnitude relative to
    the largest value in that row.

    Args:
        df: Wide-format DataFrame with at least 3 rows. Row 2 is the
            Change row. Columns from index 1 onward are month values.

    Returns:
        List of style dicts compatible with Shiny's render.DataGrid styles param.
    """
    if df.empty or df.shape[0] < 3:
        return []

    row_idx = 2
    cells = []
    for col_idx in range(1, df.shape[1]):
        try:
            val = df.iloc[row_idx, col_idx]
        except (IndexError, KeyError):
            continue
        if pd.isna(val):
            continue
        try:
            cells.append((row_idx, col_idx, float(val)))
        except (ValueError, TypeError):
            continue

    return diverging_styles(cells)
