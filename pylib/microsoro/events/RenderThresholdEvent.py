from dataclasses import dataclass
import typing


@dataclass(frozen=True, eq=True)
class RenderThresholdEvent:
    """Reports threshold component of simulation to be drawn.

    See Also
    --------
    HaltPastFinishLine
        Originates event.
    """

    m: float  # slope
    b: float  # intercept
    independent_axis: typing.Literal["horizontal", "vertical"]
    flavor: typing.Literal["finish"] = "finish"  # default value

    def get_spanning_coordinates(
        self: "RenderThresholdEvent",
        xlim: typing.Tuple[float, float],
        ylim: typing.Tuple[float, float],
        scale: float,
    ) -> typing.Tuple["float", "float", "float", "float"]:
        """Get coordinates for line spanning specified viewing window.

        Returns
        -------
        tuple[float, float, float, float]
            Coordinates for spanning line as (x1, y1, x2, y2).
        """
        m, b, independent_axis = self.m, self.b, self.independent_axis
        i1, i2 = {"horizontal": xlim, "vertical": ylim}[independent_axis]
        d1, d2 = i1 * m + b, i2 * m + b
        (x1, x2), (y1, y2), s = xlim, ylim, scale
        tform_y = lambda y: s * (y - y1)
        tform_x = lambda x: s * (x - x1)
        return {
            "horizontal": [tform_x(i1), tform_y(d1), tform_x(i2), tform_y(d2)],
            "vertical": [tform_x(d1), tform_y(i1), tform_x(d2), tform_y(i2)],
        }[independent_axis]
