from flask import Flask, render_template, escape
from flask_restful import Resource, Api, reqparse, abort
from os import urandom
from re import compile as re_compile


VERSION_REGEX = re_compile(r"^\d+[.\d]*(?<!\.)$")
HOST = "localhost"
PORT = 8000


app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(32).hex()
api = Api(app)


class VersionChecker(Resource):
    api_path = "/api/v1/version_checker"
    query_params = "ver_1=<version_number_1>&ver_2=<version_number_2>"

    str_map = {-1: "before", 0: "equal to", 1: "after"}

    parser = reqparse.RequestParser()
    parser.add_argument(
        "ver_1",
        type=str,
        required=True,
        help="ver_1 (Version Number 1) is Required as query parameter",
    )
    parser.add_argument(
        "ver_2",
        type=str,
        required=True,
        help="ver_2 (Version Number 2) is Required as query parameter",
    )

    def _check_versions(self, version_1: str, version_2: str) -> int:
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

    def get(self):
        """Handles the GET request to version_checker"""
        args = self.parser.parse_args()
        ver_1 = args.get("ver_1")
        ver_2 = args.get("ver_2")
        if VERSION_REGEX.match(ver_1) and VERSION_REGEX.match(ver_2):
            key = self._check_versions(ver_1, ver_2)
            return {"result": f"{ver_1} is {self.str_map.get(key)} {ver_2}"}
        abort(400, message="Invalid Version Number Format")


api.add_resource(VersionChecker, VersionChecker.api_path)


@app.route("/")
@app.route("/docs/")
@app.route("/redoc/")
@app.route("/api/v1/")
def index():
    return render_template(
        "index.html",
        host=HOST,
        port=PORT,
        api_path=VersionChecker.api_path,
        query_params=escape(VersionChecker.query_params),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, threaded=True, debug=False)
