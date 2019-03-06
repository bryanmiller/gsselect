Gemini URL-based Submission of ToO Triggers
Bryan Miller and Shane Walker
2019feb13

Gemini has implemented a web-based service for receiving
target-of-opportunity triggers.  This aleviates the need for PIs to
fetch and then store their programs to submit a trigger and allows the
triggering process to be better automated, thus improving the overall
response time.

The details of the trigger are formatted as an URL string which can be
submitted to Gemini using any browser or URL tool such as wget.  The
following parameters are available.

prog        - program id
email       - email address for user key
password    - password for user key associated with email, site specific
obsnum      - id of the template observation to clone and update,
              must be 'On hold'
target      - name of the target
ra          - target RA [J2000], format 'HH:MM:SS.SS'
dec         - target Dec[J2000], format 'DD:MM:SS.SSS'
mags        - target magnitude information (optional)
note        - text to include in a "Finding Chart" note (optional)
posangle    - position angle [degrees E of N], defaults to 0 (optional)
exptime     - exposure time [seconds], if not given then value in template used (optional)
group       - name of the group for the new observation (optional)
gstarget    - name of guide star (optional, but must be set if any gs* parameter given)
gsra        - guide star RA [J2000] (optional, but must be set if any gs* parameter given)
gsdec       - guide star Dec[J2000] (optional, but must be set if any gs* parameter given)
gsmags      - guide star magnitude (optional)
gsprobe     - PWFS1, PWFS2, OIWFS, or AOWFS (optional, but must be set if any gs* parameter given)
ready       - if "true" set the status to "Prepared/Ready" (defaults to true) 
windowDate  - interpreted in UTC in the format 'YYYY-MM-DD'
windowTime  - interpreted in UTC in the format 'HH:MM'
windowDuration - integer hours
elevationType - "none", "hourAngle", or "airmass"
elevationMin - minimum value for hourAngle/airmass
elevationMax - maximum value for hourAngle/airmass

The server authenticates the request, finds the matching template
observation, clones it, and then updates it with the remainder of the
information.  That way the template observation can be reused in the
future.  The target name, ra, and dec are straightforward.  The note
text is added to a new note, the identified purpose of which is to
contain a link to a finding chart.  The "ready" parameter is used to
determine whether to mark the observation as Prepared (Ready) or not 
(and thereby generate the TOO trigger).

The exposure time parameter, if given, only sets the exposure time in the
instrument "static component", which is tied to the first sequence step.
Any exposure times defined in additional instrument iterators in the
template observation sequence will not be changed. If the exposure time is not
given then the value defined in the template observation is used. The
exposure time must be an integer between 1 and 1200 seconds.

Special characters or line-feeds in the text notes must be URL
encoded.

If the group is specified and it does not exist (using a
case-sensitive match) then a new group is created.

The guide star ra, dec, and probe are optional but recommended since
there is no guarantee, especially for GMOS, that a guide star will
be available at the requested position angle. If no guide star is given
then the OT will attempt to find a guide star. If any gs* parameter
is specified, then gsra, gsdec, and gsprobe must all be specified.
Otherwise an HTTP 400 (Bad Request) is returned with the message
"guide star not completely specified".  If gstarget is missing or ''
but other gs* parameters are present, then it defaults to "GS".

If "target", "ra", or "dec" are missing, then an HTTP 400 (Bad
Request) is returned with the name of the missing parameter.

If any ra, dec, or guide probe parameter cannot be parsed, it also
generates a bad request response.

Magnitudes are optional, but when supplied must contain all three elements 
(value, band, system). Multiple magnitudes can be supplied; use a comma to 
delimit them (for example "24.2/U/Vega,23.4/r/AB"). Magnitudes can be specified 
in Vega, AB or Jy systems in the following bands:

u
U
B
g
V
UC
r
R
i
I
z
Y
J
H
K
L
M
N
Q
AP



