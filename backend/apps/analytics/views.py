from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.permissions import IsAnalystOrAbove
from apps.users.models import Role
from .services import AnalyticsService


class DashboardView(APIView):
    permission_classes = [IsAnalystOrAbove]

    def get(self, request):
        """
        GET /api/v1/dashboard/
        """
        user = None if request.user.role == Role.ADMIN else request.user

        return Response({
            "summary": AnalyticsService.get_dashboard_summary(user),
            "monthly_trends": list(AnalyticsService.get_monthly_trends(user)),
            "category_breakdown": list(AnalyticsService.get_category_breakdown(user)),
        })
