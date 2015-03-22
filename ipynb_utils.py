# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 12:43:10 2015

@author: Christopher R. Carlson, crcarlson@gmail.com

Helper functions for changing the display of IPython notebooks as of 
Feb 2015.

"""
def toggle_js():
    """
    Return javascript string which creates code-hiding behavior

    IPython code cell hiding script inspired by the site below:
    From http://blog.nextgenetics.net/?e=102 
    Damian Kao
    damian.kao@gmail.com
    """
        
    s = '''
        <script>
                 code_show=true;
                 function code_toggle() {
                     if (code_show){
                         $('div.input').hide();
                     } else {
                         $('div.input').show();
                     }
                     code_show = !code_show
                 } 
                 $( document ).ready(code_toggle);
            </script>
            (The code for this notebook is by default hidden for 
            easier reading.  To toggle the code on/off, click 
            <a href="javascript:code_toggle()">here</a>)
            '''
    return s
            
def inject_css(path):
    """
    HTML string to include a custom stylesheet at <path>
    """

    s = '<link rel="stylesheet" type="text/css" href="%s">' % path
    
    return s
    
def inject_css2(path):
    """
    HTML string to include a custom stylesheet at <path>
    """
    f = open(path,'r')
    s = '<style>\n%s\n</style>' % f.read()
    
    return s


