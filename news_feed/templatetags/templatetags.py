from django import template

register = template.Library()

@register.filter
def parent_comments(comments):
	return comments.filter(parent__isnull=True)

@register.filter
def update_counter(value):
    counter = value + 1
    return counter
