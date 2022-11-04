from .models import *
from django.forms import *
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class UserLoginForm(AuthenticationForm):
    username = CharField(label='Логин', widget=(TextInput(attrs={})))
    password = CharField(label='Пароль', widget=(PasswordInput(attrs={})))


class UserRegisterForm(UserCreationForm):
    username = CharField(label='Логин', widget=(TextInput(attrs={})))
    password1 = CharField(label='Пароль', widget=(PasswordInput(attrs={})))
    password2 = CharField(label='Подтверждение пароля', widget=(PasswordInput(attrs={})))
    email = EmailField(label='Электронная почта', help_text="Введите cвой действующий почтовый ящик", widget=(EmailInput(attrs={})))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date', 'location']


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['photo', 'content']
        photo = ImageField(validators=[FileExtensionValidator('jpg')])

        error_css_class = 'err'
        field_classes = {
            'photo': ImageField,
        }
        widgets = {
            'content': Textarea(attrs={'class': 'new-post__content-input'}),
        }


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'class': 'comment-form__input input',
                'placeholder': 'what are you thinking about?'
            }),
        }

    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)
        # self.fields['content'].widget.attrs.update({'class': 'myfieldclass'})
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'comment-form__input'


