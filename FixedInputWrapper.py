class FixedInputWrapper(object):

    def __init__(self, wrapped_component, fixed_state):
        self._component = wrapped_component
        self._fixed_state = fixed_state

    @property
    def input_properties(self):
        return_dict = {}
        print(self._component)
        print(self._component.input_properties.keys())
        for name, properties in self._component.input_properties:
            if name not in self._fixed_state:
                return_dict[name] = properties
        return return_dict

    def __getattr__(self, item):
        return getattr(self._component, item)

    def __call__(self, state, *args, **kwargs):
        state.update(self._fixed_state)
        return self._component(state, *args, **kwargs)