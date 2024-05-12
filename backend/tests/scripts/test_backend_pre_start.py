from unittest.mock import MagicMock, patch
from sqlmodel import select

from backend.backend_pre_start import init
from backend.app import logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    exec_mock = MagicMock(return_value=True)
    session_mock.configure_mock(**{"exec.return_value": exec_mock})

    mocked_session = patch("sqlmodel.Session", return_value=session_mock)
    mocked_logger_info = patch.object(logger, "info")
    mocked_logger_error = patch.object(logger, "error")
    mocked_logger_warn = patch.object(logger, "warning")

    with mocked_session, mocked_logger_info, mocked_logger_error, mocked_logger_warn:
        try:
            init(engine_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

        assert (
            connection_successful
        ), "The database connection should be successful and not raise an exception."

        assert session_mock.exec.called_once_with(
            select(1)
        ), "The session should execute a select statement once."
