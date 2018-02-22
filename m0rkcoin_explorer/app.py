from sanic import Sanic

from m0rkcoin_explorer.site.routes import _site_bp

app = Sanic()

app.static('/static', './static')

app.blueprint(_site_bp)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
