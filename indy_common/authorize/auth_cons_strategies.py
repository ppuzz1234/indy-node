from abc import abstractmethod, ABCMeta

from common.exceptions import LogicError
from indy_common.authorize.auth_actions import split_action_id
from indy_common.authorize.auth_constraints import AbstractAuthConstraint, AbstractConstraintSerializer
from state.pruning_state import PruningState


class AbstractAuthStrategy(metaclass=ABCMeta):
    def __init__(self, auth_map, anyone_can_write_map={}):
        self.auth_map = auth_map
        self.anyone_can_write_map = anyone_can_write_map

    @abstractmethod
    def get_auth_constraint(self, action_id) -> AbstractAuthConstraint:
        raise NotImplementedError()

    @abstractmethod
    def _find_auth_constraint_key(self, action_id, auth_map):
        raise NotImplementedError()

    @staticmethod
    def is_accepted_action_id(from_auth_map, from_req):
        am = split_action_id(from_auth_map)
        r = split_action_id(from_req)
        if r.prefix != am.prefix:
            return False
        if r.txn_type != am.txn_type:
            return False
        if r.field != am.field and \
                am.field != '*':
            return False
        if r.old_value != am.old_value and \
                am.old_value != '*':
            return False
        if r.new_value != am.new_value and \
                am.new_value != '*':
            return False
        return True


class LocalAuthStrategy(AbstractAuthStrategy):

    def get_auth_constraint(self, action_id) -> AbstractAuthConstraint:
        if self.anyone_can_write_map:
            am_id = self._find_auth_constraint_key(action_id, self.anyone_can_write_map)
            if am_id:
                return self.anyone_can_write_map.get(am_id)
        am_id = self._find_auth_constraint_key(action_id, self.auth_map)
        return self.auth_map.get(am_id)

    def _find_auth_constraint_key(self, action_id, auth_map):
        for am_id in auth_map.keys():
            if self.is_accepted_action_id(am_id, action_id):
                return am_id


class ConfigLedgerAuthStrategy(AbstractAuthStrategy):

    def __init__(self,
                 auth_map,
                 state: PruningState,
                 serializer: AbstractConstraintSerializer,
                 anyone_can_write_map={}):
        super().__init__(auth_map=auth_map,
                         anyone_can_write_map=anyone_can_write_map)
        self.state = state
        self.serializer = serializer

    def get_auth_constraint(self, action_id: str) -> AbstractAuthConstraint:
        """
        Find rule_id for incoming action_id
        """
        if self.anyone_can_write_map:
            am_id = self._find_auth_constraint_key(action_id, self.anyone_can_write_map)
            if am_id:
                return self.anyone_can_write_map.get(am_id)
        am_id = self._find_auth_constraint_key(action_id, self.auth_map)
        if not am_id:
            return None
        """
        Get auth constraint from state
        """
        from_state = self.state.get(key=am_id.encode(),
                                    isCommitted=False)
        if not from_state:
            raise LogicError("There is no any auth constraints for given rule_id: {}".format(am_id))
        constraint = self.serializer.deserialize(from_state)
        if not constraint:
            raise LogicError("Cannot initialize constraint object from state")

        return constraint

    def _find_auth_constraint_key(self, action_id, auth_map):
        for am_id in auth_map.keys():
            if self.is_accepted_action_id(am_id, action_id):
                return am_id
