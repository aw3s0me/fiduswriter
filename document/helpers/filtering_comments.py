from document.models import RIGHTS_CHOICES
from django.conf import settings

class CommentFilter():
    """
    Class for filtering comments
    author: akorovin
    """
    def __init__(self, user_info):
        self.user_info = user_info
        #get access right of current user
        self.access_right = user_info.access_rights
        self.rights = self._convert_rights_to_dict(RIGHTS_CHOICES)
        self.right_name = self.rights[self.access_right]
        self.visibility_role_dict = self._get_visibility_info_from_cfg(
                self.right_name)

    def _convert_rights_to_dict(self, access_rights):
        """
        Converts access rights list to dict for convenience
        :param access_rights:
        :type access_rights:
        :return: Users access rights
        :rtype: dict
        """
        return dict((x, y) for x, y in access_rights)

    def _get_visibility_info_from_cfg(self, right_name):
        """
        Gets information about comment visibility from configuration.py
        :param right_name: Current user right name
        :type right_name: string
        :return: Visibility option
        :rtype: dict
        """
        if right_name == 'reader':
            return dict()

        return settings.VISIBILITY[self.right_name]

    def _init_document_access_rights_dict(self, access_rights):
        """
        For convenience transforms access rights list to dict
        :param access_rights:
        :type access_rights:
        :return: Access rights
        :rtype: dict
        """
        #to renew access rights information
        self.access_right = access_rights
        return  dict((x['user_id'], x) for x in access_rights)

    def _can_be_visible_rest(self, user_rights_str, cur_phase):
        """
        Check visibility if not owner and reader
        :param user_rights_str:
        :type user_rights_str:
        :param cur_phase:
        :type cur_phase:
        :return:
        :rtype:
        """
        #if no such user in dict (cfg.py)
        if user_rights_str not in self.visibility_role_dict:
            return False

        user_instructions = self.visibility_role_dict[user_rights_str]
        return 'always' in user_instructions or cur_phase in user_instructions

    def _is_reader(self, user_rights_str):
        """
        Check if reader
        :param user_rights_str:
        :type user_rights_str:
        :param cur_phase:
        :type cur_phase:
        :return:
        :rtype:
        """
        return user_rights_str == 'reader'

    def _can_be_visisble_self(self, user_id):
        """
        Checks if it is the same user. user must see its own comments
        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """
        return self.user_info.user.id == user_id

    def _fill_comments_dict(self, comments, access_rights_dict, cur_phase):
        """
        For iterating comment dict
        :param comments:
        :type comments: dict
        :param access_rights_dict:
        :type access_rights_dict: dict
        :param cur_phase:
        :type cur_phase: string
        :return: Filtered comments
        :rtype: dict
        """
        filtered_comments = dict()

        #1) get from comment the role of user (rolename)
        #2) get from visibility dict instructions what to do. if always - add to filtered comments
        for comment_id, comment in comments.iteritems():
            user_id = comment['user']

            #own user always can see his own comment
            if self._can_be_visisble_self(user_id):
                filtered_comments[comment_id] = comment
                continue

            #TODO: no info about owner in AccessRights table => exception. remove this when resolve
            try:
                user_rights_dict = access_rights_dict[user_id]
                user_rights_code = user_rights_dict['rights']
                user_rights_str = self.rights[user_rights_code]
            except:
                user_rights_str = 'author'

            # if comment of reader role and current phase publication - add to filtered comments.
            # readers can leave comments in publication phase
            if self._is_reader(user_rights_str):
                #TODO: leave in publication
                #if cur_phase == 'publication':
                #    filtered_comments[comment_id] = comment
                #TODO: or leave any phase?
                filtered_comments[comment_id] = comment
                continue

            if self._can_be_visible_rest(user_rights_str, cur_phase):
                filtered_comments[comment_id] = comment

        return filtered_comments

    def filter_comments_by_role(self, comments, cur_phase, cur_access_rights):
        """
        Filtering comments
        :param comments:
        :type comments:
        :param cur_phase:
        :type cur_phase:
        :param cur_access_rights:
        :type cur_access_rights:
        :return: Filtered comments
        :rtype: dict
        """
        access_rights_dict = self._init_document_access_rights_dict(cur_access_rights)
        #own_user_rights_code = access_rights_dict[self.user_info.user.id]['rights']
        #own_user_rights = self.rights[own_user_rights_code]
        #own_user_visibility = self.visibility_role_dict[own_user_rights]

        #TODO: return all comments without filtering if owner????
        #readers can see comments only when publ phase.
        if self.user_info.is_owner == True or \
                (self.right_name == 'reader' and cur_phase == 'publication'):
            return comments

        filtered_comments = self._fill_comments_dict(comments,
                                                     access_rights_dict,
                                                     cur_phase)
        return filtered_comments
