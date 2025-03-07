# backend/payment/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StripePayment(models.Model):
    user = models.ForeignKey(User, related_name='stripe_payments', on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=250, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=250, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.CharField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('forever', 'Forever')], max_length=10)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} - {self.status}"
    
    
class KassaPayment(models.Model):
    user = models.ForeignKey(User, related_name='kassa_payments', on_delete=models.CASCADE)
    kassa_payment_id = models.CharField(max_length=250, blank=True, null=True)
    information_payment = models.CharField(max_length=250, blank=True, null=True) # Разная информация о платеже
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.CharField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('forever', 'Forever')], max_length=10)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refund', 'Refund'), ('refund_failed', 'Refund Failed')], max_length=20, default='pending')    
    kassa_payment_status = models.CharField(
        choices=[('waiting_for_capture', 'Waiting for capture'), 
                ('succeeded', 'Succeeded'), 
                ('failed', 'Failed'),
                ('canceled', 'Canceled'),  # Добавляем статус отмены
                ('refund_succeeded', 'Refund Succeeded')],  # Статус успешного возврата
    max_length=20, 
    default='waiting_for_capture'
)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Новые поля:
    expires_at = models.DateTimeField(blank=True, null=True)
    authorization_details = models.JSONField(blank=True, null=True)  # Чтобы хранить детализированные данные о 3D Secure
    payment_method = models.JSONField(blank=True, null=True)  # Чтобы хранить информацию о способе оплаты (карта, кошелек и т.д.)
    income_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Сумма после вычета комиссии

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} - {self.status} - {self.kassa_payment_status}"

