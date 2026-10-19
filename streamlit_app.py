import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EduPro Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 EduPro Course Demand & Revenue Dashboard")

st.write(
    "An interactive dashboard to analyze course demand, "
    "enrollment patterns, and revenue."
)

# Load course analysis data
@st.cache_data
def load_data():
    course_data = pd.read_csv("course_analysis.csv")

    try:
        category_data = pd.read_csv("category_revenue.csv")
    except FileNotFoundError:
        category_data = pd.DataFrame()

    return course_data, category_data


try:
    course_data, category_data = load_data()

    st.success("Project data loaded successfully!")

    st.header("📌 Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Courses", len(course_data))

    if "Enrollment_Count" in course_data.columns:
        col2.metric(
            "Total Enrollments",
            f"{course_data['Enrollment_Count'].sum():,.0f}"
        )
    else:
        col2.metric("Total Enrollments", "Not available")

    if "Course_Revenue" in course_data.columns:
        col3.metric(
            "Total Revenue",
            f"{course_data['Course_Revenue'].sum():,.2f}"
        )
    else:
        col3.metric("Total Revenue", "Not available")

    st.divider()

    st.header("📚 Course Analysis")

    if "CourseCategory" in course_data.columns:
        st.subheader("Courses by Category")
        category_counts = course_data["CourseCategory"].value_counts()
        st.bar_chart(category_counts)

    if (
        "CourseID" in course_data.columns
        and "Enrollment_Count" in course_data.columns
    ):
        st.subheader("Top 10 Courses by Demand")

        top_demand = course_data.nlargest(10, "Enrollment_Count")

        st.bar_chart(
            top_demand.set_index("CourseID")["Enrollment_Count"]
        )

    if (
        "CourseID" in course_data.columns
        and "Course_Revenue" in course_data.columns
    ):
        st.subheader("Top 10 Courses by Revenue")

        top_revenue = course_data.nlargest(10, "Course_Revenue")

        st.bar_chart(
            top_revenue.set_index("CourseID")["Course_Revenue"]
        )

    if (
        "CoursePrice" in course_data.columns
        and "CourseRating" in course_data.columns
    ):
        st.subheader("Course Price and Rating")

        st.scatter_chart(
            course_data,
            x="CoursePrice",
            y="CourseRating"
        )

    if not category_data.empty:
        st.header("💰 Category Revenue Analysis")
        st.dataframe(category_data, use_container_width=True)

        numeric_columns = category_data.select_dtypes(
            include="number"
        ).columns.tolist()

        category_column = next(
            (
                col for col in category_data.columns
                if "category" in col.lower()
            ),
            None
        )

        revenue_column = next(
            (
                col for col in numeric_columns
                if "revenue" in col.lower()
                or "amount" in col.lower()
            ),
            None
        )

        if category_column and revenue_column:
            category_chart = category_data.set_index(category_column)
            st.bar_chart(category_chart[revenue_column])

    st.header("📄 Course Analysis Data")
    st.dataframe(course_data, use_container_width=True)

    st.download_button(
        "Download Course Analysis CSV",
        data=course_data.to_csv(index=False).encode("utf-8"),
        file_name="course_analysis.csv",
        mime="text/csv"
    )

except FileNotFoundError as error:
    st.error(
        f"Required file not found: {error}. "
        "Please check that the CSV files are uploaded "
        "to the GitHub repository."
    )

except Exception as error:
    st.error(f"Something went wrong: {error}")
