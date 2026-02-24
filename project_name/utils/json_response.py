from rest_framework.response import Response


class DetailResponse(Response):
    def __init__(
        self,
        data=None,
        msg="success",
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        std_data = {"code": 2000, "data": data, "msg": msg}
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):
    def __init__(
        self,
        data=None,
        msg="error",
        code=400,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        std_data = {"code": code, "data": data, "msg": msg}
        super().__init__(std_data, status, template_name, headers, exception, content_type)
