import math

class LteUtil():


  def calc_LTE_freqmhz_from_chan(f_low, dl_channeln, nofs, bw=10e6,
                              num_rb=50, start_rb=0):
    """
    Returns the center frequency of the signal.
    :param f_low:
    :param dl_channeln:
    :param nofs:
    :param bw:
    :param num_rb:
    :param start_rb:
    :return:
    """
    try:
      f_low = float(f_low)
      dl_channeln = int(dl_channeln)
      nofs = int(nofs)
      bw = float(bw) / 1e6
      num_rb = int(num_rb)
      start_rb = int(start_rb)
    except Exception as e:
      print(e.message)
    #Fdownlink = FDL_Low + 0.1 (NDL - NDL_Offset)
    ## Fuplink = FUL_Low + 0.1 (NUL - NUL_Offset)
    #    txfreq = rxfreq + Fuplink=FULLow+0.1(NUL−NULOffset)
    lo = (f_low + (0.1 * (dl_channeln - nofs)))
    f = lo - (bw / 2) + (((num_rb / 2) * 200e3) / 1e6) + ((start_rb * (200e3)) / 1e6)

    return f * 1e6

  def cwm_bw_from_uxm_bw(uxm_bw):
    if '1P4' in uxm_bw:
      cmw_bw = 'B014'
    elif 'BW3' in uxm_bw:
      cmw_bw = 'B030'
    elif 'BW5' in uxm_bw:
      cmw_bw = 'B050'
    else:
      cmw_bw = 'B{}'.format( int(uxm_bw[2:])*10 )
    return cmw_bw
  def get_lassen_lte_rxarb_by_bw(bw):
    cmw_bw = LteUtil.cwm_bw_from_uxm_bw(bw)
    arbfile = None
    if cmw_bw == 'B014':
      arbfile = 'D:\CMW100_WV\SMU_NodeB_Ant0_FRC_1p4MHz.wv'
    if cmw_bw == 'B030':
      arbfile = 'D:\CMW100_WV\SMU_NodeB_Ant0_FRC_03MHz.wv'
    if cmw_bw == 'B050':
      arbfile = 'D:\CMW100_WV\SMU_NodeB_Ant0_FRC_5MHz.wv'
    if cmw_bw == 'B100':
      arbfile = 'D:\CMW100_WV\SMU_NodeB_Ant0_FRC_10MHz.wv'
    if cmw_bw == 'B150':
      arbfile = 'D:\CMW100_WV\SMU_NodeB_Ant0_FRC_15MHz.wv'
    if cmw_bw == 'B200':
      arbfile = 'D:\CMW100_WV\SMU_NodeB_Ant0_FRC_20MHz.wv'
    return arbfile
