from logging import getLogger

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError

from core.constants.global_constants import SourceEndpoint
from core.apps.users.models import User

logger = getLogger(__name__)


class Auth0Service(object):
    AUTH0_USER_CREATED_SUCCESSFULLY_STATUS_CODE = 201
    AUTH0_SUCCESSFUL_STATUS_CODE = 200

    def __init__(self):
        self.access_token = self.get_access_token()

    def get_access_token(self):
        data = {
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "audience": f"{settings.AUTH0_API_ENDPOINT_URL}/",  # watch the slash
            "grant_type": "client_credentials"
        }
        response = requests.post(settings.AUTH0_FETCH_TOKEN_API_URL, json=data)
        if response.status_code == Auth0Service.AUTH0_SUCCESSFUL_STATUS_CODE:
            return response.json().get("access_token")

        logger.error(f"Error while fetching access token from auth, response: {response.status_code}, {response.text}")

    def create_auth0_user(self, user: User, info, raw_password: str, registered_user=False):
        """
        API docs for this endpoint can be found here
        https://auth0.com/docs/api/management/v2#!/Users/post_users
        :param user:
        :param raw_password:
        :param registered_user:
        :return:
        """
        logger.info(f"Auth0Service: creating new user {user}")
        data = {
            "email": user.email,
            "user_metadata": info.get('user_metadata', {}),
            "blocked": False,
            "email_verified": False if registered_user else True,
            "app_metadata": {},
            "user_id": f"{user.id}",
            "connection": "Username-Password-Authentication",
            "password": raw_password,
            "verify_email": True if registered_user else False,
            "name": user.username,
            "nickname": user.username
        }
        response = requests.post(url=f"{settings.AUTH0_API_ENDPOINT_URL}/users", json=data, headers={
            "Authorization": f"Bearer {self.access_token}"
        })
        if response.status_code != Auth0Service.AUTH0_USER_CREATED_SUCCESSFULLY_STATUS_CODE:
            logger.error(f"Failed to create new user for auth0 , response: {response.status_code}, {response.text}")

        logger.info(f"Auth0Service: user {user} was created successfully")

    def fetch_auth0_user(self, email) -> dict:
        """
        API DOCs here https://auth0.com/docs/api/management/v2#!/Users/get_users,
        sample response:
            [
                {
                    "created_at": "2020-10-04T14:35:57.885Z",
                    "email": "fmsalam@asaltech.com",
                    "email_verified": false,
                    "identities": [
                        {
                            "user_id": "5f79ddcda511fe006b79ba49",
                            "provider": "auth0",
                            "connection": "Username-Password-Authentication",
                            "isSocial": false
                        }
                    ],
                    "name": "fmsalam@asaltech.com",
                    "nickname": "fmsalam",
                    "picture": "https://s.gravatar.com/avatar/0023fa27909fa0a0236747bb72669794?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Ffm.png",
                    "updated_at": "2020-12-09T09:17:56.389Z",
                    "user_id": "auth0|5f79ddcda511fe006b79ba49",
                    "last_login": "2020-12-09T09:17:56.389Z",
                    "last_ip": "213.6.248.58",
                    "logins_count": 492
                }
        ]
        """
        logger.info(f"Auth0Service: fetching User {email} from auth0.")
        response = requests.get(url=f"{settings.AUTH0_API_ENDPOINT_URL}/users?q=email:{email}",
                                headers={
                                    "Authorization": f"Bearer {self.access_token}", 'content-type': "application/json"
                                })
        logger.info(
            f"Response from calling Auth0Service: fetching User {email} from auth0. \n {response} {response.text}")
        if not response or response.status_code != Auth0Service.AUTH0_SUCCESSFUL_STATUS_CODE:
            logger.error(
                f"Failed to fetch user for auth0 , response: {response.status_code}, {response.text}")
            raise Exception("Failed to fetch user from auth platform")

        logger.info(f"Auth0Service: User {email} info was fetched successfully.")
        searched_users_list = response.json()
        if len(searched_users_list) >= 1:
            return searched_users_list[0]

    def change_auth0_user_password(self, user: User, new_password: str):
        """
        API Docs here: https://auth0.com/docs/api/management/v2#!/Users/patch_users_by_id
        https://auth0.com/docs/connections/database/password-change#using-the-management-api
        """
        data = {
            "connection": "Username-Password-Authentication",
            "password": new_password,
        }
        auth0_user_dict = self.fetch_auth0_user(email=user.email)
        if not auth0_user_dict or not auth0_user_dict.get("user_id"):
            logger.error(
                f"Failed to change user password for auth0 [User was not fetched successfully from AUTH0]."
                f" user email {user.email}")
            return
        auth0_user_id = auth0_user_dict['user_id']
        logger.info(f"Calling Auth0 API to change password for user: {user.email}, auth0_user_id: {auth0_user_id}")
        response = requests.patch(url=f"{settings.AUTH0_API_ENDPOINT_URL}/users/{auth0_user_id}", json=data, headers={
            "Authorization": f"Bearer {self.access_token}", 'content-type': "application/json"
        })
        logger.info(f"Response from calling Auth0 API to change password for user:"
                    f" {user.email}, auth0_user_id: {auth0_user_id}"
                    f"is: {response}, {response.text}")
        if not response or response.status_code != Auth0Service.AUTH0_SUCCESSFUL_STATUS_CODE:
            logger.error(
                f"Failed to change user password for auth0 , response: {response.status_code}, {response.text}")

        logger.info(f"Auth0Service: User {user} password has been changed successfully")

    def change_auth0_user_userinfo(self, user: User, info, source_endpoint: SourceEndpoint = SourceEndpoint.ADMIN_PANEL):
        """
        API Docs here: https://auth0.com/docs/api/management/v2#!/Users/patch_users_by_id
        https://auth0.com/docs/connections/database/password-change#using-the-management-api
        """
        auth0_user_dict = self.fetch_auth0_user(email=user.email)

        if not auth0_user_dict or not auth0_user_dict.get("user_id"):
            logger.error(
                f"Failed to change user information for auth0 [User was not fetched successfully from AUTH0]."
                f" user email {user.email}")
            return

        is_username_and_password = not auth0_user_dict["user_id"].startswith("google")

        data = {}
        if is_username_and_password:
            data.update({
                "connection": "Username-Password-Authentication",
                "nickname": info['username']
            })

        if source_endpoint == SourceEndpoint.ADMIN_PANEL:
            data.update({"user_metadata": info['user_metadata']})
            if is_username_and_password:
                data.update({"name": f"{info['first_name']} {info['last_name']}"})

        auth0_user_id = auth0_user_dict['user_id']

        logger.info(f"Calling Auth0 API to change information for user: {user.email}, auth0_user_id: {auth0_user_id}")
        response = requests.patch(url=f"{settings.AUTH0_API_ENDPOINT_URL}/users/{auth0_user_id}", json=data, headers={
            "Authorization": f"Bearer {self.access_token}", 'content-type': "application/json"
        })
        logger.info(f"Response from calling Auth0 API to change information for user:"
                    f" {user.email}, auth0_user_id: {auth0_user_id}"
                    f"is: {response}, {response.text}")
        if not response or response.status_code != Auth0Service.AUTH0_SUCCESSFUL_STATUS_CODE:
            logger.error(
                f"Failed to change user's information for auth0 , response: {response.status_code}, {response.text}")
        logger.info(f"Auth0Service: User {user} information has been changed successfully")

    def verify_user_email(self, email: str, identity=None):
        """
        API docs for this endpoint can be found here
        https://auth0.com/docs/api/management/v2#!/Tickets/post_email_verification
        :param email:
        :param identity:
        :return:
        """
        user = self.fetch_auth0_user(email)
        if not user:
            raise ValidationError("invalid user")

        id_from_identity = f"{identity.get('provider')}|{identity.get('user_id')}" if identity else None
        user_id = user['user_id'] or id_from_identity

        if not user_id:
            raise ValidationError("invalid user_id")

        logger.info(f"Auth0Service: send user verification email of user_id: {user_id}")
        data = {
            "user_id": f"{user_id}",
        }
        if identity:
            data["identity"] = identity

        response = requests.post(url=f"{settings.AUTH0_API_ENDPOINT_URL}/jobs/verification-email", json=data, headers={
            "Authorization": f"Bearer {self.access_token}"
        })
        if response.status_code != Auth0Service.AUTH0_USER_CREATED_SUCCESSFULLY_STATUS_CODE:
            logger.error(
                f"Failed to send verification email on auth0 , response: {response.status_code}, {response.text}")

        logger.info(f"Auth0Service: email verification of user_id {user_id} was sent successfully")
        return response


