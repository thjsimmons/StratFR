"""
Frequency Response Plot for Fender Stratocaster Electronics 
with PyQt GUI Tone Controls and Pickup Settings

"""


import sys
import numpy as np

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qwt5 as Qwt

class GUI(QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        
        self.create_main_frame()
   
        # Default Circuit Component Values
        self.Rw = 5.5
        self.Cw = 100 
        self.Lw = 3
        self.Ct = 47 
      
    def create_plot(self):
        plot = Qwt.QwtPlot(self)
        plot.setCanvasBackground(Qt.black)
        plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Log Frequency (Hz)')
        plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 10, 0.5)          # X-axis range, ticks
        plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'Magnitude (dB)')
        plot.setAxisScale(Qwt.QwtPlot.yLeft, -40, 40, 5)            # Y-axis range, ticks
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
        self.update_plot()
    
    def create_switch(self):
        self.switch = QSlider(Qt.Horizontal)
        self.switch.setMinimum(1)
        self.switch.setMaximum(5)
        self.switch.setValue(3)
        self.switch.setTickPosition(QSlider.TicksBelow)
        self.switch.setTickInterval(5)

    def on_switch_change(self):
        self.update_circuit_pixmap()
        self.update_plot()

    def create_ctrl_groupbox(self):
        # Create tone knobs and slider widgets, place in layout:
        self.ctrl_layout = QVBoxLayout() 
        self.knob_layout = QHBoxLayout()
        self.tone1_layout = QVBoxLayout()

        self.tone1_layout.addWidget(QLabel('Middle Tone'))
        self.tone_knob1 = self.create_knob()
        self.connect(self.tone_knob1, SIGNAL('valueChanged(double)'), self.on_knob_change)
        self.tone1_layout.addWidget(self.tone_knob1)
        self.tone1_layout.addStretch(1)
     
        self.tone2_layout = QVBoxLayout() # consists of 1 label, 1 knob
        self.tone2_layout.addWidget(QLabel('Neck Tone'))
        self.tone_knob2 = self.create_knob()
        self.connect(self.tone_knob2, SIGNAL('valueChanged(double)'), self.on_knob_change)
        self.tone2_layout.addWidget(self.tone_knob2)
        self.tone2_layout.addStretch(1)

        self.vol_layout = QVBoxLayout() # consists of 1 label, 1 knob
        self.vol_layout.addWidget(QLabel('Volume'))
        self.vol_knob = self.create_knob()
        self.connect(self.vol_knob, SIGNAL('valueChanged(double)'), self.on_knob_change)
        self.vol_layout.addWidget(self.vol_knob)
        self.vol_layout.addStretch(1)

        self.switch_layout = QVBoxLayout() # consists of 1 label, 1 switch
        self.switch_layout.addWidget(QLabel('5-Way Switch'))
        self.create_switch()
        self.connect(self.switch, SIGNAL('valueChanged(int)'), self.on_switch_change)
        self.switch_layout.addWidget(self.switch)
        
        self.knob_layout.addLayout(self.tone1_layout)
        self.knob_layout.addLayout(self.tone2_layout)
        self.knob_layout.addLayout(self.vol_layout)
        self.ctrl_layout.addLayout(self.knob_layout)
        self.ctrl_layout.addLayout(self.switch_layout)
        self.ctrl_layout.addStretch(1)
        self.ctrl_groupbox = QGroupBox("Tone Controls")
        self.ctrl_groupbox.setLayout(self.ctrl_layout)

    def create_circuit_groupbox(self):
        self.circuit_layout = QVBoxLayout()
        self.create_circuit_pixmap()
        self.circuit_label = QLabel()
        self.circuit_label.setPixmap(self.circuit_pixmap)
        self.circuit_layout.addWidget(self.circuit_label)
        self.circuit_groupbox = QGroupBox('Equivalent Circuit')
        self.circuit_groupbox.setLayout(self.circuit_layout)
       
    def create_circuit_pixmap(self):
        # Get circuit image from circuits folder, set fixed size
        fileName = ''
        if self.switch.value() == 1:
            fileName = './circuits/B.png'           # Bridge pickup setting equivalent circuit
        elif self.switch.value() == 2:
            fileName = './circuits/BM.png'          # Bridge+Middle pickup setting equivalent circuit
        elif self.switch.value() == 3:
            fileName = './circuits/M.png'           # Middle pickup setting equivalent circuit
        elif self.switch.value() == 4:
            fileName = './circuits/MN.png'          # Middle+Neck pickup setting equivalent circuit
        elif self.switch.value() == 5:
            fileName = './circuits/N.png'           # Neck pickup setting equivalent circuit
        self.circuit_pixmap = QPixmap(fileName)
        self.circuit_pixmap = self.circuit_pixmap.scaledToHeight(320)  

    def create_guitar_groupbox(self):
        # Creates bottom half of GUI, with tone controls and circuit image
        self.guitar_layout = QHBoxLayout()
        self.guitar_layout.addWidget(self.ctrl_groupbox)
        self.guitar_layout.addWidget(self.circuit_groupbox)
        self.guitar_groupbox = QGroupBox()
        self.guitar_groupbox.setLayout(self.guitar_layout)
        
    def create_graph_groupbox(self):
        # Place plot in a layout
        self.graph_layout = QVBoxLayout()
        self.plot, self.curve = self.create_plot()
        self.graph_layout.addWidget(self.plot)
        self.graph_groupbox = QGroupBox()
        self.graph_groupbox.setLayout(self.graph_layout)
        
    def create_var_groupbox(self):
        # Create line-edit table for changing variables:
        self.table_layout = QVBoxLayout()
        self.var_form = QFormLayout()
        self.table_layout.addStretch(1)

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

        self.table_layout.addLayout(self.var_form)
        self.table_layout.addStretch(1)
        self.var_groupbox = QGroupBox()
        self.var_groupbox.setLayout(self.table_layout)
        
    def on_Rw_text(self, text):
        # Update plot when user changes Rw
        self.Rw = float(text)
        self.update_plot()
        
    def on_Cw_text(self, text):
        # Update plot when user changes Cw
        self.Cw = float(text)
        self.update_plot()
        
    def on_Lw_text(self, text):
        # Update plot when user changes Lw
        self.Lw = float(text)
        self.update_plot()
        
    def on_Ct_text(self, text):
        # Update plot when user changes Ct
        self.Ct = float(text)
        self.update_plot()
         
    def create_plot_groupbox(self):
        # Create plot and variable line-edits:
        self.plot_layout = QHBoxLayout()
        self.plot_layout.addWidget(self.graph_groupbox)
        self.plot_layout.addWidget(self.var_groupbox)
        self.plot_groupbox = QGroupBox('Frequency Response Log-Log Plot')
        self.plot_groupbox.setLayout(self.plot_layout)

    def update_main_frame(self):
        # Redraw main frame, called when the circuit image needs to update
        self.main_frame = QWidget()
        self.main_layout = QVBoxLayout() 
        self.main_layout.addWidget(self.plot_groupbox)
        self.main_layout.addWidget(self.guitar_groupbox)
        self.main_frame.setLayout(self.main_layout)
        self.setCentralWidget(self.main_frame)

    def create_main_frame(self):
        # Create all components and widgets:
        self.create_ctrl_groupbox()    # sub-component of guitar_groupbox
        self.create_circuit_groupbox() # sub-component of guitar_groupbox
        self.create_guitar_groupbox()  # sub-component of main_layout
        self.create_graph_groupbox()   # sub-component of plot_groupbox
        self.create_var_groupbox()     # sub-component of plot_groupbox
        self.create_plot_groupbox()    # sub-component of main_layout
        
        # Place all components in GUI:
        self.main_frame = QWidget()
        self.main_layout = QVBoxLayout() 
        self.main_layout.addWidget(self.plot_groupbox)
        self.main_layout.addWidget(self.guitar_groupbox)
        self.main_frame.setLayout(self.main_layout)
        
        # Set Qt Window Size 
        self.setFixedWidth(1200)
        self.setFixedHeight(800)

        self.setCentralWidget(self.main_frame)
        
    def update_circuit_pixmap(self):
        # Updates circuit image on switch change 
        self.create_circuit_groupbox()
        self.create_guitar_groupbox()
        self.update_main_frame()
        
    def update_plot(self):
        # Updates plot on knob, slider, variable changes
        exp_f = np.arange(0, 10, 0.001)        # X values 
        Hf_dB = self.transferFunction(exp_f)   # Y values
        self.curve.setData(exp_f, Hf_dB)
        self.plot.replot()
        
    def transferFunction(self, exp_fs): 
        val = int(self.switch.value())
        output = []

        Lw = self.Lw                                                                                # pickup winding inductance
        Rw = self.Rw * 1000                                                                         # pickup winding resistance
        Cw = self.Cw * 10**(-12)                                                                    # pickup winding capacitance
        Ct = self.Ct * 10**(-9)                                                                     # tone capacitor value
        Rt = 250*1000                                                                               # tone pot resistor value
        a_t = self.tone_knob1.value() / 10 if self.tone_knob1.value()/10 > 0 else 10**(-12)         # middle tone pot percentile position
        b_t = self.tone_knob2.value() / 10 if self.tone_knob2.value()/10 > 0 else 10**(-12)         # neck tone pot percentile position
        a_v = self.vol_knob.value()/10 if self.vol_knob.value()/10 > 0 else 10**(-12)               # volume pot percentile position

        if val == 1: # Bridge Pickup Transfer Function
            for exp_f in exp_fs:
                a = Lw*Cw 
                b = Rw*Cw 
                f = np.power(10, exp_f)                                                             # frequency (Hz)
                Hw = 20*np.log10(a_v / np.sqrt((1-a*(2*np.pi*f)**2)**2 + (b*(2*np.pi*f))**2))
                output.append(Hw)
            
        elif val == 2: # Bridge+Middle Pickup Transfer Function (Symmetrical for both Pickups)
            for exp_f in exp_fs:
                a = a_t*Rt*Ct
                b = 2*a_t*Rt*Ct*Lw*Cw                  
                c = 2*a_t*Rt*Rw*Ct*Cw + 2*Lw*Cw + Lw*Ct 
                d = 2*a_t*Rt*Ct + Rw*Ct + 2*Rw*Cw     
                f = np.power(10, exp_f)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))
                output.append(Hw)

        elif val == 3: # Middle Pickup Transfer Function (Symmetrical for both Pickups)
            for exp_f in exp_fs:
                a = a_t*Rt*Ct
                b = a_t*Rt*Ct*Cw*Lw
                c = a_t*Rt*Rw*Ct*Cw
                d = Rw*Cw+Rw*Ct+a_t*Rt*Ct
                f = np.power(10, exp_f)                                                             # frequency (Hz)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))
                output.append(Hw)

        elif val == 4: # Middle+Neck Pickup Transfer Function (Symmetrical for both Pickups)
             for exp_f in exp_fs:
                ab_t = (a_t*b_t)/(a_t + b_t)
                a = ab_t*Rt*Ct
                b = 2*ab_t*Rt*Ct*Lw*Cw                   
                c = 2*ab_t*Rt*Rw*Ct*Cw + 2*Lw*Cw + Lw*Ct 
                d = 2*ab_t*Rt*Ct + Rw*Ct + 2*Rw*Cw      
                f = np.power(10, exp_f)                                                             # frequency (Hz)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))
                output.append(Hw)

        elif val == 5: # Neck Pickup Transfer Function 
            for exp_f in exp_fs:
                a = b_t*Rt*Ct
                b = b_t*Rt*Ct*Cw*Lw
                c = b_t*Rt*Rw*Ct*Cw
                d = Rw*Cw+Rw*Ct+b_t*Rt*Ct
                f = np.power(10, exp_f)                                                             # frequency (Hz)
                Hw = 20*np.log10(a_v * np.sqrt(1 + (a*(2*np.pi*f))**2) / np.sqrt((1 - c*(2*np.pi*f)**2)**2 + (d*(2*np.pi*f) - b*(2*np.pi*f)**3)**2))
                output.append(Hw)
        return output
    
def main():
    app = QApplication(sys.argv)
    form = GUI()
    form.update_plot()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
    

