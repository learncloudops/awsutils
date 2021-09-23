import pytest
from awsutils.services import (
    PutEventsResponse, PutEventEntry, EventBridgeClient)

EVENT_BUS_NAME = 'test_event_bus'

@pytest.fixture
def event_bus(events_client):
  events_client.create_event_bus(Name=EVENT_BUS_NAME)

def test_create_event_bridge_client():
  eb = EventBridgeClient(
        event_source_name='event_source',
        event_bus_name='event_bus')
  assert eb is not None

def test_create_client_fails_when_source_name_null():
  try:
    eb = EventBridgeClient(
        event_source_name=None,
        event_bus_name='event_bus')
    pytest.fail()
  except ValueError as e:
    assert str(e) == 'the event source cannot be null'


def test_create_client_fails_when_bus_name_null():
  try:
    eb = EventBridgeClient(
        event_source_name='event_source',
        event_bus_name=None)
    pytest.fail()
  except ValueError as e:
    assert str(e) == 'the event bus name is required'


def test_eb(events_client, event_bus):
  response = events_client.list_event_buses(NamePrefix=EVENT_BUS_NAME)
  assert len(response['EventBuses']) == 1

def test_eb_put_event(events_client, event_bus):
    eb = EventBridgeClient(
        event_source_name='event_source',
        event_bus_name=EVENT_BUS_NAME)
    res:PutEventsResponse = eb.put_events(event_data=[{'test':'msg'}])
    assert res.failure_count == 0
    assert len(res.entries) == 1
    entry:PutEventEntry = res.entries[0]
    print(entry)
    assert entry.event_id is None
    assert entry.err_code is None
    assert entry.err_msg is None
