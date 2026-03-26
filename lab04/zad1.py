import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

class SimpleNet:
    def __init__(self):
        self.w1, self.w2, self.b1 =  0.2, -0.3,  0.4
        self.w3, self.w4, self.b2 = -0.5,  0.1, -0.2
        self.w5, self.w6, self.b3 =  0.3, -0.4,  0.2

    def forward(self, feature1, feature2):
        self.feature1, self.feature2 = feature1, feature2 

        self.prognoza1 = self.w1*feature1 + self.w2*feature2 + self.b1 
        self.wartosc_prognoza1 = sigmoid(self.prognoza1) 

        self.prognoza2 = self.w3*feature1 + self.w4*feature2 + self.b2
        self.wartosc_prognoza2 = sigmoid(self.prognoza2)

        self.ostateczna_prognoza = self.w5*self.wartosc_prognoza1 + self.w6*self.wartosc_prognoza2 + self.b3
        return self.ostateczna_prognoza

    def train(self, wlasciwa_odpowiedz, wrazliwosc_zmian=0.1): 
        L = 0.5 * (self.ostateczna_prognoza - wlasciwa_odpowiedz)**2 

        rozbieznosc = self.ostateczna_prognoza - wlasciwa_odpowiedz 

        d1 = rozbieznosc * self.w5 * self.wartosc_prognoza1 * (1 - self.wartosc_prognoza1)
        d2 = rozbieznosc * self.w6 * self.wartosc_prognoza2 * (1 - self.wartosc_prognoza2)
        
        self.w5 -= wrazliwosc_zmian * rozbieznosc * self.wartosc_prognoza1 
        self.w6 -= wrazliwosc_zmian * rozbieznosc * self.wartosc_prognoza2
        self.b3 -= wrazliwosc_zmian * rozbieznosc

        self.w1 -= wrazliwosc_zmian * d1 * self.feature1
        self.w2 -= wrazliwosc_zmian * d1 * self.feature2
        self.b1 -= wrazliwosc_zmian * d1
        
        self.w3 -= wrazliwosc_zmian * d2 * self.feature1
        self.w4 -= wrazliwosc_zmian * d2 * self.feature2
        self.b2 -= wrazliwosc_zmian * d2

        return L

siec = SimpleNet()

y_hat = siec.forward(0.6, 0.1)
print(f"Forward bez treningu: {y_hat:.3f}")

L = siec.train(0.8)
print(f"Strata bez treningu: {L:.3f}")
print(f"w5={siec.w5:.3f} w6={siec.w6:.3f}")

siec_pod_nauke = SimpleNet()
for _ in range(10):
    siec_pod_nauke.forward(0.6, 0.1)
    L = siec_pod_nauke.train(0.8)

y_hat_final = siec_pod_nauke.forward(0.6, 0.1)
print(f"\nPo nauce: ŷ={y_hat_final}  cel=0.8  strata={L:.5f}")