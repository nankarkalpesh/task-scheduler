import streamlit as st
import pandas as pd

# ----------------------------
# Job Class
# ----------------------------
class Job:
    def __init__(self, job_id, deadline, profit):
        self.job_id = job_id
        self.deadline = deadline
        self.profit = profit

# ----------------------------
# Greedy Scheduling Algorithm
# ----------------------------
def job_scheduling(jobs):
    jobs.sort(key=lambda x: x.profit, reverse=True)  # sort by profit
    max_deadline = max(job.deadline for job in jobs)
    slots = [-1] * (max_deadline + 1)

    total_profit = 0
    scheduled_jobs = []

    for job in jobs:
        for t in range(job.deadline, 0, -1):
            if slots[t] == -1:
                slots[t] = job.job_id
                total_profit += job.profit
                scheduled_jobs.append(job.job_id)
                break

    return scheduled_jobs, total_profit, slots

# ----------------------------
# Streamlit App
# ----------------------------
st.set_page_config(page_title="Task Scheduling with Deadlines", layout="centered")

st.title("Task Scheduling with Deadlines")
st.write("""
This app schedules tasks with **deadlines** and **profits** using a Greedy Algorithm.  
It chooses the most profitable tasks that fit into available time slots.
""")

# Input: number of jobs
n = st.number_input("Enter number of tasks:", min_value=1, max_value=10, value=4)

jobs = []

# Input: job details
st.subheader("Enter Task Details")
for i in range(n):
    col1, col2, col3 = st.columns(3)
    with col1:
        job_id = st.text_input(f"Task ID {i+1}", value=chr(65+i))
    with col2:
        deadline = st.number_input(f"Deadline {i+1}", min_value=1, value=i+1, key=f"dl{i}")
    with col3:
        profit = st.number_input(f"Profit {i+1}", min_value=1, value=(i+1)*10, key=f"pr{i}")
    jobs.append(Job(job_id, deadline, profit))

# Run Scheduling
if st.button("Run Scheduling"):
    scheduled, profit, slots = job_scheduling(jobs)

    st.success("Scheduling Completed")

    # Table of Jobs
    df = pd.DataFrame([[j.job_id, j.deadline, j.profit, "Yes" if j.job_id in scheduled else "No"] 
                       for j in jobs],
                      columns=["Job ID", "Deadline", "Profit", "Scheduled"])
    st.subheader("Jobs Summary")
    st.dataframe(df)

    # Total Profit
    st.subheader("Total Profit")
    st.info(f"Maximum Profit Achieved = {profit}")

    # Simple Timeline Data
    timeline_data = []
    for t in range(1, len(slots)):
        timeline_data.append({
            "Time Slot": t,
            "Job": slots[t] if slots[t] != -1 else "Empty"
        })

    timeline_df = pd.DataFrame(timeline_data)

    st.subheader("Job Scheduling Timeline")
    st.table(timeline_df)
