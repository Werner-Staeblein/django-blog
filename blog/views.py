from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
import time
import cloudinary
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
    
        print("received a post request")
        
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
    
    comment_form = CommentForm()

    print("About to render the template")

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form
        },
    )


def comment_edit(request, slug, comment_id):
    """ view to edit comments """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """view to delete comment"""

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def upload_to_cloudinary(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        file_to_upload = request.FILES['file']

        timestamp = str(int(time.time()))  # Ensure this timestamp is correct
        print(f"DEBUG: Timestamp used: {timestamp}")

        signature = cloudinary.utils.api_sign_request(
            {'timestamp': timestamp, 'type': 'upload'},
            cloudinary.config().api_secret
        )
        print(f"DEBUG: Generated Signature: {signature}")

        try:
            result = cloudinary.uploader.upload(
                file_to_upload,
                signature=signature,
                timestamp=timestamp,
                type='upload'
            )
            print(f"DEBUG: Cloudinary Response: {result}")

            # Assuming you have a field in your Post model to store the Cloudinary public ID
            post.image_public_id = result['public_id']
            post.save()

            messages.add_message(request, messages.SUCCESS, 'Image uploaded successfully!')

        except Exception as e:
            # Handle exception
            print(f"Error uploading to Cloudinary: {e}")
            messages.add_message(request, messages.ERROR, 'Error uploading image to Cloudinary')

    return render(request, 'upload_form.html', {'post': post})
