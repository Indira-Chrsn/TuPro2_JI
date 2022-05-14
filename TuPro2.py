from ast import Or
from re import M, X
from textwrap import dedent
from numpy import maximum, real
import pandas as pd
import xlsxwriter
from operator import itemgetter

'''
- di bawah ini adalah variabel data digunakan untuk membaca file bengkel.xlsx
- df merupakan variabel yang digunakan untuk menampung data-data pada file bengkel.xlsx dengan format data frame
singkatnya, section di bawah ini untuk membaca file bengkel.xlsx dan mengubahnya menjadi bentuk data frame di python.
'''
data = pd.read_excel(r'C:\Users\User\Downloads\bengkel.xlsx')
df = pd.DataFrame(data)

'''
- membuat list yang menampung values dari masing-masing kolom yang ada di file bengkel.xlsx (id, servis, dan harga) untuk mempermudah perhitungan fuzzy
- variable dfcp digunakan untuk menampung fungsi df.copy yang berfungsi untuk mengcopy values dari kolom yang dipilih.
- Values dari masing-masing kolom kemudian dimasukkan ke dalam list yang telah dibuat sebelumnya dengan menggunakan fungsi append
'''
dfcp = df.copy()
id = []
servis = []
harga = []
i = 0
while (i < len(df)):
    id.append(dfcp.id[i])
    servis.append(dfcp.servis[i])
    harga.append(dfcp.harga[i])
    # id[i] = dfcp.id[i]
    i+=1

# print("id: ",id)
# print("servis: ",servis)
# print("harga: ",harga)
# print("\n\n")

'''
==== MEMBERSHIP FUNCTION INPUT ====



=== SERVIS ===
jumlah linguistic: 4
nama linguistic: tidak memuaskan, kurang memuaskan, memuaskan, sangat memuaskan
'''
# tidak memuaskan
tdk_puas = []
temp = 0
i = 0
while (i < len(dfcp.servis)):
    x = dfcp.servis[i]
    if (x > 30):
        tdk_puas.append(0)
    elif (x <= 10):
        tdk_puas.append(1)
    else:
        temp = (30 - x)/(30-10)
        tdk_puas.append(temp)
    i+=1
# print("nilai tidak memuaskan= ",tdk_puas)
# print("\n\n")

# kurang memuaskan
krg_puas = []
i = 0
while (i < len(dfcp.servis)):
    x = dfcp.servis[i]
    if (x <= 10) or (x > 70):
        krg_puas.append(0)
    elif (30 < x <= 50):
        krg_puas.append(1)
    elif (50 < x <= 70):
        temp = (70 - x)/(70-50)
        krg_puas.append(temp)
    else:
        temp = (x-10)/(30-10)
        krg_puas.append(temp)
    i+=1
# print("nilai kurang memuaskan= ",krg_puas)
# print("\n\n")

# memuaskan
puas = []
i = 0
while (i < len(dfcp.servis)):
    x = dfcp.servis[i]
    if (x <= 50) or (x > 90):
        puas.append(0)
    elif (70 < x <= 80):
        puas.append(1)
    elif (80 < x <= 90):
        temp = (90 - x)/(90-80)
        puas.append(temp)
    else:
        temp = (x-50)/(70-50)
        puas.append(temp)
    i+=1
# print("nilai memuaskan= ",puas)
# print("\n\n")

# sangat memuaskan
sgt_puas = []
i = 0
while (i < len(dfcp.servis)):
    x = dfcp.servis[i]
    if (x <= 80):
        sgt_puas.append(0)
    elif (x > 90):
        sgt_puas.append(1)
    else:
        temp = (x-80)/(90-80)
        sgt_puas.append(temp)
    i+=1
# print("nilai sangat memuaskan= ",sgt_puas)
# print("\n\n")

'''
=== HARGA ===
jumlah linguistic: 3
nama linguistic: murah, sedang, mahal
'''
# murah
murah = []
i = 0
while (i < len(dfcp.harga)):
    x = dfcp.harga[i]
    if (x >= 5):
        murah.append(0)
    elif (x < 3):
        murah.append(1)
    else:
        temp = (5 - x)/(5 - 3)
        murah.append(temp)
    i+=1
# print("nilai murah= ",murah)
# print("\n\n")

# sedang
sedang = []
i = 0
while (i < len(dfcp.harga)):
    x = dfcp.harga[i]
    if ((x <= 3) or (x >= 9)):
        sedang.append(0)
    elif (5 <= x <= 7):
        sedang.append(1)
    elif (x == 8):
        temp = (9 - x)/(9 - 7)
        sedang.append(temp)
    else:
        temp = (x - 3)/(5 - 3)
        sedang.append(temp)
    i+=1
# print("nilai sedang= ",sedang)
# print("\n\n")

# mahal
mahal = []
i = 0
while (i < len(dfcp.harga)):
    x = dfcp.harga[i]
    if (x < 7):
        mahal.append(0)
    elif (x >= 9):
        mahal.append(1)
    else:
        temp = (x - 7)/(9 - 7)
        mahal.append(temp)
    i+=1
# print("nilai mahal= ",mahal)
# print("\n\n")

'''
==== INFERENCE ====
tabel aturan inference:
 ___________________________________________________________________________
|           |  Tidak        |  Kurang       |  Memuaskan    |  Sangat       |
|           |  Memuaskan    |  Memuaskan    |               |  Memuaskan    |
|-----------|---------------|---------------|---------------|---------------|
|  Murah    |  Considered   |  Considered   |  Recommended  |  Recommended  |
| ----------|---------------|---------------|---------------|---------------|
|  Sedang   |      Not      |      Not      |  Considered   |  Recommended  |
|           |  Recommended  |  Recommended  |               |               |
|-----------|---------------|---------------|---------------|---------------|
|  Mahal    |      Not      |      Not      |  Considered   |  Considered   |
|           |  Recommended  |  Recommended  |               |               |
 ````````````````````````````````````````````````````````````````````````````

Jumlah Linguistic Output (peringkat): 3
nama linguistic output (peringkat): recommended, considered, not recommended
'''

def recommended(puas, sgtPuas, Murah, Sedang):
    '''
    Pada fungsi untuk mencari koefisien recommended, parameter yang digunakan hanya memuaskan, sangat memuaskan, murah, dan sedang, karena berdasarkan tabel inference, pada linguistic tidak memuaskan, kurang memuaskan, dan mahal sudah pasti tidak akan recommended (nilai koef = 0)
    '''
# mencari nilai minimum untuk inference (linguistic recommended)
    if (sgtPuas > Murah):
        a = Murah
    else:
        a = sgtPuas

    if (sgtPuas > Sedang):
        b = Sedang
    else:
        b = sgtPuas

    if (puas > Murah):
        c = Murah
    else:
        c = puas

    if (puas > Sedang):
        d = Sedang
    else:
        d = puas

#mencari nilai maximum untuk linguistic "Recommended"
    if (a >= b):
        temp = a
    else:
        temp = b

    if (temp <= c):
        temp = c
    
    if (temp <= d):
        temp = d

    return temp


def notRecommended(tdkPuas, krgPuas, Sedang, Mahal):
    '''
    pada fungsi ini, parameter yang digunakan juga tidak mencakup semua linguistic yang ada karena alasan yang sama dengan fungsi recommended.
    '''

# mencari nilai minimum untuk inference (linguistic not recommended)
    if (tdkPuas > Sedang):
        a = Sedang
    else:
        a = tdkPuas

    if (tdkPuas > Mahal):
        b = Mahal
    else:
        b = tdkPuas

    if (krgPuas > Sedang):
        c = Sedang
    else:
        c = krgPuas

    if (krgPuas > Mahal):
        d = Mahal
    else:
        d = krgPuas

#mencari nilai maximum untuk linguistic "Not Recommended"
    if (a >= b):
        temp = a
    else:
        temp = b

    if (temp <= c):
        temp = c
    
    if (temp <= d):
        temp = d

    return temp

def considered(tdkPuas, krgPuas, puas, sgtPuas, Murah, Sedang, Mahal):
    '''
    pada fungsi ini semua linguistic input menjadi parameter fungsi, karena linguistic "considered" bisa dihasilkan oleh semua linguistic input
    '''

# mencari nilai minimum untuk inference (linguistic considered)
    # tidak memuaskan
    a = min(tdkPuas, Murah)
    b = min(tdkPuas, Sedang)
    c = min(tdkPuas, Mahal)

    # kurang memuaskan
    d = min(krgPuas, Murah)
    e = min(krgPuas, Sedang)
    f = min(krgPuas, Mahal)

    # memuaskan
    g = min(puas, Murah)
    h = min(puas, Sedang)
    j = min(puas, Mahal)

    # sangat memuaskan
    k = min(sgtPuas, Murah)
    l = min(sgtPuas, Sedang)
    m = min(sgtPuas, Mahal)

# mencari nilai maximum untuk linguistic "Considered"
    temp = [a,b,c,d,e,f,g,h,j,k,l,m]

    return max(temp)

recom = []
Not_recom = []
consd = []

# Menghitung nilai Recommended, Considered, dan Not Recommended dari masing-masing bengkel dan memasukkan hasilnya ke dalam list yang telah dibuat
i = 0
while (i < len(df)):
    recom.append(recommended(puas[i], sgt_puas[i], murah[i], sedang[i]))
    Not_recom.append(notRecommended(tdk_puas[i],krg_puas[i],sedang[i],mahal[i]))
    consd.append(considered(tdk_puas[i], krg_puas[i], puas[i], sgt_puas[i], murah[i], sedang[i], mahal[i]))
    i+=1


'''
==== DEFUZZIFICATION ====
Metode yang digunakan adalah Takagi-Sugeno Style.
nilai crisp yang akan digunakan adalah:
- Recommended = 100
- Considered = 70
- Not Recommended = 40

Nilai crisp hasil defuzzification akan ditampung dalam list rating
'''

def deffuzification(recom, consd, notRecom):
    r = ((40 * notRecom + 70 * consd + 100 * recom) / (notRecom + consd + recom))
    return r

rating = []
i = 0
while (i < len(df)):
    rating.append(deffuzification(recom[i], consd[i], Not_recom[i]))
    i+=1

# print(rating)


'''
==== RATING TOP 10 BENGKEL ====
'''

dictTop = {id[i]: rating[i] for i in range(len(id))}
# dictTop = sorted(dictTop.items(), key=lambda x: x[1], reverse=True)

# print(dictTop)
n = 10 #batas banyaknya data yang akan diambil
top10 = dict(sorted(dictTop.items(), key = itemgetter(1), reverse=True)[:n]) #sorting dictionary dictTop secara descending, kemudian memasukkan 10 data dengan rating terbaik ke dalam dictionary top10.

# print("\n\n\n")
# print(top10)


'''
==== EXPORTING DATA TO XLSX FILE ====
menggunakan library pandas
'''
keys = top10.keys()
values = top10.values()

# df2 = pd.DataFrame(data=top10, index=[0])
df2 = pd.DataFrame({"id": keys, "Rating": values})
# df2 = (df2.T)
# print(df2)
df2.to_excel('Peringkat.xlsx')









'''
==== REFERENCES ====
https://www.geeksforgeeks.org/python-n-largest-values-in-dictionary/
https://stackoverflow.com/questions/54031133/python-dictionary-to-columns-in-xlsx
https://www.geeksforgeeks.org/python-get-first-n-keyvalue-pairs-in-given-dictionary/
https://stackoverflow.com/questions/28555112/export-a-simple-dictionary-into-excel-file-in-python
https://www.codegrepper.com/code-examples/python/save+a+list+of+dictionary+python+to+excel
https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/
https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
https://www.codegrepper.com/code-examples/python/how+to+read+excel+file+in+python
https://www.w3schools.com/python/python_dictionaries.asp
https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
'''