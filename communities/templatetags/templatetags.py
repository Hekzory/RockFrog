from django import template

register = template.Library()

@register.filter
def parent_comments(comments):
	return comments.filter(parent__isnull=True)

@register.simple_tag
def can_plus(article, user):
	return article.can_plus_article(user)

@register.simple_tag
def can_plus_comment(comment, user):
	return comment.can_plus(user)

@register.simple_tag
def can_comment(article, user):
	if not user.is_authenticated:
		return False
	if article.__class__.__name__ != "PersonalArticle":
		if not article.group.can_see_group(user):
			return False
	return True

@register.simple_tag
def update_counter(value):
    counter = value + 1
    return counter

@register.filter
def class_name(value):
    return value.__class__.__name__
