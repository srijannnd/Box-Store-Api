from api import helpers
from api.models import Box, User
import jwt
from api.filters import box_filters, staff_user_params, user_params


def create_user(data):
    data['password'] = helpers.convert_password_to_md5(data['password'])
    try:
        if User.objects.filter(username=data['username']).exists():
            return "Username Already Exists", False
        elif User.objects.filter(email=data['email']).exists():
            return "Email Already Exists", False
        else:
            User.objects.create(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
                email=data['email'],
                is_staff=data['is_staff']
            )
            user_details = User.objects.get(username=data['username'])
            token = jwt.encode({'id': user_details.id}, 'box-api',
                               algorithm='HS256')
            return {
                "user_id": user_details.id,
                "first_name": user_details.first_name,
                "is_staff": user_details.is_staff,
                "token": token}, True
    except Exception as e:
        print(e)
        return str(e)


def validate_login_data(data):
    username = data['username']
    password = data['password']
    error_messages = []
    res = None
    password_md5 = helpers.convert_password_to_md5(password)
    if User.objects.filter(username=username, password=password_md5).exists():
        user_details = User.objects.get(username=username)
        token = jwt.encode({'id': user_details.id}, 'box-api',
                           algorithm='HS256')
        res = {
                "user_id": user_details.id,
                "first_name": user_details.first_name,
                "is_staff": user_details.is_staff,
                "token": token}
    else:
        error_messages.append("Oops!! Username and Password do not match")
    return res, error_messages


def add_box(data, user_id):
    Box.objects.create(
        length=data['length'],
        width=data['width'],
        height=data['height'],
        created_by_id=user_id
    )
    return list_user_boxes(user_id, filter_type='', number=0)


def update_box(data):
    box = Box.objects.get(pk=data['box_id'])
    box.length = data['length'] if 'length' in data else box.length
    box.width = data['width'] if 'width' in data else box.width
    box.height = data['height'] if 'height' in data else box.height
    box.save()
    res = {'length': box.length,
           'width': box.width,
           'height': box.height,
           'area': box.area,
           'volume': box.volume}
    return res, True


def list_user_boxes(user_id, filter_type, number):
    kwargs = {
        box_filters[filter_type]: number
    } if filter_type else {}
    boxes = Box.objects.filter(**kwargs, created_by_id=user_id).values(*staff_user_params).order_by('-created_at')
    return boxes, True


def list_all_boxes(user_id, filter_type, number):
    user = User.objects.get(pk=user_id)
    kwargs = {
        box_filters[filter_type]: number
    } if filter_type else {}
    boxes = Box.objects.filter(**kwargs)
    if user.is_staff:
        boxes = boxes.values(*staff_user_params).order_by('-created_at')
    else:
        boxes = boxes.values(*user_params).order_by('-created_at')
    return boxes, True


def delete_box(data, user_id):
    success = False
    box = Box.objects.filter(pk=data['id'])
    if len(box) > 0 and box[0].created_by_id == user_id:
        box[0].delete()
        success = True
    boxes = list_user_boxes(user_id, filter_type='', number=0)
    return success, boxes[0]
