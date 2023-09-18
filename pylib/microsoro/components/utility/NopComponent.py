import typing


class NopComponent:
    def __call__(
        self: "NopComponent",
        state: typing.Optional,
        event_buffer: typing.Optional,
    ) -> None:
        pass
