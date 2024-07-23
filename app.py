from flask import Flask, render_template
import setup

def create_app(test_config=None):
    app = setup.init(test_config)

    @app.route('/')
    def hello():
        return render_template('hello.html')

    @app.route('/hello')
    def hello_name():
        return render_template('helloname.html', name='ぽよちん')
    
    return app