from .models import Reader


# Adds reader profile to user if it's the first time person logs in
def create_reader(backend, user, response, *args, **kwargs):
    if not user.is_reader:
        user.is_reader = True
        Reader.objects.create(user=user)
        user.save()
