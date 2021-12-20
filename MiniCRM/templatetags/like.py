from django import template
from ..models import CompanyLikes, MessageLike, CompanyDisLike, MessageDisLike

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, company_id):
    request = context['request']
    try:
        company_likes = CompanyLikes.objects.get(company_id=company_id, liked_by=request.user.id).like
    except Exception as e:
        return False
    if company_likes:
        return True
    else:
        return False


@register.simple_tag(takes_context=True)
def is_disliked(context, company_id):
    request = context['request']
    try:
        company_dislikes = CompanyDisLike.objects.get(company_id=company_id, disliked_by=request.user.id).dislike
    except Exception as e:
        return False
    if company_dislikes:
        return True
    else:
        return False


@register.simple_tag()
def count_likes(company_id):
    return CompanyLikes.objects.filter(company_id=company_id, like=True).count()


@register.simple_tag()
def count_dislikes(company_id):
    return CompanyDisLike.objects.filter(company_id=company_id, dislike=True).count()


@register.simple_tag(takes_context=True)
def company_likes_id(context, company_id):
    request = context['request']
    return CompanyLikes.objects.get(company_id=company_id, liked_by=request.user.id).id


@register.simple_tag(takes_context=True)
def company_dislikes_id(context, company_id):
    request = context['request']
    return CompanyDisLike.objects.get(company_id=company_id, disliked_by=request.user.id).id


@register.simple_tag(takes_context=True)
def is_liked_message(context, message_id):
    request = context['request']
    try:
        message_likes = MessageLike.objects.get(message=message_id, liked_by=request.user.id).like
    except Exception as e:
        message_likes = False
    return message_likes


@register.simple_tag(takes_context=True)
def is_disliked_message(context, message_id):
    request = context['request']
    try:
        message_dislikes = MessageDisLike.objects.get(message_id=message_id, disliked_by=request.user.id).dislike
    except Exception as e:
        return False
    if message_dislikes:
        return True
    else:
        return False


@register.simple_tag(takes_context=True)
def message_likes_id(context, message_id):
    request = context['request']
    return MessageLike.objects.get(message=message_id, liked_by=request.user.id).id


@register.simple_tag(takes_context=True)
def message_dislikes_id(context, message_id):
    request = context['request']
    return MessageDisLike.objects.get(message_id=message_id, disliked_by=request.user.id).id


@register.simple_tag()
def count_likes_message(message_id):
    return MessageLike.objects.filter(message_id=message_id, like=True).count()


@register.simple_tag()
def count_dislikes_message(message_id):
    return MessageDisLike.objects.filter(message_id=message_id, dislike=True).count()
