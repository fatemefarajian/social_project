from django import forms
from .models import User, Post, Comment
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label='username or phone')
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput())


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='رمز')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='تکرار رمز')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسوررد ها مطابقت ندارند')
        else:
            return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists")
        return phone


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'photo', 'date_of_birth', 'bio', 'job']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists")
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    name = forms.CharField(max_length=100, required=True, label='نام')
    email = forms.EmailField(error_messages={'invalid': 'لطفاً یک ایمیل معتبر وارد کنید.'}, label='ایمیل')
    phone = forms.CharField(max_length=11, min_length=11, required=True, label='تلفن')
    message = forms.CharField(widget=forms.Textarea, required=True, label='پیام')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label='موضوع')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.startswith('09'):
                raise forms.ValidationError('شماره تلفن باید با پیش شماره09 شروع شود')
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن  وارد شده عددی نیست ')
            if not len(phone) == 11:
                raise forms.ValidationError('شماره تلفن باید 11 عدد باشد')
            else:
                return phone


class CreationPostForm(forms.ModelForm):
    image1 = forms.ImageField(label='تصویر اول')
    image2 = forms.ImageField(label='تصویر دوم')

    class Meta:
        model = Post
        fields = ['description', 'tags']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']