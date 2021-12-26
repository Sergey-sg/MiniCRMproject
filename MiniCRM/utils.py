from MiniCRM.models import Company, CompanyLikes, CompanyDisLike, Message, MessageLike, MessageDisLike


class LikeMixins:

    def get_like_dislike(self, request):
        if 'company_id' in request.POST:
            obj = Company.objects.get(id=request.POST.get('company_id'))
            like = CompanyLikes
            dislike = CompanyDisLike
        else:
            obj = Message.objects.get(id=request.POST.get('message_id'))
            like = MessageLike
            dislike = MessageDisLike
        try:
            if 'company_id' in request.POST:
                obj_like = like.objects.get(company=obj, liked_by=request.user)
                obj_dislike = dislike.objects.get(company=obj, disliked_by=request.user)
            else:
                obj_like = like.objects.get(message=obj, liked_by=request.user)
                obj_dislike = dislike.objects.get(message=obj, disliked_by=request.user)
        except Exception:
            if 'company_id' in request.POST:
                obj_like = like(company=obj, liked_by=request.user)
                obj_dislike = dislike(company=obj, disliked_by=request.user)
            else:
                obj_like = like(message=obj, liked_by=request.user)
                obj_dislike = dislike(message=obj, disliked_by=request.user)
        return {'obj_like': obj_like, 'obj_dislike': obj_dislike}
