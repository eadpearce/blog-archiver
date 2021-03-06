# Generated by Django 3.1.4 on 2020-12-03 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('post_url', models.URLField()),
                ('tags', models.JSONField(blank=True, null=True)),
                ('summary', models.TextField()),
                ('source_url', models.URLField(blank=True, null=True)),
                ('content', models.JSONField(blank=True, null=True)),
                ('layout', models.JSONField(blank=True, null=True)),
                ('trail', models.JSONField(blank=True, null=True)),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.blog')),
            ],
        ),
    ]
