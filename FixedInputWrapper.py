class FixedInputWrapper(object):

    def __init__(self, wrapped_component, fixed_state):
        self._component = wrapped_component
        self._fixed_state = fixed_state

    @property
    def input_properties(self):
        return_dict = {}
        for name in self._component.input_properties:
            if name not in self._fixed_state:
                properties = self._component.input_properties[name]
                return_dict[name] = properties
        return return_dict

    def __getattr__(self, item):
        print('GET_ATTR')
        print(item)
        return getattr(self._component, item)

    def __call__(self, state, *args, **kwargs):
        print('CALL')
        self.checkQProf(   state)
        state.update(self._fixed_state)
        return self._component(state, *args, **kwargs)

    def checkQProf(self, state):
        validation = array([[[7.971684e-03]],
                            [[7.495124e-03]],
                            [[6.208342e-03]],
                            [[5.659282e-03]],
                            [[5.129867e-03]],
                            [[4.688474e-03]],
                            [[4.193747e-03]],
                            [[3.604757e-03]],
                            [[3.050940e-03]],
                            [[2.278415e-03]],
                            [[1.462291e-03]],
                            [[8.918543e-04]],
                            [[5.201116e-04]],
                            [[3.067158e-04]],
                            [[2.045334e-04]],
                            [[1.719684e-04]],
                            [[1.532107e-04]],
                            [[5.892009e-05]],
                            [[2.748316e-05]],
                            [[1.567088e-05]],
                            [[7.200140e-06]],
                            [[1.465907e-09]],
                            [[2.762313e-14]],
                            [[7.226609e-20]],
                            [[3.179606e-26]],
                            [[2.748316e-33]],
                            [[5.187848e-41]],
                            [[1.897848e-49]]])

        print('FIXED', self._fixed_state['specific_humidity'].values[:] == validation)
        print('STATE', state['specific_humidity'].values[:] == validation)
