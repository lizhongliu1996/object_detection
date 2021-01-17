from object_detection import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["start_string"] = df["start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["end_string"] = df["end"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(plot_width=500,plot_height=100, x_axis_type = "datetime", sizing_mode='scale_width', title="motion graph")
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1


hover = HoverTool(tooltips=[("start:"," @start_string"),("end:"," @end_string")])
p.add_tools(hover)

q= p.quad(left = "start", right="end",bottom =0,top =1, color = "Green", source = cds)

output_file("graph.html")
show(p)
