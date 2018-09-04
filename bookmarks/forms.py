from django import forms


class SearchForm(forms.Form):
    query = forms.charField(
        label=u'Enter a keyword to search for',
        widget=forms.TextInput(attrs={'size': 32})
    )
