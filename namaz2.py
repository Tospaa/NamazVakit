"""This is basically a web scraping program for getting praying times from a site.
You use a city name as the input and program scrapes it to give you the wanted values.

This program uses tkinter as GUI library and bs4 as parsing and manipulating html data.

Written by Musa Ecer musaecer@gmail.com

This program was designed for Python 3
"""

import urllib.request
from bs4 import BeautifulSoup
import tkinter
from time import strftime
from os.path import isfile

__author__ = "Musa Ecer"
__version__ = "0.3"
__email__ = "musaecer@gmail.com"


def sehir_bul():
    sehir = giris.get()
    sehir = sehir.replace("İ", "I")  # büyük i harfi olunca lower() fonksiyonu saçmalıyo. onu burda hallettim.
    sehir = sehir.lower()
    sehir = sehir.replace("ş", "s")
    sehir = sehir.replace("ı", "i")
    sehir = sehir.replace("ğ", "g")
    sehir = sehir.replace("ö", "o")
    sehir = sehir.replace("ü", "u")
    sehir = sehir.replace("ç", "c")

    if sehir == "adapazari" or sehir == "sakarya":
        sehir = "adapazari-sakarya"
    if sehir == "kocaeli":
        sehir = "izmit"
    if sehir == "afyonkarahisar":
        sehir = "afyon"

    return sehir


def site_bul():
    sehir = sehir_bul()

    sehirlink = "http://www.namazvakti.net/turkiye/{0}-diyanet-ezan-vakitleri.html".format(sehir)

    page = urllib.request.urlopen(sehirlink)
    site = BeautifulSoup(page, "lxml")  # lxml kütüphanesi yoksa bunu html.parser olarak değiştirebilirsin.
    return site


def kontrol():
    defter = open("data.txt").readlines()
    open("data.txt").close()
    defter2 = defter[0].split()
    if defter2[0] == strftime("%d") and defter2[1] == strftime("%m") and defter2[2] == strftime("%y"):
        durum = False
        for i in defter:
            i2 = i.split()
            if i2[0] == sehir_bul():
                durum = True
                break
        return durum
    else:
        return False


def main_func(*args):
    bilgiEtiket["fg"] = "black"
    bilgiEtiket["text"] = "Hesaplanıyor..."
    bilgiEtiket.update_idletasks()

    if not isfile("data.txt"):
        open("data.txt", "w").write("Selam\nDunya\n")
        open("data.txt").close()

    kitap = open("data.txt").readlines()
    open("data.txt").close()

    if kontrol():
        arblist = []
        for item in kitap:
            arblist = item.split()
            if arblist[0] == sehir_bul():
                break

        sabahLabel["text"] = arblist[1]
        ogleLabel["text"] = arblist[2]
        ikindiLabel["text"] = arblist[3]
        aksamLabel["text"] = arblist[4]
        yatsiLabel["text"] = arblist[5]

        bilgiEtiket["text"] = " "
    else:
        try:
            site = site_bul()
            sabahLabel["text"] = vakit("v im", site)
            ogleLabel["text"] = vakit("v og", site)
            ikindiLabel["text"] = vakit("v ik", site)
            aksamLabel["text"] = vakit("v ak", site)
            yatsiLabel["text"] = vakit("v ya", site)

            bilgiEtiket["text"] = "Sonlandırılıyor..."
            bilgiEtiket.update_idletasks()

            if (kitap[0].split()[0] + kitap[0].split()[1] + kitap[0].split()[2]) == strftime("%d%m%y"):
                veri = open("data.txt", "a")
                veri.write(
                    sehir_bul() + " " + sabahLabel["text"] + " " + ogleLabel["text"] + " " + ikindiLabel["text"] + " " +
                    aksamLabel["text"] + " " + yatsiLabel["text"] + "\n")
                veri.close()
            else:
                veri = open("data.txt", "w")
                veri.write(strftime("%d %m %y") + "\n")
                veri.write(
                    sehir_bul() + " " + sabahLabel["text"] + " " + ogleLabel["text"] + " " + ikindiLabel["text"] + " " +
                    aksamLabel["text"] + " " + yatsiLabel["text"] + "\n")
                veri.close()

            bilgiEtiket["text"] = " "

        except:
            sabahLabel["text"] = "00:00"
            ogleLabel["text"] = "00:00"
            ikindiLabel["text"] = "00:00"
            aksamLabel["text"] = "00:00"
            yatsiLabel["text"] = "00:00"

            bilgiEtiket["fg"] = "red"
            bilgiEtiket["text"] = "Ağ ya da girdi hatası."


def vakit(vak, sitesite):
    vakitlist = []

    for ul in sitesite.find_all("ul", vak):  # "ul" tagi içinde "vak" classında olanları al
        for li in ul.find_all("li"):  # yukarıda aldığın "ul"ların içindeki "li" taglarını al
            vakitlist.append(li.get_text())  # yukarıda bulduğun "li" taglarını "vakitlist"e ekle

    strvakit = vakitlist[1][-5:]  # listeden ikinci elemanı al ve bu elemanın da son 5 karakterini al, gerisini sil
    return strvakit


pencere = tkinter.Tk()
pencere.resizable(False, False)
pencere.title("Namaz Vakit v0.3")
pencere.wm_iconbitmap("info")
pencere.bind("<Return>", main_func)
label1 = tkinter.Label(text="Şehir giriniz: ")
giris = tkinter.Entry()
giris.insert(0, "Afyon")
buton = tkinter.Button(text="Hesapla", command=main_func)
label2 = tkinter.Label(text="Sabah Namazı: ", font=("Helvetica", 20))
label3 = tkinter.Label(text="Öğle Namazı: ", font=("Helvetica", 20))
label4 = tkinter.Label(text="İkindi Namazı: ", font=("Helvetica", 20))
label5 = tkinter.Label(text="Akşam Namazı: ", font=("Helvetica", 20))
label6 = tkinter.Label(text="Yatsı Namazı: ", font=("Helvetica", 20))
bilgiEtiket = tkinter.Label(text=" ", font=("Helvetica", 20))
sabahLabel = tkinter.Label(text="00:00", font=("Helvetica", 20))
ogleLabel = tkinter.Label(text="00:00", font=("Helvetica", 20))
ikindiLabel = tkinter.Label(text="00:00", font=("Helvetica", 20))
aksamLabel = tkinter.Label(text="00:00", font=("Helvetica", 20))
yatsiLabel = tkinter.Label(text="00:00", font=("Helvetica", 20))
label1.grid(row=0, column=0, sticky="w")
giris.grid(row=0, column=1, padx=10)
buton.grid(row=1, column=0, columnspan=2, sticky="we", pady=20)
label2.grid(row=2, column=0, sticky="w")
label3.grid(row=3, column=0, sticky="w")
label4.grid(row=4, column=0, sticky="w")
label5.grid(row=5, column=0, sticky="w")
label6.grid(row=6, column=0, sticky="w")
sabahLabel.grid(row=2, column=1, padx=10)
ogleLabel.grid(row=3, column=1, padx=10)
ikindiLabel.grid(row=4, column=1, padx=10)
aksamLabel.grid(row=5, column=1, padx=10)
yatsiLabel.grid(row=6, column=1, padx=10)
bilgiEtiket.grid(row=7, column=0, columnspan=2)

tkinter.mainloop()
