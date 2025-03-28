import connexion
import six

from swagger_server.models.login_registration_request import LoginRegistrationRequest  # noqa: E501
from swagger_server.utils import user_authentication
from swagger_server.controllers import authorization_controller

import logging
def authentication_login(body=None):  # noqa: E501
    """Login with a username and password.

     # noqa: E501

    :param body: Registration method to login
    :type body: dict | bytes

    :rtype: None
    """

    logging.warning("Authenticating for user ["+body.get('username')+"]")

    if connexion.request.is_json:

        # logging.warning("Authentication is json!!!")
        body = LoginRegistrationRequest.from_dict(connexion.request.get_json())  # noqa: E501
        # logging.warning(body)
        if body.username is not None and body.password is not None:
            user = body.to_dict()
            try:
                # logging.warning("into try is json!!!")
                user_id=user_authentication.validate_user(user["username"], user["password"])
                # logging.warning(user_id)

                if user_id is not None:

                    #should generate and store the token!
                    token=authorization_controller.generate_token(str(user_id)+"_/_"+user["username"])

                    user_authentication.update_user_info(identifier="username",value_id=user["username"],
                                                         type_input="token", value_input=token)


                    #should register this token to database!
                    auth_response={}
                    auth_response["info"]="User authorized (for the next 2 hours)"
                    auth_response["token"]=token
                    #return "User authorized (for the next 10 minutes), Token: " + token
                    logging.info("User successfully authenticated")
                    return auth_response
                else:
                    logging.warning("User not authorized")
                    return "User not authorized"

            except Exception as ce_:
                return ce_
        else:
            return "Wrong request. Please provide the required info for logging"

