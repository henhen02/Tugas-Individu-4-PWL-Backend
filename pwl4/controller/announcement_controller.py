from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_defaults, view_config
from datetime import datetime

from ..models import Announcement


@view_defaults(route_name="announcement")
class AnnouncementView:
    def __init__(self, request):
        self.request: Request = request

    def server_error(self):  # Capek ngetik ulang terus, buat fungsi ajalah
        return Response(
            status=500,
            content_type="application/json",
            json={"message": "Internal server error!"},
        )

    @view_config(request_method="GET", permission="view")
    def get_all_announcements(self):  # Get all of announcements
        try:
            announcements = self.request.dbsession.query(Announcement).all()
            return Response(
                status=200,
                content_type="application/json",
                json={
                    "data": [
                        {
                            "id": announcement.id,
                            "title": announcement.title,
                            "content": announcement.content,
                            "created_at": str(announcement.created_at),
                        }
                        for announcement in announcements  # List Comprehension
                    ]
                },
            )
        except DBAPIError:
            self.server_error()

    @view_config(request_method="POST", permission="admin")
    def create_new_announcement(self):  # Create new announcement
        try:
            title = self.request.json_body["title"]
            content = self.request.json_body["content"]
            announcement = Announcement(title=title, content=content)
            self.request.dbsession.add(announcement)

            return Response(
                status=201,
                content_type="application/json",
                json={"message": "Success add new announcement"},
            )

        except DBAPIError:
            self.server_error()

    @view_config(route_name="announcement_id", request_method="GET", permission="view")
    def get_announcement_by_id(self):  # Get announcement by id
        try:
            id = self.request.matchdict["id"]
            announcement = (
                self.request.dbsession.query(Announcement).filter_by(id=id).first()
            )
            if announcement:
                return Response(
                    status=200,
                    content_type="application/json",
                    json={
                        "data": {
                            "id": announcement.id,
                            "title": announcement.title,
                            "content": announcement.content,
                            "created_at": str(announcement.created_at),
                        }
                    },
                )
            else:
                return Response(
                    status=404,
                    content_type="application/json",
                    json={"message": "Announcement not found!"},
                )
        except DBAPIError:
            self.server_error()

    @view_config(route_name="announcement_id", request_method="PUT", permission="admin")
    def update_announcement_by_id(self):  # Update announcement by id
        try:
            id = self.request.matchdict["id"]
            announcement = (
                self.request.dbsession.query(Announcement).filter_by(id=id).first()
            )
            if announcement:
                announcement.title = self.request.json_body["title"]
                announcement.content = self.request.json_body["content"]
                announcement.created_at = datetime.now()

                return Response(
                    status=200,
                    content_type="application/json",
                    json={"message": "Success update announcement!"},
                )
            else:
                return Response(
                    status=404,
                    content_type="application/json",
                    json={"message": "Announcement not found!"},
                )
        except DBAPIError:
            self.server_error()

    @view_config(
        route_name="announcement_id", request_method="DELETE", permission="admin"
    )
    def delete_announcement_by_id(self):  # Delete announcement by id
        try:
            id = self.request.matchdict["id"]
            announcement = (
                self.request.dbsession.query(Announcement).filter_by(id=id).first()
            )
            if announcement:
                self.request.dbsession.delete(announcement)
                return Response(
                    status=200,
                    content_type="application/json",
                    json={"message": "Success delete announcement!"},
                )
            else:
                return Response(
                    status=404,
                    content_type="application/json",
                    json={"message": "Announcement not found!"},
                )
        except DBAPIError:
            self.server_error()
