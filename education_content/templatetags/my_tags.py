from django import template

register = template.Library()


# Creating a simple template tag
@register.simple_tag
def mediapath(format_string):
    # This tag returns a string representing the media path for a given format_string.
    # It's designed to be used in templates like: {% mediapath "images/my_image.jpg" %}
    return f'/media/{format_string}'


# Creating a template filter
@register.filter
def mediapath_filter(text):
    # This filter appends "/media/" to the beginning of the input text.
    # It's designed to be used in templates like: {{ "images/my_image.jpg" | mediapath_filter }}
    return f'/media/{text}'
