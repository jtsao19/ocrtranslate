import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

def onselect(eclick, erelease):
    # Selecting region using mouse
    if eclick.ydata > erelease.ydata:
        eclick.ydata, erelease.ydata = erelease.ydata, eclick.ydata
    if eclick.xdata > erelease.xdata:
        eclick.xdata, erelease.xdata = erelease.xdata, eclick.xdata
        
    # Zoom out if too close (just click)
    # Top-Left is (0,0)
    if erelease.xdata-eclick.xdata < 10:
        eclick.xdata = ax.get_xlim()[0] - 10
        erelease.xdata = ax.get_xlim()[1] + 10
    if erelease.ydata-eclick.ydata < 10:
        eclick.ydata = ax.get_ylim()[1] - 10
        erelease.ydata = ax.get_ylim()[0] + 10
    
    ax.set_ylim(erelease.ydata, eclick.ydata)   # Bottom, Top
    ax.set_xlim(eclick.xdata, erelease.xdata)   # Left, Right
    fig.canvas.draw()

def select(img):
    # From the screenshot of monitor, display a matplotlib GUI to click and drag selection range
    # Returns coordinates of 2 bounding corners
    global fig
    global ax
    
    # creates the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt_image=plt.imshow(img)
        
    # Rectangle selector
    rs = widgets.RectangleSelector(
        ax, onselect, drawtype='box',
        rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.4, fill=True))
    
    #close window
    plt.show() 
    return rs.extents
