from django.db import models


class AreaOrganizacional(models.Model):

    nombre = models.CharField(
        max_length=150
    )

    orden = models.PositiveIntegerField(
        default=1,
        help_text="Orden del área en la web"
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = "Área Organizacional"
        verbose_name_plural = "Áreas Organizacionales"

    def __str__(self):
        return f"[{self.orden}] {self.nombre}"


class Cargo(models.Model):

    area = models.ForeignKey(
        AreaOrganizacional,
        on_delete=models.PROTECT,
        related_name='cargos',
        null=True,
        blank=True
    )

    nombre = models.CharField(
        max_length=100
    )

    orden = models.PositiveIntegerField(
        default=1,
        help_text="Orden del cargo dentro del área"
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            'area__orden',
            'orden',
            'nombre'
        ]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return f"{self.area.nombre} → {self.nombre}"


class Trabajador(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name='trabajadores'
    )

    foto = models.ImageField(
        upload_to='trabajadores_fotos/'
    )

    email = models.EmailField(
        unique=True
    )

    linkedin = models.URLField(
        blank=True
    )

    orden = models.PositiveIntegerField(
        default=0,
        help_text="Orden dentro del cargo"
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            'cargo__area__orden',
            'cargo__orden',
            'orden',
            'nombre'
        ]
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    def __str__(self):
        return f"{self.nombre} - {self.cargo.nombre}"