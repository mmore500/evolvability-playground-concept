import typing
import warnings

import numpy as np
import opytional as opyt
from skimage import transform as skimg_transform

from . import defaults
from .Params import Params


class Structure:
    """Fixed configuration for cell and inter-cell structure.

    Attributes
    ----------
    bc, br, ba, bd : np.ndarray
        Damping constants for columns, rows, ascending diagonals, and
        descending diagonals, respectively, as 2-dimensional floating point
        arrays.
    kc, kr, ka, kd : np.ndarray
        Spring constants (stiffness) for columns, rows, ascending diagonals,
        and descending diagonals, respectively, as 2-dimensional floating point
        arrays.
    lc, lr, la, ld : np.ndarray
        Spring rest lengths for columns, rows, ascending diagonals, and
        descending diagonals, respectively, as 2-dimensional floating point
        arrays.
    m : np.ndarray, optional
        Cell masses, as 2-dimensional floating point array.

    Properties
    ----------
    height : int
        Number of cell rows in state.
    width : int
        Number of cell columns in state.
    """

    bc: np.ndarray  # damping constant, columns
    br: np.ndarray  # damping constant, rows
    ba: np.ndarray  # damping constant, ascending diagonals
    bd: np.ndarray  # damping constant, descending diagonals

    kc: np.ndarray  # spring constant, columns
    kr: np.ndarray  # spring constant, rows
    ka: np.ndarray  # spring constant, ascending diagonals
    kd: np.ndarray  # spring constant, descending diagonals

    lc: np.ndarray  # spring lengths, columns
    lr: np.ndarray  # spring lengths, rows
    la: np.ndarray  # spring lengths, ascending diagonals
    ld: np.ndarray  # spring lengths, descending diagonals

    m: np.ndarray  # masses

    @property
    def height(self: "Structure") -> int:
        """Number of cell rows in state."""
        res = self.m.shape[0]
        assert np.clip(res, *defaults.nrow_lim) == res
        return res

    @property
    def width(self: "Structure") -> int:
        """Number of cell columns in state."""
        res = self.m.shape[1]
        assert np.clip(res, *defaults.ncol_lim) == res
        return res

    def __init__(
        self: "Structure",
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        params: typing.Optional[Params] = None,
        b: typing.Optional[np.ndarray] = None,  # cellwise norms
        k: typing.Optional[np.ndarray] = None,  # cellwise norms
        l: typing.Optional[np.ndarray] = None,  # cellwise norms
        m: typing.Optional[np.ndarray] = None,  # cellwise norms
    ) -> None:
        """Initialize Structure.

        Parameters
        ----------
        height : int, optional
            Number of cell rows in state.

            If not provided, `defaults.nrow` will be used.
        width : int, optional
            Number of cell columns in state.

            If not provided, `defaults.ncol` will be used.
        params : Params, optional
            Mapped-to ranges for cellwise norms and fallback parameters for any
            unspecified structure elements.

            If not provided, default-initialized Params will be used.
        b, k, l, m : np.ndarray, optional
            Cellwise norms, each provided as a 2D array of floating point values between 0 and 1.

            For spring damping constants, spring stiffness constants, spring
            natural lengths, and cell masses, respectively. These will be
            interpolated to match specified `height` and `width`, if needed. If
            not provided, the default parameter value from `params` will used
            in structure.
        """
        if height is None:
            height = defaults.nrow
        if not np.clip(height, *defaults.nrow_lim) == height:
            raise ValueError(
                f"value {height=} not within limits {defaults.nrow_lim}",
            )

        if width is None:
            width = defaults.ncol
        if not np.clip(width, *defaults.ncol_lim) == width:
            raise ValueError(
                f"value {width=} not within limits {defaults.ncol_lim}",
            )

        # set placeholder for height, width lookup, overwritten later
        self.m = np.full((height, width), 1.0)

        if params is None:
            params = Params()

        if b is None:  # set from params
            assert np.clip(params.b, *params.b_lim) == params.b
            self.bc = np.full((height - 1, width), params.b)
            self.br = np.full((height, width - 1), params.b)
            self.ba = np.full((height - 1, width - 1), params.b)
            self.bd = np.full((height - 1, width - 1), params.b)
        else:  # set from norm
            self.set_b_to_norms(b, params.b_lim)

        if k is None:  # set from params
            assert np.clip(params.k, *params.k_lim) == params.k
            self.kc = np.full((height - 1, width), params.k)
            self.kr = np.full((height, width - 1), params.k)
            self.ka = np.full((height - 1, width - 1), params.k)
            self.kd = np.full((height - 1, width - 1), params.k)
        else:  # set from norm
            self.set_k_to_norms(k, params.k_lim)

        if l is None:  # set from params
            assert np.clip(params.l, *params.l_lim) == params.l
            self.lc = np.full((height - 1, width), params.l)
            self.lr = np.full((height, width - 1), params.l)
            self.la = np.full((height - 1, width - 1), params.l_diag)
            self.ld = np.full((height - 1, width - 1), params.l_diag)
        else:  # set from norm
            self.set_l_to_norms(l, params.l_lim)

        if m is None:  # set from params
            assert np.clip(params.m, *params.m_lim) == params.m
            self.m = np.full((height, width), params.m)
        else:  # set from norm
            self.set_m_to_norms(m, params.m_lim)

        if not self.validate(params):
            raise ValueError

    def __eq__(self: "Structure", other: "Structure") -> bool:
        """Test equality."""
        return (
            np.array_equal(self.bc, other.bc)
            and np.array_equal(self.br, other.br)
            and np.array_equal(self.ba, other.ba)
            and np.array_equal(self.bd, other.bd)
            and np.array_equal(self.kc, other.kc)
            and np.array_equal(self.kr, other.kr)
            and np.array_equal(self.ka, other.ka)
            and np.array_equal(self.kd, other.kd)
            and np.array_equal(self.lc, other.lc)
            and np.array_equal(self.lr, other.lr)
            and np.array_equal(self.la, other.la)
            and np.array_equal(self.ld, other.ld)
            and np.array_equal(self.m, other.m)
        )

    @staticmethod
    def make_random(
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        params: typing.Optional[Params] = None,
        interpolate_from_height: typing.Optional[int] = None,
        interpolate_from_width: typing.Optional[int] = None,
    ) -> "Structure":
        """Create `Structure` object with randomized cell and inter-cell
        configuration.

        Static factory method.

        Parameters
        ----------
        height : int, optional
            Number of cell rows in state.

            If not provided, defaults to `defaults.nrow`.
        width : int, optional
            Number of cell columns in state

            If not provided, defaults to `defaults.ncol`.
        params : Params, optional
            Mapped-to ranges for cellwise norms and fallback parameters for any
            unspecified structure elements.

            If not provided, default-initialized Params will be used.
        interpolate_from_height : int, optional
            Number of , interpolated from if necessary.

            If not provided, defaults to `height`.
        interpolate_from_width : int, optional
            Width from which to interpolate. If not provided, it defaults to the value of `width`.

        Returns
        -------
        Structure
            Initialized object with randomized configuration.
        """
        if height is None:
            height = defaults.nrow
        if not np.clip(height, *defaults.nrow_lim) == height:
            raise ValueError(
                f"value {height=} not within limits {defaults.nrow_lim}",
            )

        if width is None:
            width = defaults.ncol
        if not np.clip(width, *defaults.ncol_lim) == width:
            raise ValueError(
                f"value {width=} not within limits {defaults.ncol_lim}",
            )

        from_height = opyt.or_value(interpolate_from_height, height)
        from_width = opyt.or_value(interpolate_from_width, width)

        return Structure(
            height=height,
            width=width,
            params=params,
            b=np.random.rand(from_height, from_width),
            k=np.random.rand(from_height, from_width),
            l=np.random.rand(from_height, from_width),
            m=np.random.rand(from_height, from_width),
        )

    @staticmethod
    def make_from_bytes(
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        params: typing.Optional[Params] = None,
        b: typing.Optional[np.ndarray] = None,  # cellwise bytes
        k: typing.Optional[np.ndarray] = None,  # cellwise bytes
        l: typing.Optional[np.ndarray] = None,  # cellwise bytes
        m: typing.Optional[np.ndarray] = None,  # cellwise bytes
    ) -> "Structure":
        """Creates a `Structure` instance from the provided byte arrays.

        Parameters
        ----------
        height : int, optional
            Number of cell rows in state.

            If not provided, defaults to `defaults.nrow`.
        width : int, optional
            Number of cell columns in state

            If not provided, defaults to `defaults.ncol`.
        params : Params, optional
            Mapped-to ranges for cellwise norms and fallback parameters for any
            unspecified structure elements.

            If not provided, default-initialized Params will be used.
        b, k, l, m : np.ndarray, optional
            Cellwise normalized values, each provided as a 2D array of integer
            values between 0 and 255.

            For spring damping constants, spring stiffness constants, spring
            natural lengths, and cell masses, respectively. These will be
            interpolated to match specified `height` and `width`, if needed. If
            not provided, the default parameter value from `params` will used
            in structure.

        Returns
        -------
        Structure
            Initialized object.

        Raises
        ------
        ValueError
            If `b`, `k`, `l`, or `m` contain values not between 0 and 255.
        """
        if b is not None and np.any(np.clip(b, 0, 255) != b):
            raise ValueError(f"{b=} must have values between 0 and 255")
        if k is not None and np.any(np.clip(k, 0, 255) != k):
            raise ValueError(f"{k=} must have values between 0 and 255")
        if l is not None and np.any(np.clip(l, 0, 255) != l):
            raise ValueError(f"{l=} must have values between 0 and 255")
        if m is not None and np.any(np.clip(m, 0, 255) != m):
            raise ValueError(f"{m=} must have values between 0 and 255")
        normalize_byte = lambda x: x / 255.0
        res = Structure(
            height=height,
            width=width,
            params=params,
            b=opyt.apply_if(b, normalize_byte),
            k=opyt.apply_if(k, normalize_byte),
            l=opyt.apply_if(l, normalize_byte),
            m=opyt.apply_if(m, normalize_byte),
        )
        assert res.validate()
        return res

    def validate(
        self: "Structure",
        params: typing.Optional[Params] = None,
    ) -> bool:
        """Test if structure contains invalid values."""
        if params is None:
            params = Params()

        h = self.height
        w = self.width
        shapes_ok: bool = (
            self.bc.shape == (h - 1, w)
            and self.br.shape == (h, w - 1)
            and self.ba.shape == (h - 1, w - 1)
            and self.bd.shape == (h - 1, w - 1)
            and self.kc.shape == (h - 1, w)
            and self.kr.shape == (h, w - 1)
            and self.ka.shape == (h - 1, w - 1)
            and self.kd.shape == (h - 1, w - 1)
            and self.lc.shape == (h - 1, w)
            and self.lr.shape == (h, w - 1)
            and self.la.shape == (h - 1, w - 1)
            and self.ld.shape == (h - 1, w - 1)
            and self.m.shape == (h, w)
        )
        if not shapes_ok:
            warnings.warn("Structure shape validation failed.")

        damping_constant_values_ok: bool = (  # spring damping constants
            np.all(np.clip(self.bc, *params.b_lim) == self.bc)
            and np.all(np.clip(self.br, *params.b_lim) == self.br)
            and np.all(np.clip(self.ba, *params.b_lim) == self.ba)
            and np.all(np.clip(self.bd, *params.b_lim) == self.bd)
        )
        if not damping_constant_values_ok:
            warnings.warn(
                "Structure damping constant value validation failed.",
            )

        stiffness_constant_values_ok: bool = (  # spring stiffness constants
            np.all(np.clip(self.kc, *params.k_lim) == self.kc)
            and np.all(np.clip(self.kr, *params.k_lim) == self.kr)
            and np.all(np.clip(self.ka, *params.k_lim) == self.ka)
            and np.all(np.clip(self.kd, *params.k_lim) == self.kd)
        )
        if not stiffness_constant_values_ok:
            warnings.warn(
                "Structure stiffness constant value validation failed.",
            )

        natural_length_values_ok: bool = (  # spring lengths
            np.all(np.clip(self.lc, *params.l_lim) == self.lc)
            and np.all(np.clip(self.lr, *params.l_lim) == self.lr)
            and np.all(np.clip(self.la, *params.l_lim_diag) == self.la)
            and np.all(np.clip(self.ld, *params.l_lim_diag) == self.ld)
        )
        if not natural_length_values_ok:
            warnings.warn("Structure natural length value validation failed.")

        mass_values_ok: bool = np.all(np.clip(self.m, *params.m_lim) == self.m)
        if not mass_values_ok:
            warnings.warn("Structure mass value validation failed.")

        values_ok: bool = (
            damping_constant_values_ok
            and stiffness_constant_values_ok
            and natural_length_values_ok
            and mass_values_ok
        )

        return shapes_ok and values_ok

    def set_b_to_norms(
        self: "Structure",
        cellwise_norms: np.ndarray,
        lim: typing.Optional[typing.Tuple[float, float]] = None,
    ) -> None:
        """Set spring damping constants from normalized values, interpolating
        within provided spring damping constant range.

        Parameters:
        -----------
        cellwise_norms : np.ndarray
            Normalized floating point values, between 0 and 1.
        lim : tuple(float, float), optional
            Spring damping constant range to map normalized values between.

            If None, `defaults.b_lim` is used.
        """
        if not np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms):
            raise ValueError(f"{cellwise_norms=} must have unit values")
        shape = (self.height, self.width)
        if cellwise_norms.shape != shape:  # interpolate if wrong shape
            cellwise_norms = skimg_transform.resize(cellwise_norms, shape)
            assert np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms)

        if lim is None:
            lim = defaults.b_lim

        lb, ub = lim
        target_values = cellwise_norms * (ub - lb) + lb
        self.bc = (target_values[:-1, :] + target_values[1:, :]) / 2
        self.br = (target_values[:, :-1] + target_values[:, 1:]) / 2
        self.ba = (target_values[:-1, :-1] + target_values[1:, 1:]) / 2
        self.bd = (target_values[1:, :-1] + target_values[:-1, :1]) / 2

    def set_k_to_norms(
        self: "Structure",
        cellwise_norms: np.ndarray,
        lim: typing.Optional[typing.Tuple[float, float]] = None,
    ) -> None:
        """Set spring stiffnesses from normalized values, interpolating
        within provided spring stiffness constant range.

        Parameters:
        -----------
        cellwise_norms : np.ndarray
            Normalized floating point values, between 0 and 1.
        lim : tuple(float, float), optional
            Spring stiffness constant range to map normalized values between.

            If None, `defaults.k_lim` is used.
        """
        if not np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms):
            raise ValueError(f"{cellwise_norms=} must have unit values")
        shape = (self.height, self.width)
        if cellwise_norms.shape != shape:  # interpolate if wrong shape
            cellwise_norms = skimg_transform.resize(cellwise_norms, shape)
            assert np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms)

        if lim is None:
            lim = defaults.k_lim

        lb, ub = lim
        target_values = cellwise_norms * (ub - lb) + lb
        self.kc = (target_values[:-1, :] + target_values[1:, :]) / 2
        self.kr = (target_values[:, :-1] + target_values[:, 1:]) / 2
        self.ka = (target_values[:-1, :-1] + target_values[1:, 1:]) / 2
        self.kd = (target_values[1:, :-1] + target_values[:-1, :1]) / 2

    def set_l_to_norms(
        self: "Structure",
        cellwise_norms: np.ndarray,
        lim: typing.Optional[typing.Tuple[float, float]] = None,
    ) -> None:
        """Set spring lengths from normalized values, interpolating within
        provided spring length range.

        Parameters:
        -----------
        cellwise_norms : np.ndarray
            Normalized floating point values, between 0 and 1.
        lim : tuple(float, float), optional
            Natural spring length range to map normalized values between.

            If None, `defaults.l_lim` is used.
        """
        if not np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms):
            raise ValueError(f"{cellwise_norms=} must have unit values")
        shape = (self.height, self.width)
        if cellwise_norms.shape != shape:  # interpolate if wrong shape
            cellwise_norms = skimg_transform.resize(cellwise_norms, shape)
            assert np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms)

        if lim is None:
            lim = defaults.l_lim

        lb, ub = lim
        target_values = cellwise_norms * (ub - lb) + lb
        self.lc = (target_values[:-1, :] + target_values[1:, :]) / 2
        self.lr = (target_values[:, :-1] + target_values[:, 1:]) / 2

        # setting up cross-spring lengths,
        # set up as diagonal lengths of cyclic (area maximizing) quadrilateral
        #
        # D-----d-----A
        # |\        / |
        # | \      /  |
        # |  q    p   |
        # |    \ /    |
        # c     X     a
        # |   /   \   |
        # |  /     \  |
        # | /       \ |
        # |/         \|
        # C-----b-----B
        #
        # unlike ascii representation,
        # note that general quadrilateral case will not have parallelism,
        # congruency, etc.

        a = self.lc[:, 1:]  # AB, right columns
        b = self.lr[1:, :]  # BC, bottom rows
        c = self.lc[:, :-1]  # CD, left columns
        d = self.lr[:-1, :]  # DA, top rows

        assert all(np.all(x >= 0) for x in (a, b, c, d))

        # if any one side is more than half the perimeter?
        # then the other sides won't be able "to connect"
        # and we need to shrink it to sum of other sides
        perimeter = a + b + c + d
        largest_side = np.maximum.reduce([a, b, c, d])
        sum_other_sides = perimeter - largest_side

        a = np.minimum.reduce([a, sum_other_sides])
        b = np.minimum.reduce([b, sum_other_sides])
        c = np.minimum.reduce([c, sum_other_sides])
        d = np.minimum.reduce([d, sum_other_sides])

        # according to wikipedia, for a cyclic (area maximizing) quadrilateral,
        # https://en.wikipedia.org/wiki/Cyclic_quadrilateral
        #
        # for p = AC (ascending) and q = BD (descending)
        #
        # p={\sqrt {\frac {(ac+bd)(ad+bc)}{ab+cd}}}
        # q={\sqrt {\frac {(ac+bd)(ab+cd)}{ad+bc}}}
        #
        # translates to
        p_numer = (a * c + b * d) * (a * d + b * c)
        p_denom = a * b + c * d
        p_ratio = np.divide(  # divide by zero -> zero
            p_numer,
            p_denom,
            out=np.zeros_like(p_numer),
            where=p_denom != 0,
        )
        p = np.sqrt(p_ratio)

        q_numer = (a * c + b * d) * (a * b + c * d)
        q_denom = a * d + b * c
        q_ratio = np.divide(  # divide by zero -> zero
            q_numer,
            q_denom,
            out=np.zeros_like(q_numer),
            where=q_denom != 0,
        )
        q = np.sqrt(q_ratio)

        # check ptolmeys theorem
        assert np.allclose(p * q, a * c + b * d)

        # check bounds on indivividual diagonals
        # note that can't use single side as lower bound due to obtuse cases
        assert np.allclose(
            p,
            np.clip(
                p,
                np.maximum(  # lower bound
                    # from Inequalities proposed in "Crux Mathematicorum"
                    # via wikipedia
                    2 * np.sqrt(a * c + b * d) - q,
                    0,  # ensure non-negative lower bound
                ),
                np.minimum.reduce([a + b, c + d]),  # upper bound
            ),
        )
        assert np.allclose(
            q,
            np.clip(
                q,
                np.maximum(  # lower bound
                    # from Inequalities proposed in "Crux Mathematicorum"
                    # via wikipedia
                    2 * np.sqrt(a * c + b * d) - p,
                    0,  # ensure non-negative lower bound
                ),
                np.minimum.reduce([b + c, d + a]),  # upper bound
            ),
        )

        # assign diagonal spring lengths
        self.la = p
        self.ld = q

    # masses
    def set_m_to_norms(
        self: "Structure",
        cellwise_norms: np.ndarray,
        lim: typing.Optional[typing.Tuple[float, float]] = None,
    ) -> None:
        """Set cell masses from normalized values, interpolating within
        provided mass range.

        Parameters:
        -----------
        cellwise_norms : np.ndarray
            Normalized floating point values, between 0 and 1.
        lim : tuple(float, float), optional
            Mass range to map normalized values between.

            If None, `defaults.m_lim` is used.
        """
        if not np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms):
            raise ValueError(f"{cellwise_norms=} must have unit values")
        shape = (self.height, self.width)
        if cellwise_norms.shape != shape:  # interpolate if wrong shape
            cellwise_norms = skimg_transform.resize(cellwise_norms, shape)
            assert np.all(np.clip(cellwise_norms, 0, 1) == cellwise_norms)

        if lim is None:
            lim = defaults.m_lim

        lb, ub = lim
        target_values = cellwise_norms * (ub - lb) + lb
        self.m = target_values
