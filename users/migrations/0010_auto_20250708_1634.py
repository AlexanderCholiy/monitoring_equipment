# Generated by Django 3.1.12 on 2025-07-08 13:34

import django.contrib.auth.password_validation
import django.core.validators
from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20250708_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendinguser',
            name='password',
            field=models.CharField(help_text='Пароль должен содержать минимум 8 символов, не может быть полностью числовым, не должен быть похож на имя пользователя и не должен быть слишком простым.', max_length=128, validators=[django.contrib.auth.password_validation.MinimumLengthValidator.validate, django.contrib.auth.password_validation.UserAttributeSimilarityValidator.validate, django.contrib.auth.password_validation.CommonPasswordValidator.validate, django.contrib.auth.password_validation.NumericPasswordValidator.validate]),
        ),
        migrations.AlterField(
            model_name='pendinguser',
            name='username',
            field=models.CharField(help_text='Имя пользователя должно содержать минимум 4 символов. Допустимые символы: латинские буквы, цифры и .-_', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Недопустимые символы в имени пользователя. Разрешены только: английские буквы, цифры и . - _', regex='^[a-zA-Z0-9._-]+$'), django.core.validators.MinLengthValidator(limit_value=4, message='Имя пользователя должно содержать минимум 4 символов.'), users.validators.validate_pending_username], verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Загрузите аватар пользователя в формате JPG или PNG', null=True, upload_to='users/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Пароль должен содержать минимум 8 символов, не может быть полностью числовым, не должен быть похож на имя пользователя и не должен быть слишком простым.', max_length=128, validators=[django.contrib.auth.password_validation.MinimumLengthValidator.validate, django.contrib.auth.password_validation.UserAttributeSimilarityValidator.validate, django.contrib.auth.password_validation.CommonPasswordValidator.validate, django.contrib.auth.password_validation.NumericPasswordValidator.validate]),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Имя пользователя должно содержать минимум 4 символов. Допустимые символы: латинские буквы, цифры и .-_', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Недопустимые символы в имени пользователя. Разрешены только: английские буквы, цифры и . - _', regex='^[a-zA-Z0-9._-]+$'), django.core.validators.MinLengthValidator(limit_value=4, message='Имя пользователя должно содержать минимум 4 символов.'), users.validators.validate_user_username], verbose_name='Имя пользователя'),
        ),
    ]
