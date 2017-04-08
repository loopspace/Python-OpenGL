class Colour:

    def __init__(self,*args):
        if isinstance(args[0],Colour):
            self.r = args[0].r
            self.g = args[0].g
            self.b = args[0].b
            self.a = args[0].a
        elif isinstance(args[0],str):
            n = args[0].lower().replace(" ","")
            if n[0] == "#":
                if len(n) == 7:
                    self.r = int(n[1:3],16)/255
                    self.g = int(n[3:5],16)/255
                    self.b = int(n[5:7],16)/255
                    self.a = 1
                elif len(n) == 4:
                    self.r = int(n[1:2],16)/15
                    self.g = int(n[2:3],16)/15
                    self.b = int(n[3:4],16)/15
                    self.a = 1
                elif len(n) == 2:
                    self.r = int(n[1:2],16)/15
                    self.g = int(n[1:2],16)/15
                    self.b = int(n[1:2],16)/15
                    self.a = 1
            elif n[0:3] == "rgb":
                pass
            elif n[0:3] == "hsl":
                pass
            elif n in svg:
                self.r = svg[n][0]
                self.g = svg[n][1]
                self.b = svg[n][2]
                self.a = svg[n][3]
            elif n in x11:
                self.r = x11[n][0]
                self.g = x11[n][1]
                self.b = x11[n][2]
                self.a = x11[n][3]
        elif len(args) == 1:
            self.r = args[0]
            self.g = args[0]
            self.b = args[0]
            self.a = 1
        elif len(args) == 2:
            self.r = args[0]
            self.g = args[0]
            self.b = args[0]
            self.a = args[1]
        elif len(args) == 3:
            self.r = args[0]
            self.g = args[1]
            self.b = args[2]
            self.a = 1
        else:
            self.r = args[0]
            self.g = args[1]
            self.b = args[2]
            self.a = args[3]

    def __str__(self):
        return "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ", " + str(self.a) + ")"


    def mix(self,c,t):
        s = 1 - t
        r = t * c.r + s * self.r
        g = t * c.g + s * self.g
        b = t * c.b + s * self.b
        a = t * c.a + s * self.a
        return Colour(r,g,b,a)

    def blend(self,c):
        s = self.a
        t = 1 - s
        r = t * c.r + s * self.r
        g = t * c.g + s * self.g
        b = t * c.b + s * self.b
        a = t * c.a + s * self.a
        return Colour(r,g,b,a)

    def shade(self,t):
        r = t * self.r
        g = t * self.g
        b = t * self.b
        a = self.a
        return Colour(r,g,b,a)
    
    def tone(self,t):
        s = (1 - t) * .5
        r = t * self.r + s 
        g = t * self.g + s
        b = t * self.b + s
        a = self.a
        return Colour(r,g,b,a)
    
    def tint(self,t):
        s = (1 - t)
        r = t * self.r + s
        g = t * self.g + s
        b = t * self.b + s
        a = self.a
        return Colour(r,g,b,a)

    def tolist(self):
        return [self.r,self.g,self.b,self.a]
    
svg = {
    "aliceblue": [239,247,255,255],
    "antiquewhite": [249,234,215,255],
    "aqua": [0,255,255,255],
    "aquamarine": [126,255,211,255],
    "azure": [239,255,255,255],
    "beige": [244,244,220,255],
    "bisque": [255,227,196,255],
    "black": [0,0,0,255],
    "blanchedalmond": [255,234,205,255],
    "blue": [0,0,255,255],
    "blueviolet": [137,43,226,255],
    "brown": [165,42,42,255],
    "burlywood": [221,183,135,255],
    "cadetblue": [94,158,160,255],
    "chartreuse": [126,255,0,255],
    "chocolate": [210,104,29,255],
    "coral": [255,126,79,255],
    "cornflowerblue": [99,149,237,255],
    "cornsilk": [255,247,220,255],
    "crimson": [220,20,59,255],
    "cyan": [0,255,255,255],
    "darkblue": [0,0,138,255],
    "darkcyan": [0,138,138,255],
    "darkgoldenrod": [183,133,11,255],
    "darkgray": [169,169,169,255],
    "darkgreen": [0,99,0,255],
    "darkgrey": [169,169,169,255],
    "darkkhaki": [188,182,107,255],
    "darkmagenta": [138,0,138,255],
    "darkolivegreen": [84,107,47,255],
    "darkorange": [255,140,0,255],
    "darkorchid": [183,49,204,255],
    "darkred": [138,0,0,255],
    "darksalmon": [232,150,122,255],
    "darkseagreen": [142,187,142,255],
    "darkslateblue": [72,61,138,255],
    "darkslategray": [47,79,79,255],
    "darkslategrey": [47,79,79,255],
    "darkturquoise": [0,206,209,255],
    "darkviolet": [147,0,211,255],
    "deeppink": [255,20,146,255],
    "deepskyblue": [0,191,255,255],
    "dimgray": [104,104,104,255],
    "dimgrey": [104,104,104,255],
    "dodgerblue": [29,144,255,255],
    "firebrick": [177,33,33,255],
    "floralwhite": [255,249,239,255],
    "forestgreen": [33,138,33,255],
    "fuchsia": [255,0,255,255],
    "gainsboro": [220,220,220,255],
    "ghostwhite": [247,247,255,255],
    "gold": [255,215,0,255],
    "goldenrod": [218,165,31,255],
    "gray": [127,127,127,255],
    "green": [0,127,0,255],
    "greenyellow": [173,255,47,255],
    "grey": [127,127,127,255],
    "honeydew": [239,255,239,255],
    "hotpink": [255,104,179,255],
    "indianred": [205,91,91,255],
    "indigo": [74,0,130,255],
    "ivory": [255,255,239,255],
    "khaki": [239,229,140,255],
    "lavender": [229,229,249,255],
    "lavenderblush": [255,239,244,255],
    "lawngreen": [124,252,0,255],
    "lemonchiffon": [255,249,205,255],
    "lightblue": [173,216,229,255],
    "lightcoral": [239,127,127,255],
    "lightcyan": [224,255,255,255],
    "lightgoldenrod": [237,221,130,255],
    "lightgoldenrodyellow": [249,249,210,255],
    "lightgray": [211,211,211,255],
    "lightgreen": [144,237,144,255],
    "lightgrey": [211,211,211,255],
    "lightpink": [255,181,192,255],
    "lightsalmon": [255,160,122,255],
    "lightseagreen": [31,177,170,255],
    "lightskyblue": [135,206,249,255],
    "lightslateblue": [132,112,255,255],
    "lightslategray": [119,135,153,255],
    "lightslategrey": [119,135,153,255],
    "lightsteelblue": [175,196,221,255],
    "lightyellow": [255,255,224,255],
    "lime": [0,255,0,255],
    "limegreen": [49,205,49,255],
    "linen": [249,239,229,255],
    "magenta": [255,0,255,255],
    "maroon": [127,0,0,255],
    "mediumaquamarine": [102,205,170,255],
    "mediumblue": [0,0,205,255],
    "mediumorchid": [186,84,211,255],
    "mediumpurple": [146,112,219,255],
    "mediumseagreen": [59,178,113,255],
    "mediumslateblue": [123,104,237,255],
    "mediumspringgreen": [0,249,154,255],
    "mediumturquoise": [72,209,204,255],
    "mediumvioletred": [198,21,132,255],
    "midnightblue": [24,24,112,255],
    "mintcream": [244,255,249,255],
    "mistyrose": [255,227,225,255],
    "moccasin": [255,227,181,255],
    "navajowhite": [255,221,173,255],
    "navy": [0,0,127,255],
    "navyblue": [0,0,127,255],
    "oldlace": [252,244,229,255],
    "olive": [127,127,0,255],
    "olivedrab": [107,141,34,255],
    "orange": [255,165,0,255],
    "orangered": [255,68,0,255],
    "orchid": [218,112,214,255],
    "palegoldenrod": [237,232,170,255],
    "palegreen": [151,251,151,255],
    "paleturquoise": [175,237,237,255],
    "palevioletred": [219,112,146,255],
    "papayawhip": [255,238,212,255],
    "peachpuff": [255,218,184,255],
    "peru": [205,132,63,255],
    "pink": [255,191,202,255],
    "plum": [221,160,221,255],
    "powderblue": [175,224,229,255],
    "purple": [127,0,127,255],
    "red": [255,0,0,255],
    "rosybrown": [187,142,142,255],
    "royalblue": [65,104,225,255],
    "saddlebrown": [138,68,19,255],
    "salmon": [249,127,114,255],
    "sandybrown": [243,164,95,255],
    "seagreen": [45,138,86,255],
    "seashell": [255,244,237,255],
    "sienna": [160,81,44,255],
    "silver": [191,191,191,255],
    "skyblue": [135,206,234,255],
    "slateblue": [105,89,205,255],
    "slategray": [112,127,144,255],
    "slategrey": [112,127,144,255],
    "snow": [255,249,249,255],
    "springgreen": [0,255,126,255],
    "steelblue": [70,130,179,255],
    "tan": [210,179,140,255],
    "teal": [0,127,127,255],
    "thistle": [216,191,216,255],
    "tomato": [255,99,71,255],
    "turquoise": [63,224,207,255],
    "violet": [237,130,237,255],
    "violetred": [208,31,144,255],
    "wheat": [244,221,178,255],
    "white": [255,255,255,255],
    "whitesmoke": [244,244,244,255],
    "yellow": [255,255,0,255],
    "yellowgreen": [154,205,49,255]
}

x11 = {
    "antiquewhite1": [255,238,219,255],
    "antiquewhite2": [237,223,204,255],
    "antiquewhite3": [205,191,175,255],
    "antiquewhite4": [138,130,119,255],
    "aquamarine1": [126,255,211,255],
    "aquamarine2": [118,237,197,255],
    "aquamarine3": [102,205,170,255],
    "aquamarine4": [68,138,116,255],
    "azure1": [239,255,255,255],
    "azure2": [224,237,237,255],
    "azure3": [192,205,205,255],
    "azure4": [130,138,138,255],
    "bisque1": [255,227,196,255],
    "bisque2": [237,212,182,255],
    "bisque3": [205,182,158,255],
    "bisque4": [138,124,107,255],
    "blue1": [0,0,255,255],
    "blue2": [0,0,237,255],
    "blue3": [0,0,205,255],
    "blue4": [0,0,138,255],
    "brown1": [255,63,63,255],
    "brown2": [237,58,58,255],
    "brown3": [205,51,51,255],
    "brown4": [138,34,34,255],
    "burlywood1": [255,211,155,255],
    "burlywood2": [237,196,145,255],
    "burlywood3": [205,170,124,255],
    "burlywood4": [138,114,84,255],
    "cadetblue1": [151,244,255,255],
    "cadetblue2": [141,228,237,255],
    "cadetblue3": [122,196,205,255],
    "cadetblue4": [82,133,138,255],
    "chartreuse1": [126,255,0,255],
    "chartreuse2": [118,237,0,255],
    "chartreuse3": [102,205,0,255],
    "chartreuse4": [68,138,0,255],
    "chocolate1": [255,126,35,255],
    "chocolate2": [237,118,33,255],
    "chocolate3": [205,102,28,255],
    "chocolate4": [138,68,19,255],
    "coral1": [255,114,85,255],
    "coral2": [237,105,79,255],
    "coral3": [205,90,68,255],
    "coral4": [138,62,47,255],
    "cornsilk1": [255,247,220,255],
    "cornsilk2": [237,232,205,255],
    "cornsilk3": [205,200,176,255],
    "cornsilk4": [138,135,119,255],
    "cyan1": [0,255,255,255],
    "cyan2": [0,237,237,255],
    "cyan3": [0,205,205,255],
    "cyan4": [0,138,138,255],
    "darkgoldenrod1": [255,184,15,255],
    "darkgoldenrod2": [237,173,14,255],
    "darkgoldenrod3": [205,149,12,255],
    "darkgoldenrod4": [138,100,7,255],
    "darkolivegreen1": [201,255,112,255],
    "darkolivegreen2": [187,237,104,255],
    "darkolivegreen3": [161,205,89,255],
    "darkolivegreen4": [109,138,61,255],
    "darkorange1": [255,126,0,255],
    "darkorange2": [237,118,0,255],
    "darkorange3": [205,102,0,255],
    "darkorange4": [138,68,0,255],
    "darkorchid1": [191,62,255,255],
    "darkorchid2": [177,58,237,255],
    "darkorchid3": [154,49,205,255],
    "darkorchid4": [104,33,138,255],
    "darkseagreen1": [192,255,192,255],
    "darkseagreen2": [179,237,179,255],
    "darkseagreen3": [155,205,155,255],
    "darkseagreen4": [104,138,104,255],
    "darkslategray1": [150,255,255,255],
    "darkslategray2": [140,237,237,255],
    "darkslategray3": [121,205,205,255],
    "darkslategray4": [81,138,138,255],
    "deeppink1": [255,20,146,255],
    "deeppink2": [237,17,136,255],
    "deeppink3": [205,16,118,255],
    "deeppink4": [138,10,79,255],
    "deepskyblue1": [0,191,255,255],
    "deepskyblue2": [0,177,237,255],
    "deepskyblue3": [0,154,205,255],
    "deepskyblue4": [0,104,138,255],
    "dodgerblue1": [29,144,255,255],
    "dodgerblue2": [28,133,237,255],
    "dodgerblue3": [23,116,205,255],
    "dodgerblue4": [16,77,138,255],
    "firebrick1": [255,48,48,255],
    "firebrick2": [237,43,43,255],
    "firebrick3": [205,38,38,255],
    "firebrick4": [138,25,25,255],
    "gold1": [255,215,0,255],
    "gold2": [237,201,0,255],
    "gold3": [205,173,0,255],
    "gold4": [138,117,0,255],
    "goldenrod1": [255,192,36,255],
    "goldenrod2": [237,179,33,255],
    "goldenrod3": [205,155,28,255],
    "goldenrod4": [138,104,20,255],
    "green1": [0,255,0,255],
    "green2": [0,237,0,255],
    "green3": [0,205,0,255],
    "green4": [0,138,0,255],
    "honeydew1": [239,255,239,255],
    "honeydew2": [224,237,224,255],
    "honeydew3": [192,205,192,255],
    "honeydew4": [130,138,130,255],
    "hotpink1": [255,109,179,255],
    "hotpink2": [237,105,167,255],
    "hotpink3": [205,95,144,255],
    "hotpink4": [138,58,98,255],
    "indianred1": [255,105,105,255],
    "indianred2": [237,99,99,255],
    "indianred3": [205,84,84,255],
    "indianred4": [138,58,58,255],
    "ivory1": [255,255,239,255],
    "ivory2": [237,237,224,255],
    "ivory3": [205,205,192,255],
    "ivory4": [138,138,130,255],
    "khaki1": [255,246,142,255],
    "khaki2": [237,229,132,255],
    "khaki3": [205,197,114,255],
    "khaki4": [138,133,77,255],
    "lavenderblush1": [255,239,244,255],
    "lavenderblush2": [237,224,228,255],
    "lavenderblush3": [205,192,196,255],
    "lavenderblush4": [138,130,133,255],
    "lemonchiffon1": [255,249,205,255],
    "lemonchiffon2": [237,232,191,255],
    "lemonchiffon3": [205,201,165,255],
    "lemonchiffon4": [138,136,112,255],
    "lightblue1": [191,238,255,255],
    "lightblue2": [177,223,237,255],
    "lightblue3": [154,191,205,255],
    "lightblue4": [104,130,138,255],
    "lightcyan1": [224,255,255,255],
    "lightcyan2": [209,237,237,255],
    "lightcyan3": [179,205,205,255],
    "lightcyan4": [122,138,138,255],
    "lightgoldenrod1": [255,235,138,255],
    "lightgoldenrod2": [237,220,130,255],
    "lightgoldenrod3": [205,189,112,255],
    "lightgoldenrod4": [138,128,75,255],
    "lightpink1": [255,174,184,255],
    "lightpink2": [237,161,173,255],
    "lightpink3": [205,140,149,255],
    "lightpink4": [138,94,100,255],
    "lightsalmon1": [255,160,122,255],
    "lightsalmon2": [237,149,114,255],
    "lightsalmon3": [205,128,98,255],
    "lightsalmon4": [138,86,66,255],
    "lightskyblue1": [175,226,255,255],
    "lightskyblue2": [164,211,237,255],
    "lightskyblue3": [140,181,205,255],
    "lightskyblue4": [95,123,138,255],
    "lightsteelblue1": [201,225,255,255],
    "lightsteelblue2": [187,210,237,255],
    "lightsteelblue3": [161,181,205,255],
    "lightsteelblue4": [109,123,138,255],
    "lightyellow1": [255,255,224,255],
    "lightyellow2": [237,237,209,255],
    "lightyellow3": [205,205,179,255],
    "lightyellow4": [138,138,122,255],
    "magenta1": [255,0,255,255],
    "magenta2": [237,0,237,255],
    "magenta3": [205,0,205,255],
    "magenta4": [138,0,138,255],
    "maroon1": [255,52,178,255],
    "maroon2": [237,48,167,255],
    "maroon3": [205,40,144,255],
    "maroon4": [138,28,98,255],
    "mediumorchid1": [224,102,255,255],
    "mediumorchid2": [209,94,237,255],
    "mediumorchid3": [179,81,205,255],
    "mediumorchid4": [122,54,138,255],
    "mediumpurple1": [170,130,255,255],
    "mediumpurple2": [159,121,237,255],
    "mediumpurple3": [136,104,205,255],
    "mediumpurple4": [93,71,138,255],
    "mistyrose1": [255,227,225,255],
    "mistyrose2": [237,212,210,255],
    "mistyrose3": [205,182,181,255],
    "mistyrose4": [138,124,123,255],
    "navajowhite1": [255,221,173,255],
    "navajowhite2": [237,206,160,255],
    "navajowhite3": [205,178,138,255],
    "navajowhite4": [138,121,94,255],
    "olivedrab1": [191,255,62,255],
    "olivedrab2": [178,237,58,255],
    "olivedrab3": [154,205,49,255],
    "olivedrab4": [104,138,33,255],
    "orange1": [255,165,0,255],
    "orange2": [237,154,0,255],
    "orange3": [205,132,0,255],
    "orange4": [138,89,0,255],
    "orangered1": [255,68,0,255],
    "orangered2": [237,63,0,255],
    "orangered3": [205,54,0,255],
    "orangered4": [138,36,0,255],
    "orchid1": [255,130,249,255],
    "orchid2": [237,122,232,255],
    "orchid3": [205,104,201,255],
    "orchid4": [138,71,136,255],
    "palegreen1": [154,255,154,255],
    "palegreen2": [144,237,144,255],
    "palegreen3": [124,205,124,255],
    "palegreen4": [84,138,84,255],
    "paleturquoise1": [186,255,255,255],
    "paleturquoise2": [174,237,237,255],
    "paleturquoise3": [150,205,205,255],
    "paleturquoise4": [102,138,138,255],
    "palevioletred1": [255,130,170,255],
    "palevioletred2": [237,121,159,255],
    "palevioletred3": [205,104,136,255],
    "palevioletred4": [138,71,93,255],
    "peachpuff1": [255,218,184,255],
    "peachpuff2": [237,202,173,255],
    "peachpuff3": [205,175,149,255],
    "peachpuff4": [138,119,100,255],
    "pink1": [255,181,196,255],
    "pink2": [237,169,183,255],
    "pink3": [205,145,158,255],
    "pink4": [138,99,108,255],
    "plum1": [255,186,255,255],
    "plum2": [237,174,237,255],
    "plum3": [205,150,205,255],
    "plum4": [138,102,138,255],
    "purple1": [155,48,255,255],
    "purple2": [145,43,237,255],
    "purple3": [124,38,205,255],
    "purple4": [84,25,138,255],
    "red1": [255,0,0,255],
    "red2": [237,0,0,255],
    "red3": [205,0,0,255],
    "red4": [138,0,0,255],
    "rosybrown1": [255,192,192,255],
    "rosybrown2": [237,179,179,255],
    "rosybrown3": [205,155,155,255],
    "rosybrown4": [138,104,104,255],
    "royalblue1": [72,118,255,255],
    "royalblue2": [67,109,237,255],
    "royalblue3": [58,94,205,255],
    "royalblue4": [38,63,138,255],
    "salmon1": [255,140,104,255],
    "salmon2": [237,130,98,255],
    "salmon3": [205,112,84,255],
    "salmon4": [138,75,57,255],
    "seagreen1": [84,255,159,255],
    "seagreen2": [77,237,147,255],
    "seagreen3": [67,205,127,255],
    "seagreen4": [45,138,86,255],
    "seashell1": [255,244,237,255],
    "seashell2": [237,228,221,255],
    "seashell3": [205,196,191,255],
    "seashell4": [138,133,130,255],
    "sienna1": [255,130,71,255],
    "sienna2": [237,121,66,255],
    "sienna3": [205,104,57,255],
    "sienna4": [138,71,38,255],
    "skyblue1": [135,206,255,255],
    "skyblue2": [125,191,237,255],
    "skyblue3": [108,165,205,255],
    "skyblue4": [73,112,138,255],
    "slateblue1": [130,110,255,255],
    "slateblue2": [122,103,237,255],
    "slateblue3": [104,89,205,255],
    "slateblue4": [71,59,138,255],
    "slategray1": [197,226,255,255],
    "slategray2": [184,211,237,255],
    "slategray3": [159,181,205,255],
    "slategray4": [108,123,138,255],
    "snow1": [255,249,249,255],
    "snow2": [237,232,232,255],
    "snow3": [205,201,201,255],
    "snow4": [138,136,136,255],
    "springgreen1": [0,255,126,255],
    "springgreen2": [0,237,118,255],
    "springgreen3": [0,205,102,255],
    "springgreen4": [0,138,68,255],
    "steelblue1": [99,183,255,255],
    "steelblue2": [91,172,237,255],
    "steelblue3": [79,147,205,255],
    "steelblue4": [53,99,138,255],
    "tan1": [255,165,79,255],
    "tan2": [237,154,73,255],
    "tan3": [205,132,63,255],
    "tan4": [138,89,43,255],
    "thistle1": [255,225,255,255],
    "thistle2": [237,210,237,255],
    "thistle3": [205,181,205,255],
    "thistle4": [138,123,138,255],
    "tomato1": [255,99,71,255],
    "tomato2": [237,91,66,255],
    "tomato3": [205,79,57,255],
    "tomato4": [138,53,38,255],
    "turquoise1": [0,244,255,255],
    "turquoise2": [0,228,237,255],
    "turquoise3": [0,196,205,255],
    "turquoise4": [0,133,138,255],
    "violetred1": [255,62,150,255],
    "violetred2": [237,58,140,255],
    "violetred3": [205,49,119,255],
    "violetred4": [138,33,81,255],
    "wheat1": [255,230,186,255],
    "wheat2": [237,216,174,255],
    "wheat3": [205,186,150,255],
    "wheat4": [138,125,102,255],
    "yellow1": [255,255,0,255],
    "yellow2": [237,237,0,255],
    "yellow3": [205,205,0,255],
    "yellow4": [138,138,0,255],
    "gray0": [189,189,189,255],
    "green0": [0,255,0,255],
    "grey0": [189,189,189,255],
    "maroon0": [175,48,95,255],
    "purple0": [160,31,239,255]
}

if __name__ == "__main__":
    c = Colour("vIOlet Red 1")
    print(c)
