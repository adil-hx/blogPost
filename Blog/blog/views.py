from click import CommandCollection
from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, starRating
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/privacypolicy")
def privacyPolicy():
    return render_template("privacypolicy.html", user=current_user)

@views.route("/loginerror")
def loginError():
    return render_template("login_error.html", user=current_user)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')
        shortdescription = request.form.get('shortdescription')
        
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, title=title, shortdescription=shortdescription, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        for comment in post.comments:
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/rate-post/<post_id>", methods=['GET', 'POST'])
@login_required
def ratingpost(post_id):
    post = Post.query.filter_by(id=post_id)
    ratingpost = starRating.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        flash('Post does not exist', category='error')
    elif starRating:
        db.session.delete(ratingpost)
        db.session.commit()
    else:
        ratingpost = starRating(author=current_user.id, post_id=post_id)
        db.session.add(ratingpost)
        db.session.commit()

    return redirect(url_for('views.home'))




    