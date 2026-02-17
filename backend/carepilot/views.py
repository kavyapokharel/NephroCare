from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .appointmentHandler import appointmentList, bookedAppointmentList
from django.http import HttpResponse
from . import gravenessScorer
from . import healthSummarizer
from . import addLog
from . import plotHandler

a = """

Hi there, we've been reviewing your health information, and it looks like you've been actively focusing on your well-being goals. You've set a good goal of increasing your water intake and maintaining a good walking routine. You've consistently logged progress in both areas.

Currently, you have successfully completed a good portion of your goals - you've logged a considerable amount of each activity (approximately 20 liters of water, 20 kilometers walked). Your spending is also manageable, with a range of around $662-$861 spent each month. 

To keep things moving forward, you're doing well with consistent activity - particularly the walking. It looks like your goal of increasing water intake is on track, and maintaining a consistent walking routine is also beneficial. You've spent a reasonable amount of money on these goals.

We'll continue to monitor your progress and offer any support we can. Please let us know if you have any questions or concerns - we want to help ensure you're feeling your best.

"""


class Consultation(APIView):

    def post(self, request):
        step = request.data.get("step")
        message = request.data.get("message")
        from_date = request.data.get("from_date")
        to_date = request.data.get("to_date")
        selected_date = request.data.get("selected_date")

        # 1) Step 1: User describes symptoms
        if step == "symptom":
            return Response({
                "step": "choose_date",
                "message": "Thank you. Select the timeline available for your consultation."
            })

        # 2) Step 2: User sends FROM → TO date
        if step == "choose_date":
            if not from_date or not to_date:
                return Response({
                    "error": "from_date and to_date are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            slots = appointmentList(from_date, to_date, doctor="Dr. Pokharel")

            if slots == None:
                return Response({
                    "step": "choose_date",
                    "message": "Sorry, we don't have any slots between dates selected.",
                    "dates": None
                })

            return Response({
                "step": "choose_date",
                "message": "Here are available appointment dates:",
                "dates": slots
            })

        # 3) Step 3: User selects final date
        if step == "confirm":
            if not selected_date:
                return Response({
                    "error": "selected_date is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            gravenessRating, summary = gravenessScorer.call(message)

            return Response({
                "step": "done",
                "message": f"Your appointment has been booked for {selected_date} with Graveness rating {gravenessRating} to your description."
            })

        return Response({
            "error": "Invalid step"
        }, status=status.HTTP_400_BAD_REQUEST)
    

class HealthSummarizer(APIView):
    def post(self, request):
        # summary = healthSummarizer.call("Sugam")
        return Response(data=a)


class HealthPlotView(APIView):
    def get(self, request):
        data_type = request.query_params.get("type")

        if data_type == 'weight':
            img = plotHandler.generateBodyWeightPlot(size=(12, 8))
            return HttpResponse(img, content_type="image/jpeg")
        if data_type == 'sugar':
            img = plotHandler.generateBloodSugarPlot(size=(12, 8))
            return HttpResponse(img, content_type='img/jpeg')
        if data_type == 'pressure':
            img = plotHandler.generateBPPlot(size=(12, 8))
            return HttpResponse(img, content_type='img/jpeg')
    
    def post(self, request):
        data_type = request.data.get("type")
        value = request.data.get("value")
        date = request.data.get("date")

        if data_type == 'weight':
            addLog.addWeightOrSugarLog(for_type='weight', date=date, measurement=float(value))
        if data_type == 'sugar':
            addLog.addWeightOrSugarLog(for_type='sugar', date=date, measurement=float(value))
        if data_type == 'pressure':
            systolic, dystolic = value.split('/')
            addLog.addBPLog(date=date, systolic=float(systolic), diastolic=float(dystolic))

        return Response({"message": "Record added successfully"})
    

class ExpenditureView(APIView):
    def get(self, request):
        logs_requested = request.query_params.get("logs")

        # Return logs instead of image
        if logs_requested == "1":
            logs = plotHandler.expenditureLog()
            return Response({"logs": logs})

        # Return pie chart image
        img = plotHandler.expenditureChart()
        return HttpResponse(img, content_type="image/png")


class AppointmentListView(APIView):
    def get(self, request):
        slots = bookedAppointmentList(from_date_str='2025-10-19 00:00:00', to_date_str='2026-11-25 00:00:00', doctor='Dr. Pokharel')

        return Response({"appointments": slots})


class GoalView(APIView):
    def get(self, request):
        goal_list = addLog.goalList()
        return Response(data=goal_list)

    def post(self, request):
        goal = request.data.get('goal')
        goal_log = addLog.goalLog(goal)
        return Response(data=goal_log)