bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):  #创建app
    app = Flask(__name__)
    app.config.from_object(config[config_name])  #将配置类中的配置导入程序
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint  #导入蓝本main
    app.register_blueprint(main_blueprint)  #在主程序中注册蓝本


    return app