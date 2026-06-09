import datetime

def get_time():

    return datetime.datetime.now().strftime(
        "%I:%M %p"
    )