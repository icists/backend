from django import forms

class MailingForm(forms.Form):
    contact = forms.FileField(label="Upload Contact File(.xlsx)")
    template = forms.ChoiceField(choices=(('eng-invi', 'English Speaker Invitation'), ('kor-invi', '한국어 연사 초청'),))
    values = forms.CharField(max_length=3000, label="Content", widget=forms.Textarea)