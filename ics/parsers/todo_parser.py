from typing import List, TYPE_CHECKING

from ics.alarm.utils import get_type_from_container
from ics.grammar.parse import ContentLine
from ics.parsers.parser import Parser, option
from ics.utils import parse_datetime, parse_duration, unescape_string

if TYPE_CHECKING:
    from ics.todo import Todo


class TodoParser(Parser):
    @option(required=True)
    def parse_dtstamp(todo: "Todo", line: ContentLine):
        if line:
            # get the dict of vtimezones passed to the classmethod
            tz_dict = todo._classmethod_kwargs["tz"]
            todo.dtstamp = parse_datetime(line, tz_dict)

    def parse_last_modified(todo: "Todo", line: ContentLine):
        if line:
            tz_dict = todo._classmethod_kwargs["tz"]
            todo.last_modified = parse_datetime(line, tz_dict)

    @option(required=True)
    def parse_uid(todo: "Todo", line: ContentLine):
        if line:
            todo.uid = line.value

    def parse_completed(todo: "Todo", line: ContentLine):
        if line:
            # get the dict of vtimezones passed to the classmethod
            tz_dict = todo._classmethod_kwargs["tz"]
            todo.completed = parse_datetime(line, tz_dict)

    def parse_created(todo: "Todo", line: ContentLine):
        if line:
            # get the dict of vtimezones passed to the classmethod
            tz_dict = todo._classmethod_kwargs["tz"]
            todo.created = parse_datetime(line, tz_dict)

    def parse_description(todo: "Todo", line: ContentLine):
        todo.description = unescape_string(line.value) if line else None

    def parse_location(todo: "Todo", line: ContentLine):
        todo.location = unescape_string(line.value) if line else None

    def parse_percent_complete(todo: "Todo", line: ContentLine):
        todo.percent = int(line.value) if line else None

    def parse_priority(todo: "Todo", line: ContentLine):
        todo.priority = int(line.value) if line else None

    def parse_summary(todo: "Todo", line: ContentLine):
        todo.name = unescape_string(line.value) if line else None

    def parse_url(todo: "Todo", line: ContentLine):
        todo.url = unescape_string(line.value) if line else None

    def parse_dtstart(todo: "Todo", line: ContentLine):
        if line:
            # get the dict of vtimezones passed to the classmethod
            tz_dict = todo._classmethod_kwargs["tz"]
            todo._timespan = todo._timespan.replace(
                begin_time=parse_datetime(line, tz_dict)
            )

    def parse_duration(todo: "Todo", line: ContentLine):
        if line:
            todo._timespan = todo._timespan.replace(
                duration=parse_duration(line.value)
            )

    def parse_due(todo: "Todo", line: ContentLine):
        if line:
            tz_dict = todo._classmethod_kwargs["tz"]
            todo._timespan = todo._timespan.replace(
                end_time=parse_datetime(line, tz_dict)
            )

    @option(multiple=True)
    def parse_valarm(todo: "Todo", lines: List[ContentLine]):
        todo.alarms = [get_type_from_container(x)._from_container(x) for x in lines]

    def parse_status(todo: "Todo", line: ContentLine):
        if line:
            todo.status = line.value
