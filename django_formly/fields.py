from django.forms import widgets
def get_field_type(field):
    if isinstance(field.widget, (widgets.TextInput,)):
        return 'input'
    elif isinstance(field.widget, (widgets.Textarea,)):
        return 'textarea'
    elif isinstance(field.widget, (widgets.CheckboxInput,)):
        return 'checkbox'
    elif isinstance(field.widget, (widgets.RadioChoiceInput,widgets.RadioSelect)):
        return 'radio'
    elif isinstance(field.widget, (widgets.Select,)):
        return 'select'

def get_field_description(key,field):
    attributes = {'templateOptions':{'label':field.label,'required':field.required},'key':key}
    if hasattr(field, 'help_text'):
        attributes['templateOptions']['description'] = field.help_text
#     if field.attrs.has_key('placeholder'):
#         attributes['placeholder'] = field.attrs['placeholder']
    attributes['type'] = get_field_type(field)
#     if options:
#         attributes['templateOptions']['options']: [{id: 1, title : "Administrator"}, {id: 2, title : "User"}]
    if hasattr(field,'choices'):
        attributes['templateOptions']['options'] = [{'value':choice[0],'name':choice[1]} for choice in field.choices]
#         print field.choices
#         for choice in field.choices:
#             print choice
#         attributes['templateOptions']['options']: [{id: 1, title : "Administrator"}, {id: 2, title : "User"}]
    return attributes

