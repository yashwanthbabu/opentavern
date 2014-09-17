# import re

from django import template
from tavern.models import get_upcoming_events

register = template.Library()


class TavernUpcomingEvents(template.Node):
    def __init__(self, user, var_name):
        """ Instantiating with the name of the variable
        to be resolved and calling variable.resolve(context)"""
        self.user = template.Variable(user)
        self.var_name = var_name

    def render(self, context):
        user = self.user.resolve(context)
        upcoming_events = get_upcoming_events(user)
        context[self.var_name] = upcoming_events
        return ''


@register.tag
def get_tavern_upcoming_events(parser, token):
    """ gets the upcoming events for
     which user has been joined"""
    args = token.split_contents()
    var_name = args[-0]
    arg_variable = args.index('request.user')
    user = args[arg_variable]
    return TavernUpcomingEvents(user, var_name)
