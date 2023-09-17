from django.shortcuts import render,redirect
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from secustomuser.models import CustomUser ,customrole
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import user_passes_test
import json
from django.apps import apps
from django.template.loader import render_to_string
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import csv
import smtplib
import openpyxl
import pandas as pd
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render, redirect
from .forms import CSVUploadForm  # Import your CSV upload form
from .email_report import (
    report_period,
    emp_data,
    attendance_percentage,
    sender_email,
    sender_password,
)

            
@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        #creating a instance of CSVUploadForm to getting data and file from request
        form = CSVUploadForm(request.POST, request.FILES)
        #check for form validations
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            #  read csv file 
            df = pd.read_csv(csv_file, header=None)

            #clear the data (getting usefull data)
            employee_data = emp_data(df)
            
            #collect all the user with role intern
            intern_users = CustomUser.objects.filter(role__name='intern')

            # Now, you can access the details of the 'Intern' users
            # for user in intern_users:
                
            #     print(f"User: {user.name}")
            #     print(f"Employee ID: {user.Employee_id}")
            #     print(f"Username: {user.username}")
            #     print(f"Email: {user.email}")
            #     print(f"Phone Number: {user.phone_no}")
            #     print(f"Organisation: {user.Organisation.name}")
            #     print("------------")
            # print()
            # print()
            # print()
            # print(employee_data.keys())
            data = {}
            for user in intern_users:
                if user.Employee_id in employee_data.keys():
                    data[str(user.Employee_id)] = employee_data[str(user.Employee_id)]
                    intern_id = user.Employee_id
                    name = user.name
                    receiver_email = user.email

                    emp_dat = employee_data[str(intern_id)]

                    #fetching data from the each user 
                    dynamic_content = {
                        "name": name,
                        "report_type": "attendance",
                        "period": report_period(df),
                        "intern_id": str(intern_id),
                        "start_date": str(emp_dat["start_date"]),
                        "last_date":str(emp_dat["last_date"]),
                        "early_leaves": str(emp_dat["early_leave"]),
                        "total_absent": str(emp_dat["total_absent"]-15),
                        "total_present": str(emp_dat["total_present"]),
                        "total_days": str(emp_dat["total_days"]-15),
                        "percent": str(attendance_percentage(emp_dat["total_present"]))
                    }
                    # print(dynamic_content)

                    # ready html page to send the email to user
                    htmlfile = render_to_string("email.html",dynamic_content)
                    # print(htmlfile)

                    

                    # Set up the email message
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    message["Subject"] = f"""YOUR Attendance Report {name}"""
                    message["Name"] = f"{name}"
                    message.attach(MIMEText(htmlfile, "html"))

                    print('Mail Ready to send ',receiver_email,sep=" ")
                    
                    # Send the email
                    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                        smtp.starttls()
                        smtp.login(sender_email, sender_password)
                        smtp.sendmail(sender_email, receiver_email, message.as_string())
                        print("Email sent successfully.")


            return JsonResponse({"data":data})
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})
def emailview(request):
     return render(request,"email.html")
    # return HttpResponse("<h1>hello</h1>")