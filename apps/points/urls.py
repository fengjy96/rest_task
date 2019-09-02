from django.urls import path, include
from rest_framework import routers
from points.views import points
from points.views.points import ProjectPointsViewSet

router = routers.DefaultRouter()
router.register('projectpoints', ProjectPointsViewSet, basename='project_points')


urlpatterns = [
    # API
    path(r'', include(router.urls)),
    #积分分配
    path(r'points/assignment', points.PointsAssignmentViewSet.as_view(), name='points_assignment'),
    # 查积分
    path(r'points', points.UserPointsViewSet.as_view(), name='points'),
    # 查剩余积分
    path(r'project/leftpoints', points.ProjectPointsExViewSet.as_view(), name='project_points_ex'),

]
