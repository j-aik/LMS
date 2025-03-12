from django import forms
from .models import CustomUser,Parent,Staff,Student # Import your User model
from .models import Staff, Subject, ClassST

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']  # Add fields you want to edit


class ParentEditForm(forms.ModelForm):
    class Meta:
        model =  Parent
        fields = "__all__"
        exclude = ['user']

class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"
        exclude = ['user']


    # subject = forms.ModelMultipleChoiceField(
    #   queryset=Subject.objects.none(),
    #   widget=forms.CheckboxSelectMultiple,
    #   required=False
    # )
    #
    # class_assigned = forms.ModelMultipleChoiceField(
    #    queryset=ClassST.objects.none(),
    #    widget=forms.CheckboxSelectMultiple,
    #    required=False
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the querysets after initialization
        self.fields['subject'].queryset = Subject.objects.all()
        self.fields['class_assigned'].queryset = ClassST.objects.all()
    # Set the querysets after initialization
    #    self.fields['subject'].queryset = Subject.objects.all()
    #    self.fields['class_assigned'].queryset = ClassST.objects.all()

class StudentEditForm(forms.ModelForm):
    class_assigned = forms.ModelChoiceField(
        queryset=ClassST.objects.all(),
        empty_label="Select a class",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    class Meta:
        model =  Student
        fields = "__all__"
        exclude = ['user']