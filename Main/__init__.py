from flask import Flask
import sys
sys.path.insert(0, 'C:\\Users\\mmoha\\Desktop\\Camera-Tracking-Using-UWB-Navigation\\Camera')
import views

def create_app():
    #Create app with configuration as following
    app = Flask(__name__, template_folder='templates')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    


    app.register_blueprint(views, url_prefix='/')
    

    return app
