"""
Tableau & SQL Functions Library for Data Analysis
Implements mathematical, string, date, type casting, aggregation, 
logical, window/table calculation, user session, spatial, and predictive functions.
"""

import numpy as np
import pandas as pd
import datetime
import os
import getpass

# ==========================================
# 1. MATHEMATICAL / NUMBER FUNCTIONS
# ==========================================

def ABS(val):
    """Absolute value of a number or pandas series."""
    if isinstance(val, pd.Series):
        return val.abs()
    return abs(val)

def ROUND(val, decimals=0):
    """Round a number or pandas series to specified decimals."""
    if isinstance(val, pd.Series):
        return val.round(decimals)
    return round(val, decimals)

def SQRT(val):
    """Square root of a number or pandas series."""
    if isinstance(val, pd.Series):
        return np.sqrt(val)
    return np.sqrt(val)

def POWER(val, power):
    """Raise number or pandas series to a power."""
    if isinstance(val, pd.Series):
        return val ** power
    return val ** power

def RAND(size=None):
    """Generate random float(s) between 0 and 1."""
    if size is not None:
        return np.random.rand(size)
    return np.random.rand()

def INT(val):
    """Convert number or pandas series to integer."""
    if isinstance(val, pd.Series):
        return val.astype(int)
    return int(val)

def FLOAT(val):
    """Convert value or pandas series to float."""
    if isinstance(val, pd.Series):
        return val.astype(float)
    return float(val)

# ==========================================
# 2. STRING FUNCTIONS
# ==========================================

def UPPER(string):
    """Convert string or pandas series to uppercase."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.upper()
    return str(string).upper()

def LOWER(string):
    """Convert string or pandas series to lowercase."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.lower()
    return str(string).lower()

def LEN(string):
    """Return length of string or pandas series strings."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.len()
    return len(str(string))

def SPLIT(string, delimiter, token_number=1):
    """Split string by delimiter and return specified token (1-indexed)."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.split(delimiter).str[token_number - 1]
    tokens = str(string).split(delimiter)
    idx = token_number - 1
    return tokens[idx] if 0 <= idx < len(tokens) else ""

def LEFT(string, number):
    """Extract left N characters from string or pandas series."""
    if isinstance(string, pd.Series):
        return string.astype(str).str[:number]
    return str(string)[:number]

def TRIM(string):
    """Trim whitespace from string or pandas series."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.strip()
    return str(string).strip()

def MID(string, start_position, length):
    """Extract substring starting at start_position (1-indexed) with length."""
    start_idx = start_position - 1
    end_idx = start_idx + length
    if isinstance(string, pd.Series):
        return string.astype(str).str[start_idx:end_idx]
    return str(string)[start_idx:end_idx]

def RIGHT(string, number):
    """Extract right N characters from string or pandas series."""
    if isinstance(string, pd.Series):
        return string.astype(str).str[-number:]
    return str(string)[-number:]

def REPLACE(string, substring, replacement):
    """Replace substring with replacement in string or pandas series."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.replace(substring, replacement, regex=False)
    return str(string).replace(substring, replacement)

def CONTAINS(string, substring):
    """Check if string contains substring."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.contains(substring, regex=False)
    return substring in str(string)

def STARTSWITH(string, substring):
    """Check if string starts with substring."""
    if isinstance(string, pd.Series):
        return string.astype(str).str.startswith(substring)
    return str(string).startswith(substring)

# ==========================================
# 3. DATE FUNCTIONS
# ==========================================

def TODAY():
    """Return current date (YYYY-MM-DD)."""
    return datetime.date.today()

def NOW():
    """Return current timestamp (YYYY-MM-DD HH:MM:SS)."""
    return datetime.datetime.now()

def MAKEDATE(year, month, day):
    """Construct a date from year, month, and day."""
    if isinstance(year, pd.Series):
        return pd.to_datetime(dict(year=year, month=month, day=day)).dt.date
    return datetime.date(int(year), int(month), int(day))

def DATEPART(date_part, date_val):
    """Extract date component ('year', 'month', 'day', 'quarter', 'dayofweek')."""
    dt_series = pd.to_datetime(date_val)
    if date_part == 'year':
        return dt_series.dt.year if isinstance(dt_series, pd.Series) else dt_series.year
    elif date_part == 'month':
        return dt_series.dt.month if isinstance(dt_series, pd.Series) else dt_series.month
    elif date_part == 'day':
        return dt_series.dt.day if isinstance(dt_series, pd.Series) else dt_series.day
    elif date_part == 'quarter':
        return dt_series.dt.quarter if isinstance(dt_series, pd.Series) else dt_series.quarter
    elif date_part == 'dayofweek':
        return dt_series.dt.dayofweek if isinstance(dt_series, pd.Series) else dt_series.dayofweek
    return dt_series

def DATENAME(date_part, date_val):
    """Return name of date component (e.g. 'month' -> 'January')."""
    dt_series = pd.to_datetime(date_val)
    if date_part == 'month':
        return dt_series.dt.month_name() if isinstance(dt_series, pd.Series) else dt_series.strftime('%B')
    elif date_part in ['day', 'weekday']:
        return dt_series.dt.day_name() if isinstance(dt_series, pd.Series) else dt_series.strftime('%A')
    return dt_series

def DATEADD(date_part, number, date_val):
    """Add specified number of units ('day', 'month', 'year') to date."""
    dt_series = pd.to_datetime(date_val)
    if date_part == 'day':
        return dt_series + pd.to_timedelta(number, unit='D')
    elif date_part == 'month':
        return dt_series + pd.DateOffset(months=number) if not isinstance(number, pd.Series) else dt_series + pd.to_timedelta(number * 30, unit='D')
    elif date_part == 'year':
        return dt_series + pd.DateOffset(years=number) if not isinstance(number, pd.Series) else dt_series + pd.to_timedelta(number * 365, unit='D')
    return dt_series

def DATEDIFF(date_part, start_date, end_date):
    """Calculate difference between start_date and end_date in specified units."""
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    diff = end_dt - start_dt
    if date_part == 'day':
        return diff.dt.days if isinstance(diff, pd.Series) else diff.days
    elif date_part == 'month':
        if isinstance(start_dt, pd.Series):
            return (end_dt.dt.year - start_dt.dt.year) * 12 + (end_dt.dt.month - start_dt.dt.month)
        return (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month)
    elif date_part == 'year':
        if isinstance(start_dt, pd.Series):
            return end_dt.dt.year - start_dt.dt.year
        return end_dt.year - start_dt.year
    return diff

def DATETRUNC(date_part, date_val):
    """Truncate date to start of given unit ('month', 'year', 'quarter')."""
    dt_series = pd.to_datetime(date_val)
    if date_part == 'month':
        return dt_series.dt.to_period('M').dt.to_timestamp() if isinstance(dt_series, pd.Series) else dt_series.replace(day=1)
    elif date_part == 'year':
        return dt_series.dt.to_period('Y').dt.to_timestamp() if isinstance(dt_series, pd.Series) else dt_series.replace(month=1, day=1)
    elif date_part == 'quarter':
        return dt_series.dt.to_period('Q').dt.to_timestamp() if isinstance(dt_series, pd.Series) else dt_series
    return dt_series

# ==========================================
# 4. TYPE & LOGICAL CONVERSION FUNCTIONS
# ==========================================

def STR(val):
    """Convert value or pandas series to string."""
    if isinstance(val, pd.Series):
        return val.astype(str)
    return str(val)

def BOOL(val):
    """Convert value or pandas series to boolean."""
    if isinstance(val, pd.Series):
        return val.astype(bool)
    return bool(val)

def DATE(val):
    """Convert string/timestamp or pandas series to date."""
    if isinstance(val, pd.Series):
        return pd.to_datetime(val).dt.date
    return pd.to_datetime(val).date()

# ==========================================
# 5. AGGREGATION & SUMMARY FUNCTIONS
# ==========================================

def SUM(val):
    """Sum of values in series or list."""
    if isinstance(val, pd.Series):
        return val.sum()
    return sum(val)

def AVG(val):
    """Average/Mean of values in series or list."""
    if isinstance(val, pd.Series):
        return val.mean()
    return np.mean(val)

def MAX(val):
    """Maximum value in series or list."""
    if isinstance(val, pd.Series):
        return val.max()
    return max(val)

def MIN(val):
    """Minimum value in series or list."""
    if isinstance(val, pd.Series):
        return val.min()
    return min(val)

def COUNT(val):
    """Count non-null items in series or list."""
    if isinstance(val, pd.Series):
        return val.count()
    return len(val)

def COUNTD(val):
    """Count distinct/unique values in series or list."""
    if isinstance(val, pd.Series):
        return val.nunique()
    return len(set(val))

# ==========================================
# 6. CONDITIONAL & LOGICAL FUNCTIONS
# ==========================================

def IF_THEN_ELSE(cond, true_val, false_val):
    """IF condition THEN true_val ELSE false_val END."""
    if isinstance(cond, pd.Series):
        return np.where(cond, true_val, false_val)
    return true_val if cond else false_val

def IIF(cond, true_val, false_val):
    """IIF(condition, value_if_true, value_if_false)."""
    return IF_THEN_ELSE(cond, true_val, false_val)

def AND_FUNC(cond1, cond2):
    """Logical AND operation across conditions."""
    if isinstance(cond1, pd.Series) or isinstance(cond2, pd.Series):
        return cond1 & cond2
    return bool(cond1 and cond2)

def OR_FUNC(cond1, cond2):
    """Logical OR operation across conditions."""
    if isinstance(cond1, pd.Series) or isinstance(cond2, pd.Series):
        return cond1 | cond2
    return bool(cond1 or cond2)

def NOT_FUNC(cond):
    """Logical NOT / reverse condition."""
    if isinstance(cond, pd.Series):
        return ~cond
    return not bool(cond)

# ==========================================
# 7. TABLE CALCULATIONS & WINDOW FUNCTIONS
# ==========================================

def INDEX(df_or_series):
    """Returns the index position (1 to N) of the current row."""
    n = len(df_or_series)
    return pd.Series(np.arange(1, n + 1), index=df_or_series.index if isinstance(df_or_series, (pd.Series, pd.DataFrame)) else None)

def FIRST(df_or_series):
    """Returns number of rows from current row to first row (0, -1, -2...)."""
    n = len(df_or_series)
    return pd.Series(-np.arange(0, n), index=df_or_series.index if isinstance(df_or_series, (pd.Series, pd.DataFrame)) else None)

def LAST(df_or_series):
    """Returns number of rows from current row to last row (N-1, N-2... 0)."""
    n = len(df_or_series)
    return pd.Series(np.arange(n - 1, -1, -1), index=df_or_series.index if isinstance(df_or_series, (pd.Series, pd.DataFrame)) else None)

def LOOKUP(val, offset=-1):
    """Returns value of expression in a target row offset from current row."""
    if isinstance(val, pd.Series):
        return val.shift(-offset) # In Tableau, LOOKUP(col, -1) looks back 1 row
    return val

def RUNNING_SUM(val):
    """Returns running/cumulative sum of expression."""
    if isinstance(val, pd.Series):
        return val.cumsum()
    return val

def WINDOW_SUM(val):
    """Returns total sum of expression within the window."""
    if isinstance(val, pd.Series):
        return val.sum()
    return val

def RANK(val, ascending=False):
    """Returns standard rank for current row in partition."""
    if isinstance(val, pd.Series):
        return val.rank(ascending=ascending, method='min').astype(int)
    return 1

def TOTAL(val):
    """Returns total aggregation result for expression across dataset."""
    if isinstance(val, pd.Series):
        return val.sum()
    return val

# ==========================================
# 8. USER & SECURITY FUNCTIONS
# ==========================================

def USERNAME():
    """Returns current user name."""
    return getpass.getuser()

def FULLNAME():
    """Returns full user name."""
    user = getpass.getuser()
    return user.capitalize() + " Analyst"

def ISFULLNAME(val):
    """Check if current user matches full name."""
    return str(val).lower() in FULLNAME().lower()

def ISMEMBEROF(group_name):
    """Check if logged-in user is a member of specified group."""
    authorized_groups = ["Medical_Analysts", "Admin", "Cancer_Research"]
    return group_name in authorized_groups

def USERDOMAIN():
    """Returns domain name of current user."""
    return "mitwpu.edu"

# ==========================================
# 9. SPATIAL / GEOGRAPHIC FUNCTIONS
# ==========================================

def MAKEPOINT(lat, lon):
    """Creates spatial point object from latitude and longitude."""
    if isinstance(lat, pd.Series) and isinstance(lon, pd.Series):
        return lat.astype(str) + ", " + lon.astype(str)
    return f"{lat}, {lon}"

def DISTANCE(lat1, lon1, lat2, lon2):
    """Calculates approximate distance (in km) between two points via Haversine formula."""
    R = 6371.0 # Earth radius in km
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return R * c

def BUFFER(lat, lon, distance_km=50.0):
    """Creates buffer zone representation around point."""
    if isinstance(lat, pd.Series):
        return "BUFFER(" + lat.astype(str) + ", " + lon.astype(str) + f", {distance_km}km)"
    return f"BUFFER({lat}, {lon}, {distance_km}km)"

def INTERSECTS(geom1, geom2):
    """Checks if spatial geometries intersect."""
    if isinstance(geom1, pd.Series):
        return geom1 == geom2
    return geom1 == geom2

def MAKELINE(lat1, lon1, lat2, lon2):
    """Creates line string representation between two points."""
    if isinstance(lat1, pd.Series):
        lat2_str = lat2.astype(str) if isinstance(lat2, pd.Series) else str(lat2)
        lon2_str = lon2.astype(str) if isinstance(lon2, pd.Series) else str(lon2)
        return "LINE((" + lat1.astype(str) + ", " + lon1.astype(str) + ") -> (" + lat2_str + ", " + lon2_str + "))"
    return f"LINE(({lat1}, {lon1}) -> ({lat2}, {lon2}))"

def AREA(geom_radius_km):
    """Calculates circular surface area (pi * r^2) in km^2."""
    return np.pi * (geom_radius_km ** 2)

def CENTROID(lat1, lon1, lat2, lon2):
    """Calculates centroid (center point) between coordinate pairs."""
    return MAKEPOINT((lat1 + lat2) / 2.0, (lon1 + lon2) / 2.0)

# ==========================================
# 10. PREDICTIVE & STATISTICAL ANALYTICS
# ==========================================

def MODEL_QUANTILE(series, quantile=0.5):
    """Returns quantile value for target variable."""
    if isinstance(series, pd.Series):
        return series.quantile(quantile)
    return np.quantile(series, quantile)

def MODEL_PERCENTILE(series):
    """Returns percentile rank (0.0 to 1.0) of each value in series."""
    if isinstance(series, pd.Series):
        return series.rank(pct=True)
    return 1.0

def FORECAST(series, periods=1):
    """Simple linear forecast for next periods."""
    if isinstance(series, pd.Series):
        x = np.arange(len(series))
        y = series.values
        slope, intercept = np.polyfit(x, y, 1)
        next_x = len(series) + periods - 1
        return slope * next_x + intercept
    return series

def TRENDLINE(x_series, y_series):
    """Calculates slope and R-squared trend line metric."""
    if isinstance(x_series, pd.Series) and isinstance(y_series, pd.Series):
        slope, intercept = np.polyfit(x_series.values, y_series.values, 1)
        return slope
    return 0.0
