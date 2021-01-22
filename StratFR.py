
import random, sys, Queue

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qwt5 as Qwt


import numpy as np

class GUI(QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
    
        self.switch = QSlider()
        self.create_main_frame()
   
        self.Rw = 5.5
        self.Cw = 100 
        self.Lw = 3
        self.Ct = 47 
      
    def create_plot(self):
        plot = Qwt.QwtPlot(self)
        plot.setCanvasBackground(Qt.black)
        plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Log Frequency (Hz)')
        plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 10, 0.5)
        plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'Magnitude (dB)')
        plot.setAxisScale(Qwt.QwtPlot.yLeft, -40, 40, 5)
        plot.setMinimumSize(900, 300)
        plot.replot()
        
        curve = Qwt.QwtPlotCurve('')
        curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        pen = QPen(QColor('limegreen'))
        pen.setWidth(2)
        curve.setPen(pen)
        curve.attach(plot)
        return plot, curve

    def create_knob(self):
        knob = Qwt.QwtKnob(self)
        knob.setRange(0, 10, 0, 1)
        knob.setScaleMaxMajor(10)
        knob.setKnobWidth(50)
        knob.setValue(10)
        return knob

    def on_knob_change(self):
        self.w = self.tone_knob1.value()
        self.p = 2 * self.tone_knob2.value()
        self.update_monitor()
        return 0
    
    def create_switch(self):
        self.switch = QSlider(Qt.Vertical)
        self.switch.setMinimum(1)
        self.switch.setMaximum(5)
        self.switch.setValue(3)
        self.switch.setTickPosition(QSlider.TicksBelow)
        self.switch.setTickInterval(5)
        return self.switch

    def on_switch_change(self):
        self.update_circuit_pixmap()
        self.update_monitor()
        return 0

    def create_ctrl_groupbox(self):
         # ========================= Guitar Layout : Control Layout =========================== #
        # QHBoxLayout(), QVBoxLayout()
        self.ctrl_layout = QHBoxLayout() # consists of 1 Label, 2 tone knob layout, 1 slider layout
        #ctrl_layout.addWidget(QLabel('Tone Controls'))

        self.tone1_layout = QVBoxLayout() # consists of 1 label, 1 knob
        self.tone1_layout.addWidget(QLabel('Tone Knob 1'))
        self.tone_knob1 = self.create_knob()

        self.connect(self.tone_knob1, SIGNAL('valueChanged(double)'), self.on_knob_change)
        self.tone1_layout.addWidget(self.tone_knob1)

        self.tone2_layout = QVBoxLayout() # consists of 1 label, 1 knob
        self.tone2_layout.addWidget(QLabel('Tone Knob 2'))
        self.tone_knob2 = self.create_knob()

        self.connect(self.tone_knob2, SIGNAL('valueChanged(double)'), self.on_knob_change)
        self.tone2_layout.addWidget(self.tone_knob2)

        self.vol_layout = QVBoxLayout() # consists of 1 label, 1 knob
        self.vol_layout.addWidget(QLabel('Volume'))
        self.vol_knob = self.create_knob()

        self.connect(self.vol_knob, SIGNAL('valueChanged(double)'), self.on_knob_change)
        self.vol_layout.addWidget(self.vol_knob)

        self.switch_layout = QVBoxLayout() # consists of 1 label, 1 switch
        self.switch_layout.addWidget(QLabel('5-Way Switch'))
        self.switch = self.create_switch()

        self.connect(self.switch, SIGNAL('valueChanged(int)'), self.on_switch_change)
        self.switch_layout.addWidget(self.switch)

        self.ctrl_layout.addLayout(self.tone1_layout)
        self.ctrl_layout.addLayout(self.tone2_layout)
        self.ctrl_layout.addLayout(self.vol_layout)
        self.ctrl_layout.addLayout(self.switch_layout)
        self.ctrl_groupbox = QGroupBox()
        self.ctrl_groupbox.setLayout(self.ctrl_layout)
        return 0

    def create_circuit_groupbox(self):
        self.circuit_layout = QVBoxLayout()
        self.circuit_pixmap = self.create_circuit_pixmap()
        self.circuit_pixmap = self.circuit_pixmap.scaledToHeight(320)  
        self.circuit_label = QLabel()
        self.circuit_label.setPixmap(self.circuit_pixmap)
        self.circuit_layout.addWidget(self.circuit_label)
        self.circuit_groupbox = QGroupBox('Equivalent Circuit')
        self.circuit_groupbox.setLayout(self.circuit_layout)
        return 0

    def create_circuit_pixmap(self):
        fileName = ''
        if self.switch.value() == 1:
            fileName = './circuits/B.png'
        elif self.switch.value() == 2:
            fileName = './circuits/BM.png'
        elif self.switch.value() == 3:
            fileName = './circuits/M.png'
        elif self.switch.value() == 4:
            fileName = './circuits/MN.png'
        elif self.switch.value() == 5:
            fileName = './circuits/N.png'
        self.circuit_pixmap = QPixmap(fileName)
        self.circuit_pixmap = self.circuit_pixmap.scaledToHeight(320)  
        return self.circuit_pixmap

    def create_guitar_groupbox(self):
        self.guitar_layout = QHBoxLayout()
        self.guitar_layout.addWidget(self.ctrl_groupbox)
        self.guitar_layout.addWidget(self.circuit_groupbox)
        self.guitar_groupbox = QGroupBox('Volume, Tone Controls')
        self.guitar_groupbox.setLayout(self.guitar_layout)
        return 0

    def create_graph_groupbox(self):
        self.graph_layout = QVBoxLayout()
        self.plot, self.curve = self.create_plot()
        self.graph_layout.addWidget(self.plot)
        self.graph_groupbox = QGroupBox()
        self.graph_groupbox.setLayout(self.graph_layout)
        return 0

    def create_var_groupbox(self):
    
        self.var_form = QFormLayout()
        e1 = QLineEdit()

        self.var_form.addWidget(QLabel('Variables'))

        e1 = QLineEdit()
        e1.setText("5.5")
        e1.textChanged.connect(self.on_Rw_text)
        e1.setMaxLength(8)
        e1.setAlignment(Qt.AlignRight)
        e1.setFont(QFont("Arial",12))
        e1.setFixedWidth(50)

        self.var_form.addRow("Rw (kOhms)", e1)

        e2 = QLineEdit()
        e2.setText("3")
        e2.textChanged.connect(self.on_Lw_text)
        e2.setMaxLength(8)
        e2.setAlignment(Qt.AlignRight)
        e2.setFont(QFont("Arial",12))
        e2.setFixedWidth(50)

        self.var_form.addRow("Lw (H)", e2)
        
        e3 = QLineEdit()
        e3.setText("100")
        e3.textChanged.connect(self.on_Cw_text)
        e3.setMaxLength(8)
        e3.setAlignment(Qt.AlignRight)
        e3.setFont(QFont("Arial",12))
        e3.setFixedWidth(50)

        self.var_form.addRow("Cw (pF)", e3)
        
        e4 = QLineEdit()
        e4.setText("47")
        e4.textChanged.connect(self.on_Ct_text)
        e4.setMaxLength(8)
        e4.setAlignment(Qt.AlignRight)
        e4.setFont(QFont("Arial",12))
        e4.setFixedWidth(50)

        self.var_form.addRow("Ct (nF)", e4)
        self.var_groupbox = QGroupBox('Variables')
        self.var_groupbox.setLayout(self.var_form)
        return 0

    def on_Rw_text(self, text):
        self.Rw = float(text)
        self.update_monitor()
        return 0

    def on_Cw_text(self, text):
        self.Cw = float(text)
        self.update_monitor()
        return 0
    def on_Lw_text(self, text):
        self.Lw = float(text)
        self.update_monitor()
        return 0
    def on_Ct_text(self, text):
        self.Ct = float(text)
        self.update_monitor()
        return 0
    
    def create_plot_groupbox(self):
        self.plot_layout = QHBoxLayout()
        self.plot_layout.addWidget(self.graph_groupbox)
        self.plot_layout.addWidget(self.var_groupbox)

        self.plot_groupbox = QGroupBox('Log-Log Frequency Response Plot: Magnitude (dB) vs. Frequency (Hz)')
        self.plot_groupbox.setLayout(self.plot_layout)
        return 0

    def update_main_frame(self):
        self.main_frame = QWidget()
        self.main_layout = QVBoxLayout() # main_layout -> (PlotLayout -> (graph_layout, var_layout), GuitarLayout -> (ctrl_layout, circuitLayout))

        self.main_layout.addWidget(self.plot_groupbox)
        self.main_layout.addWidget(self.guitar_groupbox)

        #self.main_layout.addStretch(1)
        self.main_frame.setLayout(self.main_layout)
        self.setCentralWidget(self.main_frame)
        return 0

    def create_main_frame(self):
        
        self.create_ctrl_groupbox()
        self.create_circuit_groupbox()
        self.create_guitar_groupbox() # <- ctrl_groupbox(), circuit_groupbox()
        self.create_graph_groupbox()
        self.create_var_groupbox()
        self.create_plot_groupbox() # <- var_groupbox(), graph_groupbox()
        self.main_frame = QWidget()
        self.main_layout = QVBoxLayout() # main_layout -> (PlotLayout -> (graph_layout, var_layout), GuitarLayout -> (ctrl_layout, circuitLayout))
        self.main_layout.addWidget(self.plot_groupbox)
        self.main_layout.addWidget(self.guitar_groupbox)
        #self.main_layout.addStretch(1)
        self.main_frame.setLayout(self.main_layout)
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        self.setCentralWidget(self.main_frame)
        return 0

    def update_circuit_pixmap(self):
        # update circuit_groupbox, keep ctrl_groupbox the same 
        # update guitar_groupbox
        self.create_circuit_groupbox()
        self.create_guitar_groupbox()
        self.update_main_frame()
        return 0

    def update_monitor(self):
        exp_f = np.arange(0, 10, 0.001)
        Hf_dB = self.transferFunction(exp_f)
        self.curve.setData(exp_f, Hf_dB)
        self.plot.replot()
        return 0
        
    def transferFunction(self, exp_fs): # x = w, y = f(w), w is an array
        val = int(self.switch.value())
        output = []

        Lw = self.Lw
        Rw = self.Rw * 1000
        Cw = self.Cw * 10**(-12)
        Ct = self.Ct * 10**(-9)
        Rt = 250*1000
        a_t = self.tone_knob1.value() / 10
        a_v = self.vol_knob.value()/10 if self.vol_knob.value()/10 > 0 else 10**(-12)

        if val == 1:
            for exp_f in exp_fs:
                a = Lw*Cw 
                b = Rw*Cw 
                f = np.power(10, exp_f)
                Hw = 20*np.log10(a_v / np.sqrt((1-a*(2*np.pi*f)**2)**2 + (b*(2*np.pi*f))**2))
                output.append(Hw)
            
        elif val == 2:
            for exp_f in exp_fs:
                a = a_t*Rt*Ct
                b = 2*a_t*Rt*Ct*Lw*Cw                   # a_t*Rt*Ct*Lw*Cw
                c = 2*a_t*Rt*Rw*Ct*Cw + 2*Lw*Cw + Lw*Ct # a_t*Rt*Rw*Ct*Cw
                d = 2*a_t*Rt*Ct + Rw*Ct + 2*Rw*Cw       # Rw*Cw+Rw*Ct+a_t*Rt*Ct
                f = np.power(10, exp_f)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))
                output.append(Hw)

        elif val == 3:
            for exp_f in exp_fs:
                a = a_t*Rt*Ct
                b = a_t*Rt*Ct*Cw*Lw
                c = a_t*Rt*Rw*Ct*Cw
                d = Rw*Cw+Rw*Ct+a_t*Rt*Ct
                f = np.power(10, exp_f)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))

                output.append(Hw)
        elif val == 4:
             for exp_f in exp_fs:
                a_t = (a_t*(self.tone_knob2.value() / 10)) / (a_t + (self.tone_knob2.value() / 10))
                a = a_t*Rt*Ct
                b = 2*a_t*Rt*Ct*Lw*Cw                   # a_t*Rt*Ct*Lw*Cw
                c = 2*a_t*Rt*Rw*Ct*Cw + 2*Lw*Cw + Lw*Ct # a_t*Rt*Rw*Ct*Cw
                d = 2*a_t*Rt*Ct + Rw*Ct + 2*Rw*Cw       # Rw*Cw+Rw*Ct+a_t*Rt*Ct
                f = np.power(10, exp_f)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))

                output.append(Hw)
        elif val == 5:
            for exp_f in exp_fs:
                a_t = self.tone_knob2.value() / 10
                a = a_t*Rt*Ct
                b = a_t*Rt*Ct*Cw*Lw
                c = a_t*Rt*Rw*Ct*Cw
                d = Rw*Cw+Rw*Ct+a_t*Rt*Ct
                f = np.power(10, exp_f)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))

                output.append(Hw)
        else:
            pass
        return output
    
def main():
    app = QApplication(sys.argv)
    form = GUI()
    form.update_monitor()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
    

