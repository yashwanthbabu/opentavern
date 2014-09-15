from django import template
import re

from tavern.models import get_users_attending_Event
from tavern.models import get_users_not_attending_event

register = template.Library()


class TavernAttendeesUsers(template.Node):
    def __init__(self, event, var_name):
        self.event = template.Variable(event)
        self.var_name = var_name

    def render(self, context):
        event = self.event.resolve(context)
        users_attending_event = get_users_attending_Event(event)
        context[self.var_name] = users_attending_event
        return ''


class TavernAttendeesNotUsers(template.Node):
    def __init__(self, event, var_name):
        self.event = template.Variable(event)
        self.var_name = var_name

    def render(self, context):
        event = self.event.resolve(context)
        users_not_attending_event = get_users_not_attending_event(event)
        context[self.var_name] = users_not_attending_event
        return ''


@register.tag
def get_tavern_not_attending_event(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    m = re.search(r'for (\w+.\w+) as (\w+)', arg)
    event, var_name = m.groups()
    return TavernAttendeesUsers(event, var_name)


@register.tag
def get_tavern_attendees(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    m = re.search(r'for (\w+.\w+) as (\w+)', arg)
    event, var_name = m.groups()
    return TavernAttendeesUsers(event, var_name)
