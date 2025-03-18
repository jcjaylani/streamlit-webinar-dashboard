# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 07:51:21 2025

@author: carba
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    file_path = "Center for Nonprofit Webinar Information.xlsx"
    df = pd.read_excel(file_path)
    df['Webinar Date'] = pd.to_datetime(df['Webinar Date'])
    df['Webinar_Year_Month'] = df['Webinar Date'].dt.to_period('M')
    return df

@st.cache_data
def load_alp_data():
    file_path = "Action Learning Projects (ALP)(Sheet1).csv"
    data = pd.read_csv(file_path, encoding='cp1252')
    data['Year_Semester'] = data['Year'].astype(str) + '-' + data['Semester']
    return data

df = load_data()
data = load_alp_data()

# Sidebar for filtering
st.sidebar.header("Filter Options")
date_range = st.sidebar.date_input("Select Date Range", [])

# Convert date_range inputs to datetime64[ns] to match 'Webinar Date'
if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    df = df[(df['Webinar Date'] >= start_date) & (df['Webinar Date'] <= end_date)]

# Group data for visualization
webinar_counts = df.groupby('Webinar_Year_Month')['Webinar Attendees'].sum().reset_index()
webinar_counts['Webinar_Year_Month'] = webinar_counts['Webinar_Year_Month'].astype(str)

# Streamlit Title
st.title("📊 Nonprofit Webinars & ALP Dashboard")

# --- CHART 1: Webinar Attendees Trend ---
st.subheader("📅 Webinar Attendees by Year-Month")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=webinar_counts['Webinar_Year_Month'], y=webinar_counts['Webinar Attendees'], color='red', ax=ax)
ax.set_xlabel("Webinar Year-Month")
ax.set_ylabel("Total Webinar Attendees")
ax.set_title("Webinar Attendees Count by Year-Month")
ax.set_xticklabels(webinar_counts['Webinar_Year_Month'], rotation=45, ha="right")
st.pyplot(fig)

# --- CHART 2: Nonprofit Project Type Distribution ---
st.subheader("📊 Distribution of Nonprofit Project Types")
summary = data.groupby('Nonprofit_Project_Type').agg(
    Project_Count=('Nonprofit_Project_Type', 'size')
).reset_index()

fig, ax = plt.subplots(figsize=(8, 8))
colors = sns.color_palette("viridis", len(summary))
ax.pie(summary['Project_Count'], labels=summary['Nonprofit_Project_Type'], autopct='%1.1f%%', startangle=140, colors=colors)
ax.set_title('Nonprofit Project Type Distribution')
st.pyplot(fig)

# --- CHART 3: Revenue or Savings by Project Type ---
st.subheader("💰 Revenue or Savings by Nonprofit Project Type")
revenue_summary = data.groupby('Nonprofit_Project_Type')['Potential Revenue Gained or Consulting Dollars Saved'].sum().reset_index()
revenue_summary = revenue_summary.sort_values(by='Potential Revenue Gained or Consulting Dollars Saved', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y='Nonprofit_Project_Type', x='Potential Revenue Gained or Consulting Dollars Saved', data=revenue_summary, palette='magma', ax=ax)
ax.set_xlabel("Total Revenue Gained or Savings")
ax.set_ylabel("Nonprofit Project Type")
ax.set_title("Revenue or Savings by Nonprofit Project Type")
st.pyplot(fig)

# --- CHART 4: Student Enrollment Trends ---
st.subheader("📚 Student Enrollment in Action Learning Projects")
student_counts = data.groupby('Year_Semester')['Student_No'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Year_Semester', y='Student_No', data=student_counts, palette='coolwarm', ax=ax)
ax.set_xlabel("Year-Semester")
ax.set_ylabel("Total Students")
ax.set_title("Total Students by Year-Semester")
ax.set_xticklabels(student_counts['Year_Semester'], rotation=45)
st.pyplot(fig)

# --- CHART 5: Student Count Distribution by Year ---
st.subheader("🎓 Student Distribution by Year")
yearly_summary = data.groupby('Year')['Student_No'].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))
colors = sns.color_palette("viridis", len(yearly_summary))
ax.pie(yearly_summary['Student_No'], labels=yearly_summary['Year'], autopct='%1.1f%%', startangle=140, colors=colors)
ax.set_title('Total Students by Year')
st.pyplot(fig)

# --- DATA TABLE ---
st.subheader("📋 Webinar Data Table")
st.dataframe(df[['Webinar Date', 'Webinar Topic', 'Webinar Attendees']])