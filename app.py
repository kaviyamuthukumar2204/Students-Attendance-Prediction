import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Absenteeism Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Absenteeism Analysis & Prediction")

st.write(
    "Analyze August attendance and view predicted absence risk "
    "for upcoming class dates."
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

HISTORY_FILE = BASE_DIR / "absenteeism_august_2026.csv"
PREDICTION_FILE = BASE_DIR / "all_future_absence_predictions.csv"


# ============================================================
# LOAD HISTORY DATA
# ============================================================

@st.cache_data
def load_history():

    data = pd.read_csv(HISTORY_FILE)

    data["DATE"] = pd.to_datetime(
        data["DATE"],
        dayfirst=True,
        errors="coerce"
    )

    return data


# ============================================================
# LOAD PREDICTION DATA
# ============================================================

@st.cache_data
def load_predictions():

    data = pd.read_csv(PREDICTION_FILE)

    data["DATE"] = pd.to_datetime(
        data["DATE"],
        errors="coerce"
    )

    return data


# ============================================================
# LOAD FILES
# ============================================================

try:

    history = load_history()
    predictions = load_predictions()

except FileNotFoundError as e:

    st.error(
        f"File not found: {e.filename}"
    )

    st.stop()


# ============================================================
# CLEAN PROBABILITY
# ============================================================

def clean_probability(value):

    if pd.isna(value):
        return None

    try:

        value = float(
            str(value)
            .replace("%", "")
            .strip()
        )

    except:

        return None

    if value <= 1:
        value = value * 100

    return value


# ============================================================
# FIND PROBABILITY COLUMN
# ============================================================

possible_probability_columns = [
    "ABSENCE PROBABILITY",
    "Absence Probability",
    "ABSENCE_PROBABILITY",
    "PROBABILITY",
    "Probability",
    "probability"
]

probability_column = None


for col in possible_probability_columns:

    if col in predictions.columns:

        probability_column = col
        break


if probability_column is None:

    for col in predictions.columns:

        if "prob" in col.lower():

            probability_column = col
            break


if probability_column is None:

    st.error(
        "Absence probability column was not found."
    )

    st.write(
        "Available columns:"
    )

    st.write(
        list(predictions.columns)
    )

    st.stop()


# ============================================================
# CREATE PROBABILITY COLUMN
# ============================================================

predictions["ABSENCE PROBABILITY"] = (
    predictions[probability_column]
    .apply(clean_probability)
)


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(probability):

    if pd.isna(probability):

        return "Unknown"

    if probability >= 60:

        return "High"

    elif probability >= 30:

        return "Medium"

    else:

        return "Low"


predictions["RISK LEVEL"] = (
    predictions["ABSENCE PROBABILITY"]
    .apply(get_risk_level)
)


# ============================================================
# FUTURE CLASS DATES
# ============================================================

FUTURE_CLASS_DATES = [

    # September 2026

    date(2026, 9, 1),
    date(2026, 9, 2),
    date(2026, 9, 3),

    date(2026, 9, 7),
    date(2026, 9, 8),
    date(2026, 9, 9),
    date(2026, 9, 10),
    date(2026, 9, 11),
    date(2026, 9, 12),

    date(2026, 9, 15),
    date(2026, 9, 16),
    date(2026, 9, 17),
    date(2026, 9, 18),

    date(2026, 9, 21),
    date(2026, 9, 22),
    date(2026, 9, 23),
    date(2026, 9, 24),
    date(2026, 9, 25),

    date(2026, 9, 28),
    date(2026, 9, 29),
    date(2026, 9, 30),


    # October 2026

    date(2026, 10, 1),

    date(2026, 10, 5),
    date(2026, 10, 6),
    date(2026, 10, 7),
    date(2026, 10, 8),
    date(2026, 10, 9),
    date(2026, 10, 10),

    date(2026, 10, 12),
    date(2026, 10, 13),
    date(2026, 10, 14),
    date(2026, 10, 15),
    date(2026, 10, 16),

    date(2026, 10, 21),
    date(2026, 10, 22),
    date(2026, 10, 23),
    date(2026, 10, 24),

    date(2026, 10, 26),
    date(2026, 10, 27),
    date(2026, 10, 28),
    date(2026, 10, 29),
    date(2026, 10, 30),
    date(2026, 10, 31),


    # November 2026

    date(2026, 11, 2),
    date(2026, 11, 3),
    date(2026, 11, 4)
]


# ============================================================
# JULY CLASS DATES
# ============================================================
# Based on the uploaded AAMEC academic calendar.
# July 1 is the commencement of odd-semester classes.
# Sundays are excluded.
# ============================================================

JULY_CLASS_DATES = [

    date(2026, 7, 1),
    date(2026, 7, 2),
    date(2026, 7, 3),
    date(2026, 7, 4),

    date(2026, 7, 6),
    date(2026, 7, 7),
    date(2026, 7, 8),
    date(2026, 7, 9),
    date(2026, 7, 10),
    date(2026, 7, 11),

    date(2026, 7, 13),
    date(2026, 7, 14),
    date(2026, 7, 15),
    date(2026, 7, 16),
    date(2026, 7, 17),
    date(2026, 7, 18),

    date(2026, 7, 20),
    date(2026, 7, 21),
    date(2026, 7, 22),
    date(2026, 7, 23),
    date(2026, 7, 24),
    date(2026, 7, 25),

    date(2026, 7, 27),
    date(2026, 7, 28),
    date(2026, 7, 29),
    date(2026, 7, 30),
    date(2026, 7, 31)
]


# ============================================================
# ROLL NUMBERS
# ============================================================

roll_numbers = sorted(
    history["ROLL NO"]
    .dropna()
    .astype(int)
    .unique()
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🎓 Student Selection")

selected_roll = st.sidebar.selectbox(
    "Select Roll Number",
    roll_numbers
)


# ============================================================
# SELECTED STUDENT HISTORY
# ============================================================

student_history = history[
    history["ROLL NO"].astype(int) == selected_roll
].copy()


# ============================================================
# SELECTED STUDENT PREDICTIONS
# ============================================================

student_predictions = predictions[
    predictions["ROLL NO"].astype(int) == selected_roll
].copy()


# ============================================================
# AUGUST ATTENDANCE
# ============================================================

total_august_classes = len(
    student_history["DATE"].drop_duplicates()
)


august_absences = int(
    student_history["ATTENDANCE"].sum()
)


august_present = (
    total_august_classes
    - august_absences
)


if total_august_classes > 0:

    august_attendance_percentage = (
        august_present
        / total_august_classes
    ) * 100

else:

    august_attendance_percentage = 0


# ============================================================
# ATTENDANCE SUMMARY
# ============================================================

st.subheader("📌 Attendance Summary")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "August Classes",
        total_august_classes
    )


with col2:

    st.metric(
        "August Present",
        august_present
    )


with col3:

    st.metric(
        "August Absences",
        august_absences
    )


with col4:

    st.metric(
        "August Attendance",
        f"{august_attendance_percentage:.2f}%"
    )


# ============================================================
# AUGUST ATTENDANCE PIE CHART
# ============================================================

st.subheader("📈 August Attendance History")


pie_data = pd.DataFrame({

    "Status": [
        "Present",
        "Absent"
    ],

    "Count": [
        august_present,
        august_absences
    ]

})


fig = px.pie(

    pie_data,

    names="Status",

    values="Count",

    hole=0.45,

    title=f"Roll No. {selected_roll} - August Attendance"

)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# FUTURE ABSENCE PREDICTIONS
# ============================================================

st.subheader("🔮 Future Absence Predictions")


# ============================================================
# RISK ORDER
# ============================================================

risk_order = {

    "High": 0,

    "Medium": 1,

    "Low": 2,

    "Unknown": 3

}


student_predictions["RISK ORDER"] = (
    student_predictions["RISK LEVEL"]
    .map(risk_order)
)


# ============================================================
# SORT:
# HIGH → MEDIUM → LOW
# THEN HIGHEST PROBABILITY FIRST
# ============================================================

student_predictions = (
    student_predictions
    .sort_values(
        by=[
            "RISK ORDER",
            "ABSENCE PROBABILITY",
            "DATE"
        ],
        ascending=[
            True,
            False,
            True
        ]
    )
)


# ============================================================
# DISPLAY PREDICTION TABLE
# ============================================================

display_predictions = student_predictions[
    [
        "DATE",
        "ABSENCE PROBABILITY",
        "RISK LEVEL"
    ]
].copy()


display_predictions["DATE"] = (
    display_predictions["DATE"]
    .dt.strftime("%d-%m-%Y")
)


display_predictions["ABSENCE PROBABILITY"] = (
    display_predictions["ABSENCE PROBABILITY"]
    .apply(
        lambda x:
        f"{x:.2f}%"
        if pd.notna(x)
        else "N/A"
    )
)


display_predictions = (
    display_predictions
    .rename(
        columns={
            "DATE": "Date",
            "ABSENCE PROBABILITY":
                "Absence Probability",
            "RISK LEVEL":
                "Risk Level"
        }
    )
)


st.dataframe(
    display_predictions,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# RISK SUMMARY
# ============================================================

st.subheader("📊 Risk Summary")


high_count = (
    student_predictions["RISK LEVEL"]
    .eq("High")
    .sum()
)


medium_count = (
    student_predictions["RISK LEVEL"]
    .eq("Medium")
    .sum()
)


low_count = (
    student_predictions["RISK LEVEL"]
    .eq("Low")
    .sum()
)


risk_col1, risk_col2, risk_col3 = st.columns(3)


with risk_col1:

    st.error(
        f"🔴 High Risk: {high_count}"
    )


with risk_col2:

    st.warning(
        f"🟠 Medium Risk: {medium_count}"
    )


with risk_col3:

    st.success(
        f"🟢 Low Risk: {low_count}"
    )


# ============================================================
# PLANNED ABSENCE SECTION
# ============================================================

st.subheader("📅 Plan Your Absences")


st.write(
    "Select one or more class dates on which "
    "you expect to be absent."
)


st.info(
    "Click a class date to select it. "
    "Click the same date again to remove it."
)


# ============================================================
# SESSION STATE
# ============================================================

if "planned_absences" not in st.session_state:

    st.session_state.planned_absences = []


st.session_state.planned_absences = [

    d
    if isinstance(d, date)
    else pd.to_datetime(d).date()

    for d in st.session_state.planned_absences

]


# ============================================================
# CALENDAR FUNCTION
# ============================================================

def calendar_month(
    year,
    month,
    allowed_dates,
    title
):

    st.markdown(
        f"### {title}"
    )


    first_day = date(
        year,
        month,
        1
    )


    if month == 12:

        next_month = date(
            year + 1,
            1,
            1
        )

    else:

        next_month = date(
            year,
            month + 1,
            1
        )


    days_in_month = (
        next_month
        - first_day
    ).days


    first_weekday = (
        first_day.weekday()
    )


    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]


    # ========================================================
    # WEEKDAY HEADER
    # ========================================================

    header_cols = st.columns(7)


    for i, day_name in enumerate(
        weekdays
    ):

        header_cols[i].markdown(
            f"**{day_name}**"
        )


    # ========================================================
    # CALENDAR GRID
    # ========================================================

    current_day = 1


    while current_day <= days_in_month:

        cols = st.columns(7)


        for weekday_index in range(7):

            # Empty cells before first day

            if (
                current_day == 1
                and weekday_index < first_weekday
            ):

                cols[
                    weekday_index
                ].write("")

                continue


            # Empty cells after month ends

            if current_day > days_in_month:

                cols[
                    weekday_index
                ].write("")

                continue


            current_date = date(
                year,
                month,
                current_day
            )


            # =================================================
            # CLASS DATE
            # =================================================

            if current_date in allowed_dates:

                is_selected = (
                    current_date
                    in st.session_state.planned_absences
                )


                if is_selected:

                    button_text = (
                        f"🟥 {current_day}"
                    )

                else:

                    button_text = (
                        f"📅 {current_day}"
                    )


                if cols[
                    weekday_index
                ].button(

                    button_text,

                    key=(
                        f"calendar_"
                        f"{year}_"
                        f"{month}_"
                        f"{current_day}"
                    ),

                    use_container_width=True

                ):

                    if (
                        current_date
                        in st.session_state.planned_absences
                    ):

                        st.session_state.planned_absences.remove(
                            current_date
                        )

                    else:

                        st.session_state.planned_absences.append(
                            current_date
                        )

                    st.rerun()


            # =================================================
            # NON-CLASS DATE
            # =================================================

            else:

                cols[
                    weekday_index
                ].button(

                    f"— {current_day}",

                    key=(
                        f"disabled_"
                        f"{year}_"
                        f"{month}_"
                        f"{current_day}"
                    ),

                    disabled=True,

                    use_container_width=True

                )


            current_day += 1


# ============================================================
# JULY 2026
# ============================================================

calendar_month(

    2026,
    7,

    JULY_CLASS_DATES,

    "July 2026"

)


# ============================================================
# SEPTEMBER 2026
# ============================================================

calendar_month(

    2026,
    9,

    [
        d
        for d in FUTURE_CLASS_DATES
        if d.month == 9
    ],

    "September 2026"

)


# ============================================================
# OCTOBER 2026
# ============================================================

calendar_month(

    2026,
    10,

    [
        d
        for d in FUTURE_CLASS_DATES
        if d.month == 10
    ],

    "October 2026"

)


# ============================================================
# NOVEMBER 2026
# ============================================================

calendar_month(

    2026,
    11,

    [
        d
        for d in FUTURE_CLASS_DATES
        if d.month == 11
    ],

    "November 2026"

)


# ============================================================
# SELECTED PLANNED ABSENCES
# ============================================================

st.subheader("📝 Selected Planned Absences")


selected_dates = sorted(
    st.session_state.planned_absences
)


if len(selected_dates) == 0:

    st.success(
        "Nil - No planned absences"
    )

else:

    for selected_date in selected_dates:

        st.write(
            f"📌 {selected_date.strftime('%d-%m-%Y')}"
        )


# ============================================================
# COUNT JULY PLANNED ABSENCES
# ============================================================

july_planned_absences = sum(

    1

    for d in selected_dates

    if (
        d.year == 2026
        and d.month == 7
    )

)


# ============================================================
# COUNT FUTURE PLANNED ABSENCES
# ============================================================

future_planned_absences = sum(

    1

    for d in selected_dates

    if d in FUTURE_CLASS_DATES

)


# ============================================================
# JULY PROJECTION
# ============================================================

july_class_days = len(
    JULY_CLASS_DATES
)


july_present = (
    july_class_days
    - july_planned_absences
)


# ============================================================
# AUGUST ACTUAL DATA
# ============================================================

# IMPORTANT:
# The correct variable is total_august_classes.

august_present_for_projection = (
    august_present
)


# ============================================================
# FUTURE PROJECTION
# ============================================================

future_class_days = len(
    FUTURE_CLASS_DATES
)


future_present = (
    future_class_days
    - future_planned_absences
)


# ============================================================
# TOTAL PROJECTED ATTENDANCE
# ============================================================

total_class_days = (

    july_class_days

    + total_august_classes

    + future_class_days

)


total_present_days = (

    july_present

    + august_present_for_projection

    + future_present

)


if total_class_days > 0:

    projected_attendance = (

        total_present_days
        / total_class_days

    ) * 100

else:

    projected_attendance = 0


# ============================================================
# PROJECTED ATTENDANCE
# ============================================================

st.subheader("📊 Projected Attendance")


proj_col1, proj_col2, proj_col3, proj_col4 = st.columns(4)


with proj_col1:

    st.metric(
        "July Planned Absences",
        july_planned_absences
    )


with proj_col2:

    st.metric(
        "Future Planned Absences",
        future_planned_absences
    )


with proj_col3:

    st.metric(
        "Projected Present Days",
        total_present_days
    )


with proj_col4:

    st.metric(
        "Projected Attendance",
        f"{projected_attendance:.2f}%"
    )


# ============================================================
# PROJECTION DETAILS
# ============================================================

st.info(
    f"""
### Projection Calculation

**July 2026**
- Class days: {july_class_days}
- Planned absences: {july_planned_absences}
- Assumed present: {july_present}

**August 2026**
- Completed classes: {total_august_classes}
- Actual present: {august_present_for_projection}
- Actual absences: {august_absences}

**September–November 2026**
- Future class days: {future_class_days}
- Planned absences: {future_planned_absences}
- Projected present: {future_present}

**Overall**
- Total class days: {total_class_days}
- Projected present days: {total_present_days}
- Projected attendance: **{projected_attendance:.2f}%**
"""
)


# ============================================================
# RISK LEVEL GUIDE
# ============================================================

st.subheader("📌 Risk Level Guide")


guide_col1, guide_col2, guide_col3 = st.columns(3)


with guide_col1:

    st.error(
        "**High Risk**\n\n"
        "Absence probability ≥ 60%"
    )


with guide_col2:

    st.warning(
        "**Medium Risk**\n\n"
        "Absence probability 30%–59.99%"
    )


with guide_col3:

    st.success(
        "**Low Risk**\n\n"
        "Absence probability < 30%"
    )


# ============================================================
# NOTE
# ============================================================

st.caption(
    "Note: July attendance data is not available in the "
    "historical dataset. July class dates are taken from "
    "the academic calendar, while unselected July class "
    "dates are treated as present for projection purposes. "
    "Therefore, the July portion of the projection is an "
    "assumption rather than actual attendance."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Student Absenteeism Analysis & Prediction "
    "using Data Analytics and Machine Learning"
)