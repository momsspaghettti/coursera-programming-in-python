from django import forms


class DummyForm(forms.Form):
    text = forms.CharField(label='Отзыв', min_length=10, max_length=1000)
    grade = forms.IntegerField(label='Оценка', min_value=1, max_value=10)
    image = forms.FileField(label='Фотография', required=False)
