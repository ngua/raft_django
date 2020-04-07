from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Room


@csrf_exempt
@require_POST
def rooms(request):
    rooms = Room.objects.all().order_by('-last_active')
    response = {
        'rooms': [
            {
                'id': room.room_id,
                'pk': room.pk,
                'active': room.last_active.strftime('%m-%d %H:%M')
            } for room in rooms
        ]
    }
    return JsonResponse(response)
