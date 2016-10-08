import pylab as pl
class uranium_decay:
    def __init__(self, NA = 100,NB = 0, tc = 1, td = 5, ts = 0.05):
        self.na = [NA]
        self.nb = [NB]
        self.t = [0]
        self.tau = tc
        self.dt = ts
        self.time = td
        self.ns = int(td//ts + 1)
    def calculate(self):
        for i in range(self.ns):
            ta = self.na[i] + (self.nb[i]-self.na[i])/self.tau * self.dt
            tb = self.nb[i] + (self.na[i]-self.nb[i])/self.tau * self.dt
            self.nb.append(tb)
            self.na.append(ta)
            self.t.append(self.t[i] + self.dt)
    def show_results(self):
        pl.plot(self.t, self.na, 'g-')
        pl.plot(self.t, self.nb, 'r-')
        pl.xlabel('time ($s$)')
        pl.ylabel('Number of Nuclei')
        pl.legend(['$NA$','$NB$']) 
        pl.grid() 
        pl.show()

a = uranium_decay()
a.calculate()
a.show_results()
