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
    return f"{round(val, 6):11}"


def display_polar(cmplx):
    mag, rad = cmath.polar(cmplx)
    deg = degrees(rad)
    return f"{round(mag,6):11} ∠ {round(deg, 4):10}°"


def display_rect(cmplx):
    return f"{round(cmplx.real,6):11} + {round(cmplx.imag, 6):11} J"


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

        Rn: Parametro de Resistencia de la linea en valor absoluto
        Xn: Parametro de REactancia de la linea en valor absoluto
        Gn: Parametro de Conductancia de la linea en valor absoluto
        Bn: Parametro de Suceptancia de la linea en valor absoluto

        bp: Barra del lado primario
        bp: Barra del lado secundario
    """

    def __init__(self, nombre, *, Sn, Vn, Rn, Xn, Gn, Bn, bp, bs):
        super().__init__(nombre)
        self.Sn = Sn
        self.Vn = Vn
        self.Rn = Rn
        self.Xn = Xn
        self.Gn = Gn
        self.Bn = Bn
        self.bp = bp
        self.bs = bs
        self.R = self.Rn / self.bp.Zb
        self.X = self.Xn / self.bp.Zb
        self.G = self.Gn / self.bp.Yb
        self.B = self.Bn / self.bp.Yb
        self.Y = 1 / complex(self.R, self.X)

    def __str__(self):
        return (
            f"{self.nombre}:\n"
            f"  Rn: {display_single(self.Rn)} Ω\n"
            f"  Xn: {display_single(self.Xn)} J Ω\n"
            f"  Gn: {display_single(self.Gn)} ℧\n"
            f"  Bn: {display_single(self.Bn)} J ℧\n"
            f"  R: {display_single(self.R)} Ω pu\n"
            f"  X: {display_single(self.X)} J Ω pu\n"
            f"  G: {display_single(self.G)} ℧ pu\n"
            f"  B: {display_single(self.B)} J ℧ pu\n"
            f"  Y: {display_rect(self.Y)} ℧ pu\n"
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


# Usos y practicas


def examen_practica():
    Sb = 50000000
    B4 = Barra("Barra 4", Sb=Sb, Vb=26000)
    print(B4)
    B8 = Barra("Barra 8", Sb=Sb, Vb=B4.Vb)
    print(B8)
    B9 = Barra("Barra 9", Sb=Sb, Vb=B8.Vb * 14.4 / 24)
    print(B9)
    B6 = Barra("Barra 6", Sb=Sb, Vb=B9.Vb * 34.5 / 13.8)
    print(B6)
    B7 = Barra("Barra 7", Sb=Sb, Vb=B6.Vb)
    print(B7)
    B2 = Barra("Barra 2", Sb=Sb, Vb=B7.Vb * 138 / 34.5)
    print(B2)
    B3 = Barra("Barra 3", Sb=Sb, Vb=B2.Vb)
    print(B3)
    B1 = Barra("Barra 1", Sb=Sb, Vb=B6.Vb * 13.8 / 34.5)
    print(B1)
    B5 = Barra("Barra 5", Sb=Sb, Vb=B4.Vb * 13.8 / 24)
    print(B5)

    L23 = Linea(
        "Linea 2-3",
        Sn=25000000,
        Vn=138000,
        Rn=8.5698,
        Xn=51.0379,
        Gn=0,
        Bn=0.000315,
        bp=B2,
        bs=B3,
    )
    print(L23)

    Tx2 = TransformadorSimple(
        "Tx2",
        Sn=25000000,
        Vp=138000,
        bp=B3,
        Vs=24000,
        bs=B4,
        Zev=0.075,
        rel=4,
    )
    print(Tx2)
    Tx4 = TransformadorSimple(
        "Tx4",
        Sn=25000000,
        Vp=24000,
        bp=B8,
        Vs=14400,
        bs=B9,
        Zev=0.0525,
        rel=4,
    )
    print(Tx4)

    Tx5 = TransformadorTap(
        "Tx5",
        Sn=25000000,
        Vp=24000,
        bp=B4,
        Vs=13800,
        bs=B5,
        Zev=0.0475,
        rel=4,
        dt=0.1 / 4,
        pos=+3,
    )
    print(Tx5)


def examen_practica_2():
    Sb = 100000000

    B6 = Barra("Barra 6", Sb=Sb, Vb=65000)
    B7 = Barra("Barra 7", Sb=Sb, Vb=B6.Vb)
    B8 = Barra("Barra 8", Sb=Sb, Vb=B7.Vb * 138 / 69)
    B9 = Barra("Barra 9", Sb=Sb, Vb=B7.Vb * 14.4 / 69)
    B4 = Barra("Barra 4", Sb=Sb, Vb=B8.Vb)
    B5 = Barra("Barra 5", Sb=Sb, Vb=B4.Vb * 20 / 115)
    B3 = Barra("Barra 3", Sb=Sb, Vb=B4.Vb)
    B2 = Barra("Barra 2", Sb=Sb, Vb=B3.Vb)
    B1 = Barra("Barra 1", Sb=Sb, Vb=B2.Vb * 18 / 115)
    print(B6)
    print(B7)
    print(B8)
    print(B9)
    print(B4)
    print(B5)
    print(B3)
    print(B2)
    print(B1)

    Tx3 = TransformadorSimple(
        "Tx3", Sn=100000000, Vp=115000, bp=B4, Vs=20000, bs=B5, Zev=0.12, rel=6.2
    )
    print(Tx3)
    Tx2 = TransformadorTriple(
        "Tx2",
        Snp=60000000,
        Sns=35000000,
        Snt=25000000,
        Vnp=138000,
        Vns=69000,
        Vnt=14400,
        bp=B8,
        bs=B7,
        bt=B9,
        Zept=rect(0.055, 90),
        Zeps=rect(0.063, 90),
        Zest=rect(0.072, 90),
    )
    print(Tx2)
    Tx1 = TransformadorTriple(
        "Tx1",
        Snp=65000000,
        Sns=45000000,
        Snt=20000000,
        Vnp=115000,
        Vns=69000,
        Vnt=18000,
        bp=B2,
        bs=B6,
        bt=B1,
    )
    Tx1.pruebas_corto_circuito(Vps=3000, Ips=300, Vpt=2000, Ipt=100, Vst=1600, Ist=560)
    print(Tx1)
    Cs = BancoCondensadores("Cs", Qn=26000, In=500, Prel=0.013, bp=B4, bs=B3)
    print(Cs)


def examen_1():
    Sb = 70000000

    B3 = Barra("Barra 3", Sb=Sb, Vb=120000)
    B2 = Barra("Barra 2", Sb=Sb, Vb=B3.Vb)
    B4 = Barra("Barra 4", Sb=Sb, Vb=B3.Vb)
    B5 = Barra("Barra 5", Sb=Sb, Vb=B4.Vb * 26 / 115)
    B8 = Barra("Barra 8", Sb=Sb, Vb=B4.Vb)
    B9 = Barra("Barra 9", Sb=Sb, Vb=B8.Vb * 13.8 / 115)
    B7 = Barra("Barra 7", Sb=Sb, Vb=B8.Vb * 72 / 115)
    B6 = Barra("Barra 6", Sb=Sb, Vb=B7.Vb)
    B1 = Barra("Barra 1", Sb=Sb, Vb=B6.Vb * 20 / 72)
    print(B2)
    print(B3)
    print(B4)
    print(B5)
    print(B8)
    print(B9)
    print(B7)
    print(B6)
    print(B1)

    l1 = 170
    L23 = Linea(
        "Linea 2-3",
        Sn=75000000,
        Vn=138000,
        Rn=l1 * 0.1,
        Xn=l1 * 0.404,
        Gn=0,
        Bn=l1 * 0.292 * 10 ** -6,
        bp=B2,
        bs=B3,
    )
    print(L23)
    L48 = Linea(
        "Linea 4-8",
        Sn=75000000,
        Vn=138000,
        Rn=l1 * 0.1,
        Xn=l1 * 0.404,
        Gn=0,
        Bn=l1 * 0.292 * 10 ** -6,
        bp=B4,
        bs=B8,
    )
    print(L48)
    l2 = 45
    L67 = Linea(
        "Linea 6-7",
        Sn=45000000,
        Vn=72000,
        Rn=l2 * 0.18,
        Xn=l2 * 0.5,
        Gn=0,
        Bn=l2 * 0.7 * 10 ** -6,
        bp=B4,
        bs=B8,
    )
    print(L67)

    Tx3 = TransformadorTap(
        "Tx3",
        Sn=100000000,
        Vp=115000,
        bp=B4,
        Vs=26000,
        bs=B5,
        Zev=0.075,
        rel=4,
        dt=0.0455,
        pos=-1,
    )
    print(Tx3)
    Tx2 = TransformadorTriple(
        "Tx2",
        Snp=75000000,
        Sns=45000000,
        Snt=25000000,
        Vnp=138000,
        Vns=72000,
        Vnt=13800,
        bp=B8,
        bs=B7,
        bt=B9,
        Zept=rect(0.05, 90),
        Zeps=rect(0.06, 90),
        Zest=rect(0.07, 90),
    )
    print(Tx2)
    Tx1 = TransformadorTriple(
        "Tx1",
        Snp=75000000,
        Sns=45000000,
        Snt=25000000,
        Vnp=138000,
        Vns=72000,
        Vnt=20000,
        bp=B2,
        bs=B6,
        bt=B1,
    )
    Tx1.pruebas_corto_circuito(Vps=2800, Ips=280, Vpt=1800, Ipt=90, Vst=1440, Ist=504)
    print(Tx1)

    print(V2_fic := B6.Vb / 72 * 138)
    print(t := B2.Vb / V2_fic)
    print(tap_fic(Tx1.Zp, t))

    G1 = Generador("G1", Sn=65000000, Vn=20000, Zev=rect(1.35, 90), b=B1)
    G2 = Generador("G2", Sn=100000000, Vn=26000, Zev=rect(1.65, 90), b=B5)
    print(G1)
    print(G2)

    Cs = BancoCondensadores("Cs", Qn=0.007 * 10 ** 6, In=256, Prel=0.0165, bp=B3, bs=B4)
    print(Cs)

    # Cs = BancoCondensadores("Cs", Qn=26000, In=500, Prel=0.013, bp=B4, bs=B3)
    # print(Cs)


def test():
    r = DeltaEstrella("N1", "N2", "N3")
    r.impedanciaDelta(Zc=0.25j, Zb=0.4j, Za=0.25j)
    print(r)


# Comienzo

if __name__ == "__main__":
    test()
