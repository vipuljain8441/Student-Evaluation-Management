import smtplib
import openpyxl
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
load_dotenv()


sender_email = os.environ.get('SENDER_EMAIL')  # Replace with your email address
sender_password = os.environ.get('PASSWORD')  


def report_period(df):
    row_1 = df.iloc[0]
    report_period = row_1.iloc[6]

    print(f'report period identified : {report_period}')
    return report_period


def emp_data(df):
    
    empcode = None
    name = None
    extract_data = False
    date_list = []
    in_time_list = []
    out_time_list = []
    status_list = []
    early_leave = 0
    total_absent = 0
    total_present = 0
    late_checkin = 0
    total_days = 0
    is_wo = False
    employee_data = {}
    
    comparison_out_time_str = "18:00"
    comparison_in_time_str = "12:00"

    for index, row in df.iterrows():
        # Extract Empcode and Name
        if row[0] == "Empcode":
            if extract_data == True:
                employee_data[empcode] = {
                    "total_days": total_days,
                    "name": name,
                    "intern_id":empcode,
                    "start_date": date_list[0],
                    "last_date":date_list[-1],
                    # "in_time": in_time_list,
                    # "out_time": out_time_list,
                    # "status": status_list,
                    "early_leave": early_leave,
                    "late_checkin": late_checkin,
                    "total_absent": total_absent,
                    "total_present": total_present,
                }
                extract_data = False
                date_list = []
                in_time_list = []
                out_time_list = []
                status_list = []
                early_leave = 0
                total_present = 0
                total_absent = 0
                total_days = 0

            empcode = row[1]
            name = row[4]

            extract_data = True

        elif extract_data and row[8] == "WO":
            is_wo = True

        elif (
            extract_data
            and row[0] != "Empcode"
            and row[0] != ["Date "]
            and row[5] != "OUTTime"
            and row[8] != "WO"
        ):
            # Extract Date, INTime, OUTTime, and Status for the current employee
            date = row[0]
            in_time = row[2]
            out_time = row[5]
            status = row[8]

            if not is_wo:
                total_days = total_days + 1
                
                if (
                    out_time != "OUTTime"
                    and out_time != "--:--"
                    and out_time != "00:00"
                ):
                    out_time_comp = datetime.strptime(out_time, "%H:%M")
                    comparison_time = datetime.strptime(
                        comparison_out_time_str, "%H:%M"
                    )

                    if out_time_comp < comparison_time:
                        early_leave = early_leave + 1

                if in_time != "INTime" and in_time != "--:--" and in_time != "00:00":
                    in_time_comp = datetime.strptime(in_time, "%H:%M")
                    comparison_time = datetime.strptime(comparison_in_time_str, "%H:%M")

                    if in_time_comp > comparison_time:
                        late_checkin = late_checkin + 1

                if status == "A":
                    total_absent = total_absent + 1
                elif status == "P":
                    total_present = total_present + 1

                date_list.append(date)
                in_time_list.append(in_time)
                out_time_list.append(out_time)
                status_list.append(status)
            else:
                is_wo = False

    print('data evaluated')
    print(type(employee_data))
    return employee_data


def attendance_percentage(present, total_days = 50):
    print(present)
    percent = ((present)/total_days) * 100
    print(percent)
    return percent

