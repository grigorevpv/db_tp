class BaseBlueprint:

    def __init__(self):
        self._blueprint = None

    def blueprint(self):
        if not self._blueprint:
            self._blueprint = self._create_blueprint()
        return self._blueprint

    def _create_blueprint(self):
        raise NotImplementedError