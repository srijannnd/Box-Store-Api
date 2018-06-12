import jwt
import hashlib
from api.models import User


def convert_password_to_md5(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def login_status(token):
    data = jwt.decode(token, 'box-api', algorithms=['HS256'])
    flag = User.objects.filter(pk=data['id']).exists()
    return flag, data['id']


def login_required(f):
    def wrap(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            flag, user_id = login_status(token)
            if flag:
                return f(request, user_id)
            else:
                return f(request, None)
        except Exception as e:
            print(e)
            return f(request, None)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
