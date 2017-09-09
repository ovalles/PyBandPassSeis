import pygtk
import gtk as Gtk
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import scipy
import pylab
import pdb

#import gdk

import read_segy
import butter


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("AJ OVALLES Seismic Processing Tools")
        self.set_border_width(20)
        self.set_default_size(800, 600)

        self.box = Gtk.HBox(False,0)
        self.add(self.box)

        self.box1 = Gtk.VBox(False,0)
        self.box.pack_start(self.box1,False,0)

        self.box2 = Gtk.HBox(False,0)
        self.box.pack_start(self.box2,False,0)

        self.table = Gtk.Table(2,2,False)
        self.box2.pack_start(self.table)



        self.labelfile = Gtk.Label("Input File: ")
        self.box1.pack_start(self.labelfile, True, True, 0)
        self.entryFileIn = Gtk.Entry()
        self.entryFileIn.set_text("PP554_t506s751.sgy")
        self.box1.pack_start(self.entryFileIn, True, True, 0)


        self.buttonUpdate = Gtk.Button(label="Update SEGY Info")
        self.buttonUpdate.connect("clicked", self.on_buttonUpdate_clicked)
        self.box1.pack_start(self.buttonUpdate, True, False, 0)

        self.tablePar = Gtk.Table(2,4,False)
        self.box1.pack_start(self.tablePar)

        self.labelFromTrc = Gtk.Label("From Trace ")        
        self.tablePar.attach(self.labelFromTrc, 0, 1, 0, 1)
        self.entryFromTrc = Gtk.Entry()
        #self.entryFromTrc.set_text("1")
        self.tablePar.attach(self.entryFromTrc, 1, 2, 0, 1)

        self.labelToTrc = Gtk.Label("To Trace ")        
        self.tablePar.attach(self.labelToTrc, 0, 1, 1, 2)
        self.entryToTrc = Gtk.Entry()
        self.tablePar.attach(self.entryToTrc, 1, 2, 1, 2)

        self.labelFromTime = Gtk.Label("From Time (ms) ")        
        self.tablePar.attach(self.labelFromTime, 0, 1, 2, 3)
        self.entryFromTime = Gtk.Entry()
        #self.entryFromTrc.set_text("1")
        self.tablePar.attach(self.entryFromTime, 1, 2, 2, 3)

        self.labelToTime = Gtk.Label("To Time (ms) ")        
        self.tablePar.attach(self.labelToTime, 0, 1, 3, 4)
        self.entryToTime = Gtk.Entry()
        self.tablePar.attach(self.entryToTime, 1, 2, 3, 4)


        self.labelPar = Gtk.Label("Bandpass Parameters  ")
        self.box1.pack_start(self.labelPar, True, True, 0) 


        self.box1_1 = Gtk.HBox(False,0)
        self.box1.pack_start(self.box1_1,False,0)

        self.box1_2 = Gtk.HBox(False,0)
        self.box1.pack_start(self.box1_2,False,0)

        self.box1_3 = Gtk.HBox(False,0)
        self.box1.pack_start(self.box1_3,False,0)

        self.box1_4 = Gtk.HBox(False,0)
        self.box1.pack_start(self.box1_4,False,0)


#        self.box2 = Gtk.HBox(False,0)
#        self.box.pack_start(self.box2,False,0)

#        self.draw1 = Gtk.DrawingArea()
#        self.box2.pack_start(self.draw1,False,0)

 #       self.tableDisp = Gtk.Table(1, 2, True)
 #       self.box2.pack_start(self.tableDisp, True, True, 0)
      

        self.label1 = Gtk.Label("Frequency 1 (Hz)  ")
        self.box1_1.pack_start(self.label1, True, True, 0)
        self.entryf1 = Gtk.Entry()
        self.entryf1.set_text("4")
        self.box1_1.pack_start(self.entryf1, True, True, 0)

        self.label2 = Gtk.Label("Frequency 2 (Hz)  ")
        self.box1_2.pack_start(self.label2, True, True, 0)
        self.entryf2 = Gtk.Entry()
        self.entryf2.set_text("12")
        self.box1_2.pack_start(self.entryf2, True, True, 0)

        self.label3 = Gtk.Label("Frequency 3 (Hz)  ")
        self.box1_3.pack_start(self.label3, True, True, 0)
        self.entryf3 = Gtk.Entry()
        self.entryf3.set_text("80")
        self.box1_3.pack_start(self.entryf3, True, True, 0)


        self.label4 = Gtk.Label("Frequency 4 (Hz)  ")
        self.box1_4.pack_start(self.label4, True, True, 0)
        self.entryf4 = Gtk.Entry()
        self.entryf4.set_text("120")
        self.box1_4.pack_start(self.entryf4, True, True, 0)

        self.labelfileo = Gtk.Label("Output File: ")
        self.box1.pack_start(self.labelfileo, True, True, 0)
        self.entryFileOut = Gtk.Entry()
        self.entryFileOut.set_text("C:/My_Documents/SeisFileOut.sgy")
        self.box1.pack_start(self.entryFileOut, True, True, 0)



        self.button1 = Gtk.Button(label="Launch Process")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.box1.pack_start(self.button1, True, False, 0)



        self.button2 = Gtk.Button(label="Goodbye")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.box1.pack_start(self.button2, True, False, 0)
#        print("PASE")
        
        self.button3 = Gtk.Button(label="Clear Display")
        self.button3.connect("clicked", self.on_button3_clicked)
        self.box1.pack_start(self.button3, True, False, 0)


    def on_button1_clicked(self, widget):

        FileIn = self.entryFileIn.get_text()
        #nt=read_segy.ntraces(FileIn)
        #ns=read_segy.nsamp_segy(FileIn)
        self.dt=int(read_segy.dt_segy(FileIn))/1000 
        print self.dt
        self.fs = 1000*float(1/(2*float(self.dt)))
        nto = int(self.entryFromTrc.get_text())
        ntf = int(self.entryToTrc.get_text())
        nso = float(self.entryFromTime.get_text())
        nsf = float(self.entryToTime.get_text())

        
#        Section=read_segy.read_segy(nt,ns,FileIn)
        Section=read_segy.read_segy_trunc(FileIn,nto-1,ntf,int(nso/self.dt),1+int(nsf/self.dt))
        Section=Section.T
        print 'Section dim :', Section.shape
        plt.imshow(Section,extent=[nto,ntf,nsf,nso],cmap='gray')
        plt.colorbar()
        plt.title('Input Section')
        plt.savefig('SeisInput.png', bbox_inches='tight')
        plt.clf()

#        if imageIn != None:
#        imageIn.remove()

        self.table.destroy()
        self.table = Gtk.Table(2,2,False)
        self.box2.pack_start(self.table)

        pix = Gtk.gdk.pixbuf_new_from_file("SeisInput.png")
        pix = pix.scale_simple(300, 400, Gtk.gdk.INTERP_BILINEAR)
        imageIn = Gtk.Image()
        imageIn.set_from_pixbuf(pix)       
#        self.box2.pack_start(imageIn, True, True, 0)
        self.table.attach(imageIn, 0, 1, 0, 1)
        imageIn.show()
#        self.table.show()
#        imageIn.destroy()
        #pdb.set_trace()
        t = scipy.linspace(0,(nsf-nso)/1000.0,int((nsf-nso)/self.dt)+1)
        #t = scipy.linspace(0,float(751-1)/1000,750)
        freqs = scipy.fftpack.fftfreq(len(Section[:,0]), t[1]-t[0])
        Sectionfft = np.apply_along_axis(scipy.fft,0,Section)
        Sectionfft = abs(Sectionfft)
        AmpSpq = np.apply_along_axis(np.sum,1,Sectionfft)
        AmpSpq = 20*scipy.log10(AmpSpq) 

        plt.plot(freqs, AmpSpq)
        plt.title('Input Section Amplitude Spectrum')
        plt.savefig('SeisInputSpq.png', bbox_inches='tight')
        plt.clf()

        pix = Gtk.gdk.pixbuf_new_from_file("SeisInputSpq.png")
        pix = pix.scale_simple(300, 150, Gtk.gdk.INTERP_BILINEAR)
        SpqimageIn = Gtk.Image()
        SpqimageIn.set_from_pixbuf(pix)       
#        self.box2.pack_start(imageIn, True, True, 0)
        self.table.attach(SpqimageIn, 0, 1, 1, 2)
        SpqimageIn.show()


        EntryF1 = float(self.entryf1.get_text())
        EntryF2 = float(self.entryf2.get_text())
        EntryF3 = float(self.entryf3.get_text())
        EntryF4 = float(self.entryf4.get_text())

        print EntryF3
        
        
        param = [EntryF2,EntryF3,500]
        OutSection = np.apply_along_axis(butter.butter_bandpass_filter,0, Section,*param)
        #pdb.set_trace()

        '''
        kparam = {"lowcut":EntryF2, "highcut":EntryF3, "fs":500} 
        OutSection = np.apply_along_axis(butter.butter_bandpass_filter,0, Section,**kparam)
        '''

        '''
        pool = mp.Pool(processes=2)
        results = [pool.apply_async(butter.butter_bandpass_filter, args=(Section[:,u],EntryF2,EntryF3,500,)) for u in range(0,len(Section[0,:]))]
        output = [p.get() for p in results]
        SectionFilt = np.array(output)
        OutSection = SectionFilt.T
        '''

        plt.imshow(OutSection,extent=[nto,ntf,nsf,nso],cmap='gray')
        plt.colorbar()
        plt.title('Output Section')
        plt.savefig('SeisOut.png', bbox_inches='tight')
        plt.clf()

        pix = Gtk.gdk.pixbuf_new_from_file("SeisOut.png")
        pix = pix.scale_simple(300, 400, Gtk.gdk.INTERP_BILINEAR)
        imageOut = Gtk.Image()
        imageOut.set_from_pixbuf(pix)
        #self.box2.pack_start(imageOut, True, True, 0)
        self.table.attach(imageOut, 1, 2, 0, 1)
        imageOut.show()



        t = scipy.linspace(0,(nsf-1)/1000,nsf)
        #freqs = scipy.fftpack.fftfreq(len(OutSection[:,0]), t[1]-t[0])
        OutSectionfft = np.apply_along_axis(scipy.fft,0,OutSection)
        OutSectionfft = abs(OutSectionfft)
        OutAmpSpq = np.apply_along_axis(np.sum,1,OutSectionfft)
        OutAmpSpq = 20*scipy.log10(OutAmpSpq) 

        plt.plot(freqs, OutAmpSpq)
        plt.title('Output Section Amplitude Spectrum')
        plt.savefig('OutSeisInputSpq.png', bbox_inches='tight')
        plt.clf()

        pix = Gtk.gdk.pixbuf_new_from_file("OutSeisInputSpq.png")
        pix = pix.scale_simple(300, 150, Gtk.gdk.INTERP_BILINEAR)
        SpqimageOut = Gtk.Image()
        SpqimageOut.set_from_pixbuf(pix)       
#        self.box2.pack_start(imageIn, True, True, 0)
        self.table.attach(SpqimageOut, 1, 2, 1, 2)
        SpqimageOut.show()


        self.table.show()
        self.box2.show()

    def on_buttonUpdate_clicked(self, widget):
        FileIn = self.entryFileIn.get_text()
        self.nt=read_segy.ntraces(FileIn)
        self.ns=read_segy.nsamp_segy(FileIn)
        self.dt=int(read_segy.dt_segy(FileIn))/1000
        self.entryFromTrc.set_text(str(1))
        self.entryToTrc.set_text(str(int(self.nt)))
        self.entryFromTime.set_text(str(0))
        self.entryToTime.set_text(str(int(self.ns-1)*self.dt))


    def on_button2_clicked(self, widget):
        print("Goodbye")

    def on_button3_clicked(self, widget):
        
        self.table.destroy()

win = MyWindow()

win.connect("delete-event", Gtk.main_quit)
win.show_all()

Gtk.main()
