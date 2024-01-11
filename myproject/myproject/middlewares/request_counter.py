class RequestCounter:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rc = 0
    
    def __call__(self, request):
        self.rc +=1 
        response = self.get_response(request)
        #print(response)
        response.data['request_count'] = self.rc
        response._is_rendered = False 
        response.render()
        return response
    
