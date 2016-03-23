import lists_endpoint

class WunderClient:

    ''' Client for accessing the Wunderlist info of a user (given by the access token) '''

    def __init__(self, access_token, client_id, api):
        '''
        Create a Wunderlist client with the given parameters.

        Params:
        access_token -- Wunderlist access token, given once a user has given Wunderlist permission access their data
        client_id -- Wunderlist-generated ID for the app accessing the client's data
        api -- WunderApi handle to API information
        '''
        self.client_id = client_id
        self.access_token = access_token
        self.api = api

    def authenticated_request(self, endpoint, method='GET', params=None, data=None):
        '''
        Send a request to the given Wunderlist API with 'X-Access-Token' and 'X-Client-ID' headers and ensure the response code is as expected given the request type

        Params:
        endpoint -- API endpoint to send request to

        Keyword Args:
        method -- GET, PUT, PATCH, DELETE, etc.
        params -- parameters to encode in the request
        data -- data to send with the request
        '''
        headers = {
                'X-Access-Token' : self.access_token,
                'X-Client-ID' : self.client_id
                }
        return self.api.request(endpoint, method=method, headers=headers, params=params, data=data)

    def get_list(self, list_id):
        ''' Gets information about the list with the given ID '''
        return lists_endpoint.get_list(self, list_id)
