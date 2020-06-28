from django import template

register = template.Library()

@register.filter
def parent_comments(comments):
	return comments.filter(parent__isnull=True)