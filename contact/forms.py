from django import forms
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class ContactForm(forms.ModelForm):


    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone', 'email', 'description', 'category')
        widgets = {
        'last_name': forms.TextInput(attrs={'placeholder': 'Escreva aqui'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError('Erro do first_name', code='Invalid')
            )

        if last_name == 'ABC':
            self.add_error(
                'last_name',
                ValidationError('Erro do last_name', code='Invalid')
            )

        return super().clean()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    class Meta:
        model = User
        fields = (
            'first_name' , 'last_name', 'email', 'username', 'password1', 'password2',
        )

    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            return self.add_error(
                'email',
                ValidationError('E-mail já cadastrado', code='invalid')
            )


        return email

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(min_length=2, max_length=30, required=True)
    last_name = forms.CharField(min_length=2, max_length=30, required=True)
    password1 = forms.CharField(
        label='password1', 
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
        )
    password2 = forms.CharField(
        label='password2', 
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Use the same password as before',
        required=False
        )
    
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username',
        )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', ValidationError('Senhas não batem'))

        return super().clean()
    
    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password1')

        if password:
            user.set_password()

        
        return user



    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                return self.add_error(
                    'email',
                    ValidationError('E-mail já cadastrado', code='invalid')
                )
            
            return email
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password1', ValidationError(errors))


        return password1






