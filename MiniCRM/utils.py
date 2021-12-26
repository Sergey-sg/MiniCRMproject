from MiniCRM.models import Company, CompanyLikes, CompanyDisLike, Message, MessageLike, MessageDisLike


class LikeMixin:

    def like_post(self, request):
        user = request.user
        if 'company_id' in request.POST:
            obj_id = request.POST.get('company_id')
            obj_inst = Company.objects.get(id=obj_id)
            like = CompanyLikes
            dislike = CompanyDisLike
        else:
            obj_id = request.POST.get('message_id')
            obj_inst = Message.objects.get(id=obj_id)
            like = MessageLike
            dislike = MessageDisLike
        try:
            if 'company_id' in request.POST:
                obj_like_inst = like.objects.get(company=obj_inst, liked_by=user)
                obj_dislike = dislike.objects.get(company=obj_inst, disliked_by=user)
            else:
                obj_like_inst = like.objects.get(message=obj_inst, liked_by=user)
                obj_dislike = dislike.objects.get(message=obj_inst, disliked_by=user)
            obj_like_inst.like = True
            obj_like_inst.save()
            obj_dislike.dislike = False
            obj_dislike.save()
        except Exception:
            if 'company_id' in request.POST:
                obj_like = like(company=obj_inst,
                                liked_by=user,
                                like=True
                                )
                obj_dislike = dislike(company=obj_inst,
                                      disliked_by=user,
                                      dislike=False)
            else:
                obj_like = like(message=obj_inst,
                                liked_by=user,
                                like=True
                                )
                obj_dislike = dislike(message=obj_inst,
                                      disliked_by=user,
                                      dislike=False)
            obj_like.save()
            obj_dislike.save()
        return request.META.get('HTTP_REFERER')
