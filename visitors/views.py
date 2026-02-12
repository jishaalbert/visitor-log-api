from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Visitor
from .serializers import VisitorSerializer
from django.db.models import Q


@api_view(['POST'])
def check_in(request):
    serializer = VisitorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def check_out(request):
    phone = request.data.get("phone")

    try:
        visitor = Visitor.objects.get(
            phone=phone,
            check_out_time__isnull=True
        )
        visitor.check_out_time = timezone.now()
        visitor.save()
        return Response({"message": "Checked out successfully"})
    except Visitor.DoesNotExist:
        return Response(
            {"error": "Active visitor not found"},
            status=404
        )


@api_view(['GET'])
def visitors_inside(request):
    visitors = Visitor.objects.filter(check_out_time__isnull=True)
    serializer = VisitorSerializer(visitors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def visitors_by_date(request):
    date = request.GET.get("date")

    if not date:
        return Response({"error": "Please provide date (YYYY-MM-DD)"})

    visitors = Visitor.objects.filter(check_in_time__date=date)
    serializer = VisitorSerializer(visitors, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def search_visitors(request):
    query = request.GET.get("q")

    visitors = Visitor.objects.filter(
        Q(name__icontains=query) | Q(phone__icontains=query)
    )

    serializer = VisitorSerializer(visitors, many=True)
    return Response(serializer.data)

