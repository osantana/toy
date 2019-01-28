class Resource:
    fields = []

    def __init__(self, **arguments):
        self.arguments = arguments
        self._fields = {}

        for field in self.fields:
            self._fields[field.name] = field

    def get(self, **kwargs):
        raise NotImplementedError('Abstract class')

    def __setitem__(self, key, value):
        if key not in self._fields:
            raise ValueError('Invalid field')

        self._fields[key].value = value

    def __getitem__(self, item):
        return self._fields[item].value

    def __contains__(self, item):
        return item in self._fields

    def update(self, data):
        for key, value in data.items():
            self._fields[key].value = value

    @property
    def data(self):
        result = {}
        for key, field in self._fields.items():
            result[key] = field.value
        return result
