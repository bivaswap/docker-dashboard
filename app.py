import docker
from flask import Flask, render_template
from string import split

app = Flask(__name__)

def sizeof(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

app.add_template_global(len, name='len')
app.add_template_global(str, name='str')
app.add_template_global(split, name='split')
app.add_template_global(sizeof, name='sizeof')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/instances/')
def instances():
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    data = client.containers.list('all')
    return render_template('instances.html', data=data)

@app.route('/images/')
def images():
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    images = client.images.list()
    return render_template('images.html', images=images)

@app.route('/search/<sTerm>')
def search(sTerm):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    search = client.images.search(sTerm)
    return render_template('search.html', search=search)

if __name__ == '__main__':
    app.run(debug=True)