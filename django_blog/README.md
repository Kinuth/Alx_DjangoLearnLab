# Django Blog Project

A multi-user blogging platform built with Django.

## Features
* **User Authentication:** Users can register, login, and logout.
* **CRUD Operations:** Users can Create, Read, Update, and Delete posts.
* **Permissions:** * Users can only update/delete their own posts.
    * Posts are publicly readable.

## How to Run
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run migrations: `python manage.py migrate`
4.  Start server: `python manage.py runserver`

## Data Handling
* **Author Assignment:** The `author` field is automatically populated based on the `request.user` session during post creation.

Django Blog Comment System Documentation

Overview

This module adds commenting functionality to the Django Blog, allowing authenticated users to discuss blog posts. It features full CRUD (Create, Read, Update, Delete) capabilities with permission enforcement.

1. Database Model (Comment)

The Comment model establishes the following relationships:

post: A Many-to-One relationship with the Post model. Access comments via post.comments.all().

author: A Many-to-One relationship with the User model.

Timestamps: Automatically tracks creation (created_at) and modification (updated_at) times.

To initialize:

python manage.py makemigrations
python manage.py migrate


2. Features & Workflow

Viewing Comments

Comments are displayed directly on the Post Detail page (post_detail.html). They are ordered chronologically (oldest first).

Adding a Comment

Route: /posts/<int:pk>/comment/

Permission: Login Required.

Users can click "Add Comment" on the post detail page. This redirects to a dedicated form. Upon success, they are redirected back to the post.

Editing a Comment

Route: /comment/<int:pk>/update/

Permission: Login Required + Author Only.

An "Edit" button appears next to comments owned by the current user.

Uses UserPassesTestMixin to prevent users from editing comments they didn't write via URL manipulation.

Deleting a Comment

Route: /comment/<int:pk>/delete/

Permission: Login Required + Author Only.

A "Delete" button appears next to comments owned by the current user.

Requires a confirmation step (POST request) to prevent accidental deletions.

3. Security

CSRF Protection: All forms utilize {% csrf_token %}.

Access Control:

LoginRequiredMixin ensures anonymous users cannot access edit/delete views.

UserPassesTestMixin logic verifies request.user == comment.author before allowing modification.

4. Testing

To verify functionality:

Log in as User A.

Navigate to a post and add a comment. Verify it appears.

Edit the comment. Verify the text updates.

Log out and log in as User B.

Verify User B can see User A's comment but cannot see the Edit/Delete buttons.

Try manually navigating to User A's edit URL (e.g., /comment/1/update/) while logged in as User B. You should receive a 403 Forbidden error.