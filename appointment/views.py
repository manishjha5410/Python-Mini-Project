from django.shortcuts import render, redirect
from .models import * 
from .forms import * 
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user_profile.models import UserProfile
# Create your views here.

class AppointmentsForAPatientView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)


class AppointmentsForADoctorView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)


class MedicalHistoryView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Prescription.objects.filter(patient=self.request.user)


class PrescriptionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Prescription.objects.filter(doctor=self.request.user)


@login_required(login_url='/login/')
def PrescriptionCreateView(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            return redirect('appointment:doc-prescriptions')
    else:
        form = PrescriptionForm()
    return render(request, 'appointment/prescription_create.html', {'form': form})


@login_required(login_url='/login/')
def OutstandingCreate(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()
            return redirect('appointment:hr_accounting')
    else:
        form = PaymentForm()
    return render(request, 'appointment/outstanding.html', {'form': form})

@login_required(login_url='/login/')
def UpdatedOutstandingPk(request, pk):
    payment = Payment.objects.get(id=pk)
    if request.method == 'POST':
        payment.paid = request.POST['paid']
        payment.outstanding = request.POST['outstanding']
        payment.total = request.POST['total']
        payment.payment_type = request.POST['payment_type']
        payment.save()
        return redirect('appointment:hr_accounting')
    else:
        payment.newDate = str(payment.date)
        return render(request, 'appointment/accounting_update.html', {'form': payment})

@login_required(login_url='/login/')
def DeleteOutstandingPk(request, pk):
    payment = Payment.objects.get(id=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('appointment:hr_accounting')
    else:
        return render(request, 'appointment/appointment_delete.html', {'form':payment})

@login_required(login_url='/login/')
def AppointmentCreateView(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('appointment:r_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/appointment_create.html', {'form': form})

@login_required(login_url='/login/')
def UpdatedPrescriptionsPk(request,pk):
    prescription = Prescription.objects.get(id=pk)
    if request.method == 'POST':
        prescription.symptoms = request.POST['symptoms']
        prescription.prescription = request.POST['prescription']
        prescription.save()
        return redirect('appointment:doc-prescriptions')
    else:
        return render(request, 'appointment/prescription_update.html', {'form': prescription})

@login_required(login_url='/login/')
def DeletePrescriptionsPk(request,pk):
    prescription = Prescription.objects.get(id=pk)
    if request.method == 'POST':
        prescription.delete()
        return redirect('appointment:doc-prescriptions')
    else:
        return render(request, 'appointment/appointment_delete.html', {'form':prescription})

@login_required(login_url='/login/')
def UpdatedAppointmentPk(request, pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == 'POST':
        appointment.status = request.POST['status']
        appointment.date = request.POST['date']
        appointment.time = request.POST['time']
        appointment.save()
        return redirect('appointment:r_dashboard')
    else:
        appointment.newDate = str(appointment.date)
        appointment.newTime = str(appointment.time)[:5]
        return render(request, 'appointment/appointment_update.html', {'form': appointment})

@login_required(login_url='/login/')
def DeleteAppointmentPk(request,pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment:r_dashboard')
    else:
        return render(request, 'appointment/appointment_delete.html', {'form':appointment})

@login_required(login_url='/login/')
def rdashboard(request):
    if request.method == "GET" and request.user.user_type == "R":
        context = {
            "totalApp" : len(Appointment.objects.all()),
            "compApp" : len(Appointment.objects.filter(status="Completed")),
            "pendApp" : len(Appointment.objects.filter(status="Pending")),
            "app_list" : Appointment.objects.all(),
            "pat_list" : UserProfile.objects.filter(user__user_type="P")[:5]
        }
        return render(request, 'appointment/r_dashboard.html', context=context)


@login_required(login_url='/login/')
def hrdashboard(request):
    if request.method == "GET" and request.user.user_type == "HR":
        context = {
            "totalPat" : len(User.objects.filter(user_type="P")),
            "totalDoc" : len(User.objects.filter(user_type="D")),
            "ondutyDoc" : len(UserProfile.objects.filter(status="Active").filter(user__user_type="D")),
            "doc_list" : UserProfile.objects.filter(user__user_type="D")
        }
        return render(request, 'appointment/hr_dashboard.html', context=context)


@login_required(login_url='/login/')
def hraccounting(request):
    if request.method == "GET" and request.user.user_type == "HR":
        context = {
            "payment_ind" : Payment.objects.filter(payment_type="I"),
            "payment_cons" : Payment.objects.filter(payment_type="C"),
        }
        return render(request, 'appointment/accounting.html', context=context)


@login_required(login_url='/login/')
def pateintpayments(request):
    if request.method == "GET":
        context = {
            "payment_me" : Payment.objects.filter(patient=request.user),
        }
        return render(request, 'appointment/payment_invoice.html', context=context)