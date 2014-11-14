from app import app


@app.route('/grihasthi/fe/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)
