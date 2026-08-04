from typing import TYPE_CHECKING
if TYPE_CHECKING: from ...kernel import Context
from ....enums.keyboard import Key, key_to_cffi, cffi_to_key

class Keyboard:
    __slots__ = (
        '_context', 
        '_keyboard', 
        '_lib', 
        '_registry',
        '_branch_pressed', 
        '_branch_active', 
        '_branch_released',
        '_requested', 
        '_pressed', 
        '_active', 
        '_released', 
        '_count'
    )

    def _register_key(self, key: Key) -> int:
        self._registry.add(key)
        cffi_key = key_to_cffi[key]
        self._requested[self._count] = cffi_key
        self._count += 1
        self._keyboard.count = self._count
        return cffi_key

    def _default_pressed(self, key: Key):
        if key in self._registry:
            cffi_key = key_to_cffi[key]
        else:
            cffi_key = self._register_key(key)

        pressed_ref = self._pressed

        def opti(_key):
            return pressed_ref[cffi_key]

        self._branch_pressed[key.value] = opti
        return self._lib.Nx_Keyboard_GetPressed(cffi_key)

    def _default_active(self, key: Key):
        if key in self._registry:
            cffi_key = key_to_cffi[key]
        else:
            cffi_key = self._register_key(key)

        active_ref = self._active

        def opti(_key):
            return active_ref[cffi_key]

        self._branch_active[key.value] = opti
        return self._lib.Nx_Keyboard_GetActive(cffi_key)

    def _default_released(self, key: Key):
        if key in self._registry:
            cffi_key = key_to_cffi[key]
        else:
            cffi_key = self._register_key(key)

        released_ref = self._released

        def opti(_key):
            return released_ref[cffi_key]

        self._branch_released[key.value] = opti
        return self._lib.Nx_Keyboard_GetReleased(cffi_key)

    def __init__(self, context: Context):
        self._context = context
        self._keyboard = self._context._interface._keyboard
        self._lib = self._context.cffi.lib
        self._registry = set()
        self._count = 0

        n = len(Key)
        self._branch_pressed = [self._default_pressed] * n
        self._branch_active = [self._default_active] * n
        self._branch_released = [self._default_released] * n

    def _update(self):
        self._requested = self._keyboard.requested_keys
        self._pressed = self._keyboard.pressed_keys
        self._active = self._keyboard.active_keys
        self._released = self._keyboard.released_keys
        self._count = self._keyboard.count

    def pressed(self, key: Key):
        return self._branch_pressed[key.value](key)

    def active(self, key: Key):
        return self._branch_active[key.value](key)

    def released(self, key: Key):
        return self._branch_released[key.value](key)