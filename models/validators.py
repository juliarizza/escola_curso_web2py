# -*- coding: utf-8 -*-

## tabelas de notas
Notas.aluno.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s %(last_name)s', zero='Selecione um')
Notas.professor.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s %(last_name)s', zero='Selecione um')

## tabela de biblioteca
Biblioteca.arquivo.requires = IS_UPLOAD_FILENAME(extension='pdf')
Biblioteca.professor.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s %(last_name)s', zero='Selecione um')

## tabela de forum
Forum.mensagem.requires = IS_NOT_EMPTY(error_message='Não pode estar vazio!')

## tabela de comentarios
Comentarios.mensagem.requires = IS_NOT_EMPTY()
Comentarios.postagem.requires = IS_IN_DB(db, 'forum.id', '%(mensagem)s', zero='Selecione um')