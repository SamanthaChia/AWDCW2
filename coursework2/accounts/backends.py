from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class InsensitiveCaseModelBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get(**{UserModel.USERNAME_FIELD__iexact: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user