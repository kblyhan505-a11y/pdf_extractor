import os #dosya yolu dosya seçimi vb
import tkinter as tk #arayüz ayarı (ui)
from tkinter import filedialog , messagebox ,scrolledtext # arayüz dosya işlemleri  hata mesajşları ve kaydırmalı metin
import fitz #pdf işlemleri için PuyMuPDF


class PDFExtractorApp:   #en genel sınıfımız (tüm arayüz ve arayüz işlemleri)
    def __init__(self, root):   #kurucu fonksiyon 
        self.root=root
        self.root.title("PDF İşlem Aracı")   #uygulama adı
        self.root.geometry("350x120")  #uygulamanın pencere ölçüsü

        self.extract_images_btn=tk.Button(root, text="PDF'ten Foto Çıkart", command=self.select_folder_for_images)
        self.extract_images_btn.pack(pady=10)
        self.extract_text_btn=tk.Button(root, text="PDF'ten Yazı Çıkart", command=self.select_pdf_for_text)
        self.extract_text_btn.pack(padx=10)

    def select_pdf_for_text(self):
        pdf_path=filedialog.askopenfilename(filetypes=[("Pdf Dosyaları","*.pdf")]) #kullanıcıdan pdf uzantılı dosya seçtiren kod
        if pdf_path:
        #buraya bir metot içersinde pdf pathi çalıştırmam lazım 
            self.extract_text(pdf_path)


    def select_folder_for_images(self): #fotoğraf çıkarmak için pdf seçme arayüzünü açan metot
        pdf_path=filedialog.askopenfilename(filetypes=[("Pdf Dosyaları","*.pdf")]) #kullanıcıdan pdf uzantılı dosya seçtiren kod
        if pdf_path:
            #buraya bir metot içersinde pdf pathi çalıştırmam lazım 
            self.select_target_folder_for_images(pdf_path)

    def select_target_folder_for_images(self, pdf_path):
        target_folder=filedialog.askdirectory(title="Hedef Klasörü Seç") #kullanıcıdan pdf uzantılı dosya seçtiren kod
        if target_folder: 
            self.extract_images(pdf_path, target_folder)            

    def extract_images(self, pdf_path, target_folder):   #fotoğrafları çıkartıp diske kaydeden metot
        try: #hata oluşabilecek kod denetimi 
            doc=fitz.open(pdf_path)  #belirtilen dosyayı fitz ile aç 
            image_count=0 #foto sayısını tutan değişken 
            for page_number in range(len(doc)):
                page=doc.load_page(page_number) #pdf de ki her sayfa için döngü sırasıyla belleğe yükler 
                images= page.get_images(full=True) #geçerli sayfa için fotoları al
                for img_index, img in enumerate(images):
                    xref=img[0]  #pdfnin içinde ki benzersiz referans numarası
                    base_image=doc.extract_image(xref) #referans numarasuyla fotonnun ham verisini çıkardık 
                    image_bytes=base_image["image"]  #resmin ikili içeriği al
                    img_filename=f"sayfa _{page_number+1}_foto_{img_index+1}.png"
                    img_path=os.path.join(target_folder, img_filename)
                    with open(img_path,"wb")as img_file:
                        img_file.write(image_bytes)  #tam veriyi yazdır
                    image_count+=1  #kaydeilen resimde fotoyu 1 arttır 
            doc.close() #pdf dosyasını kapatır serbest bırakır
            messagebox.showinfo("Başarılı",f"{image_count} Fotoğraf Başarıyla Kaydedildi")
        except Exception as e:
            messagebox.showerror("Hata", f"Hata OLuştu:{e}")
    def extract_text(self , pdf_path):
        try:   #hata yönetmi
            doc=fitz.open(pdf_path)  #belirtilen dosyayı fitz ile aç 
            pages_text=[] #her sayfanın metnini ayrı ayrı tutabilmek için liste oluştur 
            for page_number in range(len(doc)): #pdf de ki her sayfa için döngü başlat 
                page=doc.load_page(page_number)
                text= page.get_text()
                pages_text.append(text.strip())
            doc.close()
            self.show_text_window(pages_text, pdf_path)
        except Exception as e:
            messagebox.showerror("Hata", f"Hata OLuştu:{e}")
    def show_text_window(self, page_text, pdf_path):   #çıkarılan metnin arayüzde sayfa sayfa gösterilmesi
        self.current_page=0  #görüntülenen sayfa indexi sıfırla
        window=tk.Toplevel(self.root)  #ana pencerenin üstünde alt pencere açar
        window.title("Çıkarılan Metin")
        window.geometry("700x520")


        info_lbl=tk.Label(window , text=f"Toplam  {len(page_text)} sayfa " , font=("Arial", 9), fg="grey") #sayfanın toplam sayısının gösteren bilgi etiketi 
        info_lbl.pack(anchor="w",  padx=10, pady=8)

        text_area=scrolledtext.ScrolledText(window, wrap=tk.WORD,font=("Arial", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        def show_page(index):    #belirtilen sayfa indexinde ki metni gösteren iç fonk
            text_area.config(state=tk.NORMAL)  #metni alınabilir bir halde 
            text_area.delete("1.0", tk.END)   #mevcut içeriği tamamen temizle 
            content=page_text[index]
            text_area.insert(tk.END, content if content else "Bu sayfada metin bulunamadı")
            text_area.config(state=tk.DISABLED)
            page_label.config(text=f"Sayfa {index +1 }/ {len(page_text)}")
            prev_btn.config(state=tk.NORMAL if index>0 else tk.DISABLED)
            next_btn.config(state=tk.NORMAL if index< (len(page_text)-1) else tk.DISABLED)
        nav_frame=tk.Frame(window)
        nav_frame.pack(pady=4)

        prev_btn=tk.Button(nav_frame, text= "Önceki" ,width= 10,command=lambda: (setattr(self, "current_page", self.current_page-1),show_page(self.current_page)))

        prev_btn.grid(row=0 , column=0, padx=5)  


        
        next_btn=tk.Button(nav_frame, text= "Sonraki" ,width= 10,command=lambda: (setattr(self, "current_page", self.current_page+1),show_page(self.current_page)))  

        next_btn.grid(row=0 , column=2, padx=5)

        page_label=tk.Label(nav_frame, text="", font=("Arial", 9))
        page_label.grid(row=0, column=1, padx=5)

        def save_all_text(): #kaydeden iç fonk
            text_path=f"{os.path.splitext(pdf_path)[0]}.txt"  #pdf uzantısını txt ile değiştirir
            with open(text_path, "w", encoding="utf-8") as f:
                for i , text in enumerate(page_text): #her sayfanın metni için döngü başlat 
                    f.write(f"--sayfa{i+1}--\n{text}\n\n") #her sayfnın başlığı ve metnini dosyaya yazdır 
            messagebox.showinfo("Kaydedildi", f"Tüm Metin Şuraya Kaydedildi:{text_path}")


        save_btn=tk.Button(window, text="Tümünü TXT olarak kaydet", command=save_all_text)
        save_btn.pack(pady=(0,8))
        show_page(0)  #çalıştığında ilk sayfayı açar


root=tk.Tk()
app=PDFExtractorApp(root)
root.mainloop()

        






