from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from os import urandom
from re import compile as re_compile


VERSION_REGEX = re_compile(r"^\d+[.\d]*(?<!\.)$")


app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(32).hex()
api = Api(app)


class VersionChecker(Resource):
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

    def _check_versions(self, version_1: str, version_2: str) -> str:
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
        if res == "equal":
            res = "equal to"
        return f"{version_1} is {res} {version_2}"

    def get(self):
        args = self.parser.parse_args()
        ver_1 = args.get("ver_1")
        ver_2 = args.get("ver_2")
        if VERSION_REGEX.match(ver_1) and VERSION_REGEX.match(ver_2):
            return {"result": self._check_versions(ver_1, ver_2)}
        abort(400, message="Invalid Version Number Format")


api.add_resource(VersionChecker, "/api/v1/version_checker")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=False)
