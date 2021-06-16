# import libraries
import numpy as np
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, ColumnDataSource

def bkplot(x=None, y=None, title='', xlabel='', ylabel=''):
    """Returns preconfigured Bokeh figure"""
    
    # list of available tools
    plot_tools = 'pan, box_zoom, ywheel_zoom, box_select, lasso_select, tap,'
    plot_actions = 'undo, redo, reset, save, xzoom_in, xzoom_out,'
    plot_inspectors = 'crosshair, hover, '
    
    plot_options = dict(plot_width=800, plot_height=500, toolbar_location='above', 
                        tools=plot_tools+plot_actions+plot_inspectors)
    
    # instantiate bokeh figure
    fig = figure(title=title, x_axis_label=xlabel, y_axis_label=ylabel, **plot_options)
    
    # remove logo
    fig.toolbar.logo = None
    
    # add a line renderer
    fig.line(x, y, line_width=2)
    
    return fig