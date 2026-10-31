import logging

import pytest

# from nest_server.main import app as nest_server_app
from nest_client import NESTClient

# from threading import Thread


logger = logging.getLogger()


# @pytest.fixture
# def app():
#     nest_server_app.config.update(
#         {
#             "TESTING": True,
#         }
#     )

#     thread = Thread(
#         target=nest_server_app.run,
#         daemon=True,
#         kwargs=dict(host="localhost", port=52425)
#     )
#     thread.start()

#     # other setup can go here

#     yield nest_server_app

#     # clean up / reset resources here


# @pytest.fixture
# def app_client(app):
#     return app.test_client()


@pytest.fixture
def nest() -> NESTClient:
    nest = NESTClient()
    nest.state["has_mpi"] = nest.get("/").json()["mpi"]
    nest.ResetKernel()
    return nest
