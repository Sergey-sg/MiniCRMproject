from django.shortcuts import redirect
from django.views import View

from ..models import Company, Message, User, CompanyLikes, CompanyDisLike, MessageLike, MessageDisLike


class AddLikeView(View):
    """
    Adds likes of company.
    """
    def post(self, request, *args, **kwargs):
        company_id = int(request.POST.get('company_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = request.META.get('HTTP_REFERER')
        user_inst = User.objects.get(id=user_id)
        company_inst = Company.objects.get(id=company_id)
        try:
            company_like_inst = CompanyLikes.objects.get(company=company_inst, liked_by=user_inst)
            company_like_inst.like = True
            company_like_inst.save()
            company_dislike = CompanyDisLike.objects.get(company=company_inst, disliked_by=user_inst)
            company_dislike.dislike = False
            company_dislike.save()
        except Exception as e:
            company_like = CompanyLikes(company=company_inst,
                                        liked_by=user_inst,
                                        like=True
                                        )
            company_like.save()
            company_dislike = CompanyDisLike(company=company_inst, disliked_by=user_inst, dislike=False)
            company_dislike.save()
        return redirect(url_form)


class AddDisLikeView(View):
    """
    Adds dislikes of company.
    """
    def post(self, request, *args, **kwargs):
        company_id = int(request.POST.get('company_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = request.META.get('HTTP_REFERER')
        user_inst = User.objects.get(id=user_id)
        company_inst = Company.objects.get(id=company_id)
        try:
            company_dislike_inst = CompanyDisLike.objects.get(company=company_inst, disliked_by=user_inst)
            company_dislike_inst.dislike = True
            company_dislike_inst.save()
            company_like = CompanyLikes.objects.get(company=company_inst, liked_by=user_inst)
            company_like.like = False
            company_like.save()
        except Exception as e:
            company_dislike = CompanyDisLike(
                company=company_inst,
                disliked_by=user_inst,
                dislike=True
                )
            company_dislike.save()
            company_like = CompanyLikes(company=company_inst, liked_by=user_inst, like=False)
            company_like.save()
        return redirect(url_form)


class RemoveLikeView(View):
    """
    Remove likes of company
    """

    def post(self, request, *args, **kwargs):
        company_likes_id = int(request.POST.get('company_likes_id'))
        url_form = request.META.get('HTTP_REFERER')
        user_id = int(request.POST.get('user_id'))
        company_like = CompanyLikes.objects.get(id=company_likes_id)
        company_id = company_like.company
        company_dislike_id = CompanyDisLike.objects.get(company=company_id, disliked_by=user_id).pk
        company_dislike = CompanyDisLike.objects.get(id=company_dislike_id)
        company_like.delete()
        company_dislike.delete()
        return redirect(url_form)


class RemoveDisLikeView(View):
    """
    Remove dislikes of company
    """

    def post(self, request, *args, **kwargs):
        company_dislikes_id = int(request.POST.get('company_dislikes_id'))
        url_form = request.META.get('HTTP_REFERER')
        company_dislike = CompanyDisLike.objects.get(id=company_dislikes_id)
        company_id = company_dislike.company_id
        manager_id = company_dislike.disliked_by
        company_like = CompanyLikes.objects.get(company=company_id, liked_by=manager_id)
        company_like.delete()
        company_dislike.delete()
        return redirect(url_form)


class AddMessageLikeView(View):
    """
    Adds likes of message.
    """
    def post(self, request, *args, **kwargs):
        message_id = int(request.POST.get('message_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = request.META.get('HTTP_REFERER')
        user_inst = User.objects.get(id=user_id)
        message_inst = Message.objects.get(id=message_id)
        try:
            message_like_inst = MessageLike.objects.get(message=message_inst, liked_by=user_inst)
            message_like_inst.like = True
            message_like_inst.save()
            message_dislike = MessageDisLike.objects.get(message=message_inst, disliked_by=user_inst)
            message_dislike.dislike = False
            message_dislike.save()
        except Exception as e:
            message_like = MessageLike(message=message_inst, liked_by=user_inst, like=True)
            message_like.save()
            message_dislike = MessageDisLike(message=message_inst, disliked_by=user_inst, dislike=False)
            message_dislike.save()
        return redirect(url_form)


class AddMessageDisLikeView(View):
    """
    Adds dislikes of message.
    """
    def post(self, request, *args, **kwargs):
        message_id = int(request.POST.get('message_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = request.META.get('HTTP_REFERER')
        user_inst = User.objects.get(id=user_id)
        message_inst = Message.objects.get(id=message_id)
        try:
            message_dislike_inst = MessageDisLike.objects.get(message=message_inst, disliked_by=user_inst)
            message_dislike_inst.dislike = True
            message_dislike_inst.save()
            message_like = MessageLike.objects.get(message=message_inst, liked_by=user_inst)
            message_like.like = False
            message_like.save()
        except Exception as e:
            message_dislike = MessageDisLike(message=message_inst, disliked_by=user_inst, dislike=True)
            message_dislike.save()
            message_like = MessageLike(message=message_inst, liked_by=user_inst, like=False)
            message_like.save()
        return redirect(url_form)


class RemoveMessageLikeView(View):
    """
    Remove likes of Message
    """
    def post(self, request, *args, **kwargs):
        message_likes_id = int(request.POST.get('message_likes_id'))
        url_form = request.META.get('HTTP_REFERER')
        user_id = int(request.POST.get('user_id'))
        message_like = MessageLike.objects.get(id=message_likes_id)
        message_id = message_like.message
        message_dislike_id = MessageDisLike.objects.get(message=message_id, disliked_by=user_id).pk
        message_dislike = MessageDisLike.objects.get(id=message_dislike_id)
        message_like.delete()
        message_dislike.delete()
        return redirect(url_form)


class RemoveMessageDisLikeView(View):
    """
    Remove dislikes of company
    """
    def post(self, request, *args, **kwargs):
        message_dislikes_id = int(request.POST.get('message_dislikes_id'))
        url_form = request.META.get('HTTP_REFERER')
        message_dislike = MessageDisLike.objects.get(id=message_dislikes_id)
        message_id = message_dislike.message_id
        manager_id = message_dislike.disliked_by
        message_like = MessageLike.objects.get(message=message_id, liked_by=manager_id)
        message_like.delete()
        message_dislike.delete()
        return redirect(url_form)
