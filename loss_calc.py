import random
from math import tanh, exp
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from statistics import mean, stdev

lam = 0
profit_rate = 1.5

list_exp = []

class Person:
    profession: str
    eng_prof: int
    age: float
    education: int
    past_exp: int
    cost_of_living: int
    total_cost: float
    eng_ready: bool
    trained: bool
    months_elapsed: int
    working: bool
    interest: float
    default_rate: float
    monthly_payment: float
    total_paid: float
    defaulted: bool
    total_due: float
    lam: float

    def __init__(self, eng_prof, profession):
        self.total_paid = 0
        self.working = False
        self.trained = False
        self.defaulted = False
        self.profession = profession
        self.months_elapsed = 0
        self.eng_prof = eng_prof
        self.total_cost = 0
        self.default_rate = self.get_def(eng_prof)
        self.interest = self.get_int()
        if eng_prof >= 9:
            self.eng_ready = True
        else:
            self.eng_ready = False

    def increment_english(self):
        r = random.randint(1, 13)
        if self.eng_prof == 0:
            if r<=5:
                self.eng_prof += 1
        elif self.eng_prof == 1:
            if r<=6:
                self.eng_prof += 1
        elif self.eng_prof == 2:
            if r<=7:
                self.eng_prof += 1
        elif self.eng_prof == 3:
            if r<=8:
                self.eng_prof += 1
        elif self.eng_prof == 4:
            if r<=9:
                self.eng_prof += 1
        elif self.eng_prof == 5:
            if r<=10:
                self.eng_prof += 1
        elif self.eng_prof == 6:
            if r<=11:
                self.eng_prof += 1
        elif self.eng_prof == 7:
            if r<=10:
                self.eng_prof += 1
        elif self.eng_prof == 8:
            if r<=9:
                self.eng_prof += 1
        elif self.eng_prof == 9:
            if r<=8:
                self.eng_prof += 1
        elif self.eng_prof == 10:
            if r<=7:
                self.eng_prof += 1
        elif self.eng_prof == 11:
            if r<=6:
                self.eng_prof += 1

        if self.eng_prof >= 9:
            self.eng_ready= True

    def train(self):
        if self.profession == 'Nursing':
            self.total_cost += random.randint(1000, 5000) #TODO: Change
            self.months_elapsed += 4 #5 months total

        self.trained = True

    def myMonthlyPayment(self, principal, annual_r, years):
        n = years * 12  # number of monthly payments
        r = (annual_r) / 12  # decimal monthly interest rate from APR
        MonthlyPayment = (r * principal * ((1 + r) ** n)) / (((1 + r) ** n) - 1)
        self.total_due = MonthlyPayment*years*12
        return MonthlyPayment

    def default(self, default_rate_10_years):
        rate = 1 - ((1 - default_rate_10_years) ** (1 / 120))
        if random.uniform(0, 1) < rate:
            return True
        return False

    def make_payment(self):
        self.total_paid += self.monthly_payment
        self.total_due -= self.monthly_payment

    def done_payments(self):
        if not self.working:
            return False
        elif self.defaulted:
            return True
        else:
            return self.total_due < 5

    def run_month(self):
        self.months_elapsed += 1
        if not self.working:
            if not self.eng_ready:
                self.months_elapsed += 1
                self.increment_english()
                self.total_cost += 400
            elif not self.trained:
                self.train()
            else:
                self.total_cost *= 1 + self.interest/12
                r = random.randint(1, 5) #TODO: Make better
                if r==1:
                    self.monthly_payment = self.myMonthlyPayment(self.total_cost, self.interest, 10)
                    self.working = True
        else:
            if not self.defaulted:
                if self.default(self.default_rate):
                    self.defaulted = True
                else:
                    self.make_payment()

    def get_def(self, eng_prof):

        A = [0, 0, 0, 0, 0]
        a = [0.1, 0.2, 0.3, 0.4, 0.5]

        # CPI
        r = random.uniform(127, 141)
        A[0] = (r - 126.7) / 14

        # EXP
        r = random.uniform(0, 15)
        A[1] = tanh(r / 3)

        # EDU
        r = random.uniform(60.8, 82.8)
        A[2] = (r - 60.8) / 22

        # ENG
        r = eng_prof
        A[3] = 1 / (1 + exp(-r + 6))

        # IND
        r = random.uniform(377, 3541)
        A[4] = (r - 377) / (3541 - 377)

        b = sum([A[i] * a[i] for i in range(5)]) / sum(a)
        q = 0.2 - 0.2 * b
        self.lam = tanh(3 * b)
        return q

    def f(self, x):
        return (1 - (1 + x / 12) ** (-1 * 120 * self.lam)) / (
                    x * 10 * self.lam) - 1 / profit_rate

    def get_int(self):
        return optimize.newton(self.f, 0.2)


# for i in range(5000):
#
#     A = [0, 0, 0, 0, 0]
#     a = [0.1, 0.2, 0.3, 0.4, 0.5]
#
#     #CPI
#     r = random.uniform(127, 141)
#     A[0] = (r-126.7)/14
#
#     #EXP
#     r = random.uniform(0, 15)
#     A[1] = tanh(r/3)
#
#     #EDU
#     r = random.uniform(60.8, 82.8)
#     A[2] = (r-60.8)/22
#
#     #ENG
#     r = random.randint(0, 13)
#     A[3] = 1/(1+exp(-r+6))
#
#     #IND
#     r = random.uniform(377, 3541)
#     A[4] = (r-377)/(3541-377)
#
#     b = sum([A[i]*a[i] for i in range(5)])/sum(a)
#     rounded_b = round(b*100)
#     lam = tanh(3*b)
#
#     q = 0.3 - 0.3*b
#
#     list_exp += [4000*q*(1-lam)]



# bins = np.arange(0, 1000, 50)
#plt.hist(list_exp, normed=True, bins=bins)
# plt.show()






# def get_lam(eng_prof):
#
#     A = [0, 0, 0, 0, 0]
#     a = [0.1, 0.2, 0.3, 0.4, 0.5]
#
#     #CPI
#     r = random.uniform(127, 141)
#     A[0] = (r-126.7)/14
#
#     #EXP
#     r = random.uniform(0, 15)
#     A[1] = tanh(r/3)
#
#     #EDU
#     r = random.uniform(60.8, 82.8)
#     A[2] = (r-60.8)/22
#
#     #ENG
#     r = eng_prof
#     A[3] = 1/(1+exp(-r+6))
#
#     #IND
#     r = random.uniform(377, 3541)
#     A[4] = (r-377)/(3541-377)
#
#     b = sum([A[i]*a[i] for i in range(5)])/sum(a)
#     q = 0.3 - 0.3*b
#     return tanh(3*b)







list_of_costs = []
list_of_repay = []
list_of_people = []
list_of_months = []
list_of_monthly = []
list_of_interest = []
list_of_default_rate = []
num_people = 0
num_defaulted = 0
num_accepted = 0
while num_people < 10000:
    num_people += 1
    r = random.randint(0,13) #Change
    p = Person(r, "Nursing")
    list_of_people += [p]

    while not p.done_payments():
        p.run_month()

    if p.monthly_payment > 75:
        continue

    if p.defaulted:
        num_defaulted += 1

    num_accepted += 1
    list_of_default_rate += [p.default_rate]
    list_of_costs += [p.total_cost]
    list_of_repay += [p.total_paid]
    list_of_months += [p.months_elapsed]
    list_of_monthly += [p.monthly_payment]
    list_of_interest += [p.interest]


print(num_people, num_accepted, num_defaulted)
print(mean(list_of_costs), stdev(list_of_costs))
print(mean(list_of_repay), stdev(list_of_repay))
print(mean(list_of_monthly))
print(mean(list_of_repay)/mean(list_of_costs))
print(mean(list_of_months))
print(mean(list_of_interest), stdev(list_of_interest))

bin1 = np.arange(0, 0.3, 0.01)
plt.hist(list_of_interest, bins=bin1, normed=True)
plt.show()

bins = np.arange(0, 200, 10)
plt.hist(list_of_monthly, normed=True, bins=bins)
#plt.hist(list_of_costs, normed=True, bins=bins)
plt.show()

bins = np.arange(0, 1, 0.03)
plt.hist(list_of_default_rate, normed=True, bins=bins)
plt.show()
