import requests
import json
import flask
from random import choice


class GitHub:
    def __init__(self, user, repo, heroku):
        self.url = 'https://api.github.com/repos/{}/{}'.format(user, repo)
        self.user = user
        self.heroku = heroku
        self.repo = repo
        self.get_cred()
        if heroku is not None:
            self.crear_hook()

    def get_cred(self):
        with open("credentials.json") as f:
            token = json.load(f)[self.user]
        self.credentials = (self.user, token)

    def crear_hook(self, name="web"):
        url = self.url + '/hooks'
        data = {"name": name, "active": True,
                "events": ["issues", "issue_commnent", "push", "pull_request"],
                "config": {"url": self.heroku,
                           "content_type": "json"}}
        req = requests.post(url, data=json.dumps(data), auth=self.credentials)
        print(req, req.json())

    def id_hook(self):
        url = self.url + '/hooks'
        req = requests.get(url, auth=self.credentials)
        a = req.json()  # Lista de webhooks
        hook = a[0]["id"]
        return hook

    def assignee_hook(self):
        url = self.url + "/assignees"
        req = requests.get(url, auth=self.credentials)
        a = req.json()  # Lista de webhooks
        return a

    def crear_issue(self, title="test", body="<Vacio>"):
        url = self.url + '/issues'
        issue = {'title': title, "body": title}
        req = requests.post(url, data=json.dumps(issue), auth=self.credentials)

    def editar_issue(self, id):  # POR HACER
        pass

    def manejo_issue(self, d, numero_issue):
        print(d.keys())
        url_issue = "https://github.com/{}/{}/issues/{}".format(self.user,
                                                                self.repo,
                                                                numero_issue)
        title = d["title"]
        user = d["user"]["login"]
        print(d, numero_issue, "ENTRA  LIST COMMENTS")
        comentario = self.list_comments(numero_issue)
        string = '''
        Autor: {}
        Issue #{} - {}
        {}
        Link: {}
                '''.format(user, numero_issue, title, comentario, url_issue)
        return string

    def ping_hook(self):
        id = self.id_hook()
        url = self.url + '/hooks/{}/tests'.format(
            id)
        req = requests.post(url, auth=self.credentials)

    def list_comments(self, issue_id):
        # repos/:owner/:repo/issues/:number/comments
        url = "{}/issues/{}/comments".format(self.url, issue_id)
        lista = requests.get(url, auth=self.credentials).json()
        lista_string = "Comentarios: \n"
        try:
            for i in lista:
                lista_string += str(i["user"]["login"]) + " :" + str(
                    i["body"]) + "\n"
        except Exception as err:
            print(err)
            print(lista)
        return lista_string

    def get_issue_number(self, number):
        # repos/:owner/:repo/issues/:number
        url = "{}/issues/{}".format(self.url, number)

        a = requests.get(url, auth=self.credentials)
        if a.status_code is 200:
            return self.manejo_issue(a.json(), number)
        else:
            return "Numero de Issue Invalida"

            # def comentar_isse(comentario):
            #     credentials = get_cred()

            #     url =
            #     url =

    def comment_issue(self, numero):
        url = "{}/issues/{}".format(self.url, numero)

        a = requests.get(url, auth=self.credentials)

    def get(self, texto):
        texto = texto.strip()
        numerico = "".join(filter(lambda x: x in "0123456789", texto))
        if numerico == texto:
            return self.get_issue_number(int(numerico))
        else:
            return "Numero de Issue Invalida"

    def post(self, texto):
        # git_api: POST /repos/:owner/:repo/issues/:number/comments
        # input: num_issue *respuesta
        try:
            numero, *respuesta = texto.strip().split(" ")

        except Exception as err:
            return "Comentario no valido, por favor intentar de nuevo"

        url = "{}/issues/{}/comments".format(self.url, numero)
        if len(respuesta) > 1:
            respuesta = " ".join(respuesta)
        requests.post(url, json={"body": respuesta}, auth=self.credentials)
        return "Comentario publicado existosamente!" + str(respuesta)

    def close(self, texto):
        # PATCH /repos/:owner/:repo/issues/:number
        texto = texto.strip()
        numerico = "".join(filter(lambda x: x in "0123456789", texto))
        url = "{}/issues/{}".format(self.url, numerico)
        req = requests.patch(url, auth=self.credentials,
                             json={"state": "closed"})
        if req.status_code == 200:
            return "La issue {} fue cerrada exitosamente! ".format(numerico)
        else:
            return "Opps parece que la issue no existe !"

    def label(self, texto):
        try:
            numero, label = texto.strip().split(" ")
        except Exception as err:
            return "Comentario no valido, por favor intentar de nuevo"
        # GET /repos/:owner/:repo/labels/:name
        # Primero se intenta recuperar el label si esta existe
        url = "{}/labels/{}".format(self.url, label)
        aux = requests.get(url, auth=self.credentials)
        if aux.status_code is not 200:
            # Significa que este label no existe
            # Por lo tanto se crea un label nuevo
            # POST /repos/:owner/:repo/labels
            colores = ["0000ff", "ff0000", "ffd700", "00ffff", "00ff00"]
            url = "{}/labels".format(self.url)
            req = requests.post(url, auth=self.credentials, json={"name": label,
                                                                  "color": choice(
                                                                      colores)})
            if req.status_code == 201:
                # POST / repos /: owner /:repo / issues /: number / labels
                url = "{}/issues/{}/labels".format(self.url, numero)
                req = requests.post(url, auth=self.credentials, json=[label])
                if req.status_code == 200:
                    return "Label {} creado exitosamente!".format(label)

            else:
                return "Opps hubo un error"
        else:
            url = "{}/issues/{}/labels".format(self.url, numero)
            req = requests.post(url, auth=self.credentials, json=[label])
            if req.status_code == 200:
                return "Label asignado existosamente! "

    def manejar_comando(self, user_input):
        chosen_one = "other"
        comandos = {"/get": self.get, "/post": self.post,
                    "/label":
                        self.label, "/close": self.close}
        for c in comandos:
            if c in user_input:
                chosen_one = c
                break
        if chosen_one in comandos:
            return comandos[chosen_one](user_input.split(chosen_one)[1:][0])
        else:
            return "Comando no valido, por favor ingrese alguno de los " \
                   "siguientes (Con su valores respectivos):\n{}".format(
                "\n".join(map(str,
                              list(comandos.keys(

                              )))))


def git_main(server="https://stiffbot.herokuapp.com/git"):
    github_token = "b81efc5d07f3f6b0c67cb58ca309343f388bd803"
    user = 'StiffmeisterIIC233'
    with open("credentials.json", "w") as file:
        json.dump({user: github_token}, file)
    a = GitHub('StiffmeisterIIC233',
               'stiff-bot', server)
    return a

# a=git_main()
# a.crear_hook()
# a.crear_issue()
# crear_hook()
# ping_hook()
# a.ping_hook()
# id_hook()
# crear_issue()
# StiffmeisterIIC233/stiff-bot
