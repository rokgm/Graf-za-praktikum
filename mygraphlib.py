# made by Rok Grgic Mesko

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from scipy.odr import ODR, Data, Model, RealData


class MyGraph:
    '''
    Basic data plotting and fitting.

    Figure, array(axes) = matplotlib.pyplot.subplots(*args, **kwargs)
    must be created before plotting.
    '''

    def __init__(self, ax, x, y, xlabel=None, ylabel=None, title=None, xerr=None, yerr=None, x_low=None, x_high=None, y_low=None, y_high=None, grid=True, legend=True):
        '''
        Constructor of data object for analysis.

        Args:
            ax : pyplot.subplots.axes.Axes
            x : list
            y : list
            
        Optional args:
            x-axis label, y-axis label : str
                (Axis label in $...$ for latex.)
                (Use raw string to treat everything as character.)
            x-axis and y-axis errors : int, float or list
            x-axis and y-axis bounds : int, float
            grid : bool
            legend : bool
        '''
        self.ax = ax
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xerr = xerr
        self.yerr = yerr
        self.x_low = x_low
        self.x_high = x_high
        self.y_low = y_low
        self.y_high = y_high
        self.grid = grid
        self.legend = legend

        if type(self.grid) != type(True) or type(self.grid) != type(False):
            raise ValueError('grid must be True or False, {} was  given'.format(self.grid))

        if type(self.legend) != type(True) or type(self.legend) != type(False):
            raise ValueError('grid must be True or False, {} was  given'.format(self.legend))

        if self.xlabel != None:
            self.ax.set_xlabel('{}'.format(self.xlabel))

        if self.ylabel != None:
            self.ax.set_ylabel('{}'.format(self.ylabel))

        if self.title != None:
            self.ax.title.set_text(self.title)

        if self.grid:    
            self.ax.grid(True, ls = '--')
    

    def __repr__(self):
        return 'Graf(ax={0.ax}, x_axis_data, y_axis_data, xlabel={0.xlabel}, ylabel={0.ylabel},\
            xerr_list, yerr_list, x_low={0.x_low}, x_high={0.x_high}, y_low={0.y_low}, y_high={0.y_high})'.format(self)


    def set_bounds(self):
        if self.x_low == None:
            self.x_low = min(self.x) - (max(self.x) - min(self.x)) / 20
        if self.x_high == None:
            self.x_high = max(self.x) + (max(self.x) - min(self.x)) / 20

        if self.y_low == None:
            self.y_low = min(self.y) - (max(self.y) - min(self.y)) / 20
        if self.y_high == None:
            self.y_high = max(self.y) + (max(self.y) - min(self.y)) / 20

        return self.x_low, self.x_high, self.y_low, self.y_high


    def graph_data(self, graph_label='podatki'):
        '''
        Plot data object on graph.

        Optional args:
            graph_label : str
                Graph label for legend. Default 'podatki'.
                (Label in $...$ for latex.)
                (Use raw string to treat everything as character.)
        '''
        if self.xerr !=None and self.yerr !=None:
            self.ax.errorbar(self.x, self.y, xerr=self.xerr, yerr=self.yerr,
                fmt='k.', ms=5, mfc='k', ecolor='k', elinewidth=0.5, capsize=4, label='podatki')
        elif self.yerr != None:
            self.ax.errorbar(self.x, self.y, yerr=self.yerr,
                fmt='k.', ms=5, mfc='k', ecolor='k', elinewidth=0.5, capsize=4, label='podatki')
        elif self.xerr != None:
            self.ax.errorbar(self.x, self.y, xerr=self.xerr,
                fmt='k.', ms=5, mfc='k', ecolor='k', elinewidth=0.5, capsize=4, label='podatki')
        else:
            self.ax.plot(self.x, self.y, 'kx', markersize=4, label='{}'.format(graph_label))
        
        self.ax.set_xlim(MyGraph.set_bounds(self)[0], MyGraph.set_bounds(self)[1])
        self.ax.set_ylim(MyGraph.set_bounds(self)[2], MyGraph.set_bounds(self)[3])    
        if self.legend:
            self.ax.legend()   


    def graph_fit(self, func, initial_para, fit_name='fit'):
        '''
        Fit parameters to data object and plot fitted graph.

        Returns scipy.odr.Output.
            output.beta -> fitted parameter values
            Check documentation for other values.

        Args:
            func    
                function for fitting
            initial_para : list
                initial function parameters

        Optional args:
            fit_name : str
                Fit label for legend. Default 'fit'.
                (Label in $...$ for latex.)
                (Use raw string to treat everything as character.)
        '''
        if self.xerr != None and self.yerr != None:
            data = RealData(self.x, self.y, sx=self.xerr, sy=self.yerr)
        elif self.yerr != None:
            data = RealData(self.x, self.y, sy=self.yerr)
        elif self.xerr != None:
            data = RealData(self.x, self.y, sx=self.xerr)
        else:
            data = RealData(self.x, self.y)

        model = Model(func)
        odr = ODR(data, model, initial_para)                    
        odr.set_job(fit_type=2)
        output = odr.run()
        print('#{}{}'.format(fit_name, (84 - len(fit_name)) * '#'))
        output.pprint()
        print('{}'.format(85 * '#')) 
        x_fit = np.linspace(MyGraph.set_bounds(self)[0], MyGraph.set_bounds(self)[1], 600)
        y_fit = func(output.beta, x_fit)                                     
        self.ax.plot(x_fit, y_fit, 'r', label='{}'.format(fit_name))
        if self.legend:
            self.ax.legend()

        return output


    def graph_model(self, func, model_para, model_name='model'):
        '''
        Plot model on same axes as data graph.

        Args:
            func : function or lambda function
                model function
            model_para : list
                function parameters

        Optional args:
            model_name : str
                Model label for legend. Default 'model'.
                (Label in $...$ for latex.)
                (Use raw string to treat everything as character.)
        '''
        x_model = np.linspace(MyGraph.set_bounds(self)[0], MyGraph.set_bounds(self)[1], 600)
        y_model = func(model_para, x_model)
        self.ax.plot(x_model, y_model, 'g', label='{}'.format(model_name))
        if self.legend:
            self.ax.legend()


    def add_text_box(self, lines, x=0.68, y=0.5, fontsize=9):
        '''
        Adds text box to subplot.

        Args:
            lines : list
                List of strings, each for line in text box.
                (Strings in $...$ for latex.)
                (Use raw string to treat everything as character.)

        Optional args:
            x, y : float
                x, y box coordinate on axes
            fontsize : int
                box fontsize
        '''
        textstr = '\n'.join([line for line in lines])
        props = dict(boxstyle='square', facecolor='white', alpha=1)
        self.ax.text(x, y, textstr, transform=self.ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props)


    @staticmethod
    def use_fancy_latex():
        '''
        Use LaTeX instead of Matplotlib MathText.
        (distinguish \\varepsilon, \\epsilon...)

        Takes longer to process.
        Requires installed Tex distribution.
        '''
        rc('font', size = 12, family = 'DejaVu Sans', serif = ['Computer Modern'])    
        rc('text', usetex = True)
        rc('xtick', labelsize = 'small')
        rc('ytick', labelsize = 'small')
        rc('legend', frameon = True, fontsize = 'medium')


    @staticmethod
    def save_figure(name):
        '''
        Save figure (layout) to pdf and png.

        Args:
            name : str

        Saves name.pdf, name.png.
        '''
        plt.savefig('{}.png'.format(name), dpi=600, bbox_inches='tight')
        plt.savefig('{}.pdf'.format(name), dpi=600, bbox_inches='tight')
