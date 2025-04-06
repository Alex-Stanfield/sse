import json

from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render

# Create your views here.

def onResult(request):
    
    # Check the HTTP method
    if request.method == 'GET':
        # Process GET request
        context = {}  # Can add data to context as needed
        
        # Get parameter 'p' from query string, default to None if not present
        p = request.GET.get('p', None)
        print(f"Debug - p parameter: {p}")

        if p is not None:
            # Return 200 OK with the value of p
            return JsonResponse({'parameter': p}, status=200)
        else:
            # Return 404 Not Found if p is missing
            return HttpResponse("Parameter 'p' not found", status=404)
    elif request.method == 'HEAD':
        # Process HEAD request (like GET but return only headers)
        response = HttpResponse()
        return response
    elif request.method == 'PUT':
        # Process PUT request
        try:
            data = json.loads(request.body)
            # Process the data...
            print(data)  # Debugging line to check the received data
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Handle unsupported methods
        return HttpResponseNotAllowed(['GET', 'HEAD', 'PUT'])
    
    
    
    return render(request, 'cognex/onResult.html')
