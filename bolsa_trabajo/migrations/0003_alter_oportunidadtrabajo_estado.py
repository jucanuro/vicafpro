# Generated by Django 4.2.20 on 2025-05-27 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bolsa_trabajo", "0002_oportunidadtrabajo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="oportunidadtrabajo",
            name="estado",
            field=models.CharField(
                choices=[
                    ("publicado", "Publicado"),
                    ("pendiente", "Pendiente"),
                    ("finalizado", "Finalizado"),
                ],
                default="publicado",
                max_length=20,
            ),
        ),
    ]
