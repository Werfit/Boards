from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
	return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
	css_class = ''
	if bound_field.form.is_bound:
		if bound_field.errors:
			css_class = 'is-invalid'
		elif field_type(bound_field) != 'PasswordInput':
			css_class = 'is-valid'

	return f'form-control {css_class}'


# Checks if field is multiselect field
@register.filter
def is_multi(bound_field):
	return field_type(bound_field) == 'CheckboxSelectMultiple'


# Checks if field is radio field
@register.filter
def is_radio(bound_field):
	return field_type(bound_field) == 'RadioSelect'
