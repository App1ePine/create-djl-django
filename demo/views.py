from rest_framework.decorators import api_view

from project_name.utils.json_response import DetailResponse, ErrorResponse

# Create your views here.
from .utils.demo_test import demo_test


@api_view(["GET"])
def demo_view(request):
    try:
        result = demo_test()
        return DetailResponse(result, msg="success")
    except Exception as error:
        return ErrorResponse({"error": f"获取数据失败: {error!s}"}, msg="error")
