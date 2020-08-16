# Generated by Django 3.0.7 on 2020-08-16 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_remove_tag_related_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('=', '='), ('>', '>'), ('<', '<')], default='=', max_length=10)),
                ('related_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_reverse_set', to='tags.Tag')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='related_tags',
            field=models.ManyToManyField(blank=True, related_name='_tag_related_tags_+', through='tags.RelatedTag', to='tags.Tag', verbose_name='related tags'),
        ),
    ]
