from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_config

# import model User
from ..models import User


@view_config(route_name="register", request_method="POST", renderer="json")
def register(request: Request):  # Register
    try:
        username = request.json_body["username"]
        password = request.json_body["password"]
        role = request.json_body["role"]
        if role == "":
            role = "user"
        users = request.dbsession.query(User).filter(User.username == username).first()
        if users is None:
            # password = User.set_password(setted_password=password)
            user = User(username=username, password=password, role=role)
            request.dbsession.add(user)
            # request.dbsession.flush()
            return Response(
                status=201,
                content_type="application/json",
                json={"message": "Register success!"},
            )
        else:
            return Response(
                status=400,
                content_type="application/json",
                json={"message": "Username already exist!"},
            )

    except DBAPIError:
        return Response(
            status=500,
            content_type="application/json",
            json={"message": "Internal server error!"},
        )


@view_config(route_name="login", request_method="POST", renderer="json")
def login(request: Request):  # Login
    try:
        username = request.json_body["username"]
        password = request.json_body["password"]
        user = request.dbsession.query(User).filter_by(username=username).first()
        if user is not None:
            if password == user.password:
                token = request.create_jwt_token(
                    user.id,
                    role=user.role,
                )
                return Response(
                    status=200,
                    content_type="application/json",
                    json={
                        "message": "Login success!",
                        "token": token,
                    },
                )
            else:
                return Response(
                    status=400,
                    content_type="application/json",
                    json={"message": "Wrong password!"},
                )
        else:
            return Response(
                status=400,
                content_type="application/json",
                json={"message": "User not found!"},
            )
    except DBAPIError:
        return Response(
            status=500,
            content_type="application/json",
            json={"message": "Internal server error!"},
        )


@view_config(route_name="logout", request_method="GET", renderer="json")
def logout(request: Request):  # Logout
    try:
        return Response(
            status=200,
            content_type="application/json",
            json={"message": "Logout success!"},
        )
    except DBAPIError:
        return Response(
            status=500,
            content_type="application/json",
            json={"message": "Internal server error!"},
        )


# @view_defaults(route_name="auth")
# class AuthView:
#     def __init__(self, request):
#         self.request: Request = request

#     def server_error(self):
#         return Response(
#             status=500,
#             content_type="application/json",
#             json={"message": "Internal server error!"},
#         )

#     @view_config(request_method="POST")
#     def login(self):  # Login
#         try:
#             username = self.request.json_body["username"]
#             password = self.request.json_body["password"]
#             user = (
#                 self.request.dbsession.query(User).filter_by(username=username).first()
#             )
#             if user is not None:
#                 if user.check_password(password):
#                     token = self.request.create_jwt_token(
#                         user.id,
#                         role=user.role,
#                     )
#                     return Response(
#                         status=200,
#                         content_type="application/json",
#                         json={
#                             "message": "Login success!",
#                             "token": token,
#                         },
#                     )
#                 else:
#                     return Response(
#                         status=400,
#                         content_type="application/json",
#                         json={"message": "Wrong password!"},
#                     )
#             else:
#                 return Response(
#                     status=400,
#                     content_type="application/json",
#                     json={"message": "User not found!"},
#                 )
#         except DBAPIError:
#             self.server_error()

#     @view_config(route_name="register", request_method="POST")
#     def register(self):  # Register
#         try:
#             username = self.request.json_body["username"]
#             password = self.request.json_body["password"]
#             user = (
#                 self.request.dbsession.query(User)
#                 .filter(User.username == username)
#                 .first()
#             )
#             if user is None:
#                 user = User(username=username, password=password, role="user")
#                 self.request.dbsession.add(user)
#                 return Response(
#                     status=201,
#                     content_type="application/json",
#                     json={"message": "Register success!"},
#                 )
#             else:
#                 return Response(
#                     status=400,
#                     content_type="application/json",
#                     json={"message": "Username already exist!"},
#                 )

#         except DBAPIError:
#             self.server_error()

#     @view_config(route_name="logout", request_method="GET")
#     def logout(self):  # Logout
#         try:
#             return Response(
#                 status=200,
#                 content_type="application/json",
#                 json={"message": "Logout success!"},
#             )
#         except DBAPIError:
#             self.server_error()
