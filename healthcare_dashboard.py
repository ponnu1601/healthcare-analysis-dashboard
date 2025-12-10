import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Healthcare Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")


# Background and sidebar styling
st.markdown("""
    <style>
    .stApp {
        background-color: black;
    }
    [data-testid="stSidebar"] {
        background-color: black;
    }
    button {
        transition: all 0.3s ease !important;
    }
    button:hover {
        border-color: #00d4ff !important;
        background-color: #0d2a2a !important;
        color: #00d4ff !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Add CSS for radio buttons with hover effect
st.markdown("""
    <style>
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 135px !important;
        width: 100% !important;
        justify-content: space-between !important;
    }
    div[role="radiogroup"] > div {
        flex: 1 !important;
    }
    div[role="radiogroup"] label {
        font-size: 2em !important;
        padding: 25px 20px !important;
        border: 2px solid #444444 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
        display: block !important;
        text-align: center !important;
        white-space: normal !important;
        min-height: 70px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #00d4ff !important;
        background-color: #0d2a2a !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 8px rgba(0, 212, 255, 0.2) !important;
    }
    div[role="radiogroup"] input[type="radio"]:checked + label {
        border-color: #00d4ff !important;
        background-color: #0d2a2a !important;
        color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection with environment variables
@st.cache_resource
def get_db_connection():
    try:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        
        if not all([db_user, db_password, db_host, db_name]):
            st.error("Database credentials not found. Please set environment variables.")
            return None
        
        engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')
        return engine
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def execute_query(engine, query):
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

# Title
st.markdown("<h1 style='text-align: center;'>🏥 Healthcare Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interactive analysis of patient records</p>", unsafe_allow_html=True)

# Connect to database
engine = get_db_connection()

if engine is None:
    st.error("Failed to connect to database. Please check your MySQL connection settings.")
    st.stop()

# Dashboard Overview
st.markdown("""
    <div style='background-color: black; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #333333;'>
        <h3 style='color: #ffffff; font-size: 1.6em;'>📋 Dashboard Overview</h2>
        <p style='color: #ffffff; line-height: 1.8;'>
        Welcome to the Healthcare Analysis Dashboard! This interactive tool allows you to explore comprehensive healthcare data 
        and gain insights into patient demographics, medical conditions, insurance patterns, and treatment outcomes. 
        </p>
        <p style='color: #ffffff; line-height: 1.8;'>
        <strong>What you can do:</strong>
        </p>
        <ul style='color: #ffffff; line-height: 1.8;'>
            <li>View complete dataset information including columns, data types, and ranges</li>
            <li>Explore demographic analysis including age, gender, and blood type distributions</li>
            <li>Analyze medical conditions with billing costs and hospital stay duration</li>
            <li>Compare insurance provider performance and patient distribution</li>
            <li>Explore admission types and their associated metrics</li>
            <li>Review medication patterns and their impact on healthcare costs</li>
        </ul>
        <p style='color: #ffffff; line-height: 1.8;'>
        Use the analysis sections below to customize your view and explore different aspects of healthcare outcomes and expenses.
        </p>
    </div>
""", unsafe_allow_html=True)

# ===== DATASET OVERVIEW SECTION =====
st.markdown("<h3 style='color: #ffffff; margin-bottom: 30px;'>🔎 Dataset Overview</h2>", unsafe_allow_html=True)

# Header stats - COMPLETE DATASET
col1, col2, col3, col4 = st.columns(4)

total_records = execute_query(engine, "SELECT COUNT(*) as count FROM patients")
date_range = execute_query(engine, "SELECT MIN(date_of_admission) as min_date, MAX(date_of_admission) as max_date FROM patients")

if total_records is not None:
    col1.markdown("<div style='text-align: center;'><div style='font-size: 2.0em; color: #00d4ff;'>" + f"{total_records['count'][0]:,}" + "</div><div style='color: #888888; font-size: 0.9em;'>📈 Total Records</div></div>", unsafe_allow_html=True)

if date_range is not None:
    min_date = date_range['min_date'][0]
    max_date = date_range['max_date'][0]
    date_diff = (max_date - min_date).days / 365
    col2.markdown("<div style='text-align: center;'><div style='font-size: 2.0em; color: #00d4ff;'>" + f"{int(date_diff)} Years" + "</div><div style='color: #888888; font-size: 0.9em;'>📅 Date Range</div></div>", unsafe_allow_html=True)

col3.markdown("<div style='text-align: center;'><div style='font-size: 2.0em; color: #00d4ff;'>15</div><div style='color: #888888; font-size: 0.9em;'>📋 Total Columns</div></div>", unsafe_allow_html=True)
col4.markdown("<div style='text-align: center;'><div style='font-size: 2.0em; color: #00d4ff;'>100%</div><div style='color: #888888; font-size: 0.9em;'>✅ Data Quality</div></div>", unsafe_allow_html=True)

# Dataset columns section
st.markdown("<h3 style='color: #ffffff; margin-top: 40px; margin-bottom: 20px;'>📋 Dataset Columns</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #888888; margin-bottom: 20px;'>Click on any column to see its details</p>", unsafe_allow_html=True)

# Column buttons in grid
columns_info = [
    ("patient_id", "👤 Patient ID"),
    ("name", "📝 Name"),
    ("age", "🎂 Age"),
    ("gender", "👫 Gender"),
    ("blood_type", "🩸 Blood Type"),
    ("medical_condition", "🏥 Medical Condition"),
    ("date_admission", "📅 Admission Date"),
    ("doctor", "👨‍⚕️ Doctor"),
    ("hospital", "🏨 Hospital"),
    ("insurance", "💳 Insurance"),
    ("billing", "💰 Billing"),
    ("room", "🚪 Room Number"),
    ("admission_type", "📋 Admission Type"),
    ("discharge_date", "🚪 Discharge Date"),
    ("medication", "💊 Medication"),
    ("test_results", "🔬 Test Results"),
]

# Initialize session state for selected column
if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None

# Create columns for buttons
cols = st.columns(4)
for idx, (col_key, col_label) in enumerate(columns_info):
    with cols[idx % 4]:
        if st.button(col_label, key=col_key, width='stretch'):
            if st.session_state.selected_column == col_key:
                st.session_state.selected_column = None
            else:
                st.session_state.selected_column = col_key

st.divider()

# Display details for selected column only if clicked
selected = st.session_state.selected_column

if selected == 'patient_id':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>👤 Patient ID</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Integer (Auto-increment)")
    st.markdown("**Range:** 1 - 55,392")
    st.markdown("**Description:** Unique identifier for each patient. Automatically assigned sequential number for each patient record.")

elif selected == 'name':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>📝 Name</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (String)")
    st.markdown("**Null Values:** 0")
    st.markdown("**Description:** Full name of the patient. Synthetic names generated for privacy.")

elif selected == 'age':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🎂 Age</div>", unsafe_allow_html=True)
    age_stats = execute_query(engine, "SELECT MIN(age) as min_age, MAX(age) as max_age, AVG(age) as avg_age FROM patients")
    if age_stats is not None:
        st.markdown("**Data Type:** Integer")
        st.markdown(f"**Range:** {int(age_stats['min_age'][0])} - {int(age_stats['max_age'][0])} years")
        st.markdown(f"**Average:** {age_stats['avg_age'][0]:.1f} years")
    st.markdown("**Description:** Patient's age at time of admission.")

elif selected == 'gender':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>👫 Gender</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    st.markdown("**Values:** Male, Female")
    gender_dist = execute_query(engine, "SELECT gender, COUNT(*) as count FROM patients GROUP BY gender")
    if gender_dist is not None:
        for idx, row in gender_dist.iterrows():
            total = total_records['count'][0] if total_records is not None else 1
            pct = (row['count'] / total * 100)
            st.markdown(f"**{row['gender']}:** {row['count']:,} ({pct:.1f}%)")
    st.markdown("**Description:** Patient's gender classification.")

elif selected == 'blood_type':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🩸 Blood Type</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    blood_types = execute_query(engine, "SELECT DISTINCT blood_type FROM patients ORDER BY blood_type")
    if blood_types is not None:
        st.markdown(f"**Unique Values:** {len(blood_types)}")
        st.markdown(f"**Types:** {', '.join(blood_types['blood_type'].tolist())}")
    st.markdown("**Description:** Patient's blood type classification. Fairly evenly distributed across all types.")

elif selected == 'medical_condition':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🏥 Medical Condition</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    conditions_unique = execute_query(engine, "SELECT DISTINCT medical_condition FROM patients ORDER BY medical_condition")
    if conditions_unique is not None:
        st.markdown(f"**Unique Conditions:** {len(conditions_unique)}")
        st.markdown(f"**Types:** {', '.join(conditions_unique['medical_condition'].tolist())}")
    st.markdown("**Description:** Primary medical condition/diagnosis of patient.")

elif selected == 'date_admission':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>📅 Date of Admission</div>", unsafe_allow_html=True)
    date_info = execute_query(engine, "SELECT MIN(date_of_admission) as min_date, MAX(date_of_admission) as max_date FROM patients")
    if date_info is not None:
        st.markdown("**Data Type:** Date (YYYY-MM-DD)")
        st.markdown(f"**Range:** {date_info['min_date'][0]} to {date_info['max_date'][0]}")
    st.markdown("**Description:** Date patient was admitted to hospital.")

elif selected == 'doctor':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>👨‍⚕️ Doctor</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (String)")
    doctor_count = execute_query(engine, "SELECT COUNT(DISTINCT doctor) as count FROM patients")
    if doctor_count is not None:
        st.markdown(f"**Unique Doctors:** {doctor_count['count'][0]:,}")
    st.markdown("**Description:** Name of doctor responsible for patient care.")

elif selected == 'hospital':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🏨 Hospital</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (String)")
    hospital_count = execute_query(engine, "SELECT COUNT(DISTINCT hospital) as count FROM patients")
    if hospital_count is not None:
        st.markdown(f"**Unique Hospitals:** {hospital_count['count'][0]:,}")
    st.markdown("**Description:** Healthcare facility where patient was admitted.")

elif selected == 'insurance':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>💳 Insurance Provider</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    insurances_unique = execute_query(engine, "SELECT DISTINCT insurance_provider FROM patients ORDER BY insurance_provider")
    if insurances_unique is not None:
        st.markdown(f"**Providers:** {', '.join(insurances_unique['insurance_provider'].tolist())}")
    st.markdown("**Description:** Patient's insurance provider.")

elif selected == 'billing':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>💰 Billing Amount</div>", unsafe_allow_html=True)
    billing_stats = execute_query(engine, "SELECT MIN(billing_amount) as min_bill, MAX(billing_amount) as max_bill, AVG(billing_amount) as avg_bill FROM patients")
    if billing_stats is not None:
        st.markdown("**Data Type:** Decimal (Currency)")
        st.markdown(f"**Range:** ${billing_stats['min_bill'][0]:,.2f} - ${billing_stats['max_bill'][0]:,.2f}")
        st.markdown(f"**Average:** ${billing_stats['avg_bill'][0]:,.2f}")
    st.markdown("**Description:** Total billing amount for healthcare services.")

elif selected == 'room':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🚪 Room Number</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Integer")
    room_info = execute_query(engine, "SELECT MIN(room_number) as min_room, MAX(room_number) as max_room FROM patients")
    if room_info is not None:
        st.markdown(f"**Range:** {int(room_info['min_room'][0])} - {int(room_info['max_room'][0])}")
    st.markdown("**Description:** Hospital room number where patient was accommodated.")

elif selected == 'admission_type':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>📋 Admission Type</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    adm_types_unique = execute_query(engine, "SELECT DISTINCT admission_type FROM patients ORDER BY admission_type")
    if adm_types_unique is not None:
        st.markdown(f"**Types:** {', '.join(adm_types_unique['admission_type'].tolist())}")
    st.markdown("**Description:** Circumstances of hospital admission (Emergency, Elective, Urgent).")

elif selected == 'discharge_date':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🚪 Discharge Date</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Date (YYYY-MM-DD)")
    discharge_info = execute_query(engine, "SELECT MIN(discharge_date) as min_date, MAX(discharge_date) as max_date FROM patients")
    if discharge_info is not None:
        st.markdown(f"**Range:** {discharge_info['min_date'][0]} to {discharge_info['max_date'][0]}")
    st.markdown("**Description:** Date patient was discharged from hospital. Used to calculate length of stay.")

elif selected == 'medication':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>💊 Medication</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    meds_unique = execute_query(engine, "SELECT DISTINCT medication FROM patients ORDER BY medication")
    if meds_unique is not None:
        st.markdown(f"**Medications:** {', '.join(meds_unique['medication'].tolist())}")
    st.markdown("**Description:** Medication prescribed/administered to patient.")

elif selected == 'test_results':
    st.markdown("<div style='color: #00d4ff; font-size: 1.4em; margin-bottom: 20px;'>🔬 Test Results</div>", unsafe_allow_html=True)
    st.markdown("**Data Type:** Text (Categorical)")
    st.markdown("**Values:** Normal, Abnormal, Inconclusive")
    st.markdown("**Description:** Results of medical tests conducted during admission.")

# ===== TABS FOR ANALYSIS SECTIONS =====
st.markdown("<h3 style='color: #ffffff; margin-top: 50px; margin-bottom: 20px;'>📊 Analysis Sections</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #888888; margin-bottom: 20px;'>Click on any analysis section below to explore detailed insights</p>", unsafe_allow_html=True)

# Analysis tabs as radio buttons
analysis_tabs = ["👥 Demographics", "🏥 Medical Conditions", "💳 Insurance", "📋 Admission Type", "💊 Medication"]

if 'selected_analysis' not in st.session_state:
    st.session_state.selected_analysis = None

# Create radio button with horizontal layout
selected_tab = st.radio(
    "Select Analysis",
    options=range(len(analysis_tabs)),
    format_func=lambda x: analysis_tabs[x],
    horizontal=True,
    label_visibility="collapsed"
)

# Update session state
st.session_state.selected_analysis = selected_tab

st.divider()

# Get selected analysis
selected_analysis = st.session_state.selected_analysis

# ===== DEMOGRAPHICS ANALYSIS =====
if selected_analysis == 0:
        # Create two columns: left for content, right for filters
        content_col, filter_col = st.columns([3, 1])
        
        with filter_col:
            st.markdown("<h3 style='color: #00d4ff; font-size: 1.1em;'>🔍 Filters</h3>", unsafe_allow_html=True)
            demo_condition = st.selectbox("Medical Condition", ['All Conditions', 'Cancer', 'Diabetes', 'Obesity', 'Asthma', 'Hypertension', 'Arthritis'], key="demo_condition")
            demo_insurance = st.selectbox("Insurance Provider", ['All Providers', 'Medicare', 'Blue Cross', 'Cigna', 'Aetna', 'UnitedHealthcare'], key="demo_insurance")
            demo_admission = st.selectbox("Admission Type", ['All Types', 'Emergency', 'Elective', 'Urgent'], key="demo_admission")
        
        with content_col:
            # Build where clause for Demographics filters
            demo_where = "WHERE 1=1"
            if demo_condition != 'All Conditions':
                demo_where += f" AND medical_condition = '{demo_condition}'"
            if demo_insurance != 'All Providers':
                demo_where += f" AND insurance_provider = '{demo_insurance}'"
            if demo_admission != 'All Types':
                demo_where += f" AND admission_type = '{demo_admission}'"
            
            # Age Statistics
            st.markdown("<h3 style='color: #00d4ff;'>Age Statistics</h3>", unsafe_allow_html=True)
            demo_age_stats = execute_query(engine, f"SELECT MIN(age) as min_age, MAX(age) as max_age, AVG(age) as avg_age FROM patients {demo_where if demo_where else ''}")
            if demo_age_stats is not None:
                age_table_data = {
                    'Metric': ['Min Age', 'Max Age', 'Avg Age'],
                    'Value': [str(int(demo_age_stats['min_age'][0])), str(int(demo_age_stats['max_age'][0])), str(round(demo_age_stats['avg_age'][0], 1))]
                }
                st.dataframe(pd.DataFrame(age_table_data), width='stretch')
            
            # Gender Distribution
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Gender Distribution</h3>", unsafe_allow_html=True)
            demo_gender = execute_query(engine, f"SELECT gender, COUNT(*) as count FROM patients {demo_where if demo_where else ''} GROUP BY gender")
            if demo_gender is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(demo_gender, width='stretch')
                with col2:
                    fig = px.pie(demo_gender, names='gender', values='count', title="Gender Distribution")
                    st.plotly_chart(fig, width='stretch')
            
            # Blood Type Distribution
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Blood Type Distribution</h3>", unsafe_allow_html=True)
            demo_blood = execute_query(engine, f"SELECT blood_type, COUNT(*) as count FROM patients {demo_where if demo_where else ''} GROUP BY blood_type ORDER BY count DESC")
            if demo_blood is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(demo_blood, width='stretch')
                with col2:
                    fig = px.bar(demo_blood, x='blood_type', y='count', title="Blood Type Distribution")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Billing by Gender
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Billing by Gender</h3>", unsafe_allow_html=True)
            demo_billing = execute_query(engine, f"SELECT gender, ROUND(AVG(billing_amount), 2) as avg_billing FROM patients {demo_where if demo_where else ''} GROUP BY gender")
            if demo_billing is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(demo_billing, width='stretch')
                with col2:
                    fig = px.bar(demo_billing, x='gender', y='avg_billing', title="Avg Billing by Gender", labels={'avg_billing': 'Avg Billing ($)'})
                    st.plotly_chart(fig, width='stretch')

# ===== MEDICAL CONDITIONS ANALYSIS =====
if selected_analysis == 1:
        # Create two columns: left for content, right for filters
        content_col, filter_col = st.columns([3, 1])
        
        with filter_col:
            st.markdown("<h3 style='color: #00d4ff; font-size: 1.1em;'>🔍 Filters</h3>", unsafe_allow_html=True)
            med_insurance = st.selectbox("Insurance Provider", ['All Providers', 'Medicare', 'Blue Cross', 'Cigna', 'Aetna', 'UnitedHealthcare'], key="med_insurance")
            med_gender = st.selectbox("Gender", ['All', 'Male', 'Female'], key="med_gender")
            med_age_range = st.slider("Age Range", min_value=13, max_value=89, value=(13, 89), key="med_age")
            med_admission = st.selectbox("Admission Type", ['All Types', 'Emergency', 'Elective', 'Urgent'], key="med_admission")
        
        with content_col:
            # Build where clause for Medical Conditions filters
            med_where = "WHERE 1=1"
            if med_insurance != 'All Providers':
                med_where += f" AND insurance_provider = '{med_insurance}'"
            if med_gender != 'All':
                med_where += f" AND gender = '{med_gender}'"
            if med_admission != 'All Types':
                med_where += f" AND admission_type = '{med_admission}'"
            med_where += f" AND age >= {med_age_range[0]} AND age <= {med_age_range[1]}"

            # Average Billing by Medical Condition
            st.markdown("<h3 style='color: #00d4ff;'>Average Billing by Medical Condition</h3>", unsafe_allow_html=True)
            med_billing = execute_query(engine, f"SELECT medical_condition, ROUND(AVG(billing_amount), 2) as avg_billing, COUNT(*) as patient_count FROM patients {med_where} GROUP BY medical_condition ORDER BY avg_billing DESC")
            if med_billing is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(med_billing, width='stretch')
                with col2:
                    fig = px.bar(med_billing, x='medical_condition', y='avg_billing', title="Avg Billing by Condition")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Length of Stay by Medical Condition
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Length of Stay by Medical Condition</h3>", unsafe_allow_html=True)
            med_los = execute_query(engine, f"SELECT medical_condition, ROUND(AVG(DATEDIFF(discharge_date, date_of_admission))) as avg_stay, COUNT(*) as patient_count FROM patients {med_where} GROUP BY medical_condition ORDER BY avg_stay DESC")
            if med_los is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(med_los, width='stretch')
                with col2:
                    fig = px.bar(med_los, x='medical_condition', y='avg_stay', title="Avg Length of Stay by Condition")
                    st.plotly_chart(fig, width='stretch')
            
            # Test Results Distribution by Medical Condition
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Test Results Distribution by Medical Condition</h3>", unsafe_allow_html=True)
            med_test = execute_query(engine, f"SELECT medical_condition, test_results, COUNT(*) as count FROM patients {med_where} GROUP BY medical_condition, test_results ORDER BY medical_condition, test_results")
            if med_test is not None:
                st.dataframe(med_test, width='stretch')
                
                # Pivot for chart
                med_test_pivot = med_test.pivot(index='medical_condition', columns='test_results', values='count').fillna(0)
                fig = px.bar(med_test_pivot, barmode='group', title="Test Results by Medical Condition")
                st.plotly_chart(fig, width='stretch')

# ===== INSURANCE PROVIDER ANALYSIS =====
if selected_analysis == 2:
        # Create two columns: left for content, right for filters
        content_col, filter_col = st.columns([3, 1])
        
        with filter_col:
            st.markdown("<h3 style='color: #00d4ff; font-size: 1.1em;'>🔍 Filters</h3>", unsafe_allow_html=True)
            ins_condition = st.selectbox("Medical Condition", ['All Conditions', 'Cancer', 'Diabetes', 'Obesity', 'Asthma', 'Hypertension', 'Arthritis'], key="ins_condition")
            ins_gender = st.selectbox("Gender", ['All', 'Male', 'Female'], key="ins_gender")
            ins_admission = st.selectbox("Admission Type", ['All Types', 'Emergency', 'Elective', 'Urgent'], key="ins_admission")
        
        with content_col:
            # Build where clause for Insurance filters
            ins_where = "WHERE 1=1"
            if ins_condition != 'All Conditions':
                ins_where += f" AND medical_condition = '{ins_condition}'"
            if ins_gender != 'All':
                ins_where += f" AND gender = '{ins_gender}'"
            if ins_admission != 'All Types':
                ins_where += f" AND admission_type = '{ins_admission}'"
            
            # Patient Distribution by Insurance Provider
            st.markdown("<h3 style='color: #00d4ff;'>Patient Distribution by Insurance Provider</h3>", unsafe_allow_html=True)
            ins_count = execute_query(engine, f"SELECT insurance_provider, COUNT(*) as patient_count FROM patients {ins_where} GROUP BY insurance_provider ORDER BY patient_count DESC")
            if ins_count is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(ins_count, width='stretch')
                with col2:
                    fig = px.pie(ins_count, names='insurance_provider', values='patient_count', title="Patient Distribution by Insurance")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Billing by Insurance Provider
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Billing by Insurance Provider</h3>", unsafe_allow_html=True)
            ins_billing = execute_query(engine, f"SELECT insurance_provider, ROUND(AVG(billing_amount), 2) as avg_billing FROM patients {ins_where} GROUP BY insurance_provider ORDER BY avg_billing DESC")
            if ins_billing is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(ins_billing, width='stretch')
                with col2:
                    fig = px.bar(ins_billing, x='insurance_provider', y='avg_billing', title="Avg Billing by Insurance")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Length of Stay by Insurance Provider
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Length of Stay by Insurance Provider</h3>", unsafe_allow_html=True)
            ins_los = execute_query(engine, f"SELECT insurance_provider, ROUND(AVG(DATEDIFF(discharge_date, date_of_admission))) as avg_stay FROM patients {ins_where} GROUP BY insurance_provider ORDER BY avg_stay DESC")
            if ins_los is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(ins_los, width='stretch')
                with col2:
                    fig = px.bar(ins_los, x='insurance_provider', y='avg_stay', title="Avg Length of Stay by Insurance")
                    st.plotly_chart(fig, width='stretch')

# ===== ADMISSION TYPE ANALYSIS =====
if selected_analysis == 3:
        # Create two columns: left for content, right for filters
        content_col, filter_col = st.columns([3, 1])
        
        with filter_col:
            st.markdown("<h3 style='color: #00d4ff; font-size: 1.1em;'>🔍 Filters</h3>", unsafe_allow_html=True)
            adm_condition = st.selectbox("Medical Condition", ['All Conditions', 'Cancer', 'Diabetes', 'Obesity', 'Asthma', 'Hypertension', 'Arthritis'], key="adm_condition")
            adm_insurance = st.selectbox("Insurance Provider", ['All Providers', 'Medicare', 'Blue Cross', 'Cigna', 'Aetna', 'UnitedHealthcare'], key="adm_insurance")
            adm_gender = st.selectbox("Gender", ['All', 'Male', 'Female'], key="adm_gender")
        
        with content_col:
            # Build where clause for Admission Type filters
            adm_where = "WHERE 1=1"
            if adm_condition != 'All Conditions':
                adm_where += f" AND medical_condition = '{adm_condition}'"
            if adm_insurance != 'All Providers':
                adm_where += f" AND insurance_provider = '{adm_insurance}'"
            if adm_gender != 'All':
                adm_where += f" AND gender = '{adm_gender}'"
            
            # Admission Type Distribution
            st.markdown("<h3 style='color: #00d4ff;'>Admission Type Distribution</h3>", unsafe_allow_html=True)
            adm_dist = execute_query(engine, f"SELECT admission_type, COUNT(*) as count FROM patients {adm_where} GROUP BY admission_type ORDER BY count DESC")
            if adm_dist is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(adm_dist, width='stretch')
                with col2:
                    fig = px.bar(adm_dist, x='admission_type', y='count', title="Patient Count by Admission Type")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Billing by Admission Type
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Billing by Admission Type</h3>", unsafe_allow_html=True)
            adm_billing = execute_query(engine, f"SELECT admission_type, ROUND(AVG(billing_amount), 2) as avg_billing FROM patients {adm_where} GROUP BY admission_type ORDER BY avg_billing DESC")
            if adm_billing is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(adm_billing, width='stretch')
                with col2:
                    fig = px.bar(adm_billing, x='admission_type', y='avg_billing', title="Avg Billing by Admission Type")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Length of Stay by Admission Type
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Length of Stay by Admission Type</h3>", unsafe_allow_html=True)
            adm_los = execute_query(engine, f"SELECT admission_type, ROUND(AVG(DATEDIFF(discharge_date, date_of_admission))) as avg_stay FROM patients {adm_where} GROUP BY admission_type ORDER BY avg_stay DESC")
            if adm_los is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(adm_los, width='stretch')
                with col2:
                    fig = px.bar(adm_los, x='admission_type', y='avg_stay', title="Avg Length of Stay by Admission Type")
                    st.plotly_chart(fig, width='stretch')

# ===== MEDICATION ANALYSIS =====
if selected_analysis == 4:
        # Create two columns: left for content, right for filters
        content_col, filter_col = st.columns([3, 1])
        
        with filter_col:
            st.markdown("<h3 style='color: #00d4ff; font-size: 1.1em;'>🔍 Filters</h3>", unsafe_allow_html=True)
            med_tab_condition = st.selectbox("Medical Condition", ['All Conditions', 'Cancer', 'Diabetes', 'Obesity', 'Asthma', 'Hypertension', 'Arthritis'], key="med_tab_condition")
            med_tab_insurance = st.selectbox("Insurance Provider", ['All Providers', 'Medicare', 'Blue Cross', 'Cigna', 'Aetna', 'UnitedHealthcare'], key="med_tab_insurance")
            med_tab_gender = st.selectbox("Gender", ['All', 'Male', 'Female'], key="med_tab_gender")
        
        with content_col:
            # Build where clause for Medication filters
            med_tab_where = "WHERE 1=1"
            if med_tab_condition != 'All Conditions':
                med_tab_where += f" AND medical_condition = '{med_tab_condition}'"
            if med_tab_insurance != 'All Providers':
                med_tab_where += f" AND insurance_provider = '{med_tab_insurance}'"
            if med_tab_gender != 'All':
                med_tab_where += f" AND gender = '{med_tab_gender}'"
            
            # Medication Distribution
            st.markdown("<h3 style='color: #00d4ff;'>Medication Distribution</h3>", unsafe_allow_html=True)
            med_tab_dist = execute_query(engine, f"SELECT medication, COUNT(*) as count FROM patients {med_tab_where} GROUP BY medication ORDER BY count DESC")
            if med_tab_dist is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(med_tab_dist, width='stretch')
                with col2:
                    fig = px.bar(med_tab_dist, x='medication', y='count', title="Patient Count by Medication")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Billing by Medication
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Billing by Medication</h3>", unsafe_allow_html=True)
            med_tab_billing = execute_query(engine, f"SELECT medication, ROUND(AVG(billing_amount), 2) as avg_billing FROM patients {med_tab_where} GROUP BY medication ORDER BY avg_billing DESC")
            if med_tab_billing is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(med_tab_billing, width='stretch')
                with col2:
                    fig = px.bar(med_tab_billing, x='medication', y='avg_billing', title="Avg Billing by Medication")
                    st.plotly_chart(fig, width='stretch')
            
            # Average Length of Stay by Medication
            st.markdown("<h3 style='color: #00d4ff; margin-top: 30px;'>Average Length of Stay by Medication</h3>", unsafe_allow_html=True)
            med_tab_los = execute_query(engine, f"SELECT medication, ROUND(AVG(DATEDIFF(discharge_date, date_of_admission))) as avg_stay FROM patients {med_tab_where} GROUP BY medication ORDER BY avg_stay DESC")
            if med_tab_los is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(med_tab_los, width='stretch')
                with col2:
                    fig = px.bar(med_tab_los, x='medication', y='avg_stay', title="Avg Length of Stay by Medication")
                    st.plotly_chart(fig, width='stretch')