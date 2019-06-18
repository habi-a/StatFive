
class Workflow():

    def __init__(self,ticket):
        self.tiket = ticket

    def next(self,group):
        pass

    def close_tickets(self,ticket):
        pass

    def change_group_assigment(self,group):
        pass

    def ongoing_tickets(self):
        pass

    def last_five_request(self):
        pass

    # method to be available for workflow

    def action(self,**kwargs):
        # launch the method below via API
        pass

    def role_assigment(self,**kwargs):
        pass

    def unlock_user(self,**kwargs):
        pass

    def archive_user(self,**kwargs):
        pass

    def change_user(self,**kwargs):
        pass
    
