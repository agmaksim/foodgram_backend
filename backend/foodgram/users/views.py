from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.serializers import (CustomUserCreateSerializer,
                                 CustomUserSerializer, FollowSerializer)

from .models import CustomUser, Follow
from .pagination import LimitPageNumberPagination

USERNAME_ALREADY_EXISTS = 'Такой username уже есть, пробуйте другой'
EMAIL_ALREADY_EXTST = 'Такой email уже есть, пробуйте другой'
ERROR_SET_PASSWORD = 'Пароль менять нельзя'


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [permissions.AllowAny, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'subscribe':
            return FollowSerializer
        return CustomUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        try:
            user = CustomUser.objects.get(
                username=username,
                email=email)
        except CustomUser.DoesNotExist:
            if CustomUser.objects.filter(username=username).exists():
                return Response(
                    USERNAME_ALREADY_EXISTS,
                    status=status.HTTP_400_BAD_REQUEST
                )
            if CustomUser.objects.filter(email=email).exists():
                return Response(
                    EMAIL_ALREADY_EXTST,
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
    )
    def users_profile(self, request):
        user = get_object_or_404(
            CustomUser,
            username=request.user.username
        )
        serializer = self.get_serializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data.get('new_password')
        )
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['POST', 'DELETE'],
            url_path=r'(?P<id>\d+)/subscribe',
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        if user == author:
            return Response(
                'Нельзя подписаться на себя!',
                status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == 'DELETE':
            object = Follow.objects.filter(
                author=author, user=user).first()
            if object is None:
                return Response(
                    'Вы не подписаны на этого пользователя!',
                    status=status.HTTP_400_BAD_REQUEST,
                    )
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if Follow.objects.filter(author=author, user=user).exists():
            return Response(
                'Вы уже подписаны на этого пользователя!',
                status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
        )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
