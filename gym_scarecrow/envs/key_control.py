class KeyControl:

    def __init__(self):
        self.bindings = {"up": pygame.K_UP,
                         "down":  pygame.K_DOWN,
                         "left":  pygame.K_LEFT,
                         "right":   pygame.K_RIGHT}

        self.input_state = {"up": False,
                            "down": False,
                            "left": False,
                            "right": False}

        self.buffer = InputBuffer()

    def lookup_binding(self, key_entered):
        for binding, key_bound in self.bindings.items():
            if key_entered == key_bound:
                return binding

        return "not found"

    def get_input(self, events):
        for event in events:

            if event.type == pygame.KEYDOWN:
                binding = self.lookup_binding(event.key)
                if binding != "not found":
                    new_input = Input()
                    new_input.input_name = binding
                    new_input.time_since_input = 0
                    self.buffer.push(new_input)
                    self.input_state[binding] = True

            if event.type == pygame.KEYUP:
                binding = self.lookup_binding(event.key)
                if binding != "not found":
                    self.input_state[binding] = False


        return self.input_state
