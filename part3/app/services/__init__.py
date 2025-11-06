from app.services.facade import HBnBFacade

facade = None


def get_facade():
    global facade
    if facade is None:
        facade = HBnBFacade()
    return facade
