from datetime import datetime
import pygal
import smtplib
import io
from contextlib import redirect_stdout

class Stoc:
    """tine stocul unui depozit"""
    def __init__(self, prod, categ, um='Buc', soldminim=0, adresa_atentionare='mailpentruclasastoc@gmail.com', sold=0):
        self.prod = prod
        self.categ = categ
        self.sold = sold
        self.um = um
        #sold minim pentru fiecare produs in parte, cu default 0 in caz ca nu se seteaza de la inceput
        self.soldminim = soldminim
        #adresa pentru receptorul emailului de atentionare, setat default, dar merge personalizat per produs
        self.mail = adresa_atentionare
        self.i = {}
        self.e = {}
        self.d = {}


    def intr(self, cant, data=str(datetime.now().strftime('%Y-%m-%d'))):
        """se pot face intrarile in stocul magazinului, ca si atribut primeste cantitatea"""
        self.data = data
        self.cant = cant
        self.sold += self.cant
        if self.d.keys():
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.i[cheie] = self.cant
        self.d[cheie] = self.data



    def iesi(self, cant, data=str(datetime.now().strftime('%Y-%m-%d'))):
        """se pot face iesirile din stocul magazinului, ca si atribut primeste cantitatea"""
        self.data = data
        self.cant = cant
        self.sold -= self.cant
        # am facut in asa fel incat stocul sa nu scada sub zero, ar fi imposibil daca nu ai destule produse
        # daca intra in if-ul asta, nu se mai inregistreaza in dictionare pentru a nu avea informatii gresite, else se inregistreaza cu succes o intrare valida
        if self.sold < 0:
            self.sold += self.cant
            print("ATENTIE, SOLD INSUFICIENT PENTRU IESIRE, SOLD MAXIM DE IESIT:", self.sold)
        #aici este partea cu soldul minim impus per produs, se anunta local prin print la folosirea metodei, dar se trimite si mail de atentionare
        elif self.sold <= self.soldminim:
            print("ATENTIE, SOLD MINIM IMPUS ATINS")
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login('mailpentruclasastoc@gmail.com', 'Parola13')
                message = 'Subject: {}\n\n{}'.format('ATENTIE STOC', 'Atentie! Stoc minim impus pentru ' + str(self.prod) + ' atins!' + ' (' + str(self.soldminim) + ' ' + str(self.um) + ')')
                server.sendmail('mailpentruclasastoc@gmail.com', self.mail, message)
                server.quit()
            except:
                print("Am esuat sa trimit emailul de atentionare!!")
            if self.d.keys():
                cheie = max(self.d.keys()) + 1
            else:
                cheie = 1
            self.e[cheie] = self.cant
            self.d[cheie] = self.data
        else:
            if self.d.keys():
                cheie = max(self.d.keys()) + 1
            else:
                cheie = 1
            self.e[cheie] = self.cant
            self.d[cheie] = self.data


    def fisap(self):
        """fisa produsului ales, tiparita local cu print"""
        print('Fisa produsului ' + self.prod + ': ' + self.um)
        print(40 * '-')
        print(' Nrc ', '  Data  ', ' Intrari ', '  Iesiri')
        print(40 * '-')
        for v in self.d.keys():
            if v in self.i.keys():
                print(str(v).rjust(5), self.d[v], str(self.i[v]).rjust(6), str(0).rjust(6))
            else:
                print(str(v).rjust(5), self.d[v], str(0).rjust(6), str(self.e[v]).rjust(6))
        print(40 * "-")
        print('Stoc actual:      ' + str(self.sold).rjust(10))
        print(40 * '-' + '\n')


    def graficprodus(self, luna):
        """metoda pentru un pie chart al unui produs ales cu intrari si iesiri pentru luna specificata in formatul 'Luna' sau 'luna'"""
        #liste folosite de pygal pentru grafic
        lista_intrari = []
        lista_iesiri = []
        #lista pentru corelarea lunii alese si intrarile/iesirile ce corespund lunii
        chei_luna = []
        #caut in dictionarul de data al produsului luna aleasa si cheia pentru intrare/iesire
        if luna == "Ianuarie" or luna == 'ianuarie':
            for cheie, valoare in self.d.items():
                if "-01-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Februarie" or luna == 'februarie':
            for cheie, valoare in self.d.items():
                if "-02-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Martie" or luna == 'martie':
            for cheie, valoare in self.d.items():
                if "-03-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Aprilie" or luna == 'aprilie':
            for cheie, valoare in self.d.items():
                if "-04-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Mai" or luna == 'mai':
            for cheie, valoare in self.d.items():
                if "-05-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Iunie" or luna == 'iunie':
            for cheie, valoare in self.d.items():
                if "-06-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Iulie" or luna == 'iulie':
            for cheie, valoare in self.d.items():
                if "-07-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "August" or luna == 'august':
            for cheie, valoare in self.d.items():
                if "-08-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Septembrie" or luna == 'septembrie':
            for cheie, valoare in self.d.items():
                if "-09-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Octombrie" or luna == 'octombrie':
            for cheie, valoare in self.d.items():
                if "-10-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Noiembrie" or luna == 'noiembrie':
            for cheie, valoare in self.d.items():
                if "-11-" in valoare:
                    chei_luna.append(cheie)
        elif luna == "Decembrie" or luna == 'decembrie':
            for cheie, valoare in self.d.items():
                if "-12-" in valoare:
                    chei_luna.append(cheie)
        #in cazul in care nu exista intrari/iesiri in luna respectiva pentru produsul ales nu se populeaza lista chei_luna, nu are rost sa facem un grafic, else facem grafic
        if not chei_luna:
            pass
        else:
            #comparam cheile pentru luna aleasa cu intrarile si iesirile din luna respectiva
            for key, value in self.i.items():
                for nr in chei_luna:
                    if nr == key:
                        lista_intrari.append(value)
            for key, value in self.e.items():
                for nr in chei_luna:
                    if nr == key:
                        lista_iesiri.append(value)
            pie_chart = pygal.Pie()
            pie_chart.title = 'Raport pentru ' + str(self.prod) + ' in luna ' + luna
            pie_chart.add('Intrari', lista_intrari)
            pie_chart.add('Iesiri', lista_iesiri)
            pie_chart.render_to_file(str(self.prod + '_pie_chart_' + luna + '.svg'))


    def trimite_fisap(self, receptor='mailpentruclasastoc@gmail.com'):
        """metoda pentru trimiterea pe email a fisei produsului, primeste ca atribut emailul receptorului"""

        #capturez printul din metoda fisap intr-o variabila pentru a o putea trimite pe email
        f = io.StringIO()
        with redirect_stdout(f):
            self.fisap()
        out = f.getvalue()

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('mailpentruclasastoc@gmail.com', 'Parola13')
            message = 'Subject: {}\n\n{}'.format('Fisa produsului pentru ' + self.prod, out)
            server.sendmail('mailpentruclasastoc@gmail.com', receptor, message)
            server.quit()
            print("Email trimis cu succes!")
        except:
            print("Am esuat sa trimit emailul cu fisa postului!!")




peste = Stoc('peste', 'carne', 'kg', 50, 'dreamer.lego@yahoo.com')
lapte = Stoc('lapte', 'lactate', 'litri')
televizoare = Stoc('televizoare', 'televizoare', 'buc', 10)



peste.intr(50)
peste.intr(500)
peste.intr(50)
peste.intr(100)
peste.iesi(400)
peste.iesi(50)

lapte.intr(100)
lapte.intr(100)
lapte.intr(100)
lapte.iesi(200)
lapte.iesi(50)
lapte.iesi(30)

televizoare.intr(300)
televizoare.intr(300)
televizoare.intr(300)
televizoare.iesi(300)


lapte.fisap()

televizoare.fisap()

televizoare.trimite_fisap()

televizoare.graficprodus('martie')

lapte.soldminim = 20

lapte.graficprodus('martie')

peste.trimite_fisap('dreamer.lego@yahoo.com')

peste.graficprodus('martie')

peste.fisap()


























