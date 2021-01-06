import pandas as pd
import numpy as np


"""
A technical analysis library for python. 

This module is under active development. 


s - pandas series
h - high series
l - low series
w - acting window (integer)
"""


def _isSeries(s):
    """

    This function ensures all expected series arguements
    are instances of Pandas.Series

    Args:
      s (pandas series): a pandas series

    Returns:
      bool: If s is a Pandas Series, False otherwise

    """

    if isinstance(s, pd.Series):
        return True
    else:
        raise TypeError("s must be of type Pandas.Series")


def tsma(s, w):
    """

    This function calculates a simple moving average on series s
    with a window length of w

    Args:
      s (pandas series): a pandas series
      w (int): length of window

    Returns:
      o: (pandas series): simple moving average series
      o: (float): last value of series if len(s) == w

    """
    _isSeries(s)

    if len(s) == w:
        return s.mean()
    return s.rolling(window=w).mean()


def tstd(s, w):
    """

    This function calculates standard deviation on series s
    with a window length of w

    Args:
      s (pandas series): a pandas series
      w (int): length of window

    Returns:
      o: (pandas series): standard deviation series
      o: (float): last value of series if len(s) == w

    """
    _isSeries(s)

    if len(s) == w:
        return s.std()
    return s.rolling(window=w).std()


def tema(s, w, wilders=False):
    """

    This function calculates an exponential moving average on series s
    with a window length of w. 

    Args:
      s (pandas series): a pandas series
      w (int): length of window
      wilders (bool): Changes alpha value to 1/w if true

    Returns:
      o: (pandas series): exponential moving average series

    """
    _isSeries(s)

    if wilders:
        return s.ewm(alpha=1/w, adjust=False).mean()
    else:
        return s.ewm(span=w, adjust=False).mean()


def trsi(s, w):
    """

    This function calculates the relative strength index on series s
    with a window length of w. Wilders alpha constant is used for EMA

    Args:
      s (pandas series): a pandas series
      w (int): length of window

    Returns:
      o: (pandas series): RSI series

    """
    _isSeries(s)

    # cite https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
    delta = s.diff()

    pos, neg = delta.copy(), delta.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0

    pos_avg = tema(pos, w, wilders=True)
    neg_avg = tema(neg, w, wilders=True).abs()

    RS = pos_avg/neg_avg

    rsi = 100 - (100/(1+RS))
    return rsi


def tatr(s, h, l, w=21):
    """

    This function calculates the Average True Range on series s
    with a window length of w.

    Args:
      s (pandas series): a pandas series close
      h (pandas series): a pandas series high
      l (pandas series): a pandas series low
      w (int): length of window Default 21

    Returns:
      o: (pandas series): ATR series

    """
    _isSeries(s)
    _isSeries(h)
    _isSeries(l)

    # cite https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
    atr1 = pd.np.abs(h - l)
    atr2 = pd.np.abs(h - s.shift())
    atr3 = pd.np.abs(l - s.shift())

    temp = pd.concat([atr1, atr2, atr3], axis=1)
    tr = temp.max(axis=1)

    atr = tema(tr, w, wilders=True)

    return atr


def tmacd(s, w_slow=26, w_fast=12, w_signal=9):
    """

    This function calculates the Moving Average Crossover Divergence on series s
    with a window length of w.

    Args:
      s (pandas series): a pandas series close
      w_slow (int): slower EMA window Default 26
      w_slow (int): faster EMA window Default 12
      w_slow (int): signal EMA window Default 9

    Returns:
      df: (pandas DataFrame): MACD, SIGNAL Lines

    """
    _isSeries(s)

    ema_fast = tema(s, w_fast)
    ema_slow = tema(s, w_slow)
    macd = ema_fast - ema_slow
    signal = tema(macd, w_signal)

    df = pd.concat([ema_fast, ema_slow, macd, signal], axis=1)
    df.columns = ['ema_fast', 'ema_slow', 'macd', 'signal']
    return df


def tbollingerbands(s, w, std_multiplier=2):
    """

    This function calculates the Bollinger Bands on series s
    with a window length of w, and a std mulitplier of 2

    Args:
      s (pandas series): a pandas series close
      w (int): length of window
      std_multiplier (int): Multiplipier for standard deviation bands

    Returns:
      df: (pandas DataFrame): SMA, LOWER_BAND, UPPER_BAND

    """
    _isSeries(s)

    sma = tsma(s, w)
    std = tstd(s, w)
    lower_band = sma - (std * std_multiplier)
    upper_band = sma + (std * std_multiplier)

    df = pd.concat([sma, lower_band, upper_band], axis=1)
    df.columns = ['sma', 'lower_band', 'upper_band']
    return df


def tkeltnerchannels(s, h, l, w, atr_multiplier=1.5):
    """

    This function calculates the Keltner Channels on series s
    with a window length of w, and a atr mulitplier of 1.5

    Args:
      s (pandas series): a pandas series close
      h (pandas series): a pandas series high
      l (pandas series): a pandas series low
      w (int): length of window 
      atr_multiplier (int): Multiplipier for ATR channels

    Returns:
      df: (pandas DataFrame): EMA, LOWER_CHANNEL, UPPER_CHANNEL

    """
    _isSeries(s)
    _isSeries(h)
    _isSeries(l)

    ema = tema(s, w)
    atr = tatr(s, h, l, w=10)
    lower_channel = ema - (atr * atr_multiplier)
    upper_channel = ema + (atr * atr_multiplier)
    df = pd.concat([ema, lower_channel, upper_channel], axis=1)
    df.columns = ['ema', 'lower_channel', 'upper_channel']
    return df


def rolling_window(a, window):
    """

    This function reshapes an array a into a rolling window of 
    (-1, window)

    Args:
      a (numpy array): a numpy array
      w (int): length of window

    Returns:
      a: (numpy array): a reshaped numpy array

    """

    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
