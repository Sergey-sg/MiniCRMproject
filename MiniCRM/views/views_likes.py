from django.shortcuts import redirect
from django.views import View

from ..models import Company, Message, CompanyLikes, CompanyDisLike, MessageLike, MessageDisLike


class AddLikeView(View):
    """
    Adds likes
    """
    def post(self, *args, **kwargs):
        if 'company_id' in self.request.POST:
            obj_id = self.request.POST.get('company_id')
            obj_inst = Company.objects.get(id=obj_id)
            like = CompanyLikes
            dislike = CompanyDisLike
        else:
            obj_id = self.request.POST.get('message_id')
            obj_inst = Message.objects.get(id=obj_id)
            like = MessageLike
            dislike = MessageDisLike
        try:
            if 'company_id' in self.request.POST:
                obj_like_inst = like.objects.get(company=obj_inst, liked_by=self.request.user)
                obj_dislike = dislike.objects.get(company=obj_inst, disliked_by=self.request.user)
            else:
                obj_like_inst = like.objects.get(message=obj_inst, liked_by=self.request.user)
                obj_dislike = dislike.objects.get(message=obj_inst, disliked_by=self.request.user)
            obj_like_inst.like = True
            obj_like_inst.save()
            obj_dislike.dislike = False
            obj_dislike.save()
        except Exception:
            if 'company_id' in self.request.POST:
                obj_like = like(company=obj_inst, liked_by=self.request.user, like=True)
                obj_dislike = dislike(company=obj_inst, disliked_by=self.request.user, dislike=False)
            else:
                obj_like = like(message=obj_inst, liked_by=self.request.user, like=True)
                obj_dislike = dislike(message=obj_inst, disliked_by=self.request.user, dislike=False)
            obj_like.save()
            obj_dislike.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class AddDisLikeView(View):
    """
    Adds dislikes.
    """
    def post(self, *args, **kwargs):
        if 'company_id' in self.request.POST:
            obj_id = self.request.POST.get('company_id')
            obj_inst = Company.objects.get(id=obj_id)
            like = CompanyLikes
            dislike = CompanyDisLike
        else:
            obj_id = self.request.POST.get('message_id')
            obj_inst = Message.objects.get(id=obj_id)
            like = MessageLike
            dislike = MessageDisLike
        try:
            if 'company_id' in self.request.POST:
                obj_like_inst = like.objects.get(company=obj_inst, liked_by=self.request.user)
                obj_dislike = dislike.objects.get(company=obj_inst, disliked_by=self.request.user)
            else:
                obj_like_inst = like.objects.get(message=obj_inst, liked_by=self.request.user)
                obj_dislike = dislike.objects.get(message=obj_inst, disliked_by=self.request.user)
            obj_like_inst.like = False
            obj_like_inst.save()
            obj_dislike.dislike = True
            obj_dislike.save()
        except Exception:
            if 'company_id' in self.request.POST:
                obj_like = like(company=obj_inst, liked_by=self.request.user, like=False)
                obj_dislike = dislike(company=obj_inst, disliked_by=self.request.user, dislike=True)
            else:
                obj_like = like(message=obj_inst, liked_by=self.request.user, like=False)
                obj_dislike = dislike(message=obj_inst, disliked_by=self.request.user, dislike=True)
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
