from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Adds image and video upload fields to the Post model.
    Both fields are optional (blank=True, null=True) so existing text-only
    posts are unaffected.
    """

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # ImageField stores the file path in the DB; actual file goes to MEDIA_ROOT/posts/images/
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/images/'),
        ),
        # FileField is used for videos to avoid the Pillow dependency for validation
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='posts/videos/'),
        ),
        # Make content optional so users can post media-only
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
