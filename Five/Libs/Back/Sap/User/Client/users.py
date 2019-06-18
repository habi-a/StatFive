from Libs.Back.Sap.User.users import Users as _


class Users(_):

    def __init__(self, l_sys=list()):
        super().__init__(l_sys)
        self._client_user_segregation()

    def _client_user_segregation(self):
        self.SEGREGATION.update({'ACCNT': ['ACCNT',
                                           'USR02',
                                           ['BNAME', 'ACCNT']],
                                 'KOSTL': ['KOSTL',
                                           'USR21',
                                           ['BNAME', 'KOSTL']]})