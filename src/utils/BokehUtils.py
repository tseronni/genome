from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter, HoverTool, ColumnDataSource, Title


class BokehUtils:
    @staticmethod
    def v_bar(title='', title_location='above', title_font='Arial', title_font_size='14pt', title_color='black', title_alpha=0.8, title_baseline='middle', title_align='center', title_offset=10,
              show_grid=True,
              x_axis_label='', x_axis_location='below', x_axis_type='auto', x_minor_ticks='auto', x_range=None, x_formatter=None,
              y_axis_label='', y_axis_location='left', y_axis_type='auto', y_minor_ticks='auto', y_range=None, y_formatter=None,
              x=None, y=None, bar_width=0.5,
              show_y_value=False, unit=None, decimals=2, x_hover_label='', y_hover_label=''):
        """
            title_location = ['above', 'below', 'left', 'right']
            x_axis_type = ['linear', 'log', 'datetime', 'mercator', 'auto']
            x_axis_location = ['below', 'above', 'auto']
            y_axis_location = ['left', 'right', 'auto']
            y_axis_type = ['linear', 'log', 'datetime', 'mercator', 'auto']
        """
        text = y
        if unit == 'thousands':
            text = [f'{str(round(valor / 1000, decimals))} Mil' for valor in y]
        if unit == 'millions':
            text = [f'{str(round(valor / 1000000, decimals))} Mi' for valor in y]
        if unit == 'billions':
            text = [f'{str(round(valor / 1000000000, decimals))} Bi' for valor in y]
        if unit == 'trillions':
            text = [f'{str(round(valor / 1000000000000, decimals))} Tri' for valor in y]

        source = ColumnDataSource(dict(x=x, y=y, text=text))

        if y_range is None:
            y_range = (0, max(y) * 1.1)

        p = figure(
            title=title,
            title_location=title_location,
            x_axis_label=x_axis_label,
            x_axis_location=x_axis_location,
            x_axis_type=x_axis_type,
            x_minor_ticks=x_minor_ticks,
            x_range=x_range,
            y_axis_label=y_axis_label,
            y_axis_location=y_axis_location,
            y_axis_type=y_axis_type,
            y_minor_ticks=y_minor_ticks,
            y_range=y_range,
            toolbar_location=None,
            tools=""
        )

        """
            text_baseline = ['top', 'middle', 'bottom']
            text_align = ['left', 'center', 'right']
        """
        p.title = Title(text=title, text_font=title_font, text_font_size=title_font_size,
                        text_color=title_color, text_alpha=title_alpha, text_baseline=title_baseline,
                        text_align=title_align, offset=title_offset)

        if not show_grid:
            p.grid.grid_line_color = None
            p.grid.band_fill_alpha = 0

        p.vbar(x='x', top='y', width=bar_width, source=source)

        """
        text_align = ['left', 'center', 'right']
        text_baseline = ['top', 'middle', 'bottom']
        """
        if show_y_value:
            p.text(source=source, x='x', y='y', text='text', text_font_size='8pt', text_color='blue', text_align='center', text_baseline='bottom')

        p.xaxis.formatter = x_formatter
        p.yaxis.formatter = y_formatter

        p.add_tools(HoverTool(tooltips=[(x_hover_label, "@x"), (y_hover_label, "@text")]))

        return p

    @staticmethod
    def v_stacked_bar(title='', title_location='above', title_font='Arial', title_font_size='14pt', title_color='black', title_alpha=0.8, title_baseline='middle', title_align='center', title_offset=10,
                      show_grid=True,
                      x_axis_label='', x_axis_location='below', x_axis_type='auto', x_minor_ticks='auto', x_range=None, x_formatter=None,
                      y_axis_label='', y_axis_location='left', y_axis_type='auto', y_minor_ticks='auto', y_range=None, y_formatter=None,
                      x=None, y=None, bar_width=0.5,
                      show_y_value=False, unit=None, decimals=2, x_hover_label='', y_hover_label=''):
        """
            title_location = ['above', 'below', 'left', 'right']
            x_axis_type = ['linear', 'log', 'datetime', 'mercator', 'auto']
            x_axis_location = ['below', 'above', 'auto']
            y_axis_location = ['left', 'right', 'auto']
            y_axis_type = ['linear', 'log', 'datetime', 'mercator', 'auto']
        """
        text = y
        if unit == 'thousands':
            text = [f'{str(round(valor / 1000, decimals))} Mil' for valor in y]
        if unit == 'millions':
            text = [f'{str(round(valor / 1000000, decimals))} Mi' for valor in y]
        if unit == 'billions':
            text = [f'{str(round(valor / 1000000000, decimals))} Bi' for valor in y]
        if unit == 'trillions':
            text = [f'{str(round(valor / 1000000000000, decimals))} Tri' for valor in y]

        source = ColumnDataSource(dict(x=x, y=y, text=text))

        if y_range is None:
            y_range = (0, max(y) * 1.1)

        p = figure(
            title=title,
            title_location=title_location,
            x_axis_label=x_axis_label,
            x_axis_location=x_axis_location,
            x_axis_type=x_axis_type,
            x_minor_ticks=x_minor_ticks,
            x_range=x_range,
            y_axis_label=y_axis_label,
            y_axis_location=y_axis_location,
            y_axis_type=y_axis_type,
            y_minor_ticks=y_minor_ticks,
            y_range=y_range,
            toolbar_location=None,
            tools=""
        )

        """
            text_baseline = ['top', 'middle', 'bottom']
            text_align = ['left', 'center', 'right']
        """
        p.title = Title(text=title, text_font=title_font, text_font_size=title_font_size,
                        text_color=title_color, text_alpha=title_alpha, text_baseline=title_baseline,
                        text_align=title_align, offset=title_offset)

        if not show_grid:
            p.grid.grid_line_color = None
            p.grid.band_fill_alpha = 0

        p.vbar_stack(x='x', top='y', width=bar_width, source=source)

        """
        text_align = ['left', 'center', 'right']
        text_baseline = ['top', 'middle', 'bottom']
        """
        if show_y_value:
            p.text(source=source, x='x', y='y', text='text', text_font_size='8pt', text_color='blue', text_align='center', text_baseline='bottom')

        p.xaxis.formatter = x_formatter
        p.yaxis.formatter = y_formatter

        p.add_tools(HoverTool(tooltips=[(x_hover_label, "@x"), (y_hover_label, "@text")]))

        return p
