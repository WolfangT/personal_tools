from tools import *


def main():
    Sb = 100 * 10 ** 6
    Vb = 230000
    print(B1 := Barra("Birch", Sb=Sb, Vb=Vb))
    B2 = Barra("Elm", Sb=Sb, Vb=Vb)
    B3 = Barra("Pine", Sb=Sb, Vb=Vb)
    B4 = Barra("Maple", Sb=Sb, Vb=Vb)
    print(B5 := Barra("B5", Sb=Sb, Vb=Vb * 115 / 230))
    print(L12 := Linea("L12", R=0.01008, X=0.05040, G=0, B=0.05125 * 2, bp=B1, bs=B2))
    # print(L12.flujo_potencias())
    print(L13 := Linea("L13", R=0.00744, X=0.03720, G=0, B=0.03875 * 2, bp=B1, bs=B3))
    # print(L13.flujo_potencias())
    print(L24 := Linea("L24", R=0.00744, X=0.03720, G=0, B=0.03875 * 2, bp=B2, bs=B4))
    # print(L24.flujo_potencias())
    print(L34 := Linea("L34", R=0.01272, X=0.06360, G=0, B=0.06375 * 2, bp=B3, bs=B4))
    # print(L34.flujo_potencias())
    print(
        TX1 := TransformadorTap(
            "TX53",
            dt=0.2 / 32,
            pos=+12,
            Sn=310 * 10 ** 6,
            Vp=115000,
            Vs=230000,
            Zev=0.0625,
            rel=3.487,
            bp=B5,
            bs=B3,
        )
    )
    # print(TX1.flujo_potencias())
    print(
        Cx := BancoCapasitores(
            "CX1",
            bp=B5,
            Sn=57.5j * 10 ** 6 / B5.Sb,
            Vn=TX1.Vp / B5.Vb,
            pj=0.03,
        )
    )
    print(
        G2 := GeneradorIdeal(
            "G2",
            bp=B4,
            Pn=330 * 10 ** 6,
            Vn=234968,
            Qnmin=-7.3 * 10 ** 6,
            Qnmax=200 * 10 ** 6,
        )
    )
    print(C1 := CargaIdeal("C1", bp=B1, Pn=50 * 10 ** 6, Qn=30.99 * 10 ** 6))
    print(C2 := CargaIdeal("C2", bp=B2, Pn=170 * 10 ** 6, Qn=105.35 * 10 ** 6))
    print(C3 := CargaIdeal("C3", bp=B3, Pn=0, Qn=0))
    print(C4 := CargaIdeal("C4", bp=B4, Pn=80 * 10 ** 6, Qn=49.58 * 10 ** 6))
    print(C5 := CargaIdeal("C5", bp=B5, Pn=200 * 10 ** 6, Qn=123.94 * 10 ** 6))
    print("Matris Admitancias")
    print(
        Ym := np.matrix(
            [
                [L12.Yp0 + L12.Yps + L13.Yp0 + L13.Yps, -L12.Yps, -L13.Yps, 0, 0],
                [-L12.Yps, L12.Ys0 + L12.Yps + L24.Yp0 + L24.Yps, 0, -L24.Yps, 0],
                [
                    -L13.Yps,
                    0,
                    L13.Yp0 + L13.Ys0 + L34.Yp0 + L34.Yps + TX1.Yps + TX1.Yp0,
                    -L34.Yps,
                    -TX1.Yps,
                ],
                [0, -L24.Yps, -L34.Yps, L24.Yps + L24.Ys0 + L34.Yps + L34.Ys0, 0],
                [0, 0, -TX1.Yps, 0, TX1.Yps + TX1.Ys0 + Cx.Yn],
            ]
        )
    )


if __name__ == "__main__":
    main()
