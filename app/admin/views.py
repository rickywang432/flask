from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
#from flask_rq import get_queue

from app import db
from app.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    InviteUserForm,
    NewUserForm,
    NewRoleForm,
    NewGroupForm,
    ChangeAccountStatusForm,
    ChangeAccountGroupForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import EditableHTML, Role, User, Group

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/new-group', methods=['GET', 'POST'])
@login_required
@admin_required
def new_group():
    """Create a new user."""
    form = NewGroupForm()
    if form.validate_on_submit():
        #if form.
        group = Group(
            name=form.group_name.data,
            )
        db.session.add(group)
        db.session.commit()
        flash('Group {} successfully created'.format(group.name),
              'form-success')
    return render_template('admin/new_group.html', form=form)

@admin.route('/new-role', methods=['GET', 'POST'])
@login_required
@admin_required
def new_role():
    """Create a new user."""
    form = NewRoleForm()
    if form.validate_on_submit():
        if form.default.data is True:
            roles = Role.query.filter_by(default=True)
            for r in roles:
                r.default = False
                db.session.add(r)
            db.session.commit()
        role = Role(
            name=form.role_name.data,
            permissions=form.permission.data,
            default=form.default.data,
            )
        db.session.add(role)
        db.session.commit()
        flash('Role {} successfully created'.format(role.name),
              'form-success')
    return render_template('admin/new_role.html', form=form)

@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        if user is not None:
            user.role.append(form.role.data)
            db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            #role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        user.role.append(form.role.data)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        status = send_email(recipient=user.email,subject= 'You Are Invited To Join Us',
                            template='account/email/invite',user=user,invite_link=invite_link)
        # get_queue().enqueue(
        #     send_email,
        #     recipient=user.email,
        #     subject='You Are Invited To Join',
        #     template='account/email/invite',
        #     user=user,
        #     invite_link=invite_link,
        # )
        if status:
            flash('A new user was successfully invited','form-success')

    return render_template('admin/new_user.html', form=form)


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    roles = Role.query.all()
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    form.roles.choices = [(r.id, r.name) for r in roles]

    if request.method == 'GET':
        if user.role:
            # This is where you prepopulate
            form.roles.data = [(r.id) for r in user.role]

    if form.validate_on_submit():
        new_roles = form.roles.data
        user.role = []
        db.session.commit()
        for r in new_roles:
            add_role = Role.query.get(r)
            user.role.append(add_role)
            db.session.add(user)

        db.session.commit()
        flash('Role for user {} successfully edited .'.format(
            user.full_name()), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-group', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_group(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the group of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    groups = Group.query.all()
    if user is None:
        abort(404)
    form = ChangeAccountGroupForm()
    form.groups.choices = [(r.id, r.name) for r in groups]

    if request.method == 'GET':
        if user.role:
            # This is where you prepopulate
            form.groups.data = [(r.id) for r in user.group]

    if form.validate_on_submit():
        new_groups = form.groups.data
        user.group = []
        db.session.commit()
        for g in new_groups:
            add_group = Group.query.get(g)
            user.group.append(add_group)
            db.session.add(user)

        db.session.commit()
        flash('Group for user {} successfully edited .'.format(
            user.full_name()), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)

@admin.route(
    '/user/<int:user_id>/change-account-status', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_status(user_id):
    if current_user.id == user_id:
        flash('You cannot change the status of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))


    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountStatusForm()

    if request.method == 'GET':
        if user.active is not None:
            # This is where you prepopulate
            form.active.data = user.active

    if form.validate_on_submit():
        user.active = form.active.data
        db.session.add(user)
        db.session.commit()
        flash('Status for user {} successfully changed to {}.'.format(
            user.full_name(), user.is_active()), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)

@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))


@admin.route('/_update_editor_contents', methods=['POST'])
@login_required
@admin_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200
