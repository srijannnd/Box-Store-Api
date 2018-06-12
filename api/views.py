from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api import methods
from rest_framework.exceptions import ValidationError
from api.models import User
from api.helpers import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@api_view(["POST"])
def signup(request):
    try:
        data, success = methods.create_user(request.data)
        return Response(status=status.HTTP_200_OK,
                        data={'success': success, 'data': data})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'success': False, 'message': str(e)})


@api_view(["POST"])
def login(request):
    try:
        data, error_messages = methods.validate_login_data(request.data)
        if data:
            return Response(status=status.HTTP_200_OK,
                            data={'success': True, 'data': data})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={'success': False, 'data': error_messages})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'success': False, 'message': str(e)})


@csrf_exempt
@login_required
@api_view(["GET", "POST", "PUT", "DELETE"])
def staff_user_boxes(request, user_id):
    try:
        res, success = ({}, False)
        if User.objects.get(pk=user_id).is_staff:
            if request.method == "GET":
                number = request.GET.get('number', 0)
                filter_type = request.GET.get('filter_type', '')
                res, success = methods.list_user_boxes(user_id, filter_type, number)
            elif request.method == "POST":
                res, success = methods.add_box(request.data, user_id)
            elif request.method == "PUT":
                res, success = methods.update_box(request.data)
            elif request.method == "DELETE":
                success, res = methods.delete_box(request.data, user_id)
            st = status.HTTP_201_CREATED if success else status.HTTP_401_UNAUTHORIZED
            return Response(status=st,
                            data={'success': success, 'data': res})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={'message': "User not found", 'success': False})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'message': "User not found", 'success': False})


@login_required
@api_view(["GET"])
def list_all_boxes(request, user_id):
    try:
        number = request.GET.get('number', 0)
        filter_type = request.GET.get('filter_type', '')
        res, success = methods.list_all_boxes(user_id, filter_type, number)
        st = status.HTTP_201_CREATED if success else status.HTTP_401_UNAUTHORIZED
        return Response(status=st,
                        data={'success': success, 'data': res})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'message': "User not found", 'success': False})
