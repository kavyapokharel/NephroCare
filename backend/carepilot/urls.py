from django.urls import path
from .views import Consultation, HealthSummarizer, HealthPlotView, ExpenditureView, AppointmentListView, GoalView

urlpatterns = [
    path('consultation/', Consultation.as_view(), name='consultation'),
    path('health-summary/', HealthSummarizer.as_view(), name='health-summary'),
    path('health-plot/', HealthPlotView.as_view(), name='health-graph'),
    path('expenditure/', ExpenditureView.as_view(), name='expenditure'),
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
    path('goal/', GoalView.as_view(), name='goal')
]