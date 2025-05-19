from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from task_manager.models import Task


@receiver(pre_save, sender=Task)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Task.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except Task.DoesNotExist:
            pass


@receiver(post_save, sender=Task)
def notify_task_owner(sender, instance, created, **kwargs):
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status is None or old_status == instance.status:
        return

    if not hasattr(instance, 'owner') or not instance.owner.email:
        return

    if instance.status == 'Done':
        subject = 'Задача закрыта'
        message = f"Ваша задача '{instance.title}' была закрыта."
    else:
        subject = 'Статус задачи изменён'
        message = (
            f"Статус вашей задачи '{instance.title}' был изменён "
            f"с '{old_status}' на '{instance.status}'."
        )

    send_mail(
        subject=subject,
        message=message,
        from_email='no-reply@taskmanager.com',
        recipient_list=[instance.owner.email],
        fail_silently=False,
    )
