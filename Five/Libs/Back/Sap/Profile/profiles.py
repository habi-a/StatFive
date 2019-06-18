from Libs.Back.Sap.misc import Misc as ms_

class Profiles():
    """
    Class profile is used to check the matrix auth activated
    d_sys = dict for selection database and pyrfc connection
    l_profiles = list of profiles
    """

    def __init__(self, dd_sys):
        self.dd_sys = dd_sys

    def SUSR_SUIM_API_RSUSR020(self, **kwargs):
        """
        get the profiles by Obj selection in kwargs
        """
        def _return(d):
            return d['ET_PROFS'] if d['ET_PROFS'] else dict()
        return {sys: _return(ms_().launch_fm(self.dd_sys[sys],
                                             'SUSR_SUIM_API_RSUSR020',
                                             **kwargs)
                             )
                for sys in self.dd_sys
                }
