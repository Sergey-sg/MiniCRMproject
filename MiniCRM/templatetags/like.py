from django import template
from ..models import CompanyLikes, MessageLike

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, company_id):
    request = context['request']
    try:
        company_likes = CompanyLikes.objects.get(company_id=company_id, liked_by=request.user.id).like
    except Exception as e:
        company_likes = False
    return company_likes


@register.simple_tag()
def count_likes(company_id):
    return CompanyLikes.objects.filter(company_id=company_id, like=True).count()


@register.simple_tag(takes_context=True)
def company_likes_id(context, company_id):
    request = context['request']
    return CompanyLikes.objects.get(company_id=company_id, liked_by=request.user.id).id


@register.simple_tag(takes_context=True)
def is_liked_message(context, message_id):
    request = context['request']
    try:
        message_likes = MessageLike.objects.get(message=message_id, liked_by=request.user.id).like
    except Exception as e:
        message_likes = False
    return message_likes


@register.simple_tag(takes_context=True)
def message_likes_id(context, message_id):
    request = context['request']
    return MessageLike.objects.get(message=message_id, liked_by=request.user.id).id
