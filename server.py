"""
Author: Maneesh Divana <maneeshd77@gmail.com>
Date  : Feb-13-2020

REST API using FastAPI to check if one version number is
"before", "equal" or "after" the other version number.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse
from re import compile as re_compile


VERSION_REGEX = re_compile(r"^\d+[.\d]*(?<!\.)$")


async def check_versions(version_1: str, version_2: str) -> int:
    """Checks if 1st version number is "before",
    "equal" or "after" the 2nd version number

    :param version_1: Version Number 1
    :type version_1: str

    :param version_2: Version Number 2
    :type version_2: str

    :return: -1 for "before" or 0 for "equal" or 1 for "after"
    :rtype: int
    """
    ver_1_list = [int(c) for c in version_1.split(".") if c.isdigit()]
    ver_2_list = [int(c) for c in version_2.split(".") if c.isdigit()]
    v1_len = len(ver_1_list)
    v2_len = len(ver_2_list)
    n = min(v1_len, v2_len)
    res = 0
    for i in range(n):
        if ver_1_list[i] == ver_2_list[i]:
            res = 0
        elif ver_1_list[i] > ver_2_list[i]:
            res = 1
            break
        else:
            res = -1
            break
    if res == 0:
        if v2_len > v1_len and any(ver_2_list[v1_len:]):
            res = -1
        elif v1_len > v2_len and any(ver_1_list[v2_len:]):
            res = 1
    return res


class SuccessMessage(BaseModel):
    result: str


class ErrorMessage(BaseModel):
    message: str


api = FastAPI()


STR_MAP = {-1: "before", 0: "equal to", 1: "after"}


@api.get(
    "/api/v1/version_checker/",
    response_model=SuccessMessage,
    responses={400: {"model": ErrorMessage}},
    status_code=200,
    description="Checks if 1st version number is 'before', 'equal' or 'after' 2nd version number",
)
async def version_checker(ver_1: str, ver_2: str):
    if not VERSION_REGEX.match(ver_1) or not VERSION_REGEX.match(ver_2):
        return JSONResponse(
            status_code=400, content={"message": "Invalid Version Number Format"}
        )
    key = await check_versions(ver_1, ver_2)
    return {"result": f"{ver_1} is {STR_MAP.get(key)} {ver_2}"}


@api.get(
    "/",
    response_description="Redirects to Swagger UI API Documentation",
    response_class=RedirectResponse,
    status_code=301,
    name="API Doc (Swagger)",
)
async def index():
    return RedirectResponse("/docs", status_code=301)


@api.get(
    "/api/v1/",
    response_description="Redirects to Redoc API Documentation",
    response_class=RedirectResponse,
    status_code=301,
    name="API Doc (Redoc)",
)
async def api_index():
    return RedirectResponse("/redoc", status_code=301)
