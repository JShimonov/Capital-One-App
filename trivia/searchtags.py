from django import forms

class searchform(forms.Form):
    # all the final variables
    YEARS_RANGE = [years for years in range(1965, 2012)]
    DIFFICULTY = [('easy', 'Easy'), ('intermediate', 'Intermediate'), ('difficult', 'Difficult'), ('none', 'None')]
    YEARS = [i for i in range(1965, 2018)]


    category = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder' : 'Category', 'style' : 'border-radius: 15px', 'id' : 'search_form'}))
    difficulty = forms.CharField(label='Difficulty Level', widget=forms.Select(choices=DIFFICULTY), required=False)
    from_date = forms.DateField(label='From ', widget=forms.SelectDateWidget(years=YEARS, empty_label=("Year", "Month", "Day")), required=False)
    to_date = forms.DateField(label='To ', widget=forms.SelectDateWidget(years=YEARS, empty_label=("Year", "Month", "Day")), required=False)
