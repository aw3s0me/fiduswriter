
from django.contrib.auth.models import User
from django.test import TestCase
from document.helpers.filtering_comments import CommentFilter
from document.models import Document
from document.helpers.session_user_info import SessionUserInfo
from django.contrib.auth.models import UserManager

class CommentFilterTestCase(TestCase):
    def setUp(self):
        try:
            self.owner = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.owner = User.objects.create_user('admin', 'admin@admin.adm', 'admin')

        self.document = Document.objects.create(owner_id=self.owner.id)

        self.access_rights = [
            {'user_name': u'author1', 'user_id': 9, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'w'},
            {'user_name': u'editor1', 'user_id': 5, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'e'},
            {'user_name': u'editor2', 'user_id': 6, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'e'},
            {'user_name': u'reader1', 'user_id': 3, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'r'},
            {'user_name': u'reader2', 'user_id': 4, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'r'},
            {'user_name': u'reviewer1', 'user_id': 7, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'c'},
            {'user_name': u'user1', 'user_id': 10, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'r'},
            {'user_name': u'user2', 'user_id': 11, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'r'},
            {'user_name': u'reviewer2', 'user_id': 8, 'avatar': '/static/img/default_avatar.png', 'document_id': 5, 'rights': u'c'}]
        self.comments = {u'1263735095':
                             {u'userName': u'alex', u'comment': u'fef', u'review:isMajor': True, u'userAvatar': u'/static/img/default_avatar.png', u'user': 2, u'date': 1454491076160, u'id': 1263735095},
                         u'2281243457':
                             {u'userName': u'reviewer1', u'comment': u'Reviewer1', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 7, u'date': 1453463957590, u'id': 2281243457},
                         u'2109250291':
                             {u'userName': u'reader1', u'comment': u'Reader1', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 3, u'date': 1453463924849, u'id': 2109250291},
                         u'1600459977':
                             {u'userName': u'alex', u'comment': u'', u'review:isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 2, u'date': 1454491061400, u'id': 1600459977},
                         u'3994840298':
                             {u'userName': u'reader2', u'comment': u'Reader2', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 4, u'date': 1453463935016, u'id': 3994840298},
                         u'1471743182':
                             {u'userName': u'author1', u'comment': u'Author1', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 9, u'date': 1453463983385, u'id': 1471743182},
                         u'1648805266':
                             {u'userName': u'user1', u'comment': u'User1', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 10, u'date': 1453464013011, u'id': 1648805266},
                         u'2046924673':
                             {u'userName': u'editor1', u'comment': u'Editor1', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 5, u'date': 1453463942024, u'id': 2046924673},
                         u'4138426008':
                             {u'userName': u'user2', u'comment': u'User2', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 11, u'date': 1453464022960, u'id': 4138426008},
                         u'4057943753':
                             {u'userName': u'reviewer2', u'comment': u'Reviewer2', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 8, u'date': 1453463971310, u'id': 4057943753},
                         u'2973318999':
                             {u'userName': u'editor2', u'comment': u'Editor2', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 6, u'date': 1453463948809, u'id': 2973318999},
                         u'408789226':
                             {u'userName': u'alex', u'comment': u'Author2', u'isMajor': False, u'userAvatar': u'/static/img/default_avatar.png', u'user': 2, u'date': 1453463995727, u'id': 408789226}}

    def _init_user(self, username, acc_right):
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, '{0}@{0}.com'.format(username), username)

        user_info = SessionUserInfo()
        user_info.init_access(self.document.id, user)
        user_info.access_rights = acc_right
        user_info.is_owner = False
        user_info.user.id = next(val['user_id']
                                 for i,val in enumerate(self.access_rights)
                                 if val['user_name'] == username)

        return (user, user_info)

    def _get_usernames_in_comments(self, filtered_comments):
        return set([filtered_comments[val]['userName'] for i,val in enumerate(filtered_comments)])

    def _test_reader_rights(self):
        user, user_info = self._init_user('reader1', 'r')
        cur_phase = 'publication'

        filter = CommentFilter(user_info)
        filtered_comments = filter.filter_comments_by_role\
            (self.comments, cur_phase, self.access_rights)
        usernames = self._get_usernames_in_comments(filtered_comments)
        #in publication phase. reader can read all comments
        expected = {u'alex', u'reader1', u'reader2', u'user1', u'reviewer2', u'reviewer1', u'editor2', u'editor1', u'author1', u'user2'}
        self.assertEqual(expected, usernames, 'Reader in {0} phase ok'.format(cur_phase))

        cur_phase = 'editing'
        filtered_comments = filter.filter_comments_by_role\
            (self.comments, cur_phase, self.access_rights)
        usernames = self._get_usernames_in_comments(filtered_comments)
        self.assertTrue(len(usernames) == 0)


    def test_author_rights(self):
        user, user_info = self._init_user('author1', 'w')
        filter = CommentFilter(user_info)
        cur_phase = 'editing'
        #alex - because he is owner. we evaluate owner as author
        expected = {'author1', 'alex'}

        filtered_comments = filter.filter_comments_by_role\
            (self.comments, cur_phase, self.access_rights)
        usernames = self._get_usernames_in_comments(filtered_comments)
        self.assertEqual(expected, usernames, 'Author in {0} phase ok'.format(cur_phase))

        cur_phase = 'publication'
        expected = {'author1', 'alex', u'reader1', u'reader2', u'user1', 'user2'}

        filtered_comments = filter.filter_comments_by_role\
            (self.comments, cur_phase, self.access_rights)
        usernames = self._get_usernames_in_comments(filtered_comments)

        self.assertEqual(expected, usernames, 'Author in {0} phase ok'.format(cur_phase))

        cur_phase = 'revision'
        expected = {'author1', 'alex'}

        filtered_comments = filter.filter_comments_by_role\
            (self.comments, cur_phase, self.access_rights)
        usernames = self._get_usernames_in_comments(filtered_comments)

        self.assertEqual(expected, usernames, 'Author in {0} phase ok'.format(cur_phase))
