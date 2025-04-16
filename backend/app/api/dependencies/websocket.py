from app.utils.connection_manager import ConnectionManager, manager


def get_connection_manager() -> ConnectionManager:
    """Dependency function to retrieve the ConnectionManager instance.

    Returns:
        ConnectionManager: A shared instance of the ConnectionManager.

    """
    return manager
