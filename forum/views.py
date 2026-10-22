from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Category, Forum, Topic, Post
from .forms import TopicForm, PostForm


def is_moderator(user):
    """
    True if the user can moderate (lock/delete).
    - Staff / Forum Admins can moderate.
    - Users in the "Moderator" group can moderate (even if not staff).
    """
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return user.groups.filter(name='Moderator').exists()


def is_forum_admin(user):
    """
    True if the user should see the Admin link and can enter the ACP.
    """
    if not user.is_authenticated:
        return False
    return user.is_staff or user.is_superuser


def home(request):
    """
    Home page: list of categories and their forums.
    Guests see only public forums (is_restricted=False).
    """
    categories = Category.objects.prefetch_related('forums').all()

    if not request.user.is_authenticated:
        for category in categories:
            category.public_forums = category.forums.filter(is_restricted=False)
    else:
        for category in categories:
            category.public_forums = category.forums.all()

    return render(request, 'forum/home.html', {'categories': categories})


def forum_detail(request, slug):
    """
    Forum page: list of topics in this forum (paginated).
    """
    forum = get_object_or_404(Forum, slug=slug)

    if forum.is_restricted and not request.user.is_authenticated:
        return render(request, 'forum/forbidden.html', status=403)

    topics = forum.topics.all()
    paginator = Paginator(topics, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/forum_detail.html', {
        'forum': forum,
        'page_obj': page_obj,
    })


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if topic.forum.is_restricted and not request.user.is_authenticated:
        return render(request, 'forum/forbidden.html', status=403)

    posts = topic.posts.all()
    paginator = Paginator(posts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle reply submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to reply.")
            return redirect('accounts:login')

        if topic.is_locked:
            messages.error(request, "This topic is locked. No new replies can be added.")
            return redirect('forum:topic_detail', pk=topic.pk)

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            topic.last_post_at = post.created_at
            topic.save(update_fields=['last_post_at'])
            messages.success(request, "Reply posted.")
            return redirect('forum:topic_detail', pk=topic.pk)
    else:
        form = PostForm()

    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'page_obj': page_obj,
        'form': form,
        'can_moderate': is_moderator(request.user),
    })


@login_required
def create_topic(request, slug):
    forum = get_object_or_404(Forum, slug=slug)

    if forum.is_restricted and not request.user.is_authenticated:
        return render(request, 'forum/forbidden.html', status=403)

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(forum=forum, author=request.user)
            messages.success(request, "Topic created successfully.")
            return redirect('forum:topic_detail', pk=topic.pk)
    else:
        form = TopicForm()

    return render(request, 'forum/topic_form.html', {
        'form': form,
        'forum': forum,
    })


@login_required
@require_POST
def toggle_lock(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if not is_moderator(request.user):
        return HttpResponseForbidden("You do not have permission to lock/unlock topics.")

    topic.is_locked = not topic.is_locked
    topic.save(update_fields=['is_locked'])
    status = "locked" if topic.is_locked else "unlocked"
    messages.success(request, f"Topic {status}.")
    return redirect('forum:topic_detail', pk=topic.pk)


@login_required
@require_POST
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    topic = post.topic

    if not is_moderator(request.user):
        return HttpResponseForbidden("You do not have permission to delete posts.")

    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('forum:topic_detail', pk=topic.pk)


@login_required
@require_POST
def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    forum = topic.forum

    if not is_moderator(request.user):
        return HttpResponseForbidden("You do not have permission to delete topics.")

    topic.delete()
    messages.success(request, "Topic deleted.")
    return redirect('forum:forum_detail', slug=forum.slug)


@login_required
def confirm_delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not is_moderator(request.user):
        return HttpResponseForbidden("You do not have permission to delete posts.")
    return render(request, 'forum/confirm_delete_post.html', {'post': post})


@login_required
def confirm_delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if not is_moderator(request.user):
        return HttpResponseForbidden("You do not have permission to delete topics.")
    return render(request, 'forum/confirm_delete_topic.html', {'topic': topic})