from django.shortcuts import render ,redirect, HttpResponse
from datetime import date, timedelta
from .models import Appointment
from singup.models import Patients
from doctor.models import Doctor
from doctor.models import TimeSlot

def holdAppointmentData(request):
    if request.method == "POST":
        request.session['app_name'] = request.session['name']
        request.session['app_email'] = request.session['email']
        request.session['app_phone'] = request.session['phone']
        request.session['app_doc_id'] = request.POST.get("doctor")
        request.session['app_date'] = request.POST.get("date")
        return redirect("/appointment/book-slot/")
    else:
        return redirect("/appointment/")


def bookAppointment_old(request):

    pid = request.session['id']
    patient = Patients.objects.get(id=pid) # fetch the Patients object

    if request.method == "POST":
        name = request.session['name']
        email = request.session['email']
        phone = request.session['phone']
        dep = request.POST.get("dep")
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")
        time = request.POST.get("time")

        dId = Doctor.objects.get(id=doctor_id)

        appointmentData = Appointment(name=name, email=email, phone=phone, department=dep, doctor=dId.name, date=date, time=time, docid=dId, pid=patient)
        appointmentData.save()

    return redirect("/appointment/")

def confirmApp(request):
    if request.method == "POST":
        app_id = request.POST.get("app_id")
        app = Appointment.objects.get(id=app_id)
        app.status = "Confirmed" # set status to cinfirm
        app.save()

        logged_doc = request.session['doc']
        doc_data = Doctor.objects.get(email=logged_doc)
        doc_id = doc_data.id

        all_app = Appointment.objects.filter(docid=doc_id, status="Pending")

        return render(request, "doctor/home.html",{'docSuc': True, 'appos': all_app, 'doctor': doc_data})
    else:
        return redirect("/doctor-site/")

def deleteApp(request):
    if request.method == "POST":
        app_id = request.POST.get("app_id")
        appo = Appointment.objects.get(id=app_id)
        appo.status = "Cancelled"
        appo.save()

        logged_doc = request.session['doc']
        doc_data = Doctor.objects.get(email=logged_doc)
        doc_id = doc_data.id

        all_app = Appointment.objects.filter(docid=doc_id, status="Pending")

        return render(request, "doctor/home.html",{'docDel': True, 'appos': all_app, 'doctor': doc_data})
    else:
        return redirect("/doctor-site/")
    
def deleteAppByAdmin(request):
    if request.method == "POST":
        deleteId = request.POST.get("delete-id")
        app = Appointment.objects.filter(id=deleteId)
        app.delete()
        all_appos = Appointment.objects.all()
        return render(request, "admin/appointments.html", {'deleteAppSucc': True, 'app': all_appos})
    else:
        return redirect("/admin/appointments/")
        
def confirmAppData(request):
    if request.method == "POST":
        slot = request.POST.get("slt")
        p_email = request.session['app_email']
        phn = request.session['app_phone']
        doc = request.session['app_doc_id']
        date = request.session['app_date']

        # patients object
        p_obj = Patients.objects.get(email=p_email)
        # doctor object
        d_obj = Doctor.objects.get(id=doc)

        # select slot and convert into Booked-Slot
        s_obj = TimeSlot.objects.get(id=slot)
        stime = s_obj.start_time
        etime = s_obj.end_time
        s_obj.is_booked = True
        s_obj.save()

        confirmAppData = Appointment(date=date, docid=d_obj, pid=p_obj, start_time=stime, end_time=etime)
        confirmAppData.save()

        return redirect("/appointment/")
    else:
        return HttpResponse("Serever Error..!.. Something Heppeens Wrong")
    
def isAttand(request):
    if request.method == "POST":
        appId = request.POST.get("idHolder")

        # object of Appointment Table
        app = Appointment.objects.get(id=appId)
        app.is_attend = True
        app.save()

        logged_doc = request.session['doc']
        all_doctors = Doctor.objects.get(email=logged_doc)

        # Object for All Apointments
        all_apps = Appointment.objects.filter(docid=all_doctors, is_attend=False)
        print(all_apps)
        
        return render(request, "doctor/home.html", {'isAttand': True, 'doctor': all_doctors, 'appos': all_apps})
    else:
        return redirect("/doctor-site/")