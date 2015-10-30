# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Hello world, web2py course!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def contato():
    form = SQLFORM.factory(
            Field('nome', requires=IS_NOT_EMPTY()),
            Field('email', requires=IS_EMAIL()),
            Field('mensagem', 'text', requires=IS_NOT_EMPTY())
            )
    if form.process().accepted:
        mail.send(
            to="julia.rizza@gmail.com",
            reply_to=form.vars.email,
            subject="Novo contato pelo site",
            message="Contato de %s pelo site, dizendo: %s" % (form.vars.nome, form.vars.mensagem)
        )
        session.flash = "Mensagem recebida!"
        redirect(URL('index'))
    elif form.errors:
        response.flash = "Erros no formulário!"
    else:
        response.flash = "Preencha o formulário!"
    return dict(form=form)

@auth.requires_permission('criar')
def inserir_notas():
    nota = request.vars.nota
    aluno = request.vars.aluno
    professor = request.vars.professor
    try:
        Notas.insert(nota=nota, aluno=aluno, professor=professor)
    except:
        session.flash = "Não pôde inserir!"
        redirect(URL('index'))
    return dict()

@auth.requires_login()
def ver_notas():
    try:
        pag = int(request.vars.pagina)
    except TypeError:
        redirect(URL('ver_notas', vars={'pagina':1}))

    inicio = (pag-1)*5
    fim = pag*5

    session.busca = session.busca or 0

    if request.post_vars.busca:
        session.busca = int(request.post_vars.busca)

    total_notas = db(Notas.nota >= session.busca).count()
    notas = db(Notas.nota >= session.busca).select(limitby=(inicio,fim))

    if pag <= 0:
        redirect(URL('ver_notas', vars={'pagina':1}))
    elif total_notas % 5 == 0 and total_notas != 0:
        redirect(URL('ver_notas', vars={'pagina':total_notas/5}))
    elif pag > (total_notas/5 + 1):
        redirect(URL('ver_notas', vars={'pagina':total_notas/5 + 1}))

    return dict(notas=notas, total_notas=total_notas)

@auth.requires_membership('Professor')
def atualizar_notas():
    db(Notas.id > 0).update(nota=9.0)
    redirect(URL('ver_notas'))

@auth.requires_membership('Professor')
def apagar_notas():
    db(Notas.id > 0).delete()
    redirect(URL('ver_notas'))

def nova_mensagem():
    form = SQLFORM(Forum)
    if form.process().accepted:
        session.flash = "Sucesso!"
        redirect(URL('forum'))
    elif form.errors:
        response.flash = "Erros no formulário!"
    else:
        response.flash = "Preencha o formulário!"
    return dict(formulario=form)

def ver_mensagem():
    id_mensagem = request.args(0, cast=int)
    mensagem = db(Forum.id == id_mensagem).select().first()
    
    Comentarios.postagem.default=id_mensagem
    Comentarios.postagem.writable = Comentarios.postagem.readable = False
    form = crud.create(Comentarios)
    comentarios = db(Comentarios.postagem == id_mensagem).select()
    
    return dict(mensagem=mensagem, form=form, comentarios=comentarios)

def forum():
    response.title += " - Fórum"
    mensagens = db(Forum.id > 0).select(cache=(cache.ram, 300))
    return dict(mensagens=mensagens)

def atualizar_mensagem():
    id_mensagem = request.args(0, cast=int)
    form = SQLFORM(Forum, id_mensagem, showid=False)
    if form.process().accepted:
        session.flash = "Sucesso!"
        redirect(URL('ver_mensagem', args=[id_mensagem]))
    elif form.errors:
        response.flash = "Erros no formulário!"
    else:
        response.flash = "Preencha o formulário!"
    return dict(form=form)

def apagar_mensagem():
    id_mensagem = request.args(0, cast=int)
    db(Forum.id == id_mensagem).delete()
    session.flash = "Mensagem apagada!"
    redirect(URL('forum'))

@auth.requires_login()
def novo_arquivo():
    Biblioteca.professor.default = auth.user.id
    Biblioteca.professor.writable = Biblioteca.professor.readable = False
    form = crud.create(Biblioteca)
    return dict(form=form)

def editar_arquivo():
    id_arquivo = request.args(0, cast=int)
    form = crud.update(Biblioteca, id_arquivo)
    return dict(form=form)

def exibir_arquivos():
    arquivos = db(Biblioteca.id > 0).select()
    return dict(arquivos=arquivos)