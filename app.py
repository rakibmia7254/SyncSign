from main import app
from api import api_bp
from admin import admin_bp

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')


if __name__ == '__main__':
    app.run(debug=True)