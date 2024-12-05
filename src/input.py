import pygame as pg

class IEventState[T]:
    linked: list[int] = []

    _current_state: T = None
    _previous_state: T = None

    def event(self, event: pg.event.Event):
        return self.check(event)
    
    def update(self):
        self._previous_state = self._current_state
    
    def check(self, event: pg.event.Event):
        return event.type in self.linked

class Input(IEventState[bool]):
    def pressed(self) -> bool:
        return self._current_state and not self._previous_state
    
    def released(self) -> bool:
        return self._previous_state and not self._current_state
    
    def down(self) -> bool:
        return self._current_state
    
class Cursor(IEventState[tuple[float, float]]):
    linked = [pg.MOUSEMOTION]

    def __init__(self):
        self._current_state = (0, 0)
        self._previous_state = (0, 0)

    def event(self, event: pg.event.Event) -> bool:
        if not super().event(event):
            return False
        self._current_state = event.dict['pos']
        self._previous_state = event.dict['rel']

    def update(self):
        self._previous_state = (0, 0)
        return

    def position(self) -> tuple[float, float]:
        return self._current_state
    
    def delta(self) -> tuple[float, float]:
        return self._previous_state 
    
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
    cursors: dict[T, list[Cursor]]

    _event_map: dict[int, list[IEventState]]

    def __init__(self):
        self.inputs = {}
        self.cursors = {}
        self._event_map = {}

    def register_cursor(self, action: T, cursor: Cursor):
        if not action in self.cursors.keys():
            self.cursors[action] = []
        if not cursor in self.cursors[action]:
            self.cursors[action].append(cursor)
            for event in cursor.linked:
                if not event in self._event_map.keys():
                    self._event_map[event] = []
                self._event_map[event].append(cursor)

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
            
    def get_cursor_pos(self, action: T):
        if action in self.cursors.keys():
            for cursor in self.cursors[action]:
                return isinstance(cursor, Cursor) and cursor.position()
             
    def get_cursor_delta(self, action: T):
        if action in self.cursors.keys():
            for cursor in self.cursors[action]:
                return isinstance(cursor, Cursor) and cursor.delta()
            
    def get_cursor_button(self, action: T, cursor_action: T):
        if action in self.inputs.keys() and cursor_action in self.cursors.keys():
            position = None
            delta = None
            pressed = None
            down = None
            released = None
            for cursor in self.cursors[cursor_action]:
                position = cursor.position()
                delta = cursor.delta()
            for input in self.inputs[action]:
                pressed = input.pressed()
                down = input.down()
                released = input.released()
            return {
                "position": position,
                "delta": delta,
                "pressed": pressed,
                "down": down,
                "released": released
            }
        
    
    def update(self, event_queue: list[pg.event.Event]):
        for _, inputs in self.inputs.items():
            for input in inputs:
                input.update()
        for _, cursors in self.cursors.items():
            for cursor in cursors:
                cursor.update()
        
        for event in event_queue:
            if event.type in self._event_map.keys():
                for input in self._event_map[event.type]:
                    input.event(event)