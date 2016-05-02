class AppfluxException:

    before = []
    after = []

    def before_notify(self, func):
        AppfluxException.before.append(func)

    def after_notify(self, func):
        AppfluxException.after.append(func)
