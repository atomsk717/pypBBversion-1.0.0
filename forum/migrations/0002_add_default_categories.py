from django.db import migrations


def create_defaults(apps, schema_editor):
    Category = apps.get_model('forum', 'Category')
    Forum = apps.get_model('forum', 'Forum')

    # Only create defaults on a completely empty database
    if Category.objects.exists():
        return

    general = Category.objects.create(
        name='General',
        slug='general',
        description='General Discussion',
        order=1
    )
    support = Category.objects.create(
        name='Support',
        slug='support',
        description='Help and Questions',
        order=2
    )
    offtopic = Category.objects.create(
        name='Off-Topic',
        slug='off-topic',
        description='Anything Else',
        order=3
    )

    Forum.objects.create(
        category=general,
        name='Introductions',
        slug='introductions',
        description='Introduce yourself. Open for guests.',
        is_restricted=False,
        order=1
    )
    Forum.objects.create(
        category=general,
        name='General Chat',
        slug='general-chat',
        description='Everyday discussions. Open for guests.',
        is_restricted=False,
        order=2
    )
    Forum.objects.create(
        category=support,
        name='Help and Questions',
        slug='help-and-questions',
        description='Ask for help. Needs login.',
        is_restricted=True,
        order=1
    )
    Forum.objects.create(
        category=support,
        name='Bug Reports',
        slug='bug-reports',
        description='Report problems. Needs login.',
        is_restricted=True,
        order=2
    )


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_defaults, migrations.RunPython.noop),
    ]