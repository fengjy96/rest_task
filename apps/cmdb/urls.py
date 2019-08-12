from django.urls import path, include
from rest_framework import routers

from cmdb.views import dict, scan, asset, connection, business, group, label


router = routers.SimpleRouter()
# 字典相关
router.register(r'dicts', dict.DictViewSet, basename="dicts")
# 扫描设备相关
router.register(r'scan/devices', scan.DeviceScanInfoViewSet, basename="scan_devices")
# 设备相关
router.register(r'devices', asset.DeviceInfoViewSet, basename="devices")
# 连接相关
router.register(r'connections', connection.ConnectionInfoViewSet, basename="connections")
# 业务相关
router.register(r'businesses', business.BusinessViewSet, basename="businesses")
# 组相关
router.register(r'groups', group.DeviceGroupViewSet, basename="groups")
# 标签相关
router.register(r'labels', label.LabelViewSet, basename="labels")

urlpatterns = [
    path(r'api/', include(router.urls)),
    # 获取字典树
    path(r'api/dict/tree/', dict.DictTreeView.as_view(), name='dict_tree'),
    # 扫描设置相关
    path(r'api/scan/setting/', scan.ScanSettingView.as_view(), name='scan_setting'),
    # 设备入库和扫描相关
    path(r'api/scan/excu/', scan.ScanExcuView.as_view(), name='scan_excu'),
    # 获取设备列表
    path(r'api/device/list/', asset.DeviceListView.as_view(), name='device_list'),
]
