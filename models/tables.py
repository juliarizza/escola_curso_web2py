# -*- coding: utf-8 -*-

Notas = db.define_table('notas',
	Field('nota', 'float', default=0, label="Nota"),
	Field('aluno', 'reference auth_user', notnull=True, label="Aluno"),
	Field('professor', 'reference auth_user', ondelete='SET NULL', label="Professor")
)

Biblioteca = db.define_table('biblioteca',
	Field('arquivo', 'upload', notnull=True, label="Arquivo"),
	Field('professor', 'reference auth_user', ondelete='SET NULL', label="Professor")
)

Forum = db.define_table('forum',
	Field('mensagem', 'text', notnull=True, label="Mensagem", widget=ckeditor.widget),
	auth.signature
)

Comentarios = db.define_table('comentarios',
	Field('mensagem', 'text', notnull=True, label="Mensagem", widget=ckeditor.widget),
	Field('postagem', 'reference forum', label="Postagem"),
	auth.signature
)