# Generated by Django 4.0.3 on 2022-12-06 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tliublog', '0005_article_is_hot_article_pageview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
    ]
