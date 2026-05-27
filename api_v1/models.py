from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    country = models.CharField(max_length=100, verbose_name='Страна')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Сайт')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('prescription', 'Рецептурный'),
        ('otc', 'Без рецепта'),
    ]
    
    name = models.CharField(max_length=255, verbose_name='Название')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='medicines')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='otc')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock_quantity = models.IntegerField(default=0, verbose_name='На складе')
    expiration_date = models.DateField(verbose_name='Срок годности')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(verbose_name='Количество')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    customer_name = models.CharField(max_length=255, verbose_name='Клиент')
    customer_phone = models.CharField(max_length=20, verbose_name='Телефон')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.medicine.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ #{self.id}"