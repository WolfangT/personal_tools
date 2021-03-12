from tools import *

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


def main():
    Sb = 100 * 10 ** 6
    Vb = 230000
    B5 = Barra("Tablaso", Sb=Sb, Vb=Vb)
    B4 = Barra("Morochas", Sb=Sb, Vb=Vb)
    print(B5)
    print(B4)
    R = 67 * 0.0702 / B5.Zb


if __name__ == "__main__":
    main()
