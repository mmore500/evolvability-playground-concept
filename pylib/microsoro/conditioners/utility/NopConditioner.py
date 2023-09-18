import typing


class NopConditioner:
    def __call__(
        self: "NopConditioner",
        state: typing.Optional,
        event_buffer: typing.Optional,
    ) -> None:
        pass
