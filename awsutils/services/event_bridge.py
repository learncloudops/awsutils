import boto3
from typing import List,Dict, Any
import json
from awsutils.services import Validate


class PutEventEntry(object):
    '''
        Encapsulates a single put_events response entry.

        There should be an entry per event submitted
    '''

    def __init__(self, event_id: str, err_code: str = None, err_msg: str = None) -> None:
        self.__event_id = event_id
        self.__err_code = err_code
        self.__err_msg = err_msg

    @property
    def event_id(self):
        return self.__event_id

    @property
    def err_code(self):
        return self.__err_code

    @property
    def err_msg(self):
        return self.__err_msg

    @staticmethod
    def create(entry: Dict):
        '''
            Builder function for creating new
            PutEventEntry objects

            :params:
                entry (dict) - expects a dict with the following format:
                {
                    'EventId': 'string',
                    'ErrorCode': 'string',
                    'ErrorMessage': 'string'
                }
            :return:
                (PutEventEntry) a entry object
        '''
        return PutEventEntry(
            event_id=entry.get('Id'),
            err_code=entry.get('ErrorCode'),
            err_msg=entry.get('ErrorMessage'))

# -----

class PutEventsResponse(object):
    '''
        Encapsulates the response from
        the event bridge put_events method
    '''

    def __init__(self, resp: Dict):
        self.__failure_count: int = resp.get('FailedEntryCount', 0)
        self.__entries: List[PutEventEntry] = [
            PutEventEntry.create(e) for e in resp['Entries']]

    @property
    def failure_count(self) -> int:
        '''
            Property accessor for the number of put_event
            attempts that failed.

            :return:
                (int) the number of failures
        '''
        return self.__failure_count

    @property
    def entries(self) -> List[PutEventEntry]:
        '''
            Property accessor for the entries collected
            describing the result of each event processed.

        '''
        return self.__entries

# ----- 

class EventBridgeClient(object):
    def __init__(self,
                event_source_name:str,
                event_bus_name:str,
                region:str ='us-east-1') -> None:
        self.__client = boto3.client('events', region_name=region)
        self.__event_source_name = event_source_name
        self.__event_bus_name = event_bus_name
        Validate.not_empty(event_source_name,'the event source cannot be null')
        Validate.not_empty(event_bus_name, 'the event bus name is required')


    def put_events(self, 
                   event_data:List[Dict]=[],
                   event_type:str='CustomEvent') -> PutEventsResponse:
        entries = [self.__create_event_bus_entry(e, event_type) for e in event_data]
        resp = self.__client.put_events(Entries=entries)
        return PutEventsResponse(resp)


    def __create_event_bus_entry(self, event_data, event_type) -> Dict:
        return{
            'Resources': [],
            'EventBusName': self.__event_bus_name,
            'Source' : self.__event_source_name,
            'DetailType': event_type,
            'Detail': json.dumps(event_data)
        }