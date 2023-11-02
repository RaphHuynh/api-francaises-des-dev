import mysql.connector

from app import settings
from app.models import *

from fastapi import UploadFile
from typing import List, Optional
from datetime import datetime, timedelta


mydb = mysql.connector.connect(
    host=settings.HOST,
    user=settings.USER,
    password=settings.PASSWORD,
    database=settings.DATABASE,
    port=settings.PORT
)


async def get_members() -> List[MemberWithCategory]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute("""
            SELECT member.*, GROUP_CONCAT(category.name) AS cat_name
            FROM member, member_has_category, category
            WHERE member.id=member_has_category.id_member AND member_has_category.id_category=category.id
            GROUP BY member.id
        """)

        return [
            MemberWithCategory(id_member=row.id, username=row.username, url_portfolio=row.url_portfolio, category_name=row.cat_name)
            for row in cursor.fetchall() if row.date_validate and not row.date_deleted
        ]


async def get_member_by_id(id_member) -> Optional[MemberIn]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute(
            "SELECT id, username, firstname, lastname, description, mail, url_portfolio FROM member WHERE id = %s", (id_member,)
        )

        res = cursor.fetchone()
        if not res:
            return None

        return MemberIn(id=res.id, username=res.username, firstname=res.firstname, lastname=res.lastname,
                        description=res.description, mail=res.mail, url_portfolio=res.url_portfolio)


async def patch_member_update(member: MemberOut) -> int:
    with  mydb.cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE member SET firstname = %s, lastname = %s, description = %s, mail = %s, url_portfolio = %s WHERE id = %s",
                (member.firstname, member.lastname, member.description, member.mail, member.url_portfolio, member.id)
            )

            mydb.commit(); return 201
        except mysql.connector.Error:
            return 400


async def get_categories() -> List[Category]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT id, name FROM category")
        return [Category(id=row.id, name=row.name) for row in cursor.fetchall()]


async def post_category(category: CategoryOut) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO category (name) VALUES (%s)", (category.name,)
            )

            mydb.commit(); return 201
        except mysql.connector.Error:
            return 400


async def get_members_category(name_category: str) -> List[GetMembers]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute(
            """SELECT member.* FROM member, member_has_category, category
               WHERE member.id = member_has_category.id_member AND member_has_category.id_category = category.id
                                                               AND category.name = %s""", (name_category,)
        )

        return [GetMembers(id=row.id, username=row.username, url_portfolio=row.url_portfolio)
                for row in cursor.fetchall() if row.date_validate and not row.date_deleted]


async def return_id_category_by_name(name: str) -> int:
    with mydb.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                "SELECT id FROM category WHERE name = %s", (name,)
            )

            res = cursor.fetchone()
            if not res:
                return -1
            
            return cursor.fetchone().id
        except TypeError:
            return -1


async def post_add_category_on_member(member: MemberHasCategory) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.executemany(
                """INSERT INTO member_has_category (id_member, id_category) VALUES (%s, %s)
                   ON DUPLICATE KEY UPDATE id_member=id_member 
                """, [(member.id_member, cat) for cat in member.id_category]
            )

            mydb.commit(); return 201
        except mysql.connector.Error:
            return 400


async def get_network_of_member_by_id(id_member: int) -> List[GetMemberHasNetwork]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute(
            """SELECT network.name, member_has_network.url, member_has_network.id_network
               FROM network, member_has_network, member
               WHERE member.id = member_has_network.id_member AND member_has_network.id_network = network.id
                                                              AND member.id = %s""", (id_member,)
        )

        return [GetMemberHasNetwork(name=row.name, url=row.url, id_network=row.id_network)
                for row in cursor.fetchall()]


async def get_category_of_member_by_id(id_member: int) -> List[CategoryOut]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute(
            """SELECT category.name FROM category, member, member_has_category
               WHERE member.id = member_has_category.id_member AND member_has_category.id_category = category.id
                                                               AND member.id = %s""", (id_member,)
        )

        return [CategoryOut(name=row.name) for row in cursor.fetchall()]


async def get_member_has_category_by_id_member(id_member: int) -> List[MemberHasCategoryOut]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute(
            """SELECT member_has_category.id_member, category.name, member_has_category.id_category
               FROM member, member_has_category, category
               WHERE member.id = member_has_category.id_member AND member_has_category.id_category = category.id
                                                               AND member.id = %s""", (id_member,)
        )

        return [
            MemberHasCategoryOut(id_member=row.id_member, name=row.name, id_category=row.id_category)
            for row in cursor.fetchall()
        ]


async def get_network() -> List[Network]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT id, name FROM network")
        return [Network(id=row.id, name=row.name) for row in cursor.fetchall()]


async def post_network_on_member(member: MemberHasNetwork) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.executemany(
                """INSERT INTO member_has_network (id_member, id_network, url)
                   VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE url = VALUES(url)
                """,
                [(member.id_member, net, url) for net, url in zip(member.id_network, member.url) if url]
            )

            mydb.commit(); return 201
        except mysql.connector.Error:
            return 400


async def delete_category_delete_by_member(member: MemberHasCategory) -> int:
    with mydb.cursor() as cursor: 
        try:
            cursor.executemany(
                "DELETE FROM member_has_category WHERE id_member = %s AND id_category = %s",
                [(member.id_member, cat) for cat in member.id_category]
            )

            mydb.commit(); return 200
        except mysql.connector.Error:
            return 400


async def delete_network_delete_by_member(member: MemberHasNetworkIn) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.executemany(
                "DELETE FROM member_has_network WHERE id_member = %s AND id_network = %s",
                [(member.id_member, net) for net in member.id_network]
            )

            mydb.commit(); return 200
        except mysql.connector.Error:
            return 400


async def add_image_portfolio(upload: UploadFile, id_member: int) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE member SET image_portfolio = %s WHERE id = %s",
                (upload.file.read(), id_member)
            )

            upload.file.close()
            mydb.commit(); return 200
        except mysql.connector.Error:
            return 500


async def get_image_by_id_member(id_member: int) -> Optional[bytes]:
    with mydb.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                "SELECT image_portfolio FROM member WHERE id = %s", (id_member,)
            )

            res = cursor.fetchone()
            if not res:
                return None
            
            return res.image_portfolio
        except mysql.connector.Error:
            return None


async def register_new_member(name: str) -> Optional[int]:
    with mydb.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO member (username) VALUES (%s)", (name,)
            )

            mydb.commit(); return cursor.lastrowid
        except mysql.connector.Error:
            return None


async def get_member_by_username(username: str) -> Optional[MemberIn]:
    with mydb.cursor(named_tuple=True) as cursor:
        cursor.execute(
            """SELECT id, username, firstname, lastname, description, mail, url_portfolio
               FROM member WHERE username = %s""", (username,)
        )

        res = cursor.fetchone()
        if not res:
            return None
        
        return MemberIn(id=res.id, username=res.username, firstname=res.firstname, lastname=res.lastname,
                        description=res.description, mail=res.mail, url_portfolio=res.url_portfolio)


async def register_token(access_token: str, refresh_token: str, id_user: int) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO session (token_session, token_refresh, id_member) VALUES (%s, %s, %s)",
                (access_token, refresh_token, id_user)
            )

            mydb.commit(); return 201
        except mysql.connector.Error:
            return 400


async def get_session(id_user: int) -> Optional[Session]:
    with mydb.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                "SELECT * FROM session WHERE id_member = %s", (id_user,)
            )

            result = cursor.fetchone()
            if not result:
                return None
            
            return Session(access_token=result.access_token, refresh_token=result.refresh_token,
                           id_member=result.id_member, date_created=result.date_created)
        except mysql.connector.Error:
            return None


async def delete_session(id_user: int) -> int:
    with mydb.cursor() as cursor:
        try:
            cursor.execute(
                "DELETE FROM session WHERE id_member = %s", (id_user,)
            )

            mydb.commit(); return 200
        except mysql.connector.Error:
            return 400


async def verif_session(session: dict) -> int:
    with mydb.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                "SELECT * FROM session WHERE id_member = %s", (session["user_id"],)
            )

            result = cursor.fetchone()
            if not result:
                return 401

            session_verif = Session(access_token=result.access_token, refresh_token=result.refresh_token,
                                    id_member=result.id_member, date_created=result.date_created)

            if session_verif.access_token == session["access_token"] and \
               session_verif.refresh_token == session["refresh_token"] and \
               session_verif.date_created + timedelta(minutes=60) > datetime.now():
                return 200
            return 401
        except mysql.connector.Error:
            return 401
