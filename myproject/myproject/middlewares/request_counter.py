from django.core.cache import cache 
import json

class RequestCounter:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rc = 0
    
    def calcPhone(self, name):
        
        if 'a' <= name[0] <= 'h':
            return "0000"
        else:
            return "1111"
    
    def __call__(self, request):
        self.rc +=1 
        response = self.get_response(request)

        if request.method == 'POST' :
            try:
                data = json.loads(request.body.decode('utf-8'))
                name = data.get('name', None)
            except:
                name = None

            if name:
                print("hellooo")
                phone = cache.get(str(name), None)
                if not phone :
                    phone = self.calcPhone(str(name))
                    cache.set(str(name), phone)
                response.data['phone'] = phone
                    
        if response.status_code == 200:
            response.data['request_count'] = self.rc
            response._is_rendered = False 
            response.render()
        return response

        
    
