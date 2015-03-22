# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 13:14:30 2015

@author: Christopher R. Carlson, crcarlson@gmail.com
"""

from math import pi
import numpy as np
import units as u
from curves import sigmoid

class Cartridge(object):
    '''
    Base class for straight walled ammunition
    '''
    def __init__(self):
        # Round physical parameters
        self.m_bullet   = -1  # Bullet weight
        self.d_chamber  = -1  # Chamber diameter
        self.d_case     = -1  # Inside case diameter
        self.l_case     = -1  # Case length
        self.l_case_i   = -1  # Case inside length
        self.l_round    = -1  # Overall round length
        
        #These parameters are for brass
        self.yield_case = 200e6       # Case yield strength, Pa
        self.uts_case   = 550e6       # Case ultimate strength, Pa
        self.gamma_case = 97e9        # Case wall modulus of elasticity, Pa
        self.u_cw     = 0.1           # Case-chamber wall friction coefficient
    
        # Combustion modeling assuming sigmoid combustion pressure
        self.p_peak    = 55 * u.ksi         # Peak sigmoid chamber pressure
        self.t_peak    = 5e-4               # Seconds
        self.alpha_s   = 6.0 / self.t_peak  # Combustion pressure timeconstant, 0-peak
        self.gama      = 1.3                # Specific heat ratio, air + CO2
        
    @property
    def a_chamber(self):
        ''' Chamber inside secional area '''
        return pi*pow(self.d_chamber,2.0)/4.0
        
    @property
    def a_case(self):
        ''' Case inside secional area '''
        return pi*pow(self.d_case,2)/4.0
    
    @property
    def a_bullet(self):
        ''' Bullet base sectional area '''
        return pi*pow(self.d_chamber,2.0)
        
    @property
    def a_cw(self):
        ''' Case wall area '''
        return pi*self.d_case*self.l_case_i
        
    @property
    def v_case(self):
        ''' Case powder volume '''
        return self.a_case * self.l_case_i

    @property
    def t_case(self):
        ''' Case wall thickness '''
        return (self.d_chamber - self.d_case)/2.0
    
    @property
    def p_yield(self):
        ''' Case yield pressure '''
        return 2.0 * self.yield_case * self.t_case / self.d_case
        
    @property
    def p_uts(self):
        ''' Case burst pressure '''
        return 2.0 * self.uts_case * self.t_case / self.d_case

    def sim(self, friction = False, l_barrel = None):
        '''
        Simulated internal ballistics
        Returns (t,X) where
        t = time vector [np array]
        X = [x, x_d, p, F]
        X = [bullet position, bullet velocity, Chamber pressure, Bolt Force]
        '''
        if not l_barrel:
            l_barrel = 18 * u.inch
        
        Ts = 1e-6
        Tf = 3.0e-3
        N = int(Tf / Ts)
        t = np.array(range(0,N))*Ts

        X = np.zeros([4,N])        # x, x_d, pressure, F_case
        for i in range(N-1):
            x = X[0,i]
            x_d = X[1,i]
            x_dd = X[2,i] * self.a_case / self.m_bullet * 0.9
        
            p_combust = self.p_peak*sigmoid(t[i], self.alpha_s, self.t_peak)
            if x > l_barrel:
                p_combust = 0

            # Expanded gas combustion pressure
            p_k = p_combust*pow(self.v_case / (self.v_case + x*self.a_case), 
                                self.gama)
        
            # Case wall friction removes force
            if not friction or p_k < self.p_yield:
                F_friction = 0
            else:
                F_friction = (p_k - self.p_yield) * self.a_cw * self.u_cw
        
            F_case =p_k * self.a_chamber - F_friction
            if F_case < 0: 
                F_case = 0
            
            X[0,i+1] = x + x_d*Ts
            X[1,i+1] = x_d + x_dd*Ts
            X[2,i+1] = p_k
            X[3,i+1] = F_case
            
        return (t, X)

class CCCIMiniMag(Cartridge):
    '''
    Physical and combustion parameters for one of the standard .22lr rounds
    '''
    def __init__(self):
        Cartridge.__init__(self)        

        # Round physical parameters
        self.m_bullet   = 40 * u.grains     # Bullet weight
        self.d_chamber  = 0.223 * u.inch    # Chamber diameter
        self.d_case     = 0.203 * u.inch    # Inside case diameter
        self.l_case     = 0.55 * u.inch     # Case length
        self.l_case_i   = 0.50 * u.inch     # Case inside length
        self.l_round    = 1.25 * u.inch     # Overall round length
    
        # Combustion modeling assuming sigmoid combustion pressure
        self.p_peak    = 55 * u.ksi         # Peak sigmoid chamber pressure
        self.t_peak    = 5e-4               # Seconds
        self.alpha_s   = 6.0 / self.t_peak  # Combustion pressure timeconstant, 0-peak
        self.gama      = 1.3                # Specific heat ratio, air + CO2
        

class C22_Al(CCCIMiniMag):
    '''
    Varmit Al's 22lr webpage data
    '''
    def __init__(self):
        CCCIMiniMag.__init__(self)
        # Combustion modeling assuming sigmoid combustion pressure
        self.p_peak    = 40 * u.ksi        # Peak sigmoid chamber pressure
        self.t_peak    = 5e-4              # Seconds
        self.alpha_s   = 6.0 / self.t_peak # sigmoid width parameter

class C9mm(Cartridge):
    '''
    Standard 9mm Luger
    '''
    def __init__(self):
        Cartridge.__init__(self)
        
        self.m_bullet   = 115   * u.grains   # Bullet weight
        self.d_chamber  = 9.8   * u.mm       # Chamber diameter
        self.d_case     = 9.03  * u.mm       # Inside case diameter
        self.l_case     = 19.15 * u.mm       # Case length
        self.l_case_i   = 15.00 * u.mm       # Case inside length
        self.l_round    = 29.69 * u.mm       # Overall round length
    
        # Combustion modeling assuming sigmoid combustion pressure
        self.p_peak    = 55 * u.ksi         # Peak sigmoid chamber pressure
        self.t_peak    = 1.5e-4               # Seconds
        self.alpha_s   = 6.0 / self.t_peak  # Combustion pressure timeconstant, 0-peak
        self.gama      = 1.15                # Specific heat ratio, air + CO2



