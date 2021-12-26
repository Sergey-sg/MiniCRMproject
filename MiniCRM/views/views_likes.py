from django.shortcuts import redirect
from django.views import View

from ..models import CompanyLikes, CompanyDisLike, MessageLike, MessageDisLike
from ..utils import LikeMixins


class AddLikeView(LikeMixins, View):
    """
    Adds likes
    """
    def post(self, *args, **kwargs):
        like_dislike = self.get_like_dislike(self.request)
        obj_like = like_dislike['obj_like']
        obj_dislike = like_dislike['obj_dislike']
        obj_like.like = True
        obj_dislike.dislike = False
        obj_like.save()
        obj_dislike.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class RemoveLikeView(View):
    """
    Remove likes.
    """
    def post(self, *args, **kwargs):
        if 'company_likes_id' in self.request.POST:
            obj_likes_id = self.request.POST.get('company_likes_id')
            like = CompanyLikes
            dislike = CompanyDisLike
        else:
            obj_likes_id = self.request.POST.get('message_likes_id')
            like = MessageLike
            dislike = MessageDisLike
        obj_like = like.objects.get(id=obj_likes_id)
        if 'company_likes_id' in self.request.POST:
            obj_dislike = dislike.objects.get(company=obj_like.company, disliked_by=self.request.user)
        else:
            obj_dislike = dislike.objects.get(message=obj_like.message, disliked_by=self.request.user)
        obj_like.delete()
        obj_dislike.delete()
        return redirect(self.request.META.get('HTTP_REFERER'))


class AddDisLikeView(LikeMixins, View):
    """
    Adds dislikes.
    """
    def post(self, *args, **kwargs):
        like_dislike = self.get_like_dislike(self.request)
        obj_like = like_dislike['obj_like']
        obj_dislike = like_dislike['obj_dislike']
        obj_like.like = False
        obj_like.save()
        obj_dislike.dislike = True
        obj_dislike.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class RemoveDisLikeView(View):
    """
    Remove dislikes.
    """
    def post(self, *args, **kwargs):
        if 'company_dislikes_id' in self.request.POST:
            obj_dislikes_id = self.request.POST.get('company_dislikes_id')
            like = CompanyLikes
            dislike = CompanyDisLike
        else:
            obj_dislikes_id = self.request.POST.get('message_dislikes_id')
            like = MessageLike
            dislike = MessageDisLike
        obj_dislike = dislike.objects.get(id=obj_dislikes_id)
        if 'company_dislikes_id' in self.request.POST:
            obj_like = like.objects.get(company=obj_dislike.company, liked_by=self.request.user)
        else:
            obj_like = like.objects.get(message=obj_dislike.message, liked_by=self.request.user)
        obj_like.delete()
        obj_dislike.delete()
        return redirect(self.request.META.get('HTTP_REFERER'))
