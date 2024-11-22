import yfinance as yf
import streamlit as st


def fetch_stock_data(ticker, group_by):
    data = fetch_raw_stock_data(ticker)
    return preprocess_data(data, group_by=group_by)


@st.cache_data
def fetch_raw_stock_data(ticker, start="2023-11-24", end="2024-11-24"):
    data = yf.download(ticker, start=start, end=end)
    return data


def preprocess_data(data, group_by="day"):
    data = data.copy()
    data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]  # Flatten MultiIndex
    data["Timestamp"] = data.index  # Make the index accessible as a column

    # Dynamically find and rename the column containing "Close"
    for col in data.columns:
        if "Close" in col:  # Adjust the keyword if needed
            data.rename(columns={col: "Close"}, inplace=True)
            break

    if group_by == "month":
        # todo fix start_time
        data["Period"] = data["Timestamp"].to_period("M").dt.start_time
    elif group_by == "week":
        # todo fix start_time
        data["Period"] = data["Timestamp"].to_period("W").dt.start_time
    else:
        data["Period"] = data["Timestamp"].dt.date

    data = data.groupby("Period").agg({"Close": "mean"}).reset_index()
    return data


if __name__ == "__main__":
    data = fetch_raw_stock_data("^GSPC")
    preprocess_data(data, group_by="week")