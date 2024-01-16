from django.http import JsonResponse

def SuccessResponse(data, status=200, message = ""):
    response_data = {
        'status': status,
        'data': data,
        'message' : message,
    }
    return JsonResponse(response_data, status=status)


def ErrorResponse(data, status=400, message = ""):
    
    response_data = {
        'status': status,
        'data': data,
        'message' : message,
        # Add any additional fields you want in the response
    }
    return JsonResponse(response_data, status=status)


def NotFoundResponse(data, status = 404, message = ""):
    response_data = {
        'status': status,
        'data': data,
        'message' : message,
        # Add any additional fields you want in the response
    }

    return JsonResponse(response_data, status=status)