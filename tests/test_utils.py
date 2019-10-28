import os
import json
import pytest
import requests
from datetime import datetime
from pythonbrasilbot.database import get_content
from pythonbrasilbot.utils import get_calendar_events,\
                                  filter_events_per_date,\
                                  get_event_template


def test_get_calendar_events_none():
    with pytest.raises(AttributeError):
        get_calendar_events(None)


def test_get_calendar_events_blank():
    with pytest.raises(AttributeError):
        get_calendar_events('')


def test_get_calendar_events_blank():
    with pytest.raises(requests.exceptions.MissingSchema):
        get_calendar_events('teste')


def test_get_calendar_events():
    conteudo = get_content(2019)

    events = get_calendar_events(conteudo['calendar_url'])
    assert iter(events)


def test_filter_events_per_date():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + "/fixtures/events.json"
    with open(file_path) as json_file:
        json_data = json.load(json_file)

        filtered = filter_events_per_date(json_data['items'], "2019-10-27")

        assert iter(filtered)
        assert len(filtered) == 31

        item = filtered[0]
        assert item['kind'] == 'calendar#event'


def test_get_event_template():
    data = dict(
        title="Nome do evento",
        author="Comunidade Python",
        time=datetime.fromisoformat('2019-10-25T09:00:00-03:00')
    )

    message = get_event_template(**data)

    time_f = data['time'].strftime("%Hh%M")
    template = f"*{data['title']}*\n- {data['author']}\n- {time_f}\n\n"

    assert template == message


def test_get_event_template_without_author():
    data = dict(
        title="Nome do evento",
        time=datetime.fromisoformat('2019-10-25T09:00:00-03:00'),
        author=None
    )

    message = get_event_template(**data)

    time_f = data['time'].strftime("%Hh%M")
    template = f"*{data['title']}*\n- {time_f}\n\n"

    assert template == message


def test_get_event_template_with_time_as_str():
    with pytest.raises(AttributeError):
        data = dict(
            title="Nome do evento",
            time="2019-10-25",
            author=None
        )
        get_event_template(**data)
