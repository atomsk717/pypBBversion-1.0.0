from django import forms
from .models import Topic, Post


class TopicForm(forms.ModelForm):
    """
    Form for creating a new topic.
    The first post of the topic is created together with the topic.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8}),
        label="Message"
    )

    class Meta:
        model = Topic
        fields = ['title']

    def save(self, commit=True, forum=None, author=None):
        topic = super().save(commit=False)
        if forum:
            topic.forum = forum
        if author:
            topic.author = author
        if commit:
            topic.save()
            # Create the first post
            Post.objects.create(
                topic=topic,
                author=author,
                content=self.cleaned_data['content']
            )
        return topic


class PostForm(forms.ModelForm):
    """
    Form for replying to an existing topic.
    """
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }
        labels = {
            'content': 'Your reply',
        }