from dataclasses import dataclass,field
from typing import List

@dataclass
class Min_Errors:
   AZkP: float = 0.
   AZkW: float = 0.
   BMAJ: float = 0.
   BMIN: float = 0.
   BPA: float = 0.
   CFLUX: float = 0.
   CONDISP: float = 0.
   DVRA: float = 0.
   DVRO: float = 0.
   DVVE: float = 0.
   GAkA: float = 0.
   GAkD: float = 0.
   GAkP: float = 0.
   INCL: float = 0.
   LC0: float = 0.
   LS0: float = 0.
   PA: float = 0.
   RADI: float = 0.
   RADSEP: float = 0.
   RAkA: float = 0.
   RAkP: float = 0.
   ROkA: float = 0.
   ROkP: float = 0.
   SBR: float = 0.
   SDIS: float = 0.
   SMkA: float = 0.
   SMkP: float = 0.
   VM0A: float = 0.
   VMkA: float = 0.
   VMkP: float = 0.
   VRAD: float = 0.
   VROT: float = 0.
   VSYS: float = 0.
   VVER: float = 0.
   WM0A: float = 0.
   WMkA: float = 0.
   WMkP: float = 0.
   XPOS: float = 0.
   YPOS: float = 0.
   Z0: float = 0.
   ZDRA: float = 0.
   ZDRO: float = 0.
   ZDVE: float = 0.

@dataclass
class Variations:
   VARY: str = '!VROT VROT_2'    # Set the parameters manually, if ! causes problems use i   AZkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Central positions of modelled azimuthal range (k  1, 2)
   AZkW: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Width of modelled azimuthal range (k  1, 2)
   BMAJ: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Observational beam HPBW, major axis
   BMIN: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Observational beam HPBW, minor axis
   BPA: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Position angle of observational beam major axis, measured anticlockwise from N
   CONDISP: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Global velocity dispersion
   GAkD: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Dispersion of kth Gaussian surface-brightness distortion (k  1, ..., 4)
   GAkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Phase of kth Gaussian surface-brightness distortion (k  1, ..., 4)
   INCL: List = field(default_factory=lambda: [10,'unit','angle','a']) #Inclination
   LC0: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Shift along the projected major axis
   LS0: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Shift along the projected minor axis
   PA: List = field(default_factory=lambda: [10,'unit','angle','a']) #Inclination
   RADI: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #List of grid nodes (ring radii)
   RAkA: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Amplitude of harmonic radial velocity kth order (k  1, ..., 4), first disk
   RAkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Phase of harmonic radial velocity kth order (k  1, ..., 4), first disk
   ROkA: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Amplitude of harmonic tangential (rotation) velocity kth order (k  1, ..., 4), first disk
   ROkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Phase of harmonic tangential (rotation) kth order (k  1, ..., 4), first disk
   SBR: List = field(default_factory=lambda: [1e-4,'unit','Jy*km/s/arcsec^2','a']) #Constant surface brightness, ith disk, i  2, 3, ...
   SDIS: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Radially dependent velocity dispersion
   SMkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Phase of harmonic surface-brightness distortion kth order (k  1, ..., 4)
   VM0A: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Amplitude of harmonics in LOS velocity 0th order: constant shift in velocity
   VMkA: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Amplitude of harmonics in LOS velocity kth order (k  1, ..., 4)
   VMkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Phase of harmonics in LOS velocity kth order (k  1, ..., 4)
   VRAD: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Mid-plane radial velocity (outwards positive)
   VROT: List = field(default_factory=lambda: [5,'res','km/s','a']) #Mid-plane Rotation velocity
   VSYS: List = field(default_factory=lambda: [0.1,'res','km/s','a']) #Recession velocity
   VVER: List = field(default_factory=lambda: [2.5,'res','km/s','a']) #Mid-plane vertical velocity
   WM0A: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Amplitude of harmonic vertical displacement 0th order: constant vertical displacement
   WMkA: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Amplitude of harmonic vertical displacement kth order (k  1, ..., 4)
   WMkP: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Phase of harmonic vertical displacement kth order (k  1, ..., 4)
   XPOS: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #Right ascension
   YPOS: List = field(default_factory=lambda: [0.3,'res','degrees','a']) #declination
   Z0: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Thickness of disk
   ZDRA: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Vertical gradient of radial velocity
   ZDRO: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Vertical gradient of rotation velocity
   ZDVE: List = field(default_factory=lambda: [1.,'res','arcsec','a']) #Vertical gradient of vertical velocity
