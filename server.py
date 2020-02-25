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


async def check_versions(version_1: str, version_2: str) -> str:
    """Checks if 1st version number is "before",
    "equal" or "after" the 2nd version number

    :param version_1: Version Number 1
    :type version_1: str

    :param version_2: Version Number 2
    :type version_2: str

    :return: "before" or "equal" or "after"
    :rtype: str
    """
    ver_1_list = [int(c) for c in version_1.split(".") if c.isdigit()]
    ver_2_list = [int(c) for c in version_2.split(".") if c.isdigit()]
    v1_len = len(ver_1_list)
    v2_len = len(ver_2_list)
    n = min(v1_len, v2_len)
    res = None
    for i in range(n):
        if ver_1_list[i] == ver_2_list[i]:
            res = "equal"
        elif ver_1_list[i] > ver_2_list[i]:
            res = "after"
            break
        else:
            res = "before"
            break
    if res == "equal" and v2_len > v1_len and any(ver_2_list[v1_len:v2_len]):
        res = "before"
    if res == "equal" and v1_len > v2_len and any(ver_1_list[v2_len:v1_len]):
        res = "after"
    if res == "equal":
        res = "equal to"
    return f"{version_1} is {res} {version_2}"


class SuccessMessage(BaseModel):
    result: str


class ErrorMessage(BaseModel):
    message: str


api = FastAPI()


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
    return {"result": await check_versions(ver_1, ver_2)}


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
