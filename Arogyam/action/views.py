from django.shortcuts import render,redirect
from .models import Admin
from doctor.models import Doctor, TimeSlot
from singup.models import Patients
from appointment.models import Appointment
from datetime import datetime


# ================== View for User Side =======================

def redirectHome(request):
    totalPatients = Patients.objects.count()
    totalDoctors = Doctor.objects.count()
    totalAppointments = Appointment.objects.count()
    return render(request, "index.html", {
        'totalPatients': totalPatients,
        'totalDoctors': totalDoctors,
        'totalApps': totalAppointments
        })

def redirectProfile(request):
    return render(request, "profile.html")

def redirectDoctor(request):
    all_doctors = Doctor.objects.all()
    return render(request, "doctor.html",{"doctors": all_doctors})

def redirectAppointment(request):
    all_doc = Doctor.objects.all()
    p_id = request.session.get('id')
    all_appointment = Appointment.objects.filter(pid=p_id)

    now = datetime.now()

    # Add 'time_left' attribute to each appointment
    for app in all_appointment:
        appointment_datetime = datetime.combine(app.date, app.start_time)

        app.timestamp = int(appointment_datetime.timestamp())

        remaining = appointment_datetime - now

        if remaining.total_seconds() <= 0:
            app.time_left = None
        else:
            total_seconds = int(remaining.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            app.time_left = f"{hours}h {minutes}m {seconds}s"

    numOfApp = all_appointment.count()
    return render(request, "appointment.html", {
        "docs": all_doc,
        "appointments": all_appointment,
        "numOfApp": numOfApp
        })

def redirectSlotPage(request):
    if request.session['app_doc_id']:
        doc = request.session['app_doc_id']
        date = request.session['app_date']
        slot = TimeSlot.objects.filter(docid=doc, slot_date=date)
        numOfSlots = TimeSlot.objects.filter(docid=doc, slot_date=date).count()
        if numOfSlots <= 0:
            return render(request, "not_avilable.html")
        else:
            return render(request, "slot.html", {'slots': slot})
    else:
        return render(request, "slot.html")

def redirectLogin(request):
    return render(request, "login.html")

def redirectSingup(request):
    return render(request, "singup.html")


# ================== View for Admin Side =======================

def redirectAdmin(request):
    return render(request, "admin/dash.html")

def redirectAdminDoctors(request):
    doctors = Doctor.objects.all() # get all records from doctor table
    return render(request, "admin/doctors.html", {"doctors": doctors})

def redirectAdminPatients(request):
    patients = Patients.objects.all() # get all recordes from Patients table
    return render(request, "admin/patients.html", {"patients": patients})

def redirectAdminAppointments(request):
    all_appos = Appointment.objects.all();
    return render(request, "admin/appointments.html", {'app': all_appos})

def redirectAdminLogin(request):
    return render(request, "admin/admin-login.html")

def logoutAdmin(request):
    del request.session['admin']
    return redirect("/")


# ================== View for Doctor Side =======================


def redirectDoctorDashboard(request):
    if 'doc' in request.session:
        logged_doc = request.session['doc']
        doc_data = Doctor.objects.get(email=logged_doc)
        doc_id = doc_data.id
        today = datetime.now()
        slots = TimeSlot.objects.filter(date=today)
        numOfSlots = slots.count()

        # appo = Appointment.objects.filter(docid=doc_id, is_attend=False)
        appo = Appointment.objects.filter(docid=doc_id)

        return render(request, "doctor/dash.html", {"doctor": doc_data, "appos": appo, "slots": slots, "numOfSlots": numOfSlots})
    else:
        return redirect("/doctor-login/")

def redirectDoctorLogin(request):
    return render(request, "doctor/doctor-login.html")




# ============================= Default Views ===========================

def adminLogin(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")

        if Admin.objects.filter(name=name, pwd=pwd).exists():
            request.session['admin'] = name
            request.session['admin_pwd'] = pwd
            return redirect("/admin/")
        else:
            return render(request, "wrong-password.html")
    else:
        return redirect("/admin-login/")