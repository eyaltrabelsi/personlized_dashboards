import os

import streamlit as st


from data_processing import fetch_stock_data
from dashboards import get_dashboard, get_dashboard_brief
# Initialize view counts in session state
if "view_counts" not in st.session_state:
    st.session_state.view_counts = {
        "S&P 500": 0,
        "Nasdaq 100": 0,
        "Bitcoin": 0,
    }

def push_based_dashboards():
    st.title("Dashboards (Push based)")

    selected_dashboard = "Bitcoin"  # Default selection
    group_by = "day"  # Default grouping
    tickers = {"S&P 500": "^GSPC", "Nasdaq 100": "^IXIC", "Bitcoin": "BTC-USD"}
    ticker = tickers[selected_dashboard]

    # Increment view count in session state
    st.session_state.view_counts[selected_dashboard] += 1

    data = fetch_stock_data(ticker, group_by)

    if not data.empty:

        image_data, fig = get_dashboard(data, selected_dashboard, group_by)

        if st.button(f"Get audio dashboard brief on {selected_dashboard}"):

            message, audio = get_dashboard_brief(image_data)

            st.audio(audio)

            with st.expander("Click to see the message and plot"):
                st.write(message)
                st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Failed to retrieve or render data. Please try again later.")


def pull_based_dashboards():
    st.title("Dashboards (Pull based)")

    col1, col2 = st.columns([1, 4])  # Adjust proportions as needed
    with col1:
        for _ in range(7):
            st.text("")
        selected_dashboard = st.radio("Select Dashboard", ["S&P 500", "Nasdaq 100", "Bitcoin"],)
        group_by = st.radio("Group Data By", ["day", "week", "month"], index=0)
    tickers = {"S&P 500": "^GSPC", "Nasdaq 100": "^IXIC", "Bitcoin": "BTC-USD"}

    ticker = tickers[selected_dashboard]

    # Increment view count in session state
    st.session_state.view_counts[selected_dashboard] += 1

    data = fetch_stock_data(ticker, group_by)

    with col2:
        if not data.empty:
            image_data, fig = get_dashboard(data, selected_dashboard, group_by)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Failed to retrieve or render data. Please try again later.")


def recommendation_based_dashboards():
    st.title("Dashboards (Recommendation based)")
    selected_dashboard = max(st.session_state.view_counts, key=st.session_state.view_counts.get)
    group_by = "day"  # Default grouping
    tickers = {"S&P 500": "^GSPC", "Nasdaq 100": "^IXIC", "Bitcoin": "BTC-USD"}
    ticker = tickers[selected_dashboard]
    # Increment view count for the selected dashboard
    st.session_state.view_counts[selected_dashboard] += 1

    data = fetch_stock_data(ticker, group_by)

    if not data.empty:

        image_data, fig = get_dashboard(data, selected_dashboard, group_by)

        with st.expander(f"Dashboard for {selected_dashboard}"):
            st.plotly_chart(fig, use_container_width=True)
            st.table(st.session_state.view_counts)


    else:
        st.error("Failed to retrieve or render data. Please try again later.")


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboards (Pull based)", "Dashboards (Push based)", "Dashboards (Personalized)", "Quality control"]
    )
    if page == "Dashboards (Pull based)":
        pull_based_dashboards()
    elif page == "Dashboards (Push based)":
        push_based_dashboards()
    elif page == "Dashboards (Personalized)":
        recommendation_based_dashboards()
    elif page == "Quality control":
        ...


if __name__ == "__main__":
    main()
