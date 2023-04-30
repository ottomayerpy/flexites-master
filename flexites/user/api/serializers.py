from rest_framework import serializers
from flexites.user.models import Organization, FlexUser

class OrganizationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class FlexUserSerializer(serializers.ModelSerializer):

    organizations = serializers.SerializerMethodField()

    class Meta:
        model = FlexUser
        fields = '__all__'

    @staticmethod
    def get_organizations(obj):
        return OrganizationsSerializer(
            Organization.objects.filter(
                id__in=FlexUser.objects.filter(
                    email=obj.email
                ).values('organizations')
            ),
            many=True
        ).data
