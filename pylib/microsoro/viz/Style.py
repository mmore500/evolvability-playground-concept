import typing

from is_sorted import is_sorted
import seaborn as sns


class Style:
    """Styling options for visualizations.

    Attributes
    ----------
    background_color : tuple of floats
        Background color as RGB. Tuple values ust be between 0.0 and 1.0.
    cell_alpha : float
        The alpha level of each cell. Must be between 0.0 and 1.0.
    cell_color_palette : tuple of tuple
        A tuple of color tuples. Interoperable with seaborn color palettes.
    cell_radius : float
        The radius of each cell. Must be non-negative.
    scale : float
        Number pixels per unit distance.
    time_dilation : float
        How much slower should the simulation be paced in recordings and real
        time animations?
    xlim : tuple of float
        The x-axis limits.
    ylim : tuple of float
        The y-axis limits.

    Properties
    ----------
    xlim_length : float
        Difference between upper and lower xlim.
    ylim_length : float
        Difference between upper and lower ylim.
    """

    background_color: typing.Tuple[float, float, float]

    cell_alpha: float
    # cell_color_palette interops with seaborn color_palette
    # tuple instead of list to allow for cached palette resampling
    cell_color_palette: typing.Tuple[typing.Tuple]
    cell_radius: float

    scale: float

    xlim: typing.Tuple[float, float]
    ylim: typing.Tuple[float, float]

    time_dilation: float

    def __init__(
        self: "Style",
        *,
        background_color: typing.Tuple[float, float, float] = (1.0, 1.0, 1.0),
        cell_alpha: float = 0.8,
        cell_color_palette: typing.Optional[typing.List[typing.Tuple]] = None,
        cell_radius: float = 0.4,
        scale: float = 10.0,
        time_dilation: float = 1.0,
        xlim: typing.Tuple[float, float] = (0, 20),
        ylim: typing.Tuple[float, float] = (0, 20),
    ) -> None:
        """Initialize a Style instance.

        Parameters
        ----------
        background_color : typle of float
            Background color as float RGB tuple.

            Tuple values ust be between 0.0 and 1.0.
        cell_alpha : float, default 0.8
            The alpha level for each cell.
        cell_color_palette : list of tuple, optional
            The color palette for cells, default is seaborn's 'husl' palette.

            Can be generated from `sns.color_palette()`.
        cell_radius : float, default 0.4
            The radius for each cell.
        scale : float, default 10.0
            How many pixels per unit distance?
        time_dilation : float, default 1.0
            How much slower should the simulation be paced in recordings and
            real time animations?
        xlim : tuple of float, default (0, 20)
            The x-axis limits.
        ylim : tuple of float, default (0, 20)
            The y-axis limits.

        Raises
        ------
        ValueError
            If `cell_alpha` is not between 0.0 and 1.0 or if `cell_radius` is
            negative.
        """
        if not len(background_color) in (3, 4):
            raise ValueError(
                f"{background_color=} must be 3-value RGB or 4-value RGBA",
            )
        if not all(0.0 <= rgb_val <= 1.0 for rgb_val in background_color):
            raise ValueError(
                f"{background_color=} has value not between 0.0 and 1.0",
            )
        self.background_color = tuple(background_color[:3])
        if not 0.0 <= cell_alpha <= 1.0:
            raise ValueError(f"{cell_alpha=} not between 0.0 and 1.0")
        self.cell_alpha = cell_alpha
        if cell_color_palette is None:
            cell_color_palette = sns.color_palette("husl", 8)
        for rgb_tup in cell_color_palette:
            if not len(rgb_tup) in (3, 4):
                raise ValueError(
                    f"{rgb_tup=} in cell_color_palette "
                    "must be 3-value RGB or 4-value RGBA",
                )
            if not all(0.0 <= rgb_val <= 1.0 for rgb_val in rgb_tup):
                raise ValueError(
                    f"{rgb_tup=} in cell_color_palette "
                    "has value not between 0.0 and 1.0",
                )
        self.cell_color_palette = tuple(cell_color_palette)
        if cell_radius < 0.0:
            raise ValueError(f"{cell_radius=} is negative")
        self.cell_radius = cell_radius

        if time_dilation < 0.0:
            raise ValueError(f"{time_dilation=} is negative")
        self.time_dilation = time_dilation
        if scale < 0.0:
            raise ValueError(f"{scale=} is negative")
        self.scale = scale
        if not len(xlim) == 2:
            raise ValueError(f"{xlim=} must have two values")
        if not is_sorted(xlim):
            raise ValueError(f"{xlim=} values must be in ascending order")
        self.xlim = tuple(map(float, xlim))
        if not len(ylim) == 2:
            raise ValueError(f"{ylim=} must have two values")
        if not is_sorted(ylim):
            raise ValueError(f"{ylim=} values must be in ascending order")
        self.ylim = tuple(map(float, ylim))

    @property
    def xlim_length(self: "Style") -> float:
        return self.xlim[1] - self.xlim[0]

    @property
    def ylim_length(self: "Style") -> float:
        return self.ylim[1] - self.ylim[0]

    def invert_y_value_renderspace(self: "Style", y: float) -> float:
        return self.ylim_length * self.scale - y
