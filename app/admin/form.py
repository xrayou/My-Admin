# coding: utf-8
from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.modles import User

record_type = [(0, 'A'), (1, 'NS'), (2, 'CNAME'), (3, 'MX')]
host_type = [(0, 'hk.zhxfei.com'), (1, 'sh.zhxfei.com'), (2, 'hkweb.zhxfei.com'), (3, 'qd.zhxfei.com')]


class UserLoginForm(FlaskForm):
    account = StringField(label='账号',
                          validators=[DataRequired('请输入账号!'), ],
                          description='账号',
                          render_kw={
                              'class': "form-control",
                              'placeholder': "请输入账号！", 'required': 'required'
                          }
                          )
    password = PasswordField(label='密码',
                             validators=[DataRequired('请输入密码'), ],
                             description='密码',
                             render_kw={
                                 'class': "form-control",
                                 'placeholder': "请输入密码！", 'required': 'required'
                             }
                             )
    submit = SubmitField(label='登录',
                         render_kw={
                             'class': 'btn btn-primary btn-block btn-flat',
                             'id': "btn-sub"
                         }
                         )

    def validate_account(self, field):
        account = field.data
        users = User.query.filter_by(name=account).count()
        if users == 0:
            raise ValidationError('账号不存在！')


class PwdForm(FlaskForm):
    old_pwd = PasswordField(label='旧密码',
                            validators=[DataRequired('请输入旧密码'), ],
                            description='旧密码',
                            render_kw={
                                'style': 'width: 300px',
                                'class': "form-control",
                                'id': 'input_pwd',
                                'placeholder': "请输入旧密码！", 'required': 'required'
                            }
                            )

    new_pwd = PasswordField(label='新密码',
                            validators=[DataRequired('请输入新密码'), ],
                            description='新密码',
                            render_kw={
                                'style': 'width: 300px',
                                'class': "form-control",
                                'id': 'input_newpwd',
                                'placeholder': "请输入新密码！", 'required': 'required'
                            }
                            )

    submit = SubmitField(
        label='修改',
        render_kw={
            'class': 'btn btn-primary',
            'id': "btn-sub"
        }
    )

    def validate_old_pwd(self, field):
        input_old_pwd = field.data
        name = session['admin']
        admin = User.query.filter_by(name=name).first()
        if not admin.check_pwd(input_old_pwd):
            raise ValidationError('旧密码输入错误！')


class RecordAddForm(FlaskForm):
    name = StringField(label='记录名称',
                       validators=[DataRequired('记录名!'), ],
                       description='record name',
                       render_kw={
                           'style': "width: 80px; margin: auto; text-align:center",
                           'required': 'required'
                       }
                       )
    value = StringField(label='value',
                        validators=[DataRequired('value!'), ],
                        description='record value',
                        render_kw={
                            'style': "width: 80px; margin: auto; text-align:center",
                            'required': 'required'
                        }
                        )
    type = SelectField(
        label='record type',
        description='record type',
        coerce=int,
        choices=record_type,
        render_kw={
            'style': 'width: 80px; margin: auto;',
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary btn-sm',
            'id': "btn-sub"
        }
    )


class CommandCommitForm(FlaskForm):
    host = SelectMultipleField(
        label='主机',
        description='command will be execute in hosts',
        coerce=int,
        choices=host_type,
        render_kw={
            'class': 'form-control',
            'id': 'select_host',
            'data - placeholder': "Select Host",
            'style': 'width: 30%'
        }
    )

    content = StringField(label='command content',
                          validators=[DataRequired('请输入执行命令!'), ],
                          description='record name',
                          render_kw={
                              'class': "form-control",
                              'style': 'width: 50%'
                          }
                          )
    submit = SubmitField(
        label='Send command',
        render_kw={
            'class': ' btn btn-default',
            'id': "btn-sub",
            'type': "submit"
        }
    )
    result = TextAreaField(
        label='执行结果',
        render_kw={
            'class': "form-control",
            'placeholder': "command execute result",
            'readonly': "True",
        }
    )

