
import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* ==============================
           MAIN APPLICATION
           ============================== */

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(
                135deg,
                #F8FAFC 0%,
                #EFF6FF 100%
            );
        }


        /* ==============================
           GREEN SIDEBAR
           ============================== */

        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #0F766E 0%,
                #115E59 55%,
                #134E4A 100%
            );
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.25);
        }


        /* ==============================
           HEADINGS
           ============================== */

        h1 {
            font-weight: 750;
        }

        h2,
        h3 {
            font-weight: 650;
        }


        /* ==============================
           METRICS
           ============================== */

        [data-testid="stMetric"] {
            border-radius: 14px;
            padding: 16px;
        }


        /* ==============================
           BUTTONS
           ============================== */

        .stButton > button {
            border-radius: 9px;
            font-weight: 600;
        }


        /* ==============================
           FILE UPLOADER
           ============================== */

        [data-testid="stFileUploader"] {
            border-radius: 12px;
        }


        /* ==============================
           EXPANDERS
           ============================== */

        [data-testid="stExpander"] {
            border-radius: 12px;
        }


        /* ==============================
           CONTAINERS
           ============================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px;
        }


        /* ==============================
           ALERTS
           ============================== */

        [data-testid="stAlert"] {
            border-radius: 10px;
        }


        /* ==============================
           DIVIDERS
           ============================== */

        hr {
            opacity: 0.5;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

