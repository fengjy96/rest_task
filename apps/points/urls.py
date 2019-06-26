from django.urls import path, include
from rest_framework import routers
from points.views import points
from points.views.points import ProjectPointsViewSet

router = routers.DefaultRouter()
router.register('projectpoints', ProjectPointsViewSet, basename='project_points')


urlpatterns = [
    # API
    path(r'api/v1/', include(router.urls)),
    #积分分配
    path(r'api/v1/points/assignment', points.PointsAssignmentViewSet.as_view(), name='points_assignment'),
    # 查积分
    path(r'api/v1/points', points.UserPointsViewSet.as_view(), name='points'),

]
