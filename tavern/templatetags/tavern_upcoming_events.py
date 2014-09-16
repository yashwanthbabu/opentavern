import re

from django import template
from tavern.models import get_upcoming_events

register = template.Library()


class TavernUpcomingEvents(template.Node):
    def __init__(self, user, var_name):
        self.user = template.Variable(user)
        self.var_name = var_name

    def render(self, context):
        user = self.user.resolve(context)
        upcoming_events = get_upcoming_events(user)
        context[self.var_name] = upcoming_events
        return ''


@register.tag
def get_tavern_upcoming_events(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    m = re.search(r'for (\w+.\w+) as (\w+)', arg)
    user, var_name = m.groups()
    return TavernUpcomingEvents(user, var_name)
