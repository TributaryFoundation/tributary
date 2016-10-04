import structlog
log = structlog.get_logger('trib')

from django import forms


class DonationForm(forms.Form):
    amount_choices = (
        ( 1500, '$15'),
        ( 5000, '$50'),
        (10000, '$100'),
    )
    name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    # if you change this field ensure that the javascript in the template still works
    # namely, the javascript code looks for this field by name to populate it's value
    stripe_card_token = forms.CharField(required=True, widget=forms.HiddenInput)

    amount = forms.TypedChoiceField(required=True, coerce=int, empty_value=None, choices=amount_choices)
    tip = forms.BooleanField(initial=True)
    instructions = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned = super(DonationForm, self).clean()
        l = log.bind(
            name=cleaned.get('name'),
            email=cleaned.get('email'),
            amount=cleaned.get('amount'),
            tip=cleaned.get('tip'),
        )
        l.info("donation form cleaned")
