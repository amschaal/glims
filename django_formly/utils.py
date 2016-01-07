from django_formly.fields import get_field_description

def generate_formly_fields(form):
    formly_fields = []
    for key, field in form.fields.items():
        formly_fields.append(get_field_description(key,field))
    return formly_fields

# def get_form(form_id):