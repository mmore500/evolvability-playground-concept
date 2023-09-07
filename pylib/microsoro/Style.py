import typing

import seaborn as sns


class Style:
    """Styling options for visualizations.

    Attributes
    ----------
    cell_alpha : float
        The alpha level of each cell. Must be between 0.0 and 1.0.
    cell_color_palette : list of tuple
        A list of color tuples. Interoperable with seaborn color palettes.
    cell_radius : float
        The radius of each cell. Must be non-negative.
    xlim : tuple of float
        The x-axis limits.
    ylim : tuple of float
        The y-axis limits.
    """

    cell_alpha: float
    # cell_color_palette interops with seaborn color_palette
    cell_color_palette: typing.List[typing.Tuple]
    cell_radius: float

    xlim: typing.Tuple[float, float]
    ylim: typing.Tuple[float, float]

    def __init__(
        self: "Style",
        *,
        cell_alpha: float = 0.8,
        cell_color_palette: typing.Optional[typing.List[typing.Tuple]] = None,
        cell_radius: float = 0.4,
        xlim: typing.Tuple[float, float] = (0, 20),
        ylim: typing.Tuple[float, float] = (0, 20),
    ) -> None:
        """Initialize a Style instance.

        Parameters
        ----------
        cell_alpha : float, default 0.8
            The alpha level for each cell.
        cell_color_palette : list of tuple, optional
            The color palette for cells, default is seaborn's 'husl' palette.
        cell_radius : float, default 0.4
            The radius for each cell.
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
        self.xlim = xlim
        self.ylim = ylim

        if not 0.0 <= cell_alpha <= 1.0:
            raise ValueError(f"{cell_alpha=} not between 0.0 and 1.0")
        self.cell_alpha = cell_alpha
        if cell_color_palette is None:
            cell_color_palette = sns.color_palette("husl", 8)
        self.cell_color_palette = cell_color_palette
        if cell_radius < 0.0:
            raise ValueError(f"{cell_radius=} is negative")
        self.cell_radius = cell_radius
