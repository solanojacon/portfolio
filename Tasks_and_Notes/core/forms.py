from django import forms
from django.core.validators import RegexValidator

validate_hex_color = RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a color in the format #RRGGBB.')


class OwnedModelForm(forms.ModelForm):
    """ModelForm that knows the logged-in user, passed in by OwnerFormMixin."""

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


class ColorInput(forms.TextInput):
    input_type = 'color'

    def __init__(self, attrs=None):
        super().__init__({'class': 'form-control form-control-color', **(attrs or {})})
