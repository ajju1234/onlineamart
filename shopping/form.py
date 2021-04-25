from django import forms

class ReviewForm(forms.Form):
	rating_choices=[
		(1, 'Very Poor'),
		(2, 'Bad'),
		(3, 'Average'),
		(4, 'Good'),
		(5, 'Very Good')
	]
	rating = forms.TypedChoiceField(choices=rating_choices, coerce=int, initial=3)
	# rating=forms.IntegerField(choices=rating_choices)
	review_text=forms.CharField(max_length=300)

class LoginForm(forms.Form):
	username= forms.CharField(max_length=150)
	password = forms.CharField(widget=forms.PasswordInput())