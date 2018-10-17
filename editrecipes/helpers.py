import datetime

from editrecipes.models import Month


def get_month(month_id=None):
    if month_id is not None:
        return Month.objects.get(id=month_id)
    else:
        this_month = datetime.datetime.now().strftime("%B")
        return Month.objects.get(month=this_month)
