import datetime
import json
import sys
import time

from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string


def sse_view(request):
    def event_stream():
        count = 0
        while True:
            count += 1
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Standard JSON data for Alpine.js
            data = {"count": count, "time": current_time}
            ypayld = f'event: message\ndata: {json.dumps(data)}\n\n'
            print(ypayld)  # Debugging line to check the JSON data
            yield ypayld #f'event: message\ndata: {json.dumps(data)}\n\n'
            
            # HTML content for HTMX
            html_content = render_to_string('sse_update.html', {'count': count, 'time': current_time}).replace('\n', '')
            # print(html_content)  # Debugging line to check the HTML content
            # yield f'event: htmx-update\ndata: {json.dumps(html_content)}\n\n'
            yield f'event: htmx-update\ndata: {html_content}\n\n'
            
            sys.stdout.flush()
            time.sleep(1)
    
    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    return response

def index(request):
    return render(request, 'sse_client.html')
