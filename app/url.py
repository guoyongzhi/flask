from app.views import *
from app import app

# app.add_url_rule('/load/<string:filename>', view_func=LoadView.as_view('load'))
# app.add_url_rule('/getyongli', view_func=Getyongli.as_view('getyongli'))
# app.add_url_rule('/generaconfig', view_func=GeneraConfig.as_view('generaconfig'))
# app.add_url_rule('/action', view_func=ActionViews.as_view("action"))


class Parameter(dict):
    def __init__(self, parameter_dict=None, source=None):
        if parameter_dict:
            super(Parameter, self).__init__(parameter_dict)
        self.source = source
