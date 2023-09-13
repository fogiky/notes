import logging

fsm = {}


def set_state(state) -> bool:
    user = 'test_user'
    if not isinstance(user, (str, int)):
        logging.error("Invalid type for `user` in `ss`")
        return False
    if not isinstance(state, (str, bool)):
        logging.error("Invalid type for `state` in `ss`")
        return False
    if state:
        fsm[str(user)] = state
    elif str(user) in fsm:
        del fsm[str(user)]
    return True


def get_state() -> str:
    user = 'test_user'
    if not isinstance(user, (str, int)):
        logging.error("Invalid type for `user` in `gs`")
        return ''
    return fsm.get(str(user), '')
