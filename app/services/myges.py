from urllib.parse import urlparse, parse_qs
import requests
import http.client
import json

CLIENT_ID = "skolae-app"
OAUTH_AUTHORIZE_URL = f"https://authentication.kordis.fr/oauth/authorize?client_id={CLIENT_ID}&response_type=token"

class myges:
    def __init__(self,LOGIN,PASSWORD) -> None:
        self.LOGIN = LOGIN
        self.PASSWORD = PASSWORD

    def get_access_token(self) -> str:
        response = requests.get(
            url=OAUTH_AUTHORIZE_URL,
            auth=(self.LOGIN, self.PASSWORD),
            allow_redirects=False,
        )

        if response.status_code == 401:
            raise Exception("Wrong credentials")

        access_token = self.extract_access_token(response.headers)

        return access_token
    
    def extract_access_token(self, headers) -> str:
        location = headers.get("Location")

        if not location:
            raise Exception("Location header not found")

        location_url = urlparse(location)

        if not location_url.fragment:
            raise Exception("Impossible to extract fragment")

        query_params = parse_qs(location_url.fragment)
        access_token = query_params.get("access_token")

        if not access_token:
            raise Exception("Impossible to extract access token")

        return access_token[0]

    def get_grades(self) -> dict:
        access_token = self.get_access_token()

        conn = http.client.HTTPSConnection("api.kordis.fr")
        payload = ''
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        conn.request("GET", "/me/2023/grades", payload, headers)
        res = conn.getresponse()
        data = res.read().decode()
        return json.loads(data).get('result')