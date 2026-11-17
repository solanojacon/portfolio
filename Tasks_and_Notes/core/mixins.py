"""Ownership rules shared by the tasks and notes apps.

Every list, task and note belongs to one user. These mixins make sure a user
can only see and change their own objects, whatever ids they send.
"""

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerQuerysetMixin(LoginRequiredMixin):
    """Limit a view to objects owned by the logged-in user.

    Objects of other users are simply not found (404), so trying ids reveals
    nothing about them.
    """

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OwnerFormMixin(LoginRequiredMixin):
    """Pass the logged-in user to the form and make them the owner on save.

    The owner never comes from the submitted data.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
