import pygame as pg

class Input:
    linked: list[int] = []

    _current_state: bool = False
    _previous_state: bool = False

    def event(self, event: pg.event.Event):
        return self.check(event)

    def update(self):
        self._previous_state = self._current_state

    def pressed(self) -> bool:
        return self._current_state and not self._previous_state
    
    def released(self) -> bool:
        return self._previous_state and not self._current_state
    
    def down(self) -> bool:
        return self._current_state
    
    def check(self, event: pg.event.Event) -> bool:
        return event.type in self.linked

class Key(Input):
    linked = [pg.KEYUP, pg.KEYDOWN, pg.TEXTINPUT, pg.TEXTEDITING]

    key: int
    modifier: int | None

    def __init__(self, keycode: int, modifiers: int = None):
        self.key = keycode
        self.modifier = modifiers

    def event(self, event: pg.event.Event) -> bool:
        if not super().event(event):
            return False
        self._previous_state = self._current_state
        if event.type == pg.KEYDOWN:
            self._current_state = True
        elif event.type == pg.KEYUP:
            self._current_state = False
        return True

    def check(self, event: pg.event.Event) -> bool:
        if event.type == pg.KEYUP:
            return event.dict['key'] == self.key and True if self.modifier == None else event.dict['mod'] == self.modifier
        elif event.type == pg.KEYDOWN:
            return event.dict['key'] == self.key and True if self.modifier == None else event.dict['mod'] == self.modifier
        return False
        
class Button(Input):
    linked = [pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN, pg.CONTROLLERBUTTONUP, pg.CONTROLLERBUTTONDOWN]

    button: int

    def __init__(self, button):
        self.button = button
    
    def event(self, event: pg.event.Event) -> bool:
        if not super().event(event):
            return False
        if event.type == pg.MOUSEBUTTONUP or event.type == pg.CONTROLLERBUTTONUP:
            self._current_state = False
        elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            self._current_state = True

    def check(self, event):
        return ((event.type == pg.MOUSEBUTTONUP or event.type == pg.MOUSEBUTTONDOWN) and event.dict['button'] == self.button)
                
class InputSet[T]:
    inputs: dict[T, list[Input]]

    _event_map: dict[int, list[Input]]

    def __init__(self):
        self.inputs = {}
        self._event_map = {}

    def register_input(self, action: T, input: Input):
        if not action in self.inputs.keys():
            self.inputs[action] = []
        if not input in self.inputs[action]:
            self.inputs[action].append(input)
            for event in input.linked:
                if not event in self._event_map.keys():
                    self._event_map[event] = []
                self._event_map[event].append(input)

    def get_action_pressed(self, action: T):
        if action in self.inputs.keys():
            for input in self.inputs[action]:
                return input.pressed()
             
    def get_action_released(self, action: T):
        if action in self.inputs.keys():
            for input in self.inputs[action]:
                return input.released()
            
    def get_action_down(self, action: T):
        if action in self.inputs.keys():
            for input in self.inputs[action]:
                return input.down()
    
    def update(self, event_queue: list[pg.event.Event]):
        for _, inputs in self.inputs.items():
            for input in inputs:
                input.update()
        for event in event_queue:
            if event.type in self._event_map.keys():
                for input in self._event_map[event.type]:
                    input.event(event)