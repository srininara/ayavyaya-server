from ayavyaya import app


@app.route('/ayavyaya/fe/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)
