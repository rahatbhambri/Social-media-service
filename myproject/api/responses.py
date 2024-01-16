from rest_framework.response import Response 

def SuccessResponse(data = {}, status=200, message = "Data Fetched Successfully"):
    response_data = {
        'status': status,
        'data': data,
        'message' : message,
    }
    return Response(response_data, status=status)


def ErrorResponse(data = {}, status=400, message = "Bad Request format"):
    
    response_data = {
        'status': status,
        'data': data,
        'message' : message,
        # Add any additional fields you want in the response
    }
    return Response(response_data, status=status)


def NotFoundResponse(data = {}, status = 404, message = "Information for the request could not be located"):
    response_data = {
        'status': status,
        'data': data,
        'message' : message,
        # Add any additional fields you want in the response
    }

    return Response(response_data, status=status)