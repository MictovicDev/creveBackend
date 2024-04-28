from django.shortcuts import render
from creveBackend import consumers
from django.http import HttpResponse

# Create your views here.


def chat(request):
    return render(request, "chat/chat.html")


async def send(request, pk):
    print(request)
    # ans = await consumers.ChatConsumer.all_messages(pk)
    return HttpResponse("Done")



