from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Post, Comment, Like, Follow
from .forms import RegisterForm, PostForm, CommentForm


# ─── Authentication ───────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Feed ─────────────────────────────────────────────────────────────────────

@login_required
def feed_view(request):
    # Show posts from users the current user follows + own posts
    following_ids = request.user.following.values_list('following_id', flat=True)
    posts = Post.objects.filter(
        author_id__in=list(following_ids) + [request.user.id]
    ).select_related('author').prefetch_related('likes', 'comments')

    # IDs of posts the current user has liked (for toggling UI)
    liked_post_ids = set(
        Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    )

    post_form = PostForm()

    if request.method == 'POST':
        # Pass request.FILES so image/video uploads are processed
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('feed')

    context = {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'post_form': post_form,
        'comment_form': CommentForm(),
    }
    return render(request, 'core/feed.html', context)


# ─── Profile ──────────────────────────────────────────────────────────────────

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).select_related('author')

    liked_post_ids = set(
        Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    )

    is_following = Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'comment_form': CommentForm(),
    }
    return render(request, 'core/profile.html', context)


# ─── Posts ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ─── Comments ─────────────────────────────────────────────────────────────────

@login_required
@require_POST
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ─── Likes ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.like_count()})


# ─── Follow ───────────────────────────────────────────────────────────────────

@login_required
@require_POST
def toggle_follow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=target_user
    )
    if not created:
        follow.delete()
        following = False
    else:
        following = True

    followers_count = target_user.followers.count()
    return JsonResponse({'following': following, 'followers_count': followers_count})


# ─── Explore (all users) ──────────────────────────────────────────────────────

@login_required
def explore_view(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')
    following_ids = set(
        request.user.following.values_list('following_id', flat=True)
    )
    context = {
        'users': users,
        'following_ids': following_ids,
    }
    return render(request, 'core/explore.html', context)
