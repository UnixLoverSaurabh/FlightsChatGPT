import json
import requests


class NewClientRequest:
    """Rest client model class used for requests."""

    def __init__(self, url, headers, body, requestType):
        self.url = url
        self.headers = headers
        self.body = body
        self.requestType = requestType
        self.ttl = 20

    def get_response(self):
        """ Rest interface to call APIs

        Args:
            self: Model class for request params
        Returns:
            (response, cookies, headers) for an api call
        """

        session = requests.session()
        session.verify = False
        # Disabling InsecureRequestWarning: `Unverified HTTPS request is being made`
        # requests.packages.urllib3.disable_warnings()

        # Initial value is None
        response = None
        session.headers = self.headers
        if "POST" == self.requestType:
            if isinstance(self.body, str):
                response = session.post(self.url, headers=self.headers, data=self.body, timeout=self.ttl)
                # response = session.post(self.url, data=self.body, timeout=timeout)
            else:
                response = session.post(self.url, headers=self.headers, data=json.dumps(self.body), timeout=self.ttl)
                # response = session.post(self.url, data=json.dumps(self.body), timeout=timeout)
        if "GET" == self.requestType:
            # response = session.get(self.url, headers=self.headers, timeout=self.ttl)
            response = session.get(self.url, timeout=self.ttl)

        return response
