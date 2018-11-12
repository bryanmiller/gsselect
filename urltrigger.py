#!/usr/bin/env python

# URL triggering script, based on tootest.pro
# See urltoo_readme.txt for more information on the API
# Bryan Miller
# 2018-01-30 created

from __future__ import print_function
import requests
from gsselect import gsselect
from parangle import parangle

if __name__ == "__main__":

    # If wait==True, then keep the new observation at On Hold (no trigger)
    wait = True
    if wait:
        ready = 'false'
    else:
        ready = 'true'

    # character string for line break
    # eol = '%0a'
    eol = '\n'

    # Program parameters
    email = 'user@email.com'                # Email associated with OT user key
    progkey = '123455'                      # User key password
    progid = 'GS-2018B-Q-999'               # Program ID

    # Use these URLs for GS
    server = 'https://139.229.34.15:8443'
    # test server
    # server = 'https://gsodbtest.gemini.edu:8443'

    # Use these URLs for GN
    # server = 'https://128.171.88.221:8443'
    # test server
    # server = 'https://gnodbtest.hi.gemini.edu:8443'

    # Observation selection
    obsid=1                                 # obsid of On-hold observation to copy

    # Target parameters
    obsnum = str(obsid).strip()             # obsid to clone, string
    target = 'TNO12345 url'                 # new target name
    ra = '12:22:22.860'                     # RA (J2000)
    dec = '4:31:03.23'                      # Dec (J2000)
    smags = '22.4/r/AB'                     # Target brightness
    l_pa = 180.
    l_pamode = 'parallactic'                # Options: fixed, flip, find, parallactic
    # l_wDate = ''
    l_wDate='2018-03-15'                    # UTC date YYYY-MM-DD for timing window
    l_wTime='01:00'                         # UTC time HH:MM for timing window
    l_wDur=48                               # Timing window duration, integer hours
    l_obsdate = l_wDate                     # UT date for parallactic angle calculation
    # l_obsime = '05:35:00'                 # UT time for parallactic angle calculation, gives parang = 0, el=55
    l_obstime = '03:24:00'                  # UT time for parallactic angle calculation, gives parang = -140, el = 43.2
    l_site = 'Gemini South'                # Site, 'Gemini South' or 'Gemini North'
    l_eltype='airmass'                      # Elevation constraint, "none", "hourAngle", or "airmass"
    l_elmin=1.0                             # minimum value for hourAngle/airmass
    l_elmax=1.6                             #  maximum value for hourAngle/airmas

    note = 'This is a test note. URL triggered.' + eol + 'Add URL to finder chart here.' # Text for note, optional
    group = 'New LIGO event'                      # optional, created if does not exist, case-sensitive match

    # Guidestar parameters
    # If gstarget is missing but other gs* parameters are present, then it defaults to "GS".
    # gstarg='GS473-048345'                 # Guide star target
    # gsra='12:22:30.212'                   # Guide star RA (J2000)
    # gsdec='04:29:35.59'                   # Guide star Dec (J2000)
    # gsmag = 11.83                         # Guide star mag
    gstarg=''                               # Guide star target
    gsra = ''                               # Guide star RA (J2000)
    gsdec=''                                # Guide star Dec (J2000)
    gsmag = 0.0                             # Guide star mag
    gsprobe='OIWFS'                         # Guide star probe (PWFS1/PWFS2/OIWFS/AOWFS)
    #gsprobe='PWFS2'                        # Guide star probe (PWFS1/PWFS2/OIWFS/AOWFS)
    l_inst='GMOS'                           # Instrument: 'GMOS', 'F2', 'GNIRS','NIFS','NIRIF/6','NIRIF/14','NIRIF/32'
    l_port='side'                           # ISS port, options: 'side', 'up', use 'side' for GMOS/F2
    l_ifu = 'none'                          # IFU option: 'none', 'two', 'red', 'blue'
    l_overw = False                         # Overwrite image/catalog table, if False, will read existing files
    l_display = True                        # Display image of field and selected guide star
    l_chop = False                          # Chopping (no longer used, should be False)
    l_pad = 5.                              # Padding applied to WFS FoV (to account for uncertainties in shape) [arcsec]
    l_rmin = -1.                            # Minimum radius for guide star search [arcmin], -1 to use default
    # Conditions
    l_iq = 'Any'                            # Image quality constraint ['20','70','85','Any']
    l_cc = 'Any'                            # Cloud cover constraint ['50', '70', '80', 'Any']
    l_sb = 'Any'                            # Sky brightness constraint ['20','50','80','Any']

    # Parallactic angle?
    if l_pamode == 'parallactic':
        l_pa = parangle(ra, dec, l_obsdate, l_obstime, l_site).value
        spa = str(l_pa).strip()
        l_pamode = 'flip' # in case of guide star selection

    # Guide star selection
    gstarg, gsra, gsdec, gsmag, gspa = gsselect(target,ra,dec,pa=l_pa,imdir='test/', site=l_site, pad=l_pad,
            inst=l_inst, ifu=l_ifu, wfs=gsprobe, chopping=l_chop, cat='UCAC4', pamode=l_pamode,
            iq=l_iq, cc=l_cc, sb=l_sb,
            overwrite=l_overw, display=l_display, verbose=False)
    print(gstarg, gsra, gsdec, gsmag, gspa)

    # form URL command
    if gstarg != '':
        spa = str(gspa).strip()
        sgsmag = str(gsmag).strip() + '/UC/Vega'

    url = server + '/too'

    # Program and target parameters
    cmd = {'prog': progid, 'password': progkey, 'email': email, 'obsnum': obsnum, 'target': target,
           'ra': ra, 'dec': dec, 'mags': smags, 'note': note, 'posangle': spa, 'ready': ready}

    if group.strip() != '':
        cmd['group'] = group.strip()

    # Guide star
    cmd['gstarget'] = gstarg
    cmd['gsra'] = gsra
    cmd['gsdec'] = gsdec
    cmd['gsmags'] = sgsmag
    cmd['gsprobe'] = gsprobe

    # timing window?
    if l_wDate.strip() != '':
        cmd['windowDate'] = l_wDate
        cmd['windowTime'] = l_wTime
        cmd['windowDuration'] = str(l_wDur).strip()

    # elevation/airmass
    if l_eltype.strip() == 'airmass' or l_eltype.strip() == 'hourAngle':
        cmd['elevationType'] = l_eltype
        cmd['elevationMin'] = str(l_elmin).strip()
        cmd['elevationMax'] = str(l_elmax).strip()

    response = requests.post(url, verify=False, params=cmd)
    # print(response.url)
    try:
        response.raise_for_status()
        newobsid = response.text
        if wait:
            print(newobsid + ' created and set On Hold')
        else:
            print(newobsid + ' triggered!')
    except requests.exceptions.HTTPError as exc:
        print('Request failed: {}'.format(response.content))
        raise exc


