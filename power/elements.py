class Element:
    def __init__(self, *, Sn=None, Sb=None, Vb=None, Ib=None, Zb=None, **kwargs):
        self.Sn = Sn
        self.Sb = Sb
        self.Vb = Vb
        self.Ib = Ib
        self.Zb = Zb

    def calculate_bases(self):
        self.Ib = self.Sb / self.Vb / sqrt(3)
        self.Zb = self.Vb ** 2 / self.Sb
        self.Yb = 1 / self.Zb


class Transformer(Element):
    def __init__(self, *, Vn1, Vn2, Zpu, Vb1=None, Vb2=None, **kwargs):
        self.Vb1 = Vb1
        self.Vb2 = Vb2
        self.Vn1 = Vn1
        self.Vn2 = Vn2
        self.Zpu = Zpu
        super().__init__(**kwargs)

    def calculate_bases(self):
        self.Ib1 = self.Sb / self.Vb1 / sqrt(3)
        self.Zb1 = self.Vb1 ** 2 / self.Sb
        self.Yb1 = 1 / self.Zb1
        self.Ib2 = self.Sb / self.Vb2 / sqrt(3)
        self.Zb2 = self.Vb2 ** 2 / self.Sb
        self.Yb2 = 1 / self.Zb2


Yp1 = -51.008697j
Ys1 = -17.00864j
Yt1 = -11.9250108j + (1 / ((1 / -11.911001j) + (1 / 1.667185j)))
Vp = 100
Ip = Vp * (1 / ((1 / Yp1) + (1 / (Ys1 + Yt1))))
print(display_rect(Ip))
