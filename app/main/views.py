# coding:utf8

from flask import render_template, redirect, url_for, flash, current_app, abort, request, make_response
from flask.ext.login import login_required, current_user
from ..decorators import admin_required, permission_required
from . import main
from .forms import *
from .. import db
from ..models import *
from ..email import send_email


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    logs = Logger.query.order_by(Logger.logtime.desc()).all()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.position = form.position.data
        current_user.qq = form.qq.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'提交成功!')
        return redirect(url_for('main.edit_profile', username=current_user.username, logs=logs))

    form.name.data = current_user.name
    form.username.data = current_user.username
    form.position.data = current_user.position
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.qq.data = current_user.qq
    form.phone.data = current_user.phone
    return render_template('edit_profile.html', form=form, username=current_user.username, logs=logs)


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')



########################################################################



@main.route('/show-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_virtmachine(id):
    if id != 0:
        virtMachine = DevicePools.query.get_or_404(id).devices.all()
    else:
        virtMachine = VirtMachine.query.all()
    return render_template('show_virtmachine.html', virtMachine=virtMachine)


@main.route('/create-device.virtmachine', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_virtmachine():
    form = EditVritMachineForm()
    if form.validate_on_submit():
        virtMachine = VirtMachine()
        virtMachine.deviceType = form.deviceType.data
        virtMachine.onstatus = form.onstatus.data
        virtMachine.usedept = form.usedept.data
        virtMachine.usestaff = form.usestaff.data
        virtMachine.mainuses = form.mainuses.data
        virtMachine.managedept = form.managedept.data
        virtMachine.managestaff = form.managestaff.data
        virtMachine.pool = DevicePools.query.get(form.pool.data)
        virtMachine.hostname = form.hostname.data
        virtMachine.os = form.os.data
        virtMachine.cpumodel = form.cpumodel.data
        virtMachine.cpucount = form.cpucount.data
        virtMachine.memsize = form.memsize.data
        virtMachine.disksize = form.disksize.data
        virtMachine.business = form.business.data
        virtMachine.powerstatus = form.powerstatus.data
        virtMachine.remarks = form.remarks.data

        try:
            db.session.add(virtMachine)
            db.session.commit()
            flash(u'虚拟机添加完成!')
        except:
            db.session.rollback()
            flash(u'虚拟机添加失败!')

        return redirect(url_for('main.show_virtmachine', id=virtMachine.deviceType))

    return render_template('create_virtmachine.html', form=form)


@main.route('/edit-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_virtmachine(id):
    virtMachine = VirtMachine.query.get_or_404(id)
    form = EditVritMachineForm()
    if form.validate_on_submit():
        virtMachine.deviceType = form.deviceType.data
        virtMachine.onstatus = form.onstatus.data
        virtMachine.usedept = form.usedept.data
        virtMachine.usestaff = form.usestaff.data
        virtMachine.mainuses = form.mainuses.data
        virtMachine.managedept = form.managedept.data
        virtMachine.managestaff = form.managestaff.data
        virtMachine.device_id = form.device_id.data
        virtMachine.pool = DevicePools.query.get(form.pool.data)
        virtMachine.hostname = form.hostname.data
        virtMachine.os = form.os.data
        virtMachine.cpumodel = form.cpumodel.data
        virtMachine.cpucount = form.cpucount.data
        virtMachine.memsize = form.memsize.data
        virtMachine.disksize = form.disksize.data
        virtMachine.business = form.business.data
        virtMachine.powerstatus = form.powerstatus.data
        virtMachine.remarks = form.remarks.data

        try:
            db.session.add(virtMachine)
            db.session.commit()
            flash(u'设备添加完成!')
        except:
            db.session.rollback()
            flash(u'设备添加失败!')

        return redirect(url_for('main.show_virtmachine', id=virtMachine.deviceType))

    form.deviceType.data = virtMachine.deviceType
    form.onstatus.data = virtMachine.onstatus
    form.usedept.data = virtMachine.usedept
    form.usestaff.data = virtMachine.usestaff
    form.mainuses.data = virtMachine.mainuses
    form.managedept.data = virtMachine.managedept
    form.managestaff.data = virtMachine.managestaff
    form.device_id.data = virtMachine.device_id
    form.pool.data = virtMachine.pool
    form.hostname.data = virtMachine.hostname
    form.os.data = virtMachine.os
    form.cpumodel.data = virtMachine.cpumodel
    form.cpucount.data = virtMachine.cpucount
    form.memsize.data = virtMachine.memsize
    form.disksize.data = virtMachine.disksize
    form.business.data = virtMachine.business
    form.powerstatus.data = virtMachine.powerstatus
    form.remarks.data = virtMachine.remarks

    return render_template('edit_virtmachine.html', form=form, virtMachine=virtMachine)


@main.route('/delete-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_virtmachine(id):
    virtMachine = VirtMachine.query.get_or_404(id)

    try:
        db.session.delete(virtMachine)
        flash(u'虚拟机: {0} 已删除!'.format(virtMachine.hostname))
    except:
        db.session.rollback()
        flash(u'虚拟机: {0} 删除失败!'.format(virtMachine.hostname))

    return redirect(url_for('main.show_virtmachine', id=virtMachine.deviceType))

########################################################################



@main.route('/xxx')
def xxx():
    return render_template('xxx.html')


# @main.route('/test', methods=['GET', 'POST'])
# @login_required
# def test():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         current_user.name = form.name.data
#         current_user.username = form.username.data
#         current_user.qq = form.qq.data
#         current_user.phone = form.phone.data
#         current_user.location = form.location.data
#         current_user.about_me = form.about_me.data
#         db.session.add(current_user)
#         flash(u'提交成功!')
#         return redirect(url_for('main.test',username=current_user.username))
#
#     form.name.data = current_user.name
#     form.username.data = current_user.username
#     form.location.data = current_user.location
#     form.about_me.data = current_user.about_me
#     form.qq.data = current_user.qq
#     form.phone.data = current_user.phone
#     return render_template('test.html',form=form)
#


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data

        try:
            db.session.add(user)
            db.session.commit()
            flash(u'修改资料成功!')
        except:
            db.session.rollback()
            flash(u'修改资料失败!')


        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


# print url_for('index')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For Administrators!'


@main.route('/moderator')
@login_required
@permission_required(Permission.ADMINISTER)
def for_moderators_only():
    return 'For moderators!'


if __name__ == '__main__':
    manager.run()
