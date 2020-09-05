from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import User
import sqlite3,os

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='REQUIRED. ADD A VALID EMAIL ID.')
    registration_no=forms.CharField(max_length=20,help_text='ENTER YOUR COLLEGE REGISTRATION NO.')
    class Meta:
        model = User
        fields = ('email',
                  'registration_no',
                  'password1',
                  'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if email.count('@')==1:
            address,domain=email.split('@')
            if '.' not in domain:
                self.add_error('email', 'Please use a valid email address')
            if '.' not in address:
                self.add_error('email', 'Please use a valid email address,no "." in address')
            elif address[2]!='.':
                self.add_error('email', 'Please use a valid email address,"." in wrong position')
        else:
            self.add_error('email','Please use a valid email address')

        if not str(email).endswith('@btech.nitdgp.ac.in'):
            self.add_error('email','Please use institute email ID.It should end with "@btech.nitdgp.ac.in"')

        #print(email)
        return email
    
    def clean_registration_no(self):
        registration_no = self.cleaned_data['registration_no'].upper().strip()
        conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'account/btech_cs_2019.sqlite3'))
        cur = conn.cursor()
        cur.execute('SELECT Name FROM cs_2019_z WHERE RegNo= ? ', (registration_no.upper(),))
        name = cur.fetchone()
        if name is None:
            registration_no=None

        if (registration_no is None) or (registration_no<settings.START_REG_NO or registration_no>settings.END_REG_NO):
            self.add_error('registration_no','You are not allowed to vote for this election.')
        return registration_no

    def clean(self):
        super().clean()
        reg=self.cleaned_data.get('registration_no')
        email=self.cleaned_data.get('email')
        if reg and email:
            if str(reg).lower() not in str(email):
                raise ValidationError('Registration no. must be present in the email correctly!')
            if str(reg).upper()!=str(email.split('@')[0].split('.')[1]).upper():
                raise ValidationError('Registration no. must be present in the email!!')

class AccountAuthenticationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('registration_no','password')

    def clean(self):
        if self.is_valid():
            registration_no=self.cleaned_data['registration_no'].upper()
            password=self.cleaned_data['password']
            #print(registration_no,password)
            if not authenticate(registration_no=registration_no,password=password):
                raise forms.ValidationError('INVALID LOGIN CREDENTIALS')

