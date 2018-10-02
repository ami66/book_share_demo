# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/23 15:25
@desc: 
"""

from django import template

from ..models import UserProfile, FollowUser

register = template.Library()


@register.simple_tag
def get_recommend_users():
    """
    获取推荐用户，测试阶段，仅获取部分用户
    :return:
    """
    users = UserProfile.objects.order_by('-date_joined')
    return users


@register.simple_tag
def check_is_following_user(request, user):
    is_following = False
    if request.user.is_authenticated and user:
        following_topics = FollowUser.objects.filter(user_from=request.user, user_to=user)
        if following_topics:
            is_following = True
    return is_following


