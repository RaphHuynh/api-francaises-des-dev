from .router_github import *
from .router_member import *
from .router_category import *
from .router_network import *
from .router_session import *

routers = (
    router_github.router,
    router_member.router,
    router_category.router,
    router_network.router,
    router_session.router
)
