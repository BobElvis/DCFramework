import urllib


class UrlHeaderGenerator(object):
    def __init__(self, endpoint, aws_signing_v4):
        self.__endpoint = endpoint
        self.__aws_signing_v4 = aws_signing_v4

    def __to_canonical_querystring(self, params):
        canonical_querystring = ""
        # parameters have to be sorted alphabetically for the signing part
        for param_key, param_value in sorted(params.items()):
            if canonical_querystring != "":
                canonical_querystring += "&"
            canonical_querystring += param_key + "=" + urllib.parse.quote(param_value)
        return canonical_querystring

    def generate(self, path, params, api_key, method, api_token=None):
        canonical_querystring = self.__to_canonical_querystring(params)
        headers = self.__aws_signing_v4.generate_headers(
            path, canonical_querystring, method
        )

        # 'host' header is added automatically by the Python 'requests' library.
        headers["Accept"] = "application/json"
        headers["Content-type"] = "application/json"
        headers["x-api-key"] = api_key

        # All endpoints require the API token, except the API token endpoint.
        if api_token:
            headers["x-dnbapi-jwt"] = api_token

        request_url = self.__endpoint + path + "?" + canonical_querystring
        return request_url, headers
