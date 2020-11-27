# Generated by Django 3.1.3 on 2020-11-16 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Имя класса')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Имя группы')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='handler.classroom', verbose_name='Класс')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Имя учителя')),
                ('phone', models.PositiveIntegerField(verbose_name='Номер учителя')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Имя ученика')),
                ('lastname', models.CharField(max_length=120, verbose_name='Фамилия ученика')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='handler.group', verbose_name='Группа')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('positive', models.TextField(verbose_name='Положительные стороны')),
                ('negative', models.TextField(verbose_name='Отрицательные стороны')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='handler.student', verbose_name='Ученик')),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='handler.teacher', verbose_name='Учитель'),
        ),
    ]