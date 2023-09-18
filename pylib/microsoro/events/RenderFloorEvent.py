from dataclasses import dataclass
import typing


@dataclass(frozen=True, eq=True)
class RenderFloorEvent:
    """Reports floor component of simulation to be drawn.

    See Also
    --------
    ApplyFloorBounce
        Originates event.
    ApplyViscousLayer
        Originates event.
    """

    m: float  # slope
    b: float  # intercept
    flavor: typing.Literal["floor", "viscous layer"] = "floor"  # default value

    def get_underfloor_polygon(
        self: "RenderFloorEvent",
        xlim: typing.Tuple[float, float],
        ylim: typing.Tuple[float, float],
        scale: float,
        invert_y: bool = True,
    ) -> typing.List[typing.Tuple[float, float]]:
        """Get points to render Floor as a polygon within a viewing window.

        Parameters
        ----------
        xlim: tuple[float, float]
            The simulation-space x bounds of viewing window, in ascending order.
        ylim: typle[float, float]
            The simulation-space y bounds of viewing window, in ascending order.
        scale: float
            Scale-up factor between simulation space and render space.
        invert_y: bool, default True
            Should render space origin fall in upper corner of viewing window?

            If set to False, render space origin will fall in lower corner of
            viewing window.

        Returns
        -------
        list[tuple[float, float]]
            Underfloor fill vertices as list of (x, y) tuples in render space.

            If underfloor fill falls entirely outside viewing window, an empty
            list is returned.

        Notes
        -----
        Assumes origin of render space falls at the viewing window's upper-left
        corner.
        """
        # unpack and prep variables
        x1, x2 = xlim
        width = x2 - x1
        if width < 0:
            raise ValueError
        y1, y2 = ylim
        height = y2 - y1
        if height < 0:
            raise ValueError
        m = self.m
        b = self.b

        b1 = m * x1 + b
        b2 = m * x2 + b

        # floor is completely below viewing window
        if b1 <= y1 and b2 <= y1:
            return []

        # assemble polygon points
        polygon_points = []
        # bottom-left corner
        if b1 >= y1:
            polygon_points.append(
                (0, 0),
            )
        # top-left corner
        polygon_points.append(
            (0, (b1 - y1) * scale),
        )
        # top-right corner
        polygon_points.append(
            (width * scale, (b2 - y1) * scale),
        )
        # bottom-right corner
        if b2 >= y1:
            polygon_points.append(
                (width * scale, 0),
            )
        assert len(polygon_points) in (3, 4)

        if invert_y:
            polygon_points = [
                (x, height * scale - y) for x, y in polygon_points
            ]

        return polygon_points
