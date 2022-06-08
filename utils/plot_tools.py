from backtrader import plot


def save_plots(cerebro, numfigs=1, iplot=False, start=None, end=None,
               width=16, hegith=9, dpi=300, tight=True, use=None, file_path='',
               *args, **kwargs
               ):
    if cerebro.p.oldsync:
        plotter = plot.Plot_OldSync(**kwargs)
    else:
        plotter = plot.Plot(**kwargs)

    figs = []
    for startlist in cerebro.runstarts:
        for si, start in enumerate(startlist):
            rfig = plotter.plot(start, figid=si * 100, numfigs=numfigs, iplot=iplot,
                                start=start, end=end, use=use
                                )
            figs.append(rfig)

    for fig in figs:
        for f in fig:
            f.savefig(file_path,bbox_inches='tight')
    return figs



