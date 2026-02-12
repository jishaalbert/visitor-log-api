from rest_framework import serializers
from .models import Visitor

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

    def validate(self, data):
        phone = data.get("phone")

        if Visitor.objects.filter(phone=phone, check_out_time__isnull=True).exists():
            raise serializers.ValidationError(
                "Visitor already checked in and not checked out."
            )

        return data

