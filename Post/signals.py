from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User



@receiver(post_save, sender=Post)
def post_save_send_email(sender, instance , created, *args, **kwargs):
    
    if created:        
        user_email =  instance.author.email
        mail_subject = "New Post Created"
        message = "A new post has been successfully created."
        to_send_email = user_email

        try:
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_send_email],
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending email: {str(e)}")