from django import forms

class searchform(forms.Form):
    YEARS_RANGE = [years for years in range(1965, 2012)]

    DIFFICULTY = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]

    category = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder' : 'Category', 'style' : 'border-radius: 15px', 'id' : 'search_form'}))
    difficulty = forms.CharField(label='Difficulty Level', widget=forms.Select(choices=DIFFICULTY), required=False)
    #from_date = forms.DateField()
    #to_date = forms.DateField()
