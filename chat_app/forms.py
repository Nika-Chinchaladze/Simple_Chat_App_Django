from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class RegisterModelForm(UserCreationForm):
    first_name = forms.CharField(max_length=1000, required=False, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=1000, required=False, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=1000, required=False,
                             widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2",)

    def __init__(self, *args, **kwargs):
        super(RegisterModelForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class LoginModelForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password",)

    def __init__(self, *args, **kwargs):
        super(LoginModelForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class HomeForm(forms.Form):
    room_name = forms.CharField(label="Create New Room", max_length=1000,
                                widget=forms.TextInput(attrs={"class": "form-control"}))


class SearchForm(forms.Form):
    room_name = forms.CharField(label="Search Room", max_length=1000,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
