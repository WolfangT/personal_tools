#!/usr/bin/env python3
# tools.py
# Herramientas de Wolfang para calculos rapidos en sistemas de potencia 1

import math
import cmath
import numpy as np

from math import sqrt, atan
from cmath import pi


# Funciones de alluda


def degrees(rad):
    """converts radians to degress"""
    return rad * 180 / pi


def radians(degrees):
    """converts degrees to radians"""
    return degrees * pi / 180


def rect(mag, deg):
    """creates a complex number from magnitude and degrees"""
    return cmath.rect(mag, radians(deg))


def inv(val):
    """invierte el val"""
    return 1 / val


def inv_sum(*vals):
    """inverso de la suma de inversos"""
    return inv(sum(inv(i) for i in vals))


def display_single(val):
    return f"{round(abs(val), 6):11}"


def display_polar(cmplx, unit=""):
    mag, rad = cmath.polar(cmplx)
    deg = degrees(rad)
    return f"{round(mag,6):11} ∠ {round(deg, 2):7}° {unit}"


def display_rect(cmplx, u_real="", u_imag="J", u_fin=""):
    return f"{round(cmplx.real,6):11} {u_real} + {round(cmplx.imag, 6):11} {u_imag} {u_fin}"


def cambio_base(val, Sn, Vn, Sb, Vb):
    """Cabio de Base de valores nominales a valores bases"""
    return val * ((Vn / Vb) ** 2) * (Sb / Sn)


def tap_fic(Z, t):
    Y = 1 / Z
    return (
        f"  Z / t:       {display_rect(Z/t)} Ω pu\n"
        f"  Z / (1-t):   {display_rect(Z/(1-t))} Ω pu\n"
        f"  Z / t(t-1):  {display_rect(Z/(t**2-t))} Ω pu\n"
        f"  Y * t:       {display_rect(Y*t)} ℧ pu\n"
        f"  Y * (1-t):   {display_rect(Y*(1-t))} ℧ pu\n"
        f"  Z * t(t-1):  {display_rect(Y*(t**2-t))} ℧ pu\n"
    )


# Clases de ayuda


class DeltaEstrella:
    """Calcular rapidamente un Delta/Estrella en Impedancia o Admitancia

    Zabc: impedancias delta
    Yabc: admitancias delta
    Z123: impedancias estrella
    Y123: admitancias estrella
    1 2 3: nodos primario, secundario, terciario
    a b c: lineas entre nodos

    delta:

    Np---c---Ns
      \     /
       b   a
        \ /
         Nt

    strella:

    Np       Ns
       1   2
         .
         3
         Nt
    """

    Np = "Np"
    Ns = "Ns"
    Nt = "Nt"
    Za = None
    Zb = None
    Zc = None
    Z1 = None
    Z2 = None
    Z3 = None
    Ya = None
    Yb = None
    Yc = None
    Y1 = None
    Y2 = None
    Y3 = None

    def __init__(self, Np=None, Ns=None, Nt=None):
        if Np:
            self.Np = Np
        if Ns:
            self.Ns = Ns
        if Nt:
            self.Nt = Nt

    def _calc(self):
        """Ussando las impedancia de estrella, calcula los otrs valores"""
        self.Y1 = 1 / self.Z1
        self.Y2 = 1 / self.Z2
        self.Y3 = 1 / self.Z3
        _edi = (self.Z1 * self.Z2) + (self.Z2 * self.Z3) + (self.Z3 * self.Z1)
        self.Za = _edi / self.Z1
        self.Zb = _edi / self.Z2
        self.Zc = _edi / self.Z3
        _eda = self.Y1 + self.Y2 + self.Y3
        self.Ya = self.Y2 * self.Y3 / _eda
        self.Yb = self.Y3 * self.Y1 / _eda
        self.Yc = self.Y1 * self.Y2 / _eda

    def impedanciasEstrella(self, Z1, Z2, Z3):
        self.Z1 = Z1
        self.Z2 = Z2
        self.Z3 = Z3
        self._calc()

    def impedanciaDelta(self, Za, Zb, Zc):
        _dei = Za + Zb + Zc
        self.Z1 = Zb * Zc / _dei
        self.Z2 = Zc * Za / _dei
        self.Z3 = Za * Zb / _dei
        self._calc()

    def AdmitanciaEstrella(self, Y1, Y2, Y3):
        self.Z1 = 1 / Y1
        self.Z2 = 1 / Y2
        self.Z3 = 1 / Y3
        self._calc()

    def AdmitanciaDelta(self, Ya, Yb, Yc):
        _dea = (Ya * Yb) + (Yb * Yc) + (Yc * Ya)
        self.Z1 = Ya / _dea
        self.Z2 = Yb / _dea
        self.Z3 = Yc / _dea
        self._calc()

    def __str__(self):
        return (
            f"{self.Np}⟍      ⟋ {self.Ns}\n"
            f"  Z1⟍  ⟋ Z2    Z1: {display_rect(self.Z1)} Ω\n"
            f"      Y        Z2: {display_rect(self.Z2)} Ω\n"
            f"      |Z3      Z3: {display_rect(self.Z3)} Ω\n"
            f"      {self.Nt}\n"
            f"\n"
            f"{self.Np}---Zc---{self.Ns}\n"
            f"  \      /     Za: {display_rect(self.Za)} Ω\n"
            f"   Zb   Za     Zb: {display_rect(self.Zb)} Ω\n"
            f"    \  /       Zc: {display_rect(self.Zc)} Ω\n"
            f"     {self.Nt}\n"
            f"\n"
            f"{self.Np}⟍      ⟋ {self.Ns}\n"
            f"  Y1⟍  ⟋ Y2    Y1: {display_rect(self.Y1)} ℧\n"
            f"      Y        Y2: {display_rect(self.Y2)} ℧\n"
            f"      |Y3      Y3: {display_rect(self.Y3)} ℧\n"
            f"      {self.Nt}\n"
            f"\n"
            f"{self.Np}---Yc---{self.Ns}\n"
            f"  \      /     Ya: {display_rect(self.Ya)} ℧\n"
            f"   Yb   Ya     Yb: {display_rect(self.Yb)} ℧\n"
            f"    \  /       Yc: {display_rect(self.Yc)} ℧\n"
            f"     {self.Nt}\n"
        )


# Clases de elementos de potencia


class Elemento:
    """Elemento trifasico base

    Args:
        nombre: nombre para mostar del elemento
    """

    def __init__(self, nombre, **kwargs):
        self.nombre = nombre

    def __str__(self):
        return f"{self.nombre}"


class Barra(Elemento):
    """Una Barra trifasica

    Establecen los valores bases para los elementos conectados a ellos

    Args:
        Sb: Potencia base
        Vb: Voltaje Base
    """

    def __init__(self, nombre, *, Sb, Vb, Ib=None, Zb=None, Yb=None):
        self.Sb = Sb
        self.Vb = Vb
        self.Ib = Ib or self.Sb / self.Vb / sqrt(3)
        self.Zb = Zb or self.Vb ** 2 / self.Sb
        self.Yb = Yb or 1 / self.Zb
        super().__init__(nombre)

    def __str__(self):
        return (
            f"{self.nombre}:\n"
            f"  Sb: {display_single(self.Sb)} W\n"
            f"  Vb: {display_single(self.Vb)} V\n"
            f"  Ib: {display_single(self.Ib)} A\n"
            f"  Zb: {display_single(self.Zb)} Ω\n"
            f"  Yb: {display_single(self.Yb)} ℧\n"
        )


class Generador(Elemento):
    def __init__(self, nombre, *, Sn, Vn, Zev, b):
        super().__init__(nombre)
        self.Sn = Sn
        self.Vn = Vn
        self.Zev = Zev
        self.b = b
        self.Z = cambio_base(self.Zev, Sn, Vn, b.Sb, b.Vb)
        self.Y = 1 / self.Z

    def __str__(self):
        return (
            f"{self.nombre}:\n"
            f"  Sn: {display_rect(self.Sn)} VA\n"
            f"  Vn: {display_rect(self.Vn)} V\n"
            f"  Z:  {display_rect(self.Z)} Ω pu\n"
            f"  Y:  {display_rect(self.Y)} ℧ pu\n"
        )


class Linea(Elemento):
    """Una Linea Mediana de transmicion trifasica

    Interconecta dos barras con los mismos valores bases

    Args:
        Sn: Potencia Nominal
        Vn: Voltaje Nominal
        In: Corriente Nominal

        L: Longitud (Kilometros)

        Rn: Parametro de Resistencia de la linea en valor absoluto (por kilmetro)
        Xn: Parametro de Reactancia de la linea en valor absoluto (por kilmetro)
        Gn: Parametro de Conductancia de la linea en valor absoluto (por kilmetro)
        Bn: Parametro de Suceptancia de la linea en valor absoluto (por kilmetro)

        bp: Barra del lado primario
        bp: Barra del lado secundario
    """

    def __init__(
        self, nombre, *, Rn, Xn, Gn, Bn, bp, bs, L=1, Sn=None, Vn=None, In=None
    ):
        super().__init__(nombre)
        self.Sn = Sn
        self.Vn = Vn
        self.In = In
        self.L = L
        self.Rn = Rn * L
        self.Xn = Xn * L
        self.Gn = Gn * L
        self.Bn = Bn * L
        self.bp = bp
        self.bs = bs
        self.R = self.Rn / self.bp.Zb
        self.X = self.Xn / self.bp.Zb
        self.G = self.Gn / self.bp.Yb
        self.B = self.Bn / self.bp.Yb

    def __str__(self):
        return (
            (f"{self.nombre}:\n" f" Valores Nominales:\n")
            + (f"  Sn:  {display_single(self.Sn)} VA\n" if self.Sn else "")
            + (f"  Vn:  {display_single(self.Vn)} V\n" if self.Vn else "")
            + (f"  In:  {display_single(self.In)} A\n" if self.In else "")
            + (
                f"  Rn: {display_single(self.Rn)} Ω\n"
                f"  Xn: {display_single(self.Xn)} J Ω\n"
                f"  Gn: {display_single(self.Gn)} ℧\n"
                f"  Bn: {display_single(self.Bn)} J ℧\n"
                f" Valores PU:\n"
                f"  R: {display_single(self.R)} Ω pu\n"
                f"  X: {display_single(self.X)} J Ω pu\n"
                f"  G: {display_single(self.G)} ℧ pu\n"
                f"  B: {display_single(self.B)} J ℧ pu\n"
            )
        )


class BancoCondensadores(Elemento):
    def __init__(self, nombre, *, Qn, In, Prel, bp, bs):
        super().__init__(nombre)
        self.Qn = Qn
        self.In = In
        self.Prel = Prel
        self.bp = bp
        self.bs = bs
        self.Pn = self.Prel * self.Qn / sqrt(1 - self.Prel ** 2)
        self.Sn = complex(self.Pn, self.Qn)
        self.Vn = self.Sn / sqrt(3) / self.In
        self.Zn = self.Vn ** 2 / self.Sn
        self.Z = self.Zn / self.bp.Zb
        self.Y = 1 / self.Z

    def __str__(self):
        return (
            f"{self.nombre}:\n"
            f"  Sn: {display_rect(self.Sn)} VA\n"
            f"  Zn: {display_rect(self.Zn)} Ω\n"
            f"  Vn: {display_polar(self.Vn)} V\n"
            f"  Z:  {display_rect(self.Z)} Ω pu\n"
            f"  Y:  {display_rect(self.Y)} ℧ pu\n"
        )


class TransformadorSimple(Elemento):
    """Transformador Trifasico simple de 2 devanados

    tiene un lado primario y un lado secundario,
    no hay preferencia de que uno sea Alta o Baja,
    eso depende de las barra a la que estan conectados

    Args:
        Sn: Potencia Nominal
        Vp: Voltaje nominal del lado primario
        Vs: Voltaje nominal del lado secundario

        Zev: Impedancia equivalente en pu
        rel: relacion X/R

        bp: Barra del lado primario
        bs: Barra del lado secundario

    """

    def __init__(self, nombre, *, Sn, Vp, Vs, Zev, rel, bp, bs):
        super().__init__(nombre)
        self.Sn = Sn
        self.Vp = Vp
        self.Vs = Vs
        self.Zev = rect(Zev, degrees(atan(rel)))
        self.bp = bp
        self.bs = bs
        self.Zp = self.Zev * ((self.Vp / self.bp.Vb) ** 2) * (self.bp.Sb / self.Sn)
        self.Zs = self.Zev * ((self.Vs / self.bs.Vb) ** 2) * (self.bs.Sb / self.Sn)
        self.Yp = 1 / self.Zp
        self.Ys = 1 / self.Zs

    def __str__(self):
        return (
            f"{self.nombre}:\n"
            f"  Sn:  {display_single(self.Sn)} VA\n"
            f"  Vn:    {display_single(self.Vp)} / {display_single(self.Vs)} V\n"
            f"  Bases: {self.bp.nombre:>11s} / {self.bs.nombre:>11s}\n"
            f"  Zev: {display_polar(self.Zev)} Ω pu\n"
            f"  Zp:  {display_rect(self.Zp)} Ω pu\n"
            f"  Zs:  {display_rect(self.Zs)} Ω pu\n"
            f"  Yp:  {display_rect(self.Yp)} ℧ pu\n"
            f"  Ys:  {display_rect(self.Ys)} ℧ pu\n"
        )


class TransformadorTap(TransformadorSimple):
    """Transformador con tap, basado en Transformador Simple

    Se asume que el tap esta conectado al primario

    Args:
        dt: regulacion por cada paso, Ej: 20% y 32 pasos -> dt = 0.2 / 32 = 0.00625
        pos: paso actual, 0 es el tap nominal, +1 es el tap por ensima, -1 el tap por devajo
    """

    def __init__(self, nombre, *, dt, pos, **kwargs):
        self.pos = pos
        self.dt = dt
        super().__init__(nombre, **kwargs)
        self.t = 1 + (self.dt * self.pos)
        self.Zs = self.Zp * self.t ** 2
        self.Ys = 1 / self.Zs

    def __str__(self):
        return (
            f"{self.nombre} (Tap {'+' if self.pos >=0 else '-'}{abs(self.pos)}):\n"
            f"  Sn:  {display_single(self.Sn)} VA\n"
            f"  Vn:    {display_single(self.Vp)} / {display_single(self.Vs)} V\n"
            f"  Bases: {self.bp.nombre:>11s} / {self.bs.nombre:>11s}\n"
            f"  t: {self.t}\n"
            f"  Zev: {display_polar(self.Zev)} Ω pu\n"
            f"  Zp:  {display_rect(self.Zp)} Ω pu\n"
            f"  Zs:  {display_rect(self.Zs)} Ω pu\n"
            f"  Yp:  {display_rect(self.Yp)} ℧ pu\n"
            f"  Ys:  {display_rect(self.Ys)} ℧ pu\n"
            f"  Ze / t:       {display_rect(self.Zp/self.t)} Ω pu\n"
            f"  Ze / (1-t):   {display_rect(self.Zp/(1-self.t))} Ω pu\n"
            f"  Ze / t(t-1):  {display_rect(self.Zp/(self.t**2-self.t))} Ω pu\n"
            f"  Ye * t:       {display_rect(self.Yp*self.t)} ℧ pu\n"
            f"  Ye * (1-t):   {display_rect(self.Yp*(1-self.t))} ℧ pu\n"
            f"  Ze * t(t-1):  {display_rect(self.Yp*(self.t**2-self.t))} ℧ pu\n"
        )


class TransformadorTriple(Elemento):
    """Transformador Trifasico de 3 devanados

    Tiene un lado primario, secundario y terciario

    Args:

    """

    def __init__(
        self,
        nombre,
        *,
        Snp,
        Sns,
        Snt,
        Vnp,
        Vns,
        Vnt,
        bp,
        bs,
        bt,
        Zept=None,
        Zeps=None,
        Zest=None,
    ):
        super().__init__(nombre)
        self.Snp = Snp
        self.Sns = Sns
        self.Snt = Snt
        self.Vnp = Vnp
        self.Vns = Vns
        self.Vnt = Vnt
        self.bp = bp
        self.bs = bs
        self.bt = bt
        self.Zept = Zept
        self.Zeps = Zeps
        self.Zest = Zest
        self.Zp = None
        self.Zs = None
        self.Zt = None
        self.Yp = None
        self.Ys = None
        self.Yt = None
        self.Zpt = self.Zept and cambio_base(
            self.Zept, self.Snp, self.Vnp, self.bp.Sb, self.bp.Vb
        )
        self.Zps = self.Zeps and cambio_base(
            self.Zeps, self.Snp, self.Vns, self.bs.Sb, self.bs.Vb
        )
        self.Zst = self.Zest and cambio_base(
            self.Zest, self.Snp, self.Vnt, self.bt.Sb, self.bt.Vb
        )
        self.Ypt = self.Zpt and 1 / self.Zpt
        self.Yps = self.Zps and 1 / self.Zps
        self.Yst = self.Zst and 1 / self.Zst
        self.tps = (self.bp.Vb / self.Vnp) / (self.bs.Vb / self.Vns)
        self.tpt = (self.bp.Vb / self.Vnp) / (self.bt.Vb / self.Vnt)
        self.tst = (self.bs.Vb / self.Vns) / (self.bt.Vb / self.Vnt)

    def pruebas_corto_circuito(self, *, Vpt, Ipt, Vps, Ips, Vst, Ist):
        zpt = (Vpt / self.bp.Vb) / (Ipt / self.bt.Ib)
        zps = (Vps / self.bp.Vb) / (Ips / self.bs.Ib)
        zst = (Vst / self.bs.Vb) / (Ist / self.bt.Ib)
        sumas = np.array([[zpt], [zps], [zst]])
        matris = np.array([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
        resultados = np.linalg.inv(matris).dot(sumas)
        [Zp], [Zs], [Zt] = resultados
        self.Zp = rect(Zp, 90)
        self.Zs = rect(Zs, 90)
        self.Zt = rect(Zt, 90)
        self.Yp = 1 / self.Zp
        self.Ys = 1 / self.Zs
        self.Yt = 1 / self.Zt

    def __str__(self):
        return (
            (
                f"{self.nombre}:\n"
                f"  Sn:    {display_single(self.Snp)} / {display_single(self.Sns)} / {display_single(self.Snt)} VA\n"
                f"  Vn:    {display_single(self.Vnp)} / {display_single(self.Vns)} / {display_single(self.Vnt)} V\n"
                f"  Bases: {self.bp.nombre:>11s} / {self.bs.nombre:>11s} / {self.bt.nombre:>11s}\n"
                f"  tps:   {self.tps}\n"
                f"  tpt:   {self.tpt}\n"
                f"  tst:   {self.tst}\n"
            )
            + (f"  Zpt: {display_rect(self.Zpt)} Ω pu\n" if self.Zpt else "")
            + (f"  Zps: {display_rect(self.Zps)} Ω pu\n" if self.Zps else "")
            + (f"  Zst: {display_rect(self.Zst)} Ω pu\n" if self.Zst else "")
            + (f"  Ypt: {display_rect(self.Ypt)} Ω pu\n" if self.Ypt else "")
            + (f"  Yps: {display_rect(self.Yps)} Ω pu\n" if self.Yps else "")
            + (f"  Yst: {display_rect(self.Yst)} Ω pu\n" if self.Yst else "")
            + (f"  Zp: {display_rect(self.Zp)} Ω pu\n" if self.Zp else "")
            + (f"  Zs: {display_rect(self.Zs)} Ω pu\n" if self.Zs else "")
            + (f"  Zt: {display_rect(self.Zt)} Ω pu\n" if self.Zt else "")
            + (f"  Yp: {display_rect(self.Yp)} Ω pu\n" if self.Yp else "")
            + (f"  Ys: {display_rect(self.Ys)} Ω pu\n" if self.Ys else "")
            + (f"  Yt: {display_rect(self.Yt)} Ω pu\n" if self.Yt else "")
            + (f"  Zp + Zs: {display_rect(self.Zp+self.Zs)} Ω pu\n" if self.Zp else "")
            + (f"  Zp + Zt: {display_rect(self.Zp+self.Zt)} Ω pu\n" if self.Zs else "")
            + (f"  Zs + Zt: {display_rect(self.Zt+self.Zs)} Ω pu\n" if self.Zt else "")
        )


class Valor(complex):
    TIPOS = {
        "S": (("W", "VAR", "VA"), "rect"),
        "V": ((None, None, "V"), "polar"),
        "I": ((None, None, "A"), "polar"),
        "Z": ((None, None, "Ω"), "rect"),
        "Y": ((None, None, "℧"), "rect"),
    }
    TIPO = None

    def __new__(cls, name, comp, barra=None):
        return super().__new__(cls, comp)

    def __init__(self, name, comp, barra=None):
        self.name = name
        self.unidad = self.TIPOS[self.TIPO][0] if self.TIPO else ("", " J", "")
        self.muestra = self.TIPOS[self.TIPO][1] if self.TIPO else "rect"
        self.barra = barra
        super().__init__()

    def __str__(self):
        u_fin = self.unidad[2] + (" pu" if self.barra else "")

        if self.muestra == "rect":
            if self.unidad[:2] == (None, None):
                val = display_rect(self, u_fin=u_fin)
            else:
                u_r = self.unidad[0] + (" pu" if self.barra else "")
                u_i = self.unidad[1] + (" pu" if self.barra else "")
                val = display_rect(self, u_r, u_i)
        elif self.muestra == "polar":
            val = display_polar(self, u_fin)
        return f"{self.name}: {val}"

    def absoluto(self):
        if self.barra:
            base = getattr(self.barra, self.TIPO + "b")
            valor = self * base
        else:
            valor = self
        return self.__class__(self.name, valor).__str__()


class S(Valor):
    TIPO = "S"


class V(Valor):
    TIPO = "V"


class I(Valor):
    TIPO = "I"


class Z(Valor):
    TIPO = "Z"


class Y(Valor):
    TIPO = "Y"


def test():
    r = DeltaEstrella("N1", "N2", "N3")
    r.impedanciaDelta(Zc=0.25j, Zb=0.4j, Za=0.25j)
    print(r)


# Comienzo

if __name__ == "__main__":
    test()
