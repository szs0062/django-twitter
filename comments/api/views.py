from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from utils.permissions import IsObjectOwner
from utils.decorators import required_params
from inbox.services import NotificationService
from ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现list，create，update， destroy的方法
    不实现retrieve（查询单个comment）的方法，因为没有这个需求
    """
    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()
    filterset_fields = ('tweet_id',)

    # POST /api/comments/ -> create
    # GET /api/comments/ -> list
    # GET /api/comments/1/ -> retrieve
    # DELETE /api/comments/1/ -> destroy
    # PATCH /api/comments/1/ -> partial_update
    # PUT /api/comments/1/ -> update
    def get_permissions(self):
        # 注意要加用AllowAny() / IsAuthenticated()实例化对象
        # 而不是AllowAny / IsAuthenticated这样只是一个类名
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'destroy']:
            return [IsAuthenticated(), IsObjectOwner()]
        return [AllowAny()]

    @required_params(params=['tweet_id'])
    @method_decorator(ratelimit(key='user', rate='1/s', method='GET', block=True))
    def list(self, request, *arg, **kwargs):
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset).prefetch_related('user').order_by("created_at")
        serializer = CommentSerializer(
            comments,
            context={'request': request},
            many=True, )
        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

    @method_decorator(ratelimit(key='user', rate='3/s', method='POST', block=True))
    def create(self, request, *arg, **kwargs):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # 注意这里必须加'data='来指定参数是传给data的
        # 因为默认的第一个参数是instance
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        # save 方法会触发serializer里的create方法，点进save的具体实现里可以看到
        comment = serializer.save()
        NotificationService.send_comment_notification(comment)
        return Response(
            CommentSerializer(comment, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    @method_decorator(ratelimit(key='user', rate='3/s', method='POST', block=True))
    def update(self, request, *args, **kwargs):
        # get_object是DRF包装的一个函数，会在找不到的时候raise 404 error
        # 所以这里无需做额外判断
        comment = self.get_object()
        serializer = CommentSerializerForUpdate(
            instance=comment,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input'
            }, status=status.HTTP_400_BAD_REQUEST)

        # save方法会触发serializer里面的update方法，点进save的具体实现里可以考到
        # save是根据instance参数有没有传来决定是触发create还是create
        comment = serializer.save()
        return Response(
            CommentSerializer(comment, context={'request': request}).data,
            status=status.HTTP_200_OK,
        )

    @method_decorator(ratelimit(key='user', rate='5/s', method='POST', block=True))
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        # DRF 里默认destroy返回的是status code = 204 no content
        # 这里return了 success=True 更直观的让前端去做判断，所以return 200更合适
        return Response({'success': True}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # <HOMEWORK 1> 通过某个 query 参数 with_all_comments 来决定是否需要带上所有 comments
        # <HOMEWORK 2> 通过某个 query 参数 with_preview_comments 来决定是否需要带上前三条 comments
        serializer = CommentSerializer(
            self.get_object(),
            context={'request': request},
        )
        return Response(serializer.data)
