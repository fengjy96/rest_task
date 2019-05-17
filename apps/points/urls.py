from django.urls import path, include

from rest_framework import routers

from points.views import points
from points.views.points import PointsAssignmentView

router = routers.DefaultRouter()
#router.register('points', PointsAssignmentView, basename='user_points')


urlpatterns = [
    # API
    #path(r'api/v1/', include(router.urls)),
    #积分分配
    path(r'api/v1/points/assignment', points.PointsAssignmentView.as_view(), name='points_assignment'),

]
