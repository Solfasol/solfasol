# Generated by Django 3.0.7 on 2020-07-03 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contributors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(unique=True)),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True, verbose_name='subtitle')),
                ('lang', models.CharField(choices=[('tr', 'Turkish'), ('en', 'English')], default='tr', max_length=7, verbose_name='language')),
                ('image', models.ImageField(upload_to='content/', verbose_name='image')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='video url')),
                ('podcast', models.URLField(blank=True, null=True, verbose_name='podcast url')),
                ('publish', models.BooleanField(default=False, verbose_name='publish')),
                ('featured', models.BooleanField(default=False, verbose_name='featured')),
                ('pinned', models.BooleanField(default=False, verbose_name='pinned')),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('view_count', models.PositiveIntegerField(default=0, editable=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'content',
                'verbose_name_plural': 'content',
                'ordering': ('-pinned', '-added'),
            },
        ),
        migrations.CreateModel(
            name='ContentSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(choices=[('t', 'text'), ('s', 'spot'), ('i', 'image')], default='t', max_length=1)),
                ('section_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='section title')),
                ('body', models.TextField(blank=True, null=True, verbose_name='section text')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Content', verbose_name='content')),
            ],
            options={
                'verbose_name': 'content section',
                'verbose_name_plural': 'content sections',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ContributionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20, verbose_name='description')),
                ('primary', models.BooleanField(default=False, verbose_name='primary')),
            ],
            options={
                'verbose_name': 'contribution type',
                'verbose_name_plural': 'contribution types',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'series',
                'verbose_name_plural': 'series',
            },
        ),
        migrations.CreateModel(
            name='ContentSectionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='content_images/', verbose_name='image')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='description')),
                ('content_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.ContentSection', verbose_name='section image')),
            ],
            options={
                'verbose_name': 'section image',
                'verbose_name_plural': 'section images',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ContentContributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Content', verbose_name='content')),
                ('contribution_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.ContributionType', verbose_name='contribution type')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contributors.Contributor', verbose_name='contributor')),
            ],
            options={
                'verbose_name': 'content - contributor',
                'verbose_name_plural': 'content - contributors',
            },
        ),
        migrations.AddField(
            model_name='content',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='content_set', through='content.ContentContributor', to='contributors.Contributor', verbose_name='contributor'),
        ),
        migrations.AddField(
            model_name='content',
            name='issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='issues.Issue', verbose_name='issue'),
        ),
        migrations.AddField(
            model_name='content',
            name='pages',
            field=models.ManyToManyField(blank=True, to='issues.Page', verbose_name='page'),
        ),
        migrations.AddField(
            model_name='content',
            name='published_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='published by'),
        ),
        migrations.AddField(
            model_name='content',
            name='related_content',
            field=models.ManyToManyField(blank=True, related_name='_content_related_content_+', to='content.Content', verbose_name='related content'),
        ),
        migrations.AddField(
            model_name='content',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Series', verbose_name='series'),
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tags.Tag', verbose_name='tags'),
        ),
    ]
