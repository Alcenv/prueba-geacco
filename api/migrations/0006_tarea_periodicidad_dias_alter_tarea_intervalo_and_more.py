# Generated by Django 4.2.2 on 2023-07-19 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_tarea_intervalo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='periodicidad_dias',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='intervalo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='SecuenciaTarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField()),
                ('dias_desde_anterior', models.IntegerField()),
                ('completado', models.BooleanField(default=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.documento')),
            ],
            options={
                'unique_together': {('documento', 'orden')},
            },
        ),
    ]
